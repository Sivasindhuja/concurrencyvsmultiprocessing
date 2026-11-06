# Python Concurrency vs. Multiprocessing Benchmark Report

## 1. Experiment objective

Compare six ways of running the same workload in Python:

- Synchronous execution
- Multithreading (`threading`)
- Asyncio
- Multiprocessing (`multiprocessing.Process`)
- `ThreadPoolExecutor`
- `ProcessPoolExecutor`

The comparison is made for an I/O-bound workload, a CPU-bound workload, and
for concurrent request handling in a FastAPI server. The goal is to show when
threads, asyncio, and processes help, and when they do not.

## 2. Machine and Python environment

| Item | Value |
| --- | --- |
| Machine | Local Windows laptop |
| CPU | 12th Gen Intel(R) Core(TM) i5-1235U |
| Cores / logical processors | 10 cores / 12 logical processors |
| RAM | 16,835,268,608 bytes (~15.7 GiB) |
| Operating system | Windows 11 Home Single Language, version 10.0.26200, 64-bit |
| Python | CPython 3.11.0 (MSC v.1933, 64-bit) |
| FastAPI | 0.162.0 |
| Uvicorn | 0.29.0 |
| HTTP client | httpx 0.28.1 |

All timings use `time.perf_counter()`. No result in this report is estimated or
invented; every value comes from the runs recorded above.

## 3. Workload configuration

### Experiment A: I/O-bound workload

- 5 tasks per run.
- Each task sleeps for 2.0 seconds (`time.sleep` or `asyncio.sleep`).
- 3 repeated runs per approach; the median is reported.
- Speedup = synchronous median / approach median.

### Experiment B: CPU-bound workload

- 4 computations of recursive `fib(35)` per run.
- `fib(35)` returns 9,227,465.
- All six approaches use the same input and the same number of computations.
- 3 repeated runs per approach; the median is reported.
- Speedup = synchronous median / approach median.

### Experiment C: FastAPI request handling

- One Uvicorn process serving `apiServer:app` on `127.0.0.1:8000`.
- 20 requests per endpoint.
- Concurrency 20, using `httpx.AsyncClient` and an `asyncio.Semaphore`.
- Endpoints are tested one after another with the same request count and
  concurrency.
- Request timeout: 300 seconds.
- Total duration, average latency, P95 latency (nearest-rank), throughput, and
  failed requests are reported.
- Throughput = number of requests / total test duration.
- Failed requests are counted without stopping the remaining requests.

The five endpoints are:

| Endpoint | Work performed |
| --- | --- |
| `/blocking-io` | Synchronous endpoint calling `time.sleep(2)`. FastAPI runs it in its threadpool, so it blocks one worker thread, not the event loop. |
| `/async-io` | Async endpoint awaiting `asyncio.sleep(2)`. |
| `/cpu-bound` | Synchronous endpoint computing `fib(35)` in FastAPI's threadpool. |
| `/cpu-process` | Async endpoint offloading `fib(35)` to the event loop's default **thread** pool. Despite the name, this endpoint does not use processes. |
| `/cpu-process-trueparallelism` | Async endpoint offloading `fib(35)` to a `ProcessPoolExecutor`. |

## 4. I/O-bound benchmark results

Three runs per approach. Median and speedup are calculated from the values
shown.

| Approach | Run 1 (s) | Run 2 (s) | Run 3 (s) | Median (s) | Speedup vs sync |
| --- | ---: | ---: | ---: | ---: | ---: |
| Synchronous | 10.003 | 10.004 | 10.002 | 10.003 | 1.00x |
| Multithreading | 2.005 | 2.003 | 2.004 | 2.004 | 4.99x |
| Asyncio | 2.005 | 2.015 | 2.004 | 2.005 | 4.99x |
| Multiprocessing | 2.340 | 2.291 | 2.292 | 2.292 | 4.36x |
| ThreadPoolExecutor | 2.004 | 2.004 | 2.003 | 2.004 | 4.99x |
| ProcessPoolExecutor | 2.318 | 2.303 | 2.337 | 2.318 | 4.32x |

## 5. CPU-bound benchmark results

Three runs per approach. Each run performs 4 × `fib(35)`.

| Approach | Run 1 (s) | Run 2 (s) | Run 3 (s) | Median (s) | Speedup vs sync |
| --- | ---: | ---: | ---: | ---: | ---: |
| Synchronous | 15.377 | 15.329 | 15.092 | 15.329 | 1.00x |
| Multithreading | 15.447 | 17.159 | 15.350 | 15.447 | 0.99x |
| Asyncio | 8.948 | 15.322 | 15.587 | 15.322 | 1.00x |
| Multiprocessing | 4.079 | 3.673 | 3.517 | 3.673 | 4.17x |
| ThreadPoolExecutor | 12.295 | 15.550 | 15.521 | 15.521 | 0.99x |
| ProcessPoolExecutor | 3.573 | 3.366 | 3.474 | 3.474 | 4.41x |

## 6. FastAPI stress-test results

20 requests per endpoint, concurrency 20, 100 requests in total. All requests
returned HTTP 200, so the failed-request count is 0 for every endpoint.

| Endpoint | Total duration (s) | Average latency (ms) | P95 latency (ms) | Throughput (req/s) | Failed requests |
| --- | ---: | ---: | ---: | ---: | ---: |
| `/blocking-io` | 2.05 | 2027.9 | 2032.1 | 9.77 | 0 |
| `/async-io` | 2.06 | 2036.1 | 2051.4 | 9.73 | 0 |
| `/cpu-bound` | 78.91 | 77916.0 | 78909.6 | 0.25 | 0 |
| `/cpu-process` | 77.92 | 65624.8 | 77709.8 | 0.26 | 0 |
| `/cpu-process-trueparallelism` | 9.52 | 7161.9 | 9457.9 | 2.10 | 0 |

## 7. Comparison tables

### Local workloads: speedup relative to synchronous execution

| Approach | I/O-bound speedup | CPU-bound speedup |
| --- | ---: | ---: |
| Synchronous | 1.00x | 1.00x |
| Multithreading | 4.99x | 0.99x |
| Asyncio | 4.99x | 1.00x |
| Multiprocessing | 4.36x | 4.17x |
| ThreadPoolExecutor | 4.99x | 0.99x |
| ProcessPoolExecutor | 4.32x | 4.41x |

### FastAPI: relative total duration

| Endpoint | Total duration (s) | Relative to `/cpu-bound` |
| --- | ---: | ---: |
| `/blocking-io` | 2.05 | 0.03x |
| `/async-io` | 2.06 | 0.03x |
| `/cpu-bound` | 78.91 | 1.00x |
| `/cpu-process` | 77.92 | 0.99x |
| `/cpu-process-trueparallelism` | 9.52 | 0.12x |

The process-pool endpoint completed the same 20 requests about 8.3 times
faster than `/cpu-bound` and about 8.2 times faster than `/cpu-process`.

## 8. Observations and limitations

### I/O-bound observations

- Synchronous execution took about 10.0 seconds, which is the expected 5 × 2.0
  seconds.
- Threads, asyncio, and `ThreadPoolExecutor` all reduced the median time to
  about 2.0 seconds, a speedup of about 5x. The five waits overlap instead of
  running one after another.
- `multiprocessing` and `ProcessPoolExecutor` also overlapped the waits, but
  took about 2.3 seconds. The extra time is process startup and inter-process
  communication overhead.

### CPU-bound observations

- Threads, asyncio, and `ThreadPoolExecutor` did not speed up the CPU-bound
  work: their medians are essentially unchanged (0.99x-1.00x). Threads are
  limited by the GIL, and the asyncio tasks call a synchronous `fib()` function
  without yielding.
- `multiprocessing` (4.17x) and `ProcessPoolExecutor` (4.41x) provided real
  parallelism because each process has its own interpreter and GIL.
- The laptop CPU showed noticeable run-to-run variation. For example, the first
  asyncio CPU run was 8.948 s while the next two were 15.322 s and 15.587 s;
  the first `ThreadPoolExecutor` run was 12.295 s. Reporting the median reduces
  the effect of this frequency/thermal variation, but the raw runs are shown
  above for transparency.

### FastAPI observations

- `/blocking-io` and `/async-io` both finished 20 concurrent requests in about
  2.05 seconds. This confirms that FastAPI's normal handling of a synchronous
  endpoint uses a threadpool: the 2-second `time.sleep` occupies worker threads
  but does not block the entire server or the event loop.
- `/cpu-bound` and `/cpu-process` were much slower, about 78-79 seconds for 20
  requests. `/cpu-bound` runs `fib()` in FastAPI's threadpool, while
  `/cpu-process` offloads `fib()` to the event loop's default thread pool.
  Both are thread-based, so the GIL prevents parallel execution and 20
  concurrent CPU-heavy requests contend with each other.
- `/cpu-process-trueparallelism` finished in 9.52 seconds, about 8.3 times
  faster than `/cpu-bound`. The `ProcessPoolExecutor` uses separate processes
  and therefore bypasses the GIL.
- All 100 requests succeeded. No request failures or HTTP errors occurred.

### Measurement limitations

- The single aggregate run of `comparisionofallthemethods.py` was interrupted by
  the execution environment during the CPU phase (after roughly 2.5 minutes of
  cumulative heavy CPU work). There was no Python traceback, and Windows
  application logs showed no Python crash. The I/O results and the CPU
  synchronous/threading results came from that run. The remaining CPU
  approaches were executed individually with the same `run()` functions, the
  same workload, the same 3-repeat protocol, and the same median calculation.
  Every value in this report is an actual measurement; none is estimated. On a
  machine where the aggregate run is not interrupted, the script runs all six
  approaches in one process.
- Process-based local timings include process and pool startup overhead. This
  is part of the measured cost of those approaches.
- The FastAPI numbers are from one 20-request batch per endpoint with no
  warm-up requests. They are useful for comparing the endpoint designs under
  identical conditions, but they are not a long-duration load test.
