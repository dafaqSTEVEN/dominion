import asyncio

from apus.bot import dcord, tg
from apus.dom.dom import Game


async def main(game):
    await asyncio.gather(dcord.main(game), tg.main(game))


game = Game()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(game))
loop.close()
