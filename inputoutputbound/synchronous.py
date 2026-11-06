# Simulating an API call or a database fetch using time.sleep().

import time

NUM_TASKS = 5
DELAY_SECONDS = 2.0


def fetchData(id):
    print(f"fetching data...{id}")
    # Simulated network/database call
    time.sleep(DELAY_SECONDS)
    print(f"Completed fetching data of id {id}")


def run():
    start = time.perf_counter()
    for i in range(NUM_TASKS):
        fetchData(i)
    end = time.perf_counter()

    print("Total time for fetching the data is:", end - start)
    return end - start


if __name__ == "__main__":
    run()

# expected time = 5 * 2 = 10 seconds
