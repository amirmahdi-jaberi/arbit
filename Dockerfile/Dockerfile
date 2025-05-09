FROM registry-de.runflare.run/public/python310:2023-08-08

ARG USE_MIRROR

WORKDIR /app

# نصب پیش‌نیازها
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

# نصب Google Chrome نسخه 125.0.6422.60
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable=125.0.6422.60-1 && \
    rm -rf /var/lib/apt/lists/*

# دانلود ChromeDriver 125.0.6422.60
RUN wget -O /tmp/chromedriver.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/125.0.6422.60/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver*

# بررسی نسخه‌ها (اختیاری)
RUN echo "Chrome version: $(google-chrome --version)" && \
    echo "ChromeDriver version: $(chromedriver --version)"

# نصب پکیج‌های پایتون
RUN pip install --upgrade pip

COPY requirements.txt /app

RUN if [ "$USE_MIRROR" = "True" ]; then \
        pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt; \
    else \
        pip install -r requirements.txt; \
    fi

COPY . /app

EXPOSE 3000

CMD ["python3", "main.py"]