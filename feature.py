from threading import Thread

class Feature:
      
    def __init__(self):
        self.thread = None
        self.is_stop = False

    def start(self, args=None):
        self.is_stop = False
        
        if self.thread and self.thread.is_alive(): return

        self.thread = Thread(target=self._thread, args=(args,))
        self.thread.start()

    def stop(self):
        self.is_stop = True