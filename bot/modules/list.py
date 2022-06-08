import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from telegram.ext import CommandHandler
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands


def list_drive(update, context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        LOGGER.info(f"Searching: {search}")
        emoji = sendMessage('🧐', context.bot, update)
        reply = sendMessage("𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴..... 𝗣𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁!\n\n 𝗜𝗳 𝗕𝗼𝗧 𝗱𝗼𝗲𝘀𝗻'𝘁 𝘀𝗲𝗻𝗱 𝗮𝗻𝘆, 𝗧𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝘄𝗶𝘁𝗵 𝗠𝗼𝘃𝗶𝗲 𝗡𝗮𝗺𝗲 & 𝗬𝗲𝗮𝗿🙂.", context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        if button:
            deleteMessage(context.bot, reply)
            deleteMessage(context.bot, emoji)
            msgg = sendMessage("𝗟𝗶𝗻𝗸 𝗦𝗲𝗻𝗱𝗲𝗱 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗣𝗠 😇", context.bot, update)
            sendPrivate(msg, context.bot, update, button)
        else:
            editMessage(f'𝗡𝗼 𝗿𝗲𝘀𝘂𝗹𝘁 𝗳𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 <code>{search}</code>', reply, button)
            deleteMessage(context.bot, emoji)

    except IndexError:
        emo = sendMessage('😡', context.bot, update)
        sendMessage("𝗗𝗼𝗻'𝘁 𝘂𝘀𝗲 𝘂𝗻𝗻𝗲𝗰𝗲𝘀𝘀𝗮𝗿𝗶𝗹𝘆, 𝗦𝗲𝗻𝗱 𝗮 𝘀𝗲𝗮𝗿𝗰𝗵 𝗸𝗲𝘆 𝗮𝗹𝗼𝗻𝗴 𝘄𝗶𝘁𝗵 𝗰𝗼𝗺𝗺𝗮𝗻𝗱", context.bot, update)
        deleteMessage(context.bot, emo)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(list_handler)
