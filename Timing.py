import time


class Timer(object):
    def __init__(self, interval):
        self.interval = interval
        self.previous = 0
        self.current = time.time()

    def get_interval(self):
        return self.interval

    def set_interval(self, interval):
        self.interval = interval

    def valid(self):
        self.current = time.time()
        if (self.current - self.previous) >= self.interval:
            self.previous = self.current
            return True
        else:
            return False
