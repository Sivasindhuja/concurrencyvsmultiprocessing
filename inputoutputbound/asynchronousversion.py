import asyncio
import time

NUM_TASKS = 5
DELAY_SECONDS = 2.0


async def fetchData(id):
    print(f"fetching data...{id}")
    # NON-BLOCKING sleep; asyncio.sleep() yields control to the event loop.
    await asyncio.sleep(DELAY_SECONDS)
    print(f"Completed fetching data of id {id}")


async def main():
    tasks = [fetchData(i) for i in range(NUM_TASKS)]
    await asyncio.gather(*tasks)


def run():
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Total Time:", end - start)
    return end - start


if __name__ == "__main__":
    run()

# expected time = 2 seconds
# asyncio uses one thread and cooperative multitasking. Unlike time.sleep(),
# asyncio.sleep() does not block the thread; the event loop can run other tasks.
