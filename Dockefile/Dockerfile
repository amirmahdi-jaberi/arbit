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
ENV CHROME_DRIVER_VERSION=124.0.6367.91

# نصب chromedriver
RUN echo "در حال دانلود chromedriver نسخه $CHROME_DRIVER_VERSION ..." && \
    wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_DRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64* chromedriver-linux64.zip

# چاپ نسخه‌ی نصب شده
RUN echo "نسخه‌ی نصب شده chromedriver:" && chromedriver --version

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های پروژه به کانتینر
COPY . /app

# نصب کتابخانه‌های پایتونی (مثلاً selenium و telebot)
RUN pip install --no-cache-dir -r requirements.txt

# اجرای ربات
CMD ["python", "main.py"]



# تنظیم نسخه‌ی مورد نظر chromedriver
