import threading
import time

NUM_TASKS = 5
DELAY_SECONDS = 2.0


def fetchData(id):
    print(f"fetching data...{id}")
    # Simulated network/database call
    time.sleep(DELAY_SECONDS)
    print(f"Completed fetching data of id {id}")


def run():
    threads = []
    start = time.perf_counter()

    for i in range(NUM_TASKS):
        t = threading.Thread(target=fetchData, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # Wait until the thread has finished

    end = time.perf_counter()
    print("Total Time:", end - start)
    return end - start


if __name__ == "__main__":
    run()

# expected time = 2 seconds (the five sleeps overlap)
