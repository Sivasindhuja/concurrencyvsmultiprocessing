import threading
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
    threads = []
    start = time.perf_counter()

    for _ in range(NUM_TASKS):
        t = threading.Thread(target=task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()
    print("Total Time:", end - start)
    return end - start


if __name__ == "__main__":
    run()

# Threads cannot speed up CPU-bound Python code because of the GIL.
