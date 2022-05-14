""" Timer class """
import time
from datetime import timedelta

class Timer:
    def __init__(self, timerlabel):
        self.running = True
        self.timerlabel = timerlabel
        self.timerlabel['text'] = "00:00:00"
      
    def stop(self):
        self.running = False
        
    def run(self):
        print("update timer")
        start_time = time.time()
        while self.running:
            elapsed_time = time.time() - start_time
            self.timerlabel['text'] = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            time.sleep(1)

    def reset(self):
        self.running = False
        self.timerlabel['text'] = '00:00:00'
  