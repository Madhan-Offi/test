from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup
from bot import AUTHORIZED_CHATS, dispatcher
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, sendMarkup
from bot.helper.telegram_helper import button_builder
from bot.helper.parser import get_gp_link


def scrape_gp(update, context):
    buttons = button_builder.ButtonMaker()
    buttons.buildbutton("๐ฃ๐ฟ๐ถ๐บ๐ฒ ๐๐ผ๐๐", "https://t.me/prime_Botz")
    buttons.buildbutton("๐๐ผ๐ถ๐ป", "https://t.me/PrimexCloud")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(1))
    try:
       query = update.message.text.split()[1]
    except:
       sendMarkup('<b>send a GPLinks along with this command ๐\n\n โ๏ธreply to the link wont wokrsโ๏ธ</b>\n๐๐ป command GpLink', context.bot, update, reply_markup)
       return
 
    if not query.startswith("https://gplinks") or query.startswith("gplinks"):
       sendMessage('<b>Sorry ๐ค , <i>scrape only for GPLinks. \nMore Links Bypasser Adding Soon.</i> ๐ค </b>', context.bot, update)
       return

    m = sendMessage('๐๐๐ฝ๐ฎ๐๐๐ถ๐ป๐ด ๐๐ผ๐๐ฟ ๐๐ฝ๐น๐ถ๐ป๐ธ ๐๐ถ๐ป๐ธ \n๐๐ก๐๐๐จ๐ ๐ฌ๐๐๐ฉ ๐ ๐ข๐๐ฃ๐ช๐ฉ๐.', context.bot, update)
    link = get_gp_link(query)
    deleteMessage(context.bot, m)
    if not link:      
       sendMessage("๐ฆ๐ผ๐บ๐ฒ๐๐ต๐ถ๐ป๐ด ๐๐ฒ๐ป๐ ๐๐ฟ๐ผ๐ป๐ด\n๐ง๐ฟ๐ ๐ฎ๐ด๐ฎ๐ถ๐ป ๐น๐ฎ๐๐ฒ๐ฟ..๐ฅบ  ", context.bot, update)
    else:
       buttons = button_builder.ButtonMaker()
       buttons.buildbutton("๐๐๐ฝ๐ฎ๐๐๐ฒ๐ฑ ๐๐ถ๐ป๐ธ", link)
       buttons.buildbutton("๐๐ผ๐ถ๐ป", "https://t.me/prime_botz")
       reply_markup = InlineKeyboardMarkup(buttons.build_menu(1))
       sendMarkup(f"๐๐ฒ๐ฟ๐ฒ ๐ถ๐ ๐๐ผ๐๐ฟ ๐ฑ๐ถ๐ฟ๐ฒ๐ฐ๐ ๐น๐ถ๐ป๐ธ ๐", context.bot, update, reply_markup)

gplink_handler = CommandHandler("scrape", scrape_gp,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(gplink_handler)

