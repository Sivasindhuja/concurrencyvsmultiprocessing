import asyncio
import httpx
import time

URL = "http://127.0.0.1:8000/cpu-bound" 
REQUESTS = 20


async def send_request(client):
    response = await client.get(URL)
    return response.status_code


async def main():
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(REQUESTS):
            tasks.append(send_request(client))

        start = time.perf_counter()
        await asyncio.gather(*tasks)
        end = time.perf_counter()

        print(f"Total time for {REQUESTS} requests(cpu bound threading):", round(end - start, 2))


asyncio.run(main())