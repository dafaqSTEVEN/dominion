import asyncio

from apus import dcord, tg


async def main():
    await asyncio.gather(dcord.main(), tg.main())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
