FROM registry-de.runflare.run/public/python310:2023-08-08

ARG USE_MIRROR

WORKDIR /app

# نصب وابستگی‌های موردنیاز برای اجرای Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# نصب Google Chrome نسخهٔ 125
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# نصب ChromeDriver نسخهٔ 125.0.6422.7600
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/125.0.6422.7600/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# نمایش نسخه‌های نصب‌شده برای اطمینان
RUN google-chrome --version && chromedriver --version

# به‌روزرسانی pip
RUN pip install --upgrade pip

# کپی فایل‌های موردنیاز
COPY requirements.txt /app

# نصب وابستگی‌های پایتون با استفاده از آینهٔ داخلی در صورت نیاز
RUN \
  if [ "$USE_MIRROR" = "True" ]; then pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt; \
  else pip install -r requirements.txt; \
  fi

COPY . /app

# حذف فایل Dockerfile از مسیر /app
RUN rm -rf /app/Dockerfile

# باز کردن پورت 3000
EXPOSE 3000

# اجرای برنامه
CMD ["python3", "main.py"]
