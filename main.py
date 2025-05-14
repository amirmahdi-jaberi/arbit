from getpricenobitex import y1 as a
from getpriceexcoino import a1 as b
from typing import Dict, List, Tuple
import telebot
from datetime import datetime as c
import time as d
import logging as e
import os as f

def g():
    if not f.path.exists('logs'):
        f.makedirs('logs')
    
    h = '%(asctime)s - %(levelname)s - %(message)s'
    e.basicConfig(
        level=e.INFO,
        format=h,
        handlers=[
            e.FileHandler(f'logs/arbitrage_{c.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
            e.StreamHandler()
        ]
    )
    return e.getLogger(__name__)

i = g()
j = "7571924632:AAEzYHus2yp5jC9JlQXID2A-9NSG5ZnYXlc"
k = telebot.TeleBot(j)

def l() -> Tuple[Dict[str, float], Dict[str, float]]:
    try:
        i.info("دریافت قیمت‌ها از نوبیتکس...")
        m = a()
        i.info(f"تعداد ارزهای دریافت شده از نوبیتکس: {len(m)}")
        
        i.info("دریافت قیمت‌ها از اکسیونو...")
        n = b()
        i.info(f"تعداد ارزهای دریافت شده از اکسیونو: {len(n)}")
        
        o = set(m.keys()) & set(n.keys())
        if not o:
            i.warning("هیچ ارز مشترکی بین دو صرافی یافت نشد")
            return {}, {}

        i.info(f"تعداد ارزهای مشترک: {len(o)}")
        p = {q: m[q] for q in o}
        r = {q: n[q] for q in o}

        return p, r
                
    except Exception as s:
        i.error(f"خطا در دریافت قیمت‌ها: {str(s)}", exc_info=True)
        return {}, {}

def t(u: Dict[str, float], v: Dict[str, float]) -> Dict[str, Dict]:
    w = {}
    for x in u.keys():
        y = u[x]
        z = v[x]
        aa = ((z - y) / y) * 100
        
        if -20 <= aa <= 20:
            w[x] = {
                'نوبیتکس': y,
                'اکسیونو': z,
                'اختلاف درصدی': aa
            }
    
    i.info(f"تعداد فرصت‌های آربیتراژ یافت شده: {len(w)}")
    return w

def ab(ac: int = None) -> List[Dict]:
    i.info("دریافت فرصت‌های آربیتراژ با اختلاف 0 تا 5 درصد...")
    ad, ae = l()
    af = t(ad, ae)
    
    ag = []
    for ah, ai in af.items():
        aj = abs(ai['اختلاف درصدی'])
        if 0 <= aj <= 5:
            ag.append({
                'currency': ah,
                'nobitex_price': ai['نوبیتکس'],
                'excoino_price': ai['اکسیونو'],
                'difference': aj
            })
    
    ag.sort(key=lambda x: x['difference'], reverse=True)
    
    if ac:
        ag = ag[:ac]
    
    i.info(f"تعداد فرصت‌های نهایی: {len(ag)}")
    return ag

def ak(al: List[Dict], am: int = 25) -> List[List[Dict]]:
    return [al[an:an + am] for an in range(0, len(al), am)]

def ao(ap: List[Dict], aq: int, ar: int) -> str:
    as_ = c.now().strftime("%Y-%m-%d %H:%M:%S")
    at = f"🔄 فرصت‌های آربیتراژ (0-5%)\n⏰ {as_}\n📌 بخش {aq} از {ar}\n\n"
    
    for au in ap:
        at += (
            f"💰 {au['currency']}\n"
            f"🏦 نوبیتکس: {au['nobitex_price']:,.0f}\n"
            f"🏦 اکسکوینو: {au['excoino_price']:,.0f}\n"
            f"📊 اختلاف: {au['difference']:.2f}%\n"
            f"{'─' * 30}\n"
        )
    
    return at

@k.message_handler(commands=['start'])
def av(aw):
    i.info(f"کاربر {aw.from_user.id} دستور start را ارسال کرد")
    ax = """
    به ربات آربیتراژ خوش آمدید! 🚀
    
    دستورات موجود:
    /opportunities - نمایش فرصت‌های آربیتراژ
    /help - راهنمای استفاده از ربات
    ❤🧡💛
    """
    k.reply_to(aw, ax)

@k.message_handler(commands=['help'])
def ay(az):
    i.info(f"کاربر {az.from_user.id} دستور help را ارسال کرد")
    ba = """
    راهنمای استفاده از ربات:
    
    1. برای دریافت فرصت‌های آربیتراژ، دستور /opportunities را ارسال کنید
    2. ربات فرصت‌ها را با اختلاف قیمت بین 0% تا 5% نمایش می‌دهد
    3. نتایج به ترتیب از بیشترین به کمترین اختلاف مرتب می‌شوند
    """
    k.reply_to(az, ba)

@k.message_handler(commands=['opportunities'])
def bb(bc):
    i.info(f"کاربر {bc.from_user.id} درخواست فرصت‌های آربیتراژ کرد")
    try:
        bd = k.reply_to(bc, "⏳ در حال دریافت اطلاعات...")
        be = ab()
        
        if not be:
            i.warning("هیچ فرصت آربیتراژی یافت نشد")
            k.edit_message_text(
                "❌ در حال حاضر فرصت آربیتراژی با اختلاف 0-5% یافت نشد.",
                chat_id=bc.chat.id,
                message_id=bd.message_id
            )
            return
        
        bf = ak(be, 25)
        bg = len(bf)
        
        for bh, bi in enumerate(bf, 1):
            bj = ao(bi, bh, bg)
            
            if bh == 1:
                k.edit_message_text(
                    bj,
                    chat_id=bc.chat.id,
                    message_id=bd.message_id,
                    parse_mode='HTML'
                )
            else:
                k.send_message(
                    bc.chat.id,
                    bj,
                    parse_mode='HTML'
                )
            
            d.sleep(0.5)
        
        i.info(f"فرصت‌های آربیتراژ در {bg} پیام ارسال شد")
        
    except Exception as bk:
        i.error(f"خطا در ارسال فرصت‌های آربیتراژ: {str(bk)}", exc_info=True)
        bl = f"❌ خطا در دریافت اطلاعات: {str(bk)}"
        try:
            k.edit_message_text(
                bl,
                chat_id=bc.chat.id,
                message_id=bd.message_id
            )
        except:
            k.reply_to(bc, bl)

def bm():
    i.info("شروع اجرای ربات...")
    
    try:
        k.remove_webhook()
        bn = k.get_updates(offset=-1)
        if bn:
            k.last_update_id = bn[-1].update_id
        
        bo = k.get_me()
        i.info(f"ربات با موفقیت متصل شد: @{bo.username}")
        
        while True:
            try:
                k.infinity_polling(timeout=90, long_polling_timeout=90, allowed_updates=[])
            except telebot.apihelper.ApiTelegramException as bp:
                if "Conflict: terminated by other getUpdates request" in str(bp):
                    i.warning("تداخل در دریافت پیام‌ها، تلاش مجدد...")
                    d.sleep(5)
                    continue
                else:
                    raise bp
            except Exception as bq:
                i.error(f"خطا در polling: {str(bq)}", exc_info=True)
                i.info("تلاش مجدد در 5 ثانیه...")
                d.sleep(5)
                
    except Exception as br:
        i.critical(f"خطای بحرانی در اجرای ربات: {str(br)}", exc_info=True)

if __name__ == "__main__":
    bm()
