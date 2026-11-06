"""Run the local I/O-bound and CPU-bound benchmarks.

Each approach is executed several times and the median wall-clock time is
reported. The speedup is calculated relative to synchronous execution.
"""

import statistics
import time

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

REPEATS = 3


def measure(func):
    """Return the median execution time of ``func`` over REPEATS runs."""
    times = []
    for run_number in range(1, REPEATS + 1):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        print(f"  run {run_number}: {elapsed:.3f}s", flush=True)
    return statistics.median(times)


def benchmark(approaches):
    """Benchmark (name, callable) pairs and add speedup vs. the first one."""
    rows = []
    baseline = None

    for name, func in approaches:
        print(f"\nBenchmarking {name} ...", flush=True)
        median = measure(func)
        if baseline is None:
            baseline = median
        speedup = baseline / median if median else float("nan")
        rows.append((name, median, speedup))

    return rows


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'Method':<22}{'Median time (s)':>18}{'Speedup':>12}")
    print("-" * 52)
    for name, median, speedup in rows:
        print(f"{name:<22}{median:>18.3f}{speedup:>11.2f}x")


if __name__ == "__main__":
    print(f"Repeats per approach: {REPEATS} (median reported)", flush=True)
    print("\nExperiment A: I/O-bound workload", flush=True)

    io_results = benchmark([
        ("Sync", io_sync.run),
        ("Threading", io_thread.run),
        ("Asyncio", io_async.run),
        ("Multiprocessing", io_process.run),
        ("ThreadPoolExecutor", io_thread_pool.run),
        ("ProcessPoolExecutor", io_process_pool.run),
    ])

    print("\nExperiment B: CPU-bound workload", flush=True)
    cpu_results = benchmark([
        ("Sync", cpu_sync.run),
        ("Threading", cpu_thread.run),
        ("Asyncio", cpu_async.run),
        ("Multiprocessing", cpu_process.run),
        ("ThreadPoolExecutor", cpu_thread_pool.run),
        ("ProcessPoolExecutor", cpu_process_pool.run),
    ])

    print_table(
        "Experiment A: I/O-bound (5 tasks, 2 s sleep each)",
        io_results,
    )
    print_table(
        "Experiment B: CPU-bound (4 x fib(35))",
        cpu_results,
    )
