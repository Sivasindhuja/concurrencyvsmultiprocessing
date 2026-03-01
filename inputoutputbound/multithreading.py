import time
import threading

def fetchData(id):
    print(f"fetching data...{id}")
    #api call
    time.sleep(2)
    print(f"Completed fetching data of id {id}")

def run():
    threads=[]

    start=time.time()

    for i in range(5):
        t=threading.Thread(target=fetchData,args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  #wait until the thread is executed


    end = time.time()
    print("Total Time:", end - start)
    if __name__ == "__main__":
        run()

#expected time = 2 seconds
#actual time =  2.003567695617676

