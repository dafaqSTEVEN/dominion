from discord.ext.commands import Bot

from apus import secret


async def main():
    dcbot = Bot(command_prefix='a?')

    @dcbot.event
    async def on_ready():
        await dcbot.send_message(destination=dcbot.get_channel('472757559732731914'), content='<@334343501728710656> SUCKSSSSSS')

    await dcbot.start(secret.discord_token)