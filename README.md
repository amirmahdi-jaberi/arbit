# Arbitrage Bot

ربات آربیتراژ ارز دیجیتال برای مقایسه قیمت‌ها بین صرافی‌های نوبیتکس و اکسیونو

## ویژگی‌ها

- دریافت خودکار قیمت‌ها از نوبیتکس و اکسیونو
- محاسبه اختلاف قیمت‌ها
- نمایش فرصت‌های آربیتراژ در تلگرام
- سیستم لاگینگ برای نظارت بر عملکرد

## پیش‌نیازها

- Python 3.8+
- Chrome یا Chromium
- ChromeDriver
- توکن ربات تلگرام

## نصب

1. کلون کردن مخزن:
```bash
git clone https://github.com/your-username/arbitrage-bot.git
cd arbitrage-bot
```

2. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

3. دانلود و نصب ChromeDriver:
- دانلود ChromeDriver متناسب با نسخه Chrome خود از [اینجا](https://chromedriver.chromium.org/downloads)
- قرار دادن فایل در پوشه `chromedriver`

4. تنظیم توکن ربات:
- توکن ربات تلگرام را در فایل `main.py` قرار دهید

## استفاده

اجرای ربات:
```bash
python main.py
```

## دستورات تلگرام

- `/start` - شروع کار با ربات
- `/help` - راهنمای استفاده
- `/opportunities` - نمایش فرصت‌های آربیتراژ

## ساختار پروژه

```
arbitrage-bot/
├── main.py              # فایل اصلی ربات
├── getpricenobitex.py   # دریافت قیمت‌ها از نوبیتکس
├── getpriceexcoino.py   # دریافت قیمت‌ها از اکسیونو
├── requirements.txt     # وابستگی‌های پروژه
├── .gitignore          # فایل‌های نادیده گرفته شده
└── README.md           # مستندات پروژه
```

## مشارکت

از مشارکت شما در بهبود پروژه استقبال می‌کنیم. لطفاً برای مشارکت:

1. یک fork از پروژه ایجاد کنید
2. یک branch جدید برای ویژگی خود ایجاد کنید
3. تغییرات خود را commit کنید
4. یک pull request ارسال کنید

## مجوز

این پروژه تحت مجوز MIT منتشر شده است. 