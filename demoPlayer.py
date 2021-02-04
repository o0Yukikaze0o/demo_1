from pygame import midi
from mido import MidiFile, MidiTrack, MetaMessage, Message
import time
from numpy import random
class Player(object):
    """MIDI Music Player"""
    def __init__(self, file, device):
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
        self.player = device
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

class RandomNote(object):
    """Generate a random note with the given pitch and probability"""
    def __init__(self, name, deltaTime, device, index=[], probability=[]):
        self.name = name
        self.deltaTime = deltaTime
        self.index = index
        self.probability = probability
        self.note = []
        self.player = device
        self.player.set_instrument(32)

    def read(self,index,probability):
        self.index = index
        self.probability = probability

    def generate(self):
        if self.probability:
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(track)

            track.append(MetaMessage("track_name",name="Piano"))
            track.append(Message('program_change', program=0, time=0))

            note = random.randint(0,self.probability[-1],24)
            for i in range(24):
                for p in range(10):
                    if note[i] <= self.probability[p]:
                        note[i] = self.index[p]
                        break
            for n in note:
                track.append(Message("note_on", note=n,velocity=64,time=32))
                track.append(Message("note_off", note=n,velocity=64,time=64))
            track.append(MetaMessage("end_of_track",time=32))
            self.note = mid
        else:
            self.note = []

    def play(self):
        if self.note:
            for msg in self.note.tracks[0]:
                if msg.type == "program_change": # change instruments
                    time.sleep(self.deltaTime*msg.time)
                    self.player.set_instrument(msg.program)
                elif msg.type == "note_on": 
                    time.sleep(self.deltaTime*msg.time)
                    self.player.note_on(msg.note, msg.velocity)
                elif msg.type == "note_off": 
                    time.sleep(self.deltaTime*msg.time)
                    self.player.note_off(msg.note, msg.velocity)

    def save(self):
        if self.note:
            self.note.save(self.name)
