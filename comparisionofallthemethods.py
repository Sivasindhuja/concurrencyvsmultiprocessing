import time
from tabulate import tabulate

# Import your existing files
import inputoutputbound.synchronous as io_sync
import inputoutputbound.multithreading as io_thread
import inputoutputbound.asynchronousversion as io_async
import inputoutputbound.multiprocessingdemo as io_process
import inputoutputbound.threadingusingpool as io_thread_pool
import inputoutputbound.mprocessingwithpool as io_process_pool

import CPUbound.synchronous as cpu_sync
import CPUbound.multithreading as cpu_thread
import CPUbound.asynchronousversion as cpu_async
import CPUbound.multiprocessingdemo as cpu_process
import CPUbound.threadingusingpool as cpu_thread_pool
import CPUbound.mprocessingusingpool as cpu_process_pool


def measure(func):
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    return round(end - start, 3)


if __name__ == "__main__":

    results = []

    results.append(["I/O Sync", measure(io_sync.run)])
    results.append(["I/O Thread", measure(io_thread.run)])
    results.append(["I/O Async", measure(io_async.run)])
    results.append(["I/O Process", measure(io_process.run)])
    results.append(["I/O ThreadPool", measure(io_thread_pool.run)])
    results.append(["I/O ProcessPool", measure(io_process_pool.run)])



    results.append(["CPU Sync", measure(cpu_sync.run)])
    results.append(["CPU Thread", measure(cpu_thread.run)])
    results.append(["CPU Async", measure(cpu_async.run)])
    results.append(["CPU Process", measure(cpu_process.run)])
    results.append(["CPU ThreadPool", measure(cpu_thread_pool.run)])
    results.append(["CPU ProcessPool", measure(cpu_process_pool.run)])

    print("\n--- Benchmark Results ---\n")
    print(tabulate(results, headers=["Method", "Time (seconds)"]))