FROM python:3.11-slim

# نصب وابستگی‌های سیستمی مورد نیاز
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
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# نصب Google Chrome نسخه 125
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# نصب ChromeDriver هماهنگ با نسخه 125
RUN rm -f /usr/local/bin/chromedriver && \
    wget https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.60/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64*

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های پروژه به کانتینر
COPY . /app

# نصب کتابخانه‌های پایتونی (مثلاً selenium و telebot)
RUN pip install --no-cache-dir -r requirements.txt

# اجرای ربات
CMD ["python", "main.py"]