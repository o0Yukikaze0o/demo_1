from numpy import zeros, amax

class Histogram(object):
    """A duration histogram of each pitch"""
    def __init__(self, hist=zeros(128, dtype=int)):
        self.hist = hist
        self.active = set() # store currently pressed keys
        self.max = 1

    def new_note(self,msg):
        """handle a new message"""
        self.update(msg.time)
        if msg.type == "note_on":
            if velocity > 0:
                self.active.add(msg.note)
            else:
                # a note_on with 0 velocity is actually a note_off
                self.active.remove(msg.note)
        elif msg.type == "note_off":
            self.active.remove(msg.note)

    def update(self,ticks):
        """Update the histogram for pressed keys"""
        for key in self.active:
            self.hist[key] += ticks
        self.max = amax(self.hist)

class ProgressBar(object):
    """status of the progress bar"""
    def __init__(self, maxTick=1):
        self.now = 0
        self.max = maxTick

    def update(self,ticks):
        if ticks == -1:
            self.now = 0
        else:
            self.now += ticks
        