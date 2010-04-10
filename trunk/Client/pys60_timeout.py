import time
import threading

class timer(threading.Thread):
    def __init__(self, interval):
        threading.Thread.__init__(self)
        self.interval = interval
        
    def run(self):
        print 'berfore'
        time.sleep(self.interval)
        print 'after'
        
def test():
    threadone = timer(10)
    threadone.setDaemon(True)
    threadone.start()
    time.sleep(15)
    
if __name__ == '__main__':
    test()

