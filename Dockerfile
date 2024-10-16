FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    unzip \
    libatomic1

RUN wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip && \
    unzip vosk-model-en-us-0.22.zip && \
    mv vosk-model-en-us-0.22 model && \
    rm vosk-model-en-us-0.22.zip

RUN pip install --no-cache-dir flask==2.0.1 werkzeug==2.0.1 yt-dlp vosk gunicorn

COPY app.py .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "300", "app:app"]
