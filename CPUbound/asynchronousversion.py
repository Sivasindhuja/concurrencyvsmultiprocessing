import asyncio
import time

FIB_N = 35
NUM_TASKS = 4


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


async def task():
    # No await here: fib() runs synchronously and blocks the event loop.
    fib(FIB_N)


async def main():
    tasks = [task() for _ in range(NUM_TASKS)]
    await asyncio.gather(*tasks)


def run():
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Total Time:", end - start)
    return end - start


if __name__ == "__main__":
    run()

# asyncio does not provide CPU parallelism; the tasks run one after another.
