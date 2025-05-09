from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import shutil





def get_excoino_prices(total_pages=5):
    """
    دریافت قیمت‌های ارزها از سایت اکسیونو
    Args:
        total_pages (int): تعداد صفحاتی که باید بررسی شود
    Returns:
        dict: دیکشنری شامل نام ارزها و قیمت آنها
    """
    # تنظیمات مرورگر
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # اجرای مرورگر در حالت مخفی
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # تنظیمات اضافی برای VPN
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--proxy-server="direct://"')
    chrome_options.add_argument('--proxy-bypass-list=*')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # مسیر chromedriver را تنظیم کن
    chrome_driver_path = shutil.which("chromedriver")  # پیدا کردن خودکار مسیر

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    
    # تنظیم user agent
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    try:
        driver.get("https://www.excoino.com/coins")
        driver.set_window_size(1920, 1080)  # تنظیم اندازه پنجره
        time.sleep(5)  # افزایش زمان انتظار برای اطمینان از بارگذاری کامل صفحه

        current_page = 1
        prices_dict = {}

        while current_page <= total_pages:
            # استخراج داده‌ها از جدول
            rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 6:
                    name = cells[1].text.strip()
                    our_price = cells[4].text.strip().replace(',', '').replace(' ریال','')
                    prices_dict[name] = float(our_price)

            # اگر به آخرین صفحه رسیدیم، خارج شو
            if current_page == total_pages:
                break

            # تلاش برای کلیک روی دکمه "صفحه بعدی"
            try:
                next_button = driver.find_element(By.XPATH, '//button[not(@disabled)][@aria-label="next page"]')
                next_button.click()
                current_page += 1
            except:
                break

        return prices_dict

    finally:
        # بستن مرورگر
        driver.quit()

# مثال استفاده از تابع
if __name__ == "__main__":
    prices = get_excoino_prices(5)
    print(prices.keys())
