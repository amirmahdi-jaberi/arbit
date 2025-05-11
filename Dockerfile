FROM python:3.11-slim

# نصب وابستگی‌های سیستمی مورد نیاز برای اجرای Chrome
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

# نصب Google Chrome Stable
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# تنظیم نسخه هماهنگ با مرورگر کروم
ENV CHROME_DRIVER_VERSION=136.0.7103.92

# نصب ChromeDriver هماهنگ با Chrome v136
RUN echo "در حال دانلود chromedriver نسخه $CHROME_DRIVER_VERSION ..." && \
    wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_DRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64* chromedriver-linux64.zip

# کپی chromedriver به مسیر اجرایی
RUN cp /usr/local/bin/chromedriver /usr/bin/

# نمایش نسخه نصب شده
RUN echo "نسخه نصب شده chromedriver:" && chromedriver --version

# تعیین دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های پروژه
COPY . /app

# نصب پکیج‌های پایتونی پروژه
RUN pip install --no-cache-dir -r requirements.txt

# اجرای اسکریپت اصلی
CMD ["python", "main.py"]
