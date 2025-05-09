FROM registry-de.runflare.run/public/python310:2023-08-08

ARG USE_MIRROR

WORKDIR /app

# نصب کتابخانه‌های مورد نیاز برای اجرای Chrome در حالت headless
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

# نصب مرورگر گوگل کروم
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# نصب chromedriver مطابق نسخه مرورگر
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+' | head -1) && \
    DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

    
# نصب پکیج‌های پایتون
RUN pip install --upgrade pip

COPY requirements.txt /app

RUN \
  if [ "$USE_MIRROR" = "True" ]; then pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt; \
  else pip install -r requirements.txt; \
  fi

COPY . /app

# حذف Dockerfile داخل image نهایی
RUN rm -f /app/Dockerfile

EXPOSE 3000

CMD ["python3", "main.py"]
