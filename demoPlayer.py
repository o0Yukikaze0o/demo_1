from pygame import midi
from mido import MidiFile
import time

MIDI_FILE_NAME = "(Nozomi Tenma) Clannad - _Shining in the Sky_.mid"

mid = MidiFile(MIDI_FILE_NAME, clip=True)
print(mid)
print("Duration: "+str(mid.length)+"s.")

# calculate the duration (seconds) of a single tick
try:
    tempo = mid.tracks[0][1].tempo
except Exception as e:
    tempo = 500000 # default setting
deltaTime = tempo / mid.ticks_per_beat * 1e-6
print("Seconds pre tick: "+str(deltaTime)+"s.")

# find the track called "Piano"
track = []
for t in mid.tracks:
    if t.name == "Piano":
        track = t 

if track:
    midi.init()
    player = midi.Output(1)
    player.set_instrument(32) # default setting
    # timestamp = time.time()

    for msg in track:
        if msg.type == "program_change": # change instruments
            time.sleep(msg.time * deltaTime)
            player.set_instrument(msg.program)
        elif msg.type == "note_on": 
            time.sleep(msg.time * deltaTime)
            player.note_on(msg.note, msg.velocity)
        elif msg.type == "note_off": 
            time.sleep(msg.time * deltaTime)
            player.note_off(msg.note, msg.velocity)

    midi.quit()
else:
    print("Failed to find the Piano track")
