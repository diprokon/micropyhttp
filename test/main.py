import asyncio

from micropyhttp import run, get, jsonify


async def job():
    # while True:
    await asyncio.sleep(5)
    print("job")


@jsonify()
@get("/hello")
async def index(**kwargs):
    return {"hello": "world"}


async def server():
    await run(static_path="static")


async def main():
    await asyncio.gather(job(), server())


try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(main())
    loop.run_forever()
    loop.close()
except KeyboardInterrupt:
    pass
