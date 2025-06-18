FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl ffmpeg  && curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp  && chmod a+rx /usr/local/bin/yt-dlp  && apt-get clean  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY cookies.txt .

ENV PORT=8080
CMD ["python", "app.py"]




