import time
from multiprocessing import Process

NUM_TASKS = 5
DELAY_SECONDS = 2.0


# ---------------------------
# I/O Task (Simulated API Call)
# ---------------------------

def fetchData(id):
    print(f"fetching data...{id}")
    time.sleep(DELAY_SECONDS)   # Simulating network/API delay
    print(f"Completed fetching data of id {id}")


# ---------------------------
# Run Function (Reusable Entry Point)
# ---------------------------

def run():
    processes = []
    start = time.perf_counter()

    for i in range(NUM_TASKS):
        p = Process(target=fetchData, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end = time.perf_counter()
    print("Total Time:", end - start)
    return end - start


# ---------------------------
# Safe Windows Entry Point
# ---------------------------

if __name__ == "__main__":
    run()
