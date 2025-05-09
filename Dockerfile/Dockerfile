FROM registry-de.runflare.run/public/python310:2023-08-08

ARG USE_MIRROR

WORKDIR /app

# نصب پیش‌نیازهای سیستم
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

# نصب Google Chrome (آخرین نسخه پایدار)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# دانلود ChromeDriver سازگار با نسخه کروم
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) && \
    DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_MAJOR_VERSION") && \
    wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$DRIVER_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver*

# به‌روزرسانی pip و نصب نیازمندی‌های پایتون
RUN pip install --upgrade pip

COPY requirements.txt /app

RUN if [ "$USE_MIRROR" = "True" ]; then \
        pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt; \
    else \
        pip install -r requirements.txt; \
    fi

COPY . /app

# حذف فایل‌های غیرضروری
RUN rm -rf /app/Dockerfile

EXPOSE 3000

CMD ["python3", "main.py"]