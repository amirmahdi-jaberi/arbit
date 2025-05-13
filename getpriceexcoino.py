from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def a1():
    b1 = Options()
   # b1.add_argument('--headless')
    b1.add_argument('--disable-gpu')
    b1.add_argument('--no-sandbox')
    b1.add_argument('--disable-dev-shm-usage')
    b1.add_argument('--ignore-certificate-errors')
    b1.add_argument('--ignore-ssl-errors')
    b1.add_argument('--disable-web-security')
    b1.add_argument('--allow-running-insecure-content')
    b1.add_argument('--proxy-server="direct://"')
    b1.add_argument('--proxy-bypass-list=*')
    b1.add_argument('--disable-extensions')
    b1.add_argument('--disable-popup-blocking')
    b1.add_argument('--disable-blink-features=AutomationControlled')
    b1.add_experimental_option('excludeSwitches', ['enable-automation'])
    b1.add_experimental_option('useAutomationExtension', False)
    c1 = "/usr/local/bin/chromedriver"
    d1 = webdriver.Chrome(service=Service(c1), options=b1)
    d1.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    try:
        d1.get("https://www.excoino.com/market/exchange/xrp_irr")
        d1.set_window_size(1920, 1080)
        time.sleep(5)
        e1 = {}
        f1 = d1.find_elements(By.CSS_SELECTOR, "tbody.ivu-table-tbody tr.ivu-table-row")
        g1 = 1
        for h1 in f1:
            try:
                i1 = h1.find_elements(By.TAG_NAME, "td")
                if len(i1) >= 3:
                    j1 = i1[0].text.strip()
                    k1 = i1[1].text.strip()
                    e1[j1] = float(k1.replace(',', ''))
                    g1 += 1
                    if g1 == 450: break
            except Exception: pass
        return e1
    finally: d1.quit()

if __name__ == "__main__":
    l1 = a1()
    print(l1)
