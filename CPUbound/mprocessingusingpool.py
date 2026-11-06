import time
from concurrent.futures import ProcessPoolExecutor

FIB_N = 35
NUM_TASKS = 4


# ---------------------------
# CPU Task (Recursive Fibonacci)
# ---------------------------

def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def cpu_task(_):
    return fib(FIB_N)


# ---------------------------
# Run Function
# ---------------------------

def run():
    start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=NUM_TASKS) as executor:
        results = list(executor.map(cpu_task, range(NUM_TASKS)))

    end = time.perf_counter()
    print("Results:", results[0])
    print("Total Time:", end - start)
    return end - start


# ---------------------------
# Safe Windows Entry Point
# ---------------------------

if __name__ == "__main__":
    run()
