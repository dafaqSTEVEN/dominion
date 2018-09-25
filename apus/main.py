import asyncio

from apus import dcord


async def main():
    await asyncio.gather(dcord.main())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()