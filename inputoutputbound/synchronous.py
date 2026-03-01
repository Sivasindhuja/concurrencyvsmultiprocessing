#simulating an API call or a database fetch using time.sleeo()

import time

def fetchData(id):
    print(f"fetching data...{id}")
    #api call
    time.sleep(2)
    print(f"Completed fetching data of id {id}")



#start time
def run():
    start=time.time()
    for i in range(5):
        fetchData(i)

    #end time

    end=time.time()

    print("Total time for fetching the data is:",end-start)

    if __name__ == "__main__":
        run()
#expected time=5*2=10
#actual time=10.006425380706787