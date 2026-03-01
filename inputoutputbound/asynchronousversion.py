import asyncio
import time

async def fetchData(id):
    print(f"fetching data...{id}")
    await asyncio.sleep(2)  # NON-BLOCKING sleep,not time.sleep()
    print(f"Completed fetching data of id {id}")

async def main():
    tasks = []
    for i in range(5):
        tasks.append(fetchData(i))  # this returns coroutine
    await asyncio.gather(*tasks)
def run():
    start = time.time()
    asyncio.run(main())
    end = time.time()

    print("Total Time:", end - start)

if __name__ == "__main__":
    run()

#expected time = 2 seconds

#actual time = 2.018479108810425


#its co-operative multitasking
#unlike multithreding this has only one thread,cpu working

#difference between time.sleep(2) and asyncio.sleep(2) is that time.sleep(2) blocks the CPU
#whereas asyncio.sleep(2) says that this function is on another operation like i/o or network devies
#cpu can be used by other processes(cooperative multitasking)


# coroutine function-a specialized function that can pause its execution (yielding control) and resume later from where it left off