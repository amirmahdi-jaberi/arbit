from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service as Svc
from selenium.webdriver.common.by import By as by
from selenium.webdriver.chrome.options import Options as Opts
import time as t

def x1():
    o = Opts()
    o.add_argument('--headless')
    o.add_argument('--disable-gpu')
    o.add_argument('--no-sandbox')
    o.add_argument('--disable-dev-shm-usage')
    o.add_argument('--ignore-certificate-errors')
    o.add_argument('--ignore-ssl-errors')
    o.add_argument('--disable-web-security')
    o.add_argument('--allow-running-insecure-content')
    o.add_argument('--proxy-server="direct://"')
    o.add_argument('--proxy-bypass-list=*')
    o.add_argument('--disable-extensions')
    o.add_argument('--disable-popup-blocking')
    o.add_argument('--disable-blink-features=AutomationControlled')
    o.add_experimental_option('excludeSwitches', ['enable-automation'])
    o.add_experimental_option('useAutomationExtension', False)
    p = "/usr/bin/chromedriver"
    d = wd.Chrome(service=Svc(p), options=o)
    d.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    try:
        d.get("https://www.excoino.com/market/exchange/xrp_irr")
        d.set_window_size(1920, 1080)
        t.sleep(5)
        r = {}
        rows = d.find_elements(by.CSS_SELECTOR, "tbody.ivu-table-tbody tr.ivu-table-row")
        c = 1
        for row in rows:
            try:
                cells = row.find_elements(by.TAG_NAME, "td")
                if len(cells) >= 3:
                    n = cells[0].text.strip()
                    p = cells[1].text.strip()
                    r[n] = float(p.replace(',', ''))
                    c += 1
                    if c == 450: break
            except Exception as e: print(f"E:{e}")
        return r
    finally: d.quit()

if __name__ == "__main__":
    p = x1()
    print(len(p))
    print(p['BTCB'])