# inputoutputbound/threadpool_component.py

import time
from concurrent.futures import ThreadPoolExecutor


# ---------------------------
# I/O Task (Simulated API)
# ---------------------------

def fetchData(id):
    print(f"fetching data...{id}")
    time.sleep(2)   # Simulating network delay
    print(f"Completed fetching data of id {id}")


# ---------------------------
# Run Function (Entry Point)
# ---------------------------

def run():
    start = time.time()

    # Create thread pool with 5 workers
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit 5 tasks
        list(executor.map(fetchData, range(5)))

    end = time.time()
    print("Total Time:", end - start)


# ---------------------------
# Safe Standalone Execution
# ---------------------------

if __name__ == "__main__":
    run()