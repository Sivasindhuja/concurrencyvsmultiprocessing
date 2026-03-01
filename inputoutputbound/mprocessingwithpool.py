# inputoutputbound/processpool_component.py

import time
from concurrent.futures import ProcessPoolExecutor


# ---------------------------
# I/O Task (Simulated API)
# ---------------------------

def fetchData(id):
    print(f"fetching data...{id}")
    time.sleep(2)   # Simulating API delay
    print(f"Completed fetching data of id {id}")


# ---------------------------
# Run Function
# ---------------------------

def run():
    start = time.time()

    # Create process pool with 5 workers
    with ProcessPoolExecutor(max_workers=5) as executor:
        # Submit 5 tasks
        list(executor.map(fetchData, range(5)))

    end = time.time()
    print("Total Time:", end - start)


# ---------------------------
# Safe Windows Entry Point
# ---------------------------

if __name__ == "__main__":
    run()