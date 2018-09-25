from telegram.ext import Updater

from apus import secret, util


def tgprt(s):
    util.gprint('[TG] ' + s)


async def main(game):
    tgprt('Starting MAIN')
    client = Updater(secret.tg_token)
    client.bot.send_message(chat_id=-273384150, text=util.get_hardware_info())

    tgprt('Sent')
    client.start_polling()
