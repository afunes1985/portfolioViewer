from random import randint
import threading
import time


def worker(semaphore):
    """thread worker function"""
    time.sleep(randint(0, 3))
    print ('Worker')
    semaphore.release()
    return

    
def main():
    semaphore = threading.Semaphore(value=5)
    threads = []
    for i in range(5):
        semaphore.acquire()
        t = threading.Thread(target=worker, args=(semaphore,))
        t.start()
        threads.append(t)
    print ('Finish with starts')
    
    for thread in threads:
        thread.join()
    print ('Finish')
 

if __name__== '__main__':
    main()

