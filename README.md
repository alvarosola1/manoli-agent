```markdown
```
# Manoli Agent (Docker Only - Gemini Compatible)

Manoli Agent es un proyecto basado en Python diseñado para [describe aquí el propósito del agente, por ejemplo:  "automatizar tareas de...", "interactuar con APIs de...", "procesar datos de...",  o si es un agente de IA: "ser un agente conversacional...", "realizar inferencias...", "aprender de datos...".  **Necesitas especificar el propósito del agente aquí**].

Este repositorio contiene el código fuente, la configuración y los recursos necesarios para ejecutar el Manoli Agent **usando Docker**.  **Actualmente, Manoli Agent solo es compatible con el modelo Gemini de Google.**

## Tabla de Contenidos

- [Características](#características)
- [Instalación con Docker](#instalación-con-docker)
    - [Prerrequisitos](#prerrequisitos)
    - [Configuración del API Key de Gemini](#configuración-del-api-key-de-gemini)
    - [Pasos](#pasos)
- [Uso](#uso)
    - [Ejemplo](#ejemplo)
- [Licencia](#licencia)
- [Contribución](#contribución)
- [Contacto](#contacto)

## Características

- **Agente configurable:**  [Describe la flexibilidad de configuración del agente si la tiene.]
- **Compatible con Gemini:**  [Indica que el agente está diseñado para funcionar con el modelo Gemini de Google.]
- **[Característica clave 3]:**  [Describe otra característica clave.]
- **[Etc...]:**  [Añade más características según sea necesario.]

*Necesitas completar esta sección con las características específicas de tu Manoli Agent.*

## Instalación con Docker

Para configurar y ejecutar Manoli Agent usando Docker, sigue estos pasos.

### Prerrequisitos

Asegúrate de tener instalado lo siguiente:

- **Docker**
- **Docker Compose**

### Configuración del API Key de Gemini

Manoli Agent requiere una API Key de Google Gemini para funcionar. Sigue estos pasos para configurarla:

1.  **Crea un archivo `.env`** en la raíz del repositorio, en el mismo directorio donde se encuentra el archivo `docker-compose.yml`.

2.  **Añade tu API Key de Gemini al archivo `.env`** con el siguiente formato:

    ```
    GEMINI_API_KEY=<TU_API_KEY>
    ```

    Reemplaza `<TU_API_KEY>` con tu API Key de Gemini real.  **Asegúrate de no commitear este archivo `.env` a tu repositorio por seguridad.**  Se ha añadido `.env` al archivo `.gitignore` para evitar commits accidentales.

### Pasos

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/alvarosola1/manoli-agent.git
    cd manoli-agent
    ```

2.  **Ejecuta Docker Compose para construir y levantar el agente:**

    ```bash
    docker-compose up --build
    ```

    Este comando construirá la imagen de Docker (si es la primera vez o si hay cambios en el `Dockerfile` o `docker-compose.yml`) y luego iniciará el contenedor del Manoli Agent en segundo plano.

## Uso

Para utilizar el Manoli Agent, puedes seguir el ejemplo proporcionado en el notebook de Jupyter: [`src/notebooks/agent_notebook.ipynb`](src/notebooks/agent_notebook.ipynb).

Este notebook contiene una demostración paso a paso de cómo:

- **Cargar y configurar el agente.**
- **Ejecutar el agente con diferentes prompts.**
- **Analizar la salida del agente.**
- **Experimentar con diferentes parámetros.**

Asegúrate de revisar el notebook para entender completamente cómo interactuar con el Manoli Agent y cómo puedes integrarlo en tus propios proyectos o flujos de trabajo.

[//]: # ` bash)
[//]: # python src/agent.py --config config.yaml --task "realizar tarea X")
[//]: #  `

## Licencia

Este proyecto está licenciado bajo los términos de la licencia especificada en el archivo [LICENSE](LICENSE). Consulta el archivo para obtener más detalles sobre los derechos y restricciones de uso.

[//]: # (Ejemplo: "Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para detalles")

## Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1.  **Haz un Fork del repositorio.**
2.  **Crea una rama con tu característica o corrección:** `git checkout -b feature/nueva-caracteristica` o `git checkout -b fix/correccion-bug`
3.  **Realiza tus cambios y commitea:** `git commit -m 'Añade nueva característica o corrige bug'`
4.  **Sube tu rama:** `git push origin feature/nueva-caracteristica`
5.  **Abre un Pull Request** en GitHub.

Por favor, asegúrate de seguir las guías de estilo de código del proyecto y añadir tests unitarios para nuevas funcionalidades.

## Contacto

[Tu Nombre/Usuario - alvarosola1] - [Tu Email o Enlace a tu perfil de GitHub/LinkedIn, etc.]

[//]: # - Enlaces a documentación adicional si la hay)
[//]: # - Agradecimientos)
[//]: # - Información sobre cómo reportar bugs o solicitar nuevas características)
[//]: # - ...)

-----

*Este README.md es una plantilla.  Por favor, rellena los campos [necesitas especificar...] y  [describe aquí...] con la información específica de tu proyecto Manoli Agent. Cuanto más detallado y preciso sea el README, más fácil será para otros entender y utilizar tu proyecto.*  **Recuerda que este agente, en su versión actual, solo es compatible con Gemini.**
```

```
He incluido el contenido en formato markdown dentro de un bloque de código (` `) para que puedas copiar y pegar directamente en tu archivo `README.md` sin problemas de formato.  Recuerda **revisar y completar todas las secciones marcadas con `[necesitas especificar...]` y `[describe aquí...]`** para personalizarlo con la información específica de tu proyecto Manoli Agent. ¡Mucha suerte con tu repositorio!