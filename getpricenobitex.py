import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

def m1():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    n1 = "https://api.nobitex.ir/market/stats"
    o1 = requests.get(n1, verify=False)
    if o1.status_code == 200:
        p1 = o1.json()
        if p1.get("status") == "ok":
            q1 = p1.get("stats", {})
            r1 = {}
            for s1, t1 in q1.items():
                if s1.endswith('-rls') and not t1.get("isClosed", False):
                    u1 = float(t1.get("bestBuy", 0))
                    v1 = float(t1.get("bestSell", 0))
                    if u1 > 0:
                        w1 = s1.replace('-rls', '').upper()
                        x1 = (u1 + v1) / 2
                        r1[w1] = x1
            return r1
    return None

def y1():
    z1 = m1()
    a2 = {}
    if z1:
        for b2 in sorted(z1.keys()):
            a2[b2] = float(z1[b2])
    return a2

if __name__ == "__main__":
    c2 = y1()
    print(c2)