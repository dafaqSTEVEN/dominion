import discord
from discord.ext.commands import Bot

from apus import secret, util


def dcprt(s):
    util.gprint('[DC] ' + s)


async def main(game):
    dcprt('Starting MAIN')
    dcbot = Bot(command_prefix='a?')

    @dcbot.event
    async def on_ready():
        dcprt('Ready')
        await dcbot.change_presence(activity=discord.Game(f'{game.get_instance_count()} dominions'))
        await dcbot.get_channel(472757559732731914).send(util.get_hardware_info())

    await dcbot.start(secret.discord_token)