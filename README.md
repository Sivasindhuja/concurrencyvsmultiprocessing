# Python Concurrency and Parallelism

A small, reproducible project that compares synchronous execution, threads,
asyncio, and processes for I/O-bound and CPU-bound workloads, and shows how the
same choices affect request handling in a FastAPI server.

## Experiments

### Experiment A: I/O-bound workload

Five tasks each sleep for 2 seconds. The same workload is run with:

- Synchronous execution
- `threading`
- `asyncio`
- `multiprocessing`
- `ThreadPoolExecutor`
- `ProcessPoolExecutor`

### Experiment B: CPU-bound workload

Four recursive `fib(35)` calculations are run with the same six approaches.
The work is identical for every approach. `fib(35)` matches the input used by
the FastAPI CPU endpoints and keeps a full repeated run practical.

### Experiment C: FastAPI request handling

Five endpoints are stress-tested with the same request count and concurrency:

| Endpoint | What it does |
| --- | --- |
| `/blocking-io` | Synchronous endpoint that calls `time.sleep(2)`. FastAPI runs it in its threadpool, so it blocks one worker thread, not the event loop. |
| `/async-io` | Async endpoint that awaits `asyncio.sleep(2)`. |
| `/cpu-bound` | Synchronous endpoint that computes `fib(35)` in FastAPI's threadpool. |
| `/cpu-process` | Async endpoint that offloads `fib(35)` to the event loop's default thread pool. The GIL still limits CPU parallelism. |
| `/cpu-process-trueparallelism` | Async endpoint that offloads `fib(35)` to a `ProcessPoolExecutor` for real CPU parallelism. |

## Project structure

```text
apiServer.py                     FastAPI application
comparisionofallthemethods.py    Local I/O and CPU benchmarks
stresstest.py                    Concurrent HTTP stress test
inputoutputbound/                Six I/O-bound implementations
CPUbound/                        Six CPU-bound implementations
benchmark_report.md              Measured results
requirements.txt                 Python dependencies
```

## Installation

Python 3.10+ is recommended. From the repository root:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the local benchmarks

```bash
python comparisionofallthemethods.py
```

The script runs every approach three times and reports the median execution
time and the speedup relative to synchronous execution. The CPU-bound phase can take several minutes depending on the machine, because each approach performs four recursive fib(35) calculations across three runs.
Individual modules can also be run directly, for example:

```bash
python inputoutputbound/multithreading.py
python CPUbound/mprocessingusingpool.py
```

On Windows, the `if __name__ == "__main__"` guards are required for the
multiprocessing examples.

## Start the FastAPI server

```bash
python -m uvicorn apiServer:app --host 127.0.0.1 --port 8000
```

## Run the stress test

With the server running in another terminal:

```bash
python stresstest.py
```

Defaults: 20 requests per endpoint, concurrency 20. Optional arguments:

```bash
python stresstest.py --requests 20 --concurrency 20 --timeout 300
```

The stress test reports total duration, average latency, P95 latency,
throughput, and failed requests for each endpoint. Failed requests are counted
and printed without stopping the rest of the test.

## Results

Measured results, environment details, and observations are in
[`benchmark_report.md`](benchmark_report.md).

## Notes on the techniques
- **Threads and asyncio** help I/O-bound workloads by allowing other tasks to make progress while one task waits for I/O. Neither approach automatically provides parallel execution of pure-Python CPU-bound code.
- **Processes** have separate interpreters and GILs, so they can execute
  CPU-bound Python code in parallel. They add startup and inter-process
  communication overhead.
- **FastAPI** runs synchronous endpoint functions in a threadpool. A blocking
  synchronous endpoint does not block the whole server, but it does occupy a
  threadpool worker.
