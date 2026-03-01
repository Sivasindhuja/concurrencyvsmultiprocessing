import time
from concurrent.futures import ThreadPoolExecutor


# ---------------------------
# CPU Task (Recursive Fibonacci)
# ---------------------------

def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def cpu_task():
    return fib(38)


# ---------------------------
# Run Function
# ---------------------------

def run():
    start = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda _: cpu_task(), range(4)))

    end = time.time()
    print("Results:", results[0])
    print("Total Time:", end - start)


if __name__ == "__main__":
    run()