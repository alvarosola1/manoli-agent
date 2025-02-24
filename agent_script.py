import asyncio
import os
import logging

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

# Carga variables de entorno (por si necesitas la clave de la API)
load_dotenv()

# Recupera la clave de la API de tu modelo
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

# Crea instancia de LLM (ajusta parámetros al modelo que uses)
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-exp',
    api_key=SecretStr(api_key)
)

# Configura el navegador
browser = Browser(
    config=BrowserConfig(
        headless=True,
        new_context_config=BrowserContextConfig(
            viewport_expansion=0,
            save_recording_path="frontend/videos"
        )
    )
)

# Configura el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

async def run_search(prompt_usuario, log_callback):
    """
    Lanza el agente con la instrucción 'prompt_usuario'.
    Utiliza 'log_callback' para registrar mensajes en tiempo real (ej. en tu frontal).
    Retorna (texto_final, video_path) si finaliza correctamente, o mensaje de error.
    'video_path' seguirá siendo None ya que la versión de 'browser_use' que usas no graba video.
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

        # Si quisieras cerrar completamente el navegador al acabar:
        # if hasattr(agent.browser, "close"):
        #     await agent.browser.close()
        #
        # o
        # if hasattr(agent.browser, "shutdown"):
        #     await agent.browser.shutdown()

        video_path = None  # No hay grabación de video en esta versión

        texto_final = "No se encontró un resultado final en la historia del agente." # <--- Inicializar aquí

        # Si es un AgentHistoryList, extraer texto final
        if hasattr(result, "all_results"):
            pasos = result.all_results
            # texto_final = None  <--- Eliminar de aquí

            for r in pasos:
                if getattr(r, "is_done", False) and getattr(r, "success", False):
                    texto_final = getattr(r, "extracted_content", None)
                    if texto_final: # Asegurarse de que no sea None, por si acaso
                        break # Parar en el primer resultado exitoso

            return (texto_final, video_path) # <--- Siempre retornar tuple
        else:
            # Si no tiene 'all_results', devuélvelo tal cual (mejor convertir a string para consistencia)
            return (str(result), video_path) # <--- Convertir a string para consistencia

    except Exception as e:
        logger.error(f"Error durante agent.run(): {e}")
        log_callback("Error del Agente: Ocurrió un error interno en el agente. "
                     "Mira los logs del servidor para más detalles.")
        return ("Error del Agente: Ocurrió un error interno. Mira los logs.", None)


if __name__ == '__main__':
    async def test_run_search():
        def dummy_log_callback(message):
            print(message)

        # Prueba simple
        result_prueba = await run_search(
            "Ve a amazon.es y busca calcetines de unicornio",
            dummy_log_callback
        )
        print(f"Resultado de prueba: {result_prueba}")

    asyncio.run(test_run_search())