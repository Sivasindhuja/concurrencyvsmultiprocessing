#using recursive fibanacci series
import time

startfun=time.time()
def fib(n):
    if(n<=1):
        return n
    return fib(n-1) +fib(n-2)


ans=fib(35)

endfunc=time.time()

print(" ans is",ans,"time is",endfunc-startfun)  #gives time as 0.9688231945037842
def run():
    start=time.time()

    for i in range(5):
        fib(38)

    end=time.time()
    print("total time : ",end-start)

if __name__ == "__main__":
    run()

#expected = 4*1 =4 seconds
#actual =  4.97472357749939




