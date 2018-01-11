import threading

class StoppableThread(threading.Thread):
    """Basic Stoppable Thread Wrapper
    Adds event for stopping the execution
    loop and exiting cleanly."""
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.stop_event = threading.Event()
        self.daemon = True

    def start(self):
        if not self.isAlive():
            self.stop_event.clear()
            threading.Thread.start(self)

    def stop(self):
        if self.isAlive():
            self.stop_event.set()
            self.join()