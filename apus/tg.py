from telegram.ext import Updater

from apus import secret, util


def tgprt(s):
    util.gprint('[TG] ' + s)


async def main():
    tgprt('Starting MAIN')
    updater = Updater(secret.tg_token)

    updater.bot.send_message(chat_id=-273384150, text='@inuwazz')
    tgprt('Sent')
