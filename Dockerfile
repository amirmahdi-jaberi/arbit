FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libgbm1 \
    libvulkan1 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

ENV CHROME_DRIVER_VERSION=136.0.7103.92

RUN echo "در حال دانلود chromedriver نسخه $CHROME_DRIVER_VERSION ..." && \
    wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_DRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64* chromedriver-linux64.zip

RUN cp /usr/local/bin/chromedriver /usr/bin/

RUN echo "نسخه نصب شده chromedriver:" && chromedriver --version

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
