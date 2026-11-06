from multiprocessing import Process
import time

FIB_N = 35
NUM_TASKS = 4


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def task():
    fib(FIB_N)


def run():
    processes = []
    start = time.perf_counter()

    for _ in range(NUM_TASKS):
        p = Process(target=task)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end = time.perf_counter()
    print("Total Time:", end - start)
    return end - start


if __name__ == "__main__":
    run()

# Processes have separate Python interpreters and separate GILs, so they can
# execute CPU-bound Fibonacci calculations in parallel.
