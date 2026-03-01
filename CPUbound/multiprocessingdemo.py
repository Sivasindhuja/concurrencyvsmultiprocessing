from multiprocessing import Process
import time

def fib(n):
    if(n<=1):
        return n
    return fib(n-1) +fib(n-2)

def task():
    fib(38)

def run():
    processes = []
    start = time.time()

    for i in range(4):
        p = Process(target=task)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end = time.time()
    print("Total Time:", end - start)


if __name__ == "__main__":
    run()
    
    #expected time = 
    #actual time = Total Time: 0.39253997802734375