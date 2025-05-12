import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

def get_all_prices():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = "https://api.nobitex.ir/market/stats"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            stats = data.get("stats", {})
            currency_bidPrice = {}
            
            for symbol, info in stats.items():
                if symbol.endswith('-rls') and not info.get("isClosed", False):
                    best_buy = float(info.get("bestBuy", 0))
                    best_sell = float(info.get("bestSell", 0))
                    if best_buy > 0:
                        new_symbol = symbol.replace('-rls', '').upper()
                        last_price = (best_buy+best_sell)/2
                        currency_bidPrice[new_symbol] = last_price
            return currency_bidPrice
        else:
            print("خطا در دریافت اطلاعات: وضعیت ناموفق")
            return None
    else:
        print(f"خطا در اتصال به API: کد وضعیت {response.status_code}")
        return None

def get_nobitex_prices():
    currency_bidPrice = get_all_prices()
    prices_dict = {}
    
    if currency_bidPrice:
        for symbol in sorted(currency_bidPrice.keys()):
            prices_dict[symbol] = float(currency_bidPrice[symbol])
    
    return prices_dict

if __name__ == "__main__":
    prices = get_nobitex_prices()
    print(prices)
