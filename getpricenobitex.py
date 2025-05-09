import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_all_prices():
    url = "https://api.nobitex.ir/market/stats"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            stats = data.get("stats", {})
            currency_bidPrice = {}  # قیمتی که می‌توانید بفروشید
            
            for symbol, info in stats.items():
                # فقط جفت ارزهای ریال را در نظر بگیر
                if symbol.endswith('-rls') and not info.get("isClosed", False):
                    best_buy = float(info.get("bestBuy", 0))
                    if best_buy > 0:
                        # تبدیل فرمت نام از btc-rls به BTC/IRR
                        new_symbol = symbol.replace('-rls', '').upper()
                        currency_bidPrice[new_symbol] = best_buy
            
            return currency_bidPrice
        else:
            print("خطا در دریافت اطلاعات: وضعیت ناموفق")
            return None
    else:
        print(f"خطا در اتصال به API: کد وضعیت {response.status_code}")
        return None

def get_nobitex_prices():
    """
    دریافت قیمت‌های خرید ارزها از نوبیتکس
    Returns:
        dict: دیکشنری شامل نام ارزها و قیمت خرید آنها
    """
    currency_bidPrice = get_all_prices()
    prices_dict = {}
    
    if currency_bidPrice:
        for symbol in sorted(currency_bidPrice.keys()):
            prices_dict[symbol] = float(currency_bidPrice[symbol])
    
    return prices_dict

# مثال استفاده از تابع
if __name__ == "__main__":
    prices = get_nobitex_prices()
    print(prices.keys())