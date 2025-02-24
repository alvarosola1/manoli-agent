FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

# Update package lists
RUN apt-get update

# Install Playwright dependencies
RUN apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0

RUN playwright install

# Copia EXPLÍCITA de agent_script.py y otros archivos necesarios (ajusta la lista si es necesario)
COPY agent_script.py ./
COPY aplicacion_web.py ./
COPY frontend ./frontend
# ... si tienes otros archivos de código fuente, cópialos aquí explícitamente ...

CMD ["uvicorn", "aplicacion_web:app", "--host", "0.0.0.0", "--port", "8000"]