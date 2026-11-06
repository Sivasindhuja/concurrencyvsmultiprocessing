import time
from concurrent.futures import ThreadPoolExecutor

NUM_TASKS = 5
DELAY_SECONDS = 2.0


# ---------------------------
# I/O Task (Simulated API)
# ---------------------------

def fetchData(id):
    print(f"fetching data...{id}")
    time.sleep(DELAY_SECONDS)   # Simulating network delay
    print(f"Completed fetching data of id {id}")


# ---------------------------
# Run Function (Entry Point)
# ---------------------------

def run():
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=NUM_TASKS) as executor:
        list(executor.map(fetchData, range(NUM_TASKS)))

    end = time.perf_counter()
    print("Total Time:", end - start)
    return end - start


# ---------------------------
# Safe Standalone Execution
# ---------------------------

if __name__ == "__main__":
    run()
