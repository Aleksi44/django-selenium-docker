FROM python:3.9.2-slim-buster

RUN useradd app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app
COPY --chown=app:app . .

RUN apt-get update --yes --quiet
RUN apt-get install --yes --quiet --no-install-recommends \
    gettext \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libxshmfence1 \
    wget \
    xdg-utils \
    netcat \
    xvfb \
 && rm -rf /var/lib/apt/lists/*

RUN dpkg -i ./bin/google-chrome.deb

RUN pip install "daphne==3.0.2"
RUN pip install -r requirements.txt

USER app

CMD set -xe; daphne -b 0.0.0.0 -p 8000 app.app.asgi:application
