import asyncio
import os
import logging

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

# Carga variables de entorno
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-exp',
    api_key=SecretStr(api_key)
)

browser = Browser(
    config=BrowserConfig(
        headless=True,
        new_context_config=BrowserContextConfig(
            viewport_expansion=0,
            save_recording_path="frontend/videos"
        )
    )
)

# Obtenemos el logger (sin añadir handlers extra)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def run_search(prompt_usuario, log_callback):
    """
    Lanza el agente con la instrucción 'prompt_usuario'.
    Utiliza 'log_callback' para registrar mensajes en tiempo real (ej. en tu frontal).
    Retorna (texto_final, video_path) si finaliza correctamente, o mensaje de error.
    'video_path' seguirá siendo None en esta versión.
    """
    def agent_log(message):
        # Callback para loguear y mandar mensajes al frontal
        log_callback(f"Agente: {message}")
        logger.info(f"Agente Log: {message}")

    agent = Agent(
        task=prompt_usuario,
        llm=llm,
        max_actions_per_step=4,
        browser=browser,
    )

    try:
        result = await agent.run(max_steps=25)
        video_path = None

        texto_final = "No se encontró un resultado final en la historia del agente."
        if hasattr(result, "all_results"):
            pasos = result.all_results
            for r in pasos:
                if getattr(r, "is_done", False) and getattr(r, "success", False):
                    texto_final = getattr(r, "extracted_content", None)
                    if texto_final:
                        break
            return (texto_final, video_path)
        else:
            return (str(result), video_path)

    except Exception as e:
        logger.error(f"Error durante agent.run(): {e}")
        log_callback("Error del Agente: Ocurrió un error interno en el agente. "
                     "Mira los logs del servidor para más detalles.")
        return ("Error del Agente: Ocurrió un error interno. Mira los logs.", None)


if __name__ == '__main__':
    async def test_run_search():
        def dummy_log_callback(message):
            print(message)

        result_prueba = await run_search(
            "Ve a amazon.es y busca calcetines de unicornio",
            dummy_log_callback
        )
        print(f"Resultado de prueba: {result_prueba}")

    asyncio.run(test_run_search())