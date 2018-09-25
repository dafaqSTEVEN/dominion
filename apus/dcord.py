from discord.ext.commands import Bot

from apus import secret, util


def dcprt(s):
    util.gprint('[DC] ' + s)


async def main():
    dcbot = Bot(command_prefix='a?')

    @dcbot.event
    async def on_ready():
        dcprt('Ready')
        await dcbot.send_message(dcbot.get_channel('472757559732731914'), '<@351342272391938048>')
    await dcbot.start(secret.discord_token)