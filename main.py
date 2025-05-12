from getpricenobitex import get_nobitex_prices as gnp
from getpriceexcoino import get_excoino_prices as gep
import telebot as tb
from datetime import datetime as dt
import time as tm
import logging as lg
import os as os

def sl():
    if not os.path.exists('logs'): os.makedirs('logs')
    lf = '%(asctime)s - %(levelname)s - %(message)s'
    lg.basicConfig(
        level=lg.INFO,
        format=lf,
        handlers=[
            lg.FileHandler(f'logs/arbitrage_{dt.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
            lg.StreamHandler()
        ]
    )
    return lg.getLogger(__name__)

logger = sl()
bt = "7873763430:AAHsAclSc_eVULYj6VxcfQuhiVsGWwpt8j8"
bot = tb.TeleBot(bt)

def gcp():
    try:
        logger.info("Getting Nobitex...")
        np = gnp()
        logger.info(f"Nobitex coins: {len(np)}")
        logger.info("Getting Excoino...")
        ep = gep()
        logger.info(f"Excoino coins: {len(ep)}")
        ck = set(np.keys()) & set(ep.keys())
        if not ck: return {}, {}
        logger.info(f"Common coins: {len(ck)}")
        return {k: np[k] for k in ck}, {k: ep[k] for k in ck}
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {}, {}

def cpd(np, ep):
    diff = {}
    for c in np.keys():
        n = np[c]
        e = ep[c]
        dp = ((e - n) / n) * 100
        if -20 <= dp <= 20:
            diff[c] = {'N': n, 'E': e, 'D': dp}
    logger.info(f"Arb ops: {len(diff)}")
    return diff

def gto(l=None):
    logger.info("Getting top ops...")
    np, ep = gcp()
    diff = cpd(np, ep)
    ops = []
    for c, d in diff.items():
        ad = abs(d['D'])
        if 0 <= ad <= 5:
            ops.append({'c': c, 'n': d['N'], 'e': d['E'], 'd': ad})
    ops.sort(key=lambda x: x['d'], reverse=True)
    return ops[:l] if l else ops

def so(ops, cs=25):
    return [ops[i:i + cs] for i in range(0, len(ops), cs)]

def fom(ops, p, tp):
    ct = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"🔄 Arb (0-5%)\n⏰ {ct}\n📌 Part {p}/{tp}\n\n"
    for o in ops:
        msg += f"💰 {o['c']}\n🏦 N: {o['n']:,.0f}\n🏦 E: {o['e']:,.0f}\n📊 Diff: {o['d']:.2f}%\n{'─'*30}\n"
    return msg

@bot.message_handler(commands=['start'])
def sw(m):
    logger.info(f"User {m.from_user.id} sent start")
    bot.reply_to(m, "Welcome! Use /help")

@bot.message_handler(commands=['help'])
def sh(m):
    logger.info(f"User {m.from_user.id} sent help")
    bot.reply_to(m, "Help: /opportunities")

@bot.message_handler(commands=['opportunities'])
def so(m):
    logger.info(f"User {m.from_user.id} requested ops")
    try:
        lm = bot.reply_to(m, "⏳ Loading...")
        ops = gto()
        if not ops:
            bot.edit_message_text("❌ No ops found.", m.chat.id, lm.message_id)
            return
        chunks = so(ops, 25)
        for i, c in enumerate(chunks, 1):
            msg = fom(c, i, len(chunks))
            if i == 1:
                bot.edit_message_text(msg, m.chat.id, lm.message_id, parse_mode='HTML')
            else:
                bot.send_message(m.chat.id, msg, parse_mode='HTML')
            tm.sleep(0.5)
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        bot.edit_message_text(f"❌ Error: {str(e)}", m.chat.id, lm.message_id)

def rb():
    logger.info("Starting bot...")
    try:
        bot.remove_webhook()
        bot.infinity_polling(timeout=90, long_polling_timeout=90)
    except Exception as e:
        logger.critical(f"Critical: {str(e)}", exc_info=True)

if __name__ == "__main__":
    rb()