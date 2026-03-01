import threading
import time

def fib(n):
    if(n<=1):
        return n
    return fib(n-1) +fib(n-2)

def task():
    fib(38)


def run():

    threads = []
    start = time.time()

    for i in range(4):
        t = threading.Thread(target=task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.time()
    print("Total Time:", end - start)

if __name__ =="__main__":
    run()
#expected = 4 * 1 = 4 seconds
#actual =  4.401406764984131
