from getpricenobitex import get_nobitex_prices
from getpriceexcoino import get_excoino_prices
from typing import Dict, List, Tuple
import telebot
from datetime import datetime
import time
import logging
import os

# تنظیمات لاگینگ
def setup_logging():
    """تنظیم سیستم لاگینگ"""
    # ایجاد پوشه logs اگر وجود نداشته باشد
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # تنظیم فرمت لاگ
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(f'logs/arbitrage_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# راه‌اندازی لاگر
logger = setup_logging()

# تنظیمات ربات تلگرام
BOT_TOKEN = "7571924632:AAEzYHus2yp5jC9JlQXID2A-9NSG5ZnYXlc"
bot = telebot.TeleBot(BOT_TOKEN)

def get_common_prices() -> Tuple[Dict[str, float], Dict[str, float]]:
    """دریافت قیمت‌های مشترک بین نوبیتکس و اکسیونو"""
    try:
        logger.info("دریافت قیمت‌ها از نوبیتکس...")
        nob_pri = get_nobitex_prices()
        logger.info(f"تعداد ارزهای دریافت شده از نوبیتکس: {len(nob_pri)}")
        
        logger.info("دریافت قیمت‌ها از اکسیونو...")
        exc_pri = get_excoino_prices(total_pages=38)
        logger.info(f"تعداد ارزهای دریافت شده از اکسیونو: {len(exc_pri)}")
        
        common_keys = set(nob_pri.keys()) & set(exc_pri.keys())
        if not common_keys:
            logger.warning("هیچ ارز مشترکی بین دو صرافی یافت نشد")
            return {}, {}

        logger.info(f"تعداد ارزهای مشترک: {len(common_keys)}")
        nobitex_common = {key: nob_pri[key] for key in common_keys}
        excoino_common = {key: exc_pri[key] for key in common_keys}

        return nobitex_common, excoino_common
                
    except Exception as e:
        logger.error(f"خطا در دریافت قیمت‌ها: {str(e)}", exc_info=True)
        return {}, {}

def calculate_price_differences(nobitex_prices: Dict[str, float], 
                             excoino_prices: Dict[str, float]) -> Dict[str, Dict]:
    """محاسبه درصد اختلاف قیمت‌ها بین دو صرافی"""
    differences = {}
    for coin in nobitex_prices.keys():
        nobitex_price = nobitex_prices[coin]
        excoino_price = excoino_prices[coin]
        
        diff_percentage = ((excoino_price - nobitex_price) / nobitex_price) * 100
        
        if -10 <= diff_percentage <= 10:
            differences[coin] = {
                'نوبیتکس': nobitex_price,
                'اکسیونو': excoino_price,
                'اختلاف درصدی': diff_percentage
            }
    
    logger.info(f"تعداد فرصت‌های آربیتراژ یافت شده: {len(differences)}")
    return differences

def get_top_opportunities(limit: int = 10) -> List[Dict]:
    """دریافت بهترین فرصت‌های آربیتراژ"""
    logger.info(f"دریافت {limit} فرصت برتر آربیتراژ...")
    nobitex_prices, excoino_prices = get_common_prices()
    differences = calculate_price_differences(nobitex_prices, excoino_prices)
    
    sorted_differences = dict(sorted(differences.items(), 
                                   key=lambda x: x[1]['اختلاف درصدی']))
    
    opportunities = []
    for coin, data in list(sorted_differences.items())[:limit]:
        opportunities.append({
            'currency': coin,
            'nobitex_price': data['نوبیتکس'],
            'excoino_price': data['اکسیونو'],
            'difference': data['اختلاف درصدی']
        })
    
    logger.info(f"تعداد فرصت‌های نهایی: {len(opportunities)}")
    return opportunities

def format_opportunities_message(opportunities: List[Dict]) -> str:
    """فرمت‌بندی پیام فرصت‌های آربیتراژ"""
    if not opportunities:
        return "❌ در حال حاضر فرصت آربیتراژی یافت نشد."
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = f"🔄 فرصت‌های آربیتراژ\n"
    message += f"⏰ {current_time}\n\n"
    
    sorted_opps = sorted(opportunities, key=lambda x: abs(x['difference']), reverse=True)
    
    for opp in sorted_opps:
        direction = "🟢 خرید از اکسکوینو"
        profit = f"{opp['difference']:.2f}%"
        nobitex_price = f"{opp['nobitex_price']:,.0f}"
        excoino_price = f"{opp['excoino_price']:,.0f}"
        
        message += (
            f"💰 {opp['currency']}\n"
            f"📊 {direction}\n"
            f"💵 قیمت خرید از اکسکوینو: {excoino_price}\n"
            f"💵 قیمت فروش به نوبیتکس: {nobitex_price}\n"
            f"📈 اختلاف: {profit}\n"
            f"{'─' * 30}\n"
        )
    
    return message

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info(f"کاربر {message.from_user.id} دستور start را ارسال کرد")
    welcome_text = """
    به ربات آربیتراژ خوش آمدید! 🚀
    
    دستورات موجود:
    /opportunities - نمایش فرصت‌های آربیتراژ
    /help - راهنمای استفاده از ربات
    """
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    logger.info(f"کاربر {message.from_user.id} دستور help را ارسال کرد")
    help_text = """
    راهنمای استفاده از ربات:
    
    1. برای دریافت فرصت‌های آربیتراژ، دستور /opportunities را ارسال کنید
    2. ربات 10 فرصت برتر را با اختلاف قیمت بین -10% تا +10% نمایش می‌دهد
    3. نتایج به ترتیب از کمترین به بیشترین اختلاف مرتب می‌شوند
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['opportunities'])
def send_opportunities(message):
    logger.info(f"کاربر {message.from_user.id} درخواست فرصت‌های آربیتراژ کرد")
    try:
        loading_msg = bot.reply_to(message, "⏳ در حال دریافت اطلاعات...")
        opportunities = get_top_opportunities(5)
        
        if not opportunities:
            logger.warning("هیچ فرصت آربیتراژی یافت نشد")
            bot.edit_message_text(
                "❌ خطا در دریافت اطلاعات. لطفاً دوباره تلاش کنید.",
                chat_id=message.chat.id,
                message_id=loading_msg.message_id
            )
            return
        
        message_text = format_opportunities_message(opportunities)
        bot.edit_message_text(
            message_text,
            chat_id=message.chat.id,
            message_id=loading_msg.message_id,
            parse_mode='HTML'
        )
        logger.info("فرصت‌های آربیتراژ با موفقیت ارسال شد")
        
    except Exception as e:
        logger.error(f"خطا در ارسال فرصت‌های آربیتراژ: {str(e)}", exc_info=True)
        error_message = f"❌ خطا در دریافت اطلاعات: {str(e)}"
        try:
            bot.edit_message_text(
                error_message,
                chat_id=message.chat.id,
                message_id=loading_msg.message_id
            )
        except:
            bot.reply_to(message, error_message)

def run_bot():
    """اجرای ربات تلگرام"""
    logger.info("شروع اجرای ربات...")
    
    try:
        # تنظیم offset به آخرین پیام دریافتی
        bot.remove_webhook()
        updates = bot.get_updates(offset=-1)
        if updates:
            bot.last_update_id = updates[-1].update_id
        
        bot_info = bot.get_me()
        logger.info(f"ربات با موفقیت متصل شد: @{bot_info.username}")
        
        while True:
            try:
                bot.infinity_polling(timeout=90, long_polling_timeout=90, allowed_updates=[])
            except telebot.apihelper.ApiTelegramException as e:
                if "Conflict: terminated by other getUpdates request" in str(e):
                    logger.warning("تداخل در دریافت پیام‌ها، تلاش مجدد...")
                    time.sleep(5)
                    continue
                else:
                    raise e
            except Exception as e:
                logger.error(f"خطا در polling: {str(e)}", exc_info=True)
                logger.info("تلاش مجدد در 5 ثانیه...")
                time.sleep(5)
                
    except Exception as e:
        logger.critical(f"خطای بحرانی در اجرای ربات: {str(e)}", exc_info=True)

if __name__ == "__main__":
    run_bot()

    