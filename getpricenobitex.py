import requests as rq
from requests.adapters import HTTPAdapter as Adp
from urllib3.util.retry import Retry as Rty
import urllib3 as ulb

def y1():
    ulb.disable_warnings(ulb.exceptions.InsecureRequestWarning)
    u = "https://api.nobitex.ir/market/stats"
    rs = rq.get(u, verify=False)
    if rs.status_code == 200:
        dt = rs.json()
        if dt.get("status") == "ok":
            st = dt.get("stats", {})
            pr = {}
            for s, i in st.items():
                if s.endswith('-rls') and not i.get("isClosed", False):
                    b = float(i.get("bestBuy", 0))
                    s = float(i.get("bestSell", 0))
                    if b > 0:
                        ns = s.replace('-rls', '').upper()
                        lp = (b + s) / 2
                        pr[ns] = lp
            return pr
    return None

def y2():
    cp = y1()
    pd = {}
    if cp:
        for s in sorted(cp.keys()):
            pd[s] = float(cp[s])
    return pd

if __name__ == "__main__":
    p = y2()
    print(p)