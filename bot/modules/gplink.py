import base64
import re
import requests
import time
import cloudscraper
from bs4 import BeautifulSoup

from urllib.parse import urlparse, parse_qs
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup
from bot import AUTHORIZED_CHATS, dispatcher
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, sendMarkup
from bot.helper.telegram_helper import button_builder


# gp link url

def link_handler(update, context):
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
       sendMessage(f'๐ฌ๐ผ๐๐ฟ ๐๐ถ๐ป๐ธ ๐๐๐ฝ๐ฎ๐๐๐ฒ๐ฑ โ \n\n๐๐๐ฝ๐ฎ๐๐๐ฒ๐ฑ ๐๐ถ๐ป๐ธ: <code>{link}</code>', context.bot, update)


# ==============================================

def get_gp_link(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)

    bs4 = BeautifulSoup(res.content, 'html.parser')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/','/')
    except:
        return False

gplink_handler = CommandHandler(BotCommands.GpCommand, link_handler,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(gplink_handler)
