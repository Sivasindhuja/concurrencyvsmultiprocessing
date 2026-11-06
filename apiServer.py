import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager

from fastapi import FastAPI

FIB_N = 35


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the process pool when the server starts and shut it down cleanly.
    app.state.process_pool = ProcessPoolExecutor()
    try:
        yield
    finally:
        app.state.process_pool.shutdown(wait=True)


app = FastAPI(lifespan=lifespan)


# 1. Blocking I/O endpoint
@app.get("/blocking-io")
def blocking_io():
    # FastAPI runs synchronous endpoints in its threadpool. This blocks one
    # worker thread for 2 seconds, but it does not block the event loop.
    time.sleep(2)
    return {"message": "Blocking I/O done"}


# 2. Async I/O endpoint
@app.get("/async-io")
async def async_io():
    await asyncio.sleep(2)  # Non-blocking: the event loop can handle other requests.
    return {"message": "Async I/O done"}


# 3. CPU-bound endpoint
@app.get("/cpu-bound")
def cpu_bound():
    # FastAPI runs this synchronous endpoint in its threadpool. The GIL still
    # prevents multiple fib() calls from executing in parallel.
    result = fib(FIB_N)
    return {"result": result}


# 4. CPU work offloaded to the event loop's default thread pool
@app.get("/cpu-process")
async def cpu_process():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, fib, FIB_N)
    return {"result": result}


# 5. CPU work offloaded to a process pool for true parallelism
@app.get("/cpu-process-trueparallelism")
async def cpu_process_true_parallelism():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(app.state.process_pool, fib, FIB_N)
    return {"result": result}
