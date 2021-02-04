from numpy import zeros, amax
import time

class Histogram(object):
    """A duration histogram of each pitch"""
    def __init__(self, deltaTime, hist=zeros(128, dtype=int)):
        self.hist = hist
        self.active = set() # store currently pressed keys
        self.max = 1
        self.deltaTime = deltaTime
        self.timestamp = time.time()

    def new_note(self,msg):
        """handle a new message"""
        self.update(msg.time)
        if msg.type == "note_on":
            if msg.velocity > 0:
                self.active.add(msg.note)
            else:
                # a note_on with 0 velocity is actually a note_off
                self.active.remove(msg.note)
        elif msg.type == "note_off":
            if msg.note in self.active:
                self.active.remove(msg.note)

    def update(self,ticks):
        """Update the histogram for pressed keys"""
        for key in self.active:
            self.hist[key] += ticks
        a = amax(self.hist)
        if a > 0:
            self.max = a
        self.timestamp = time.time()

    def clearActive(self):
        """remove all keys from the active set"""
        ticks = int((time.time() - self.timestamp) / self.deltaTime)
        for key in self.active:
            self.hist[key] += ticks
        self.active = set()
        