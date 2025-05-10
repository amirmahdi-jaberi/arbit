FROM python:3.10-slim

# نصب وابستگی‌های مورد نیاز برای Chrome و Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    fonts-liberation \
    xdg-utils \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libgbm1 \
    libxrandr2 \
    libxext6 \
    libxfixes3 \
    && rm -rf /var/lib/apt/lists/*

# نصب Google Chrome نسخه 114
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_114.0.5735.90-1_amd64.deb && \
    rm google-chrome-stable_114.0.5735.90-1_amd64.deb

# نصب chromedriver نسخه 114.0.5735.90
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# تنظیم مسیر کاری
WORKDIR /app
COPY . /app

# نصب پکیج‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt

# اجرای پروژه
CMD ["python", "main.py"]