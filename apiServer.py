from fastapi import FastAPI
import time
import asyncio

app = FastAPI()


# 1️. Blocking I/O Endpoint


@app.get("/blocking-io")
def blocking_io():
    time.sleep(2)  # Blocks entire worker thread
    return {"message": "Blocking I/O done"}


# 2️. Async I/O Endpoint

@app.get("/async-io")
async def async_io():
    await asyncio.sleep(2)  # Non-blocking
    return {"message": "Async I/O done"}



# 3️. CPU Bound Endpoint

def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


@app.get("/cpu-bound")
def cpu_bound():
    result = fib(35)
    return {"result": result}


# 4️ CPU with Process Offload(to unblock the blocked worker thread to protect the async)

@app.get("/cpu-process")
async def cpu_process():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, fib, 35)
    return {"result": result}

#4. for true parallelism
from concurrent.futures import ProcessPoolExecutor

process_pool = ProcessPoolExecutor()

@app.get("/cpu-process-trueparallelism")
async def cpu_process():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(process_pool, fib, 35)
    return {"result": result}