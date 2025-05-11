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
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
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

logger = setup_logging()
BOT_TOKEN = "7873763430:AAHsAclSc_eVULYj6VxcfQuhiVsGWwpt8j8"
bot = telebot.TeleBot(BOT_TOKEN)

def get_common_prices() -> Tuple[Dict[str, float], Dict[str, float]]:
    """دریافت قیمت‌های مشترک بین نوبیتکس و اکسیونو"""
    try:
        logger.info("دریافت قیمت‌ها از نوبیتکس...")
        nob_pri = get_nobitex_prices()
        logger.info(f"تعداد ارزهای دریافت شده از نوبیتکس: {len(nob_pri)}")
        
        logger.info("دریافت قیمت‌ها از اکسیونو...")
        exc_pri = get_excoino_prices()
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
        
        if -20 <= diff_percentage <= 20:
            differences[coin] = {
                'نوبیتکس': nobitex_price,
                'اکسیونو': excoino_price,
                'اختلاف درصدی': diff_percentage
            }
    
    logger.info(f"تعداد فرصت‌های آربیتراژ یافت شده: {len(differences)}")
    return differences

def get_top_opportunities(limit: int = None) -> List[Dict]:
    """دریافت فرصت‌های آربیتراژ با اختلاف 0 تا 5 درصد"""
    logger.info("دریافت فرصت‌های آربیتراژ با اختلاف 0 تا 5 درصد...")
    nobitex_prices, excoino_prices = get_common_prices()
    differences = calculate_price_differences(nobitex_prices, excoino_prices)
    
    opportunities = []
    for coin, data in differences.items():
        abs_diff = abs(data['اختلاف درصدی'])
        if 0 <= abs_diff <= 5:
            opportunities.append({
                'currency': coin,
                'nobitex_price': data['نوبیتکس'],
                'excoino_price': data['اکسیونو'],
                'difference': abs_diff
            })
    
    opportunities.sort(key=lambda x: x['difference'], reverse=True)
    
    if limit:
        opportunities = opportunities[:limit]
    
    logger.info(f"تعداد فرصت‌های نهایی: {len(opportunities)}")
    return opportunities

def split_opportunities(opportunities: List[Dict], chunk_size: int = 25) -> List[List[Dict]]:
    """تقسیم لیست فرصت‌ها به دسته‌های کوچکتر"""
    return [opportunities[i:i + chunk_size] for i in range(0, len(opportunities), chunk_size)]

def format_opportunity_message(opportunities: List[Dict], part: int, total_parts: int) -> str:
    """فرمت‌بندی پیام برای یک دسته از فرصت‌ها"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"🔄 فرصت‌های آربیتراژ (0-5%)\n⏰ {current_time}\n"
    message += f"📌 بخش {part} از {total_parts}\n\n"
    
    for opp in opportunities:
        message += (
            f"💰 {opp['currency']}\n"
            f"🏦 نوبیتکس: {opp['nobitex_price']:,.0f}\n"
            f"🏦 اکسکوینو: {opp['excoino_price']:,.0f}\n"
            f"📊 اختلاف: {opp['difference']:.2f}%\n"
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
    2. ربات فرصت‌ها را با اختلاف قیمت بین 0% تا 5% نمایش می‌دهد
    3. نتایج به ترتیب از بیشترین به کمترین اختلاف مرتب می‌شوند
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['opportunities'])
def send_opportunities(message):
    logger.info(f"کاربر {message.from_user.id} درخواست فرصت‌های آربیتراژ کرد")
    try:
        loading_msg = bot.reply_to(message, "⏳ در حال دریافت اطلاعات...")
        opportunities = get_top_opportunities()
        
        if not opportunities:
            logger.warning("هیچ فرصت آربیتراژی یافت نشد")
            bot.edit_message_text(
                "❌ در حال حاضر فرصت آربیتراژی با اختلاف 0-5% یافت نشد.",
                chat_id=message.chat.id,
                message_id=loading_msg.message_id
            )
            return
        
        chunks = split_opportunities(opportunities, 25)
        total_parts = len(chunks)
        
        for i, chunk in enumerate(chunks, 1):
            message_text = format_opportunity_message(chunk, i, total_parts)
            
            if i == 1:
                bot.edit_message_text(
                    message_text,
                    chat_id=message.chat.id,
                    message_id=loading_msg.message_id,
                    parse_mode='HTML'
                )
            else:
                bot.send_message(
                    message.chat.id,
                    message_text,
                    parse_mode='HTML'
                )
            
            time.sleep(0.5)  # تأخیر کوتاه برای جلوگیری از محدودیت تلگرام
        
        logger.info(f"فرصت‌های آربیتراژ در {total_parts} پیام ارسال شد")
        
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