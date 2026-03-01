import time
from multiprocessing import Process


# ---------------------------
# I/O Task (Simulated API Call)
# ---------------------------

def fetchData(id):
    print(f"fetching data...{id}")
    time.sleep(2)   # Simulating network/API delay
    print(f"Completed fetching data of id {id}")


# ---------------------------
# Run Function (Reusable Entry Point)
# ---------------------------

def run():
    processes = []
    start = time.time()

    for i in range(5):
        p = Process(target=fetchData, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end = time.time()
    print("Total Time:", end - start)


# ---------------------------
# Safe Windows Entry Point
# ---------------------------

if __name__ == "__main__":
    run()