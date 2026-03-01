import asyncio
import time


def fib(n):
    if(n<=1):
        return n
    return fib(n-1) +fib(n-2)

async def task():
    fib(38)

async def main():
    tasks = []
    for i in range(4):
         tasks.append(task())
    await asyncio.gather(*tasks)
def run():
    start = time.time()
    asyncio.run(main())
    end = time.time()

    print("Total Time:", end - start)

if __name__ == "__main__":
    run()
#expected = 4 * 1 = 4 seconds
#actual =  4.226021766662598