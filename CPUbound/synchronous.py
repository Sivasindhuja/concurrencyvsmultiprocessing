# Using the recursive Fibonacci sequence as a CPU-bound workload.

import time

FIB_N = 35
NUM_TASKS = 4


def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def run():
    start = time.perf_counter()

    for _ in range(NUM_TASKS):
        fib(FIB_N)

    end = time.perf_counter()
    print("total time : ", end - start)
    return end - start


if __name__ == "__main__":
    run()
