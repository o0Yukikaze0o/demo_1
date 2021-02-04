from pygame import midi
from mido import MidiFile
import time
class Player(object):
    """MIDI Music Player"""
    def __init__(self, file):
        self.mid = MidiFile(file, clip=True)
        # calculate the duration (seconds) of a single tick
        try:
            tempo = self.mid.tracks[0][1].tempo
        except Exception as e:
            tempo = 500000 # default setting
        self.deltaTime = tempo / self.mid.ticks_per_beat * 1e-6
        # find the track called "Piano"
        self.track = []
        for t in self.mid.tracks:
            if t.name == "Piano":
                self.track = t 
                break
        midi.init()
        self.player = midi.Output(1)
        self.player.set_instrument(32)
        self.isPlaying = False
        self.nextTick = 0
        self.maxTick = len(self.track)
        try:
            self.wait = self.track[0].time * self.deltaTime
        except Exception as e:
            self.wait = 0
        self.timeForNextMessage = time.time() + self.wait 

    def playNextMessage(self,timestamp):
        msg = []
        if timestamp >= self.timeForNextMessage:
            msg = self.track[self.nextTick]
            # messages that won't affect playing would be ignored
            if msg.type == "program_change": # change instruments
                self.player.set_instrument(msg.program)
            elif msg.type == "note_on": 
                self.player.note_on(msg.note, msg.velocity)
            elif msg.type == "note_off": 
                self.player.note_off(msg.note, msg.velocity)

            if self.nextTick+1 >= self.maxTick:
                self.nextTick = 0
                self.isPlaying = False
                self.timeForNextMessage = time.time()
                self.wait = 0
            else:
                self.nextTick += 1
                self.wait = self.track[self.nextTick].time * self.deltaTime
                self.timeForNextMessage = time.time() + self.wait
        return msg

    def update(self, flag=True):
        """recalculate waiting time for next message."""
        if flag:
            self.isPlaying = not self.isPlaying
            if self.isPlaying:
                self.timeForNextMessage = time.time() + self.wait
            else:
                self.wait = self.timeForNextMessage - time.time()
        else:
            self.timeForNextMessage = time.time()
            self.wait = 0
