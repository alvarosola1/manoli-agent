import os
import logging
import asyncio
import glob
import re
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from agent_script import run_search

app = FastAPI()

app.mount("/videos", StaticFiles(directory="frontend/videos"), name="videos")
templates = Jinja2Templates(directory="frontend")

web_app_logger = logging.getLogger("aplicacion_web")
web_app_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
web_app_logger.addHandler(ch)

conversation_history = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "conversation_history": conversation_history
    })

@app.post("/ejecutar_agente", response_class=HTMLResponse)
async def ejecutar_agente_endpoint(request: Request, prompt_usuario: str = Form(...)):
    """
    Recibe el prompt, ejecuta el agente y muestra el video y texto final.
    Solo mostrará el 'extracted_content' donde is_done=True y success=True.
    """
    web_app_logger.info(f"Prompt del usuario: {prompt_usuario}")

    user_message = {"role": "user", "content": prompt_usuario}
    conversation_history.append(user_message)

    agent_log_output = []

    def web_log_callback(mensaje):
        lower_mensaje = mensaje.lower().strip()
        if "agenthistorylist(" in lower_mensaje:
            short_msg = "(Historial interno del agente omitido en log)"
            agent_log_output.append(short_msg)
            web_app_logger.info(short_msg)
        elif mensaje.startswith("Agente:"):
            texto = mensaje[len("Agente:"):].strip()
            agent_log_output.append(texto)
            web_app_logger.info(f"Log de agente (chat): {texto}")
        else:
            web_app_logger.info(f"Otro log: {mensaje}")

    agent_response_text = ""
    video_url = None

    try:
        web_app_logger.info(f"Ejecutando agente con prompt: {prompt_usuario}")
        result = await run_search(prompt_usuario, web_log_callback)

        # -------------------------------------------
        # FUNCIÓN PARA EXTRAER SÓLO EL FINAL
        # -------------------------------------------
        def extraer_texto_final(full_text: str) -> str:
            """
            De una cadena potencialmente con AgentHistoryList(...) y ActionResult(...),
            devuelve SOLO el 'extracted_content' del bloque con is_done=True, success=True.
            Si no lo encuentra, usa un fallback.
            """
            # Dividimos en bloques por "ActionResult("
            blocks = full_text.split("ActionResult(")
            texto_final = None
            for block in blocks:
                if "is_done=True" in block and "success=True" in block:
                    match_ec = re.search(r"extracted_content='(.*?)'", block, flags=re.DOTALL)
                    if match_ec:
                        texto_final = match_ec.group(1)
                        break

            if texto_final:
                return texto_final
            else:
                return "(No se encontró extracted_content final)"

        # 1) Si el agente devuelve (texto, video_path)
        if isinstance(result, tuple):
            text_part, maybe_video_path = result
            text_part = str(text_part)
            # Extraemos el texto final
            agent_response_text = extraer_texto_final(text_part)

        # 2) Si es un string
        elif isinstance(result, str):
            agent_response_text = extraer_texto_final(result)
            maybe_video_path = None

        else:
            # Caso raro (ninguna de las anteriores)
            agent_response_text = str(result)
            maybe_video_path = None

        # -------------------------------------------
        # Resolución del video
        # -------------------------------------------
        if 'maybe_video_path' in locals() and maybe_video_path and os.path.exists(maybe_video_path):
            nombre_video = os.path.basename(maybe_video_path)
            video_url = f"/videos/{nombre_video}"
        else:
            video_files = glob.glob("frontend/videos/*.webm")
            if video_files:
                newest_file = max(video_files, key=os.path.getmtime)
                nombre_video = os.path.basename(newest_file)
                video_url = f"/videos/{nombre_video}"

        web_app_logger.info("Agente finalizado.")

        if not agent_response_text:
            agent_response_text = "Agente finalizado, no se obtuvo respuesta."

    except Exception as e:
        error_msg = f"Error al ejecutar el agente: {e}"
        web_app_logger.error(error_msg)
        agent_log_output.append(error_msg)
        agent_response_text = error_msg

    agent_response = {
        "role": "agent",
        "response_text": agent_response_text,
        "video_url": video_url,
        "log_lines": agent_log_output
    }
    conversation_history.append(agent_response)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "conversation_history": conversation_history
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)