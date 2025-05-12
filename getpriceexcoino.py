from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_excoino_prices():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
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

    chrome_driver_path = "/usr/bin/chromedriver"

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    try:
        driver.get("https://www.excoino.com/market/exchange/xrp_irr")
        driver.set_window_size(1920, 1080)
        time.sleep(5)

        prices_dict = {}
        
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody.ivu-table-tbody tr.ivu-table-row")
        
        n=1
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3:
                    name = cells[0].text.strip()
                    price = cells[1].text.strip()
                    prices_dict[name] = float(price.replace(',', ''))
                    n+=1
                    if n==450:
                        break
            except Exception as e:
                print(f"Error processing row: {e}")

        return prices_dict

    finally:
        driver.quit()

if __name__ == "__main__":
    prices = get_excoino_prices()
    print(len(prices))
    print(prices['BTCB'])