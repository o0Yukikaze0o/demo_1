# README
## Background
This simple application can play the piano track in a given MIDI file, and calculate the pitch histogram of all played notes.

It can also generate short random rhythms based on the frequencies of occurrence of ten most common notes in the histogram. The rhythm would be played once after generating, and users may save the rhythm if they like it.

It takes me a whole night to develop it. I hope this demo can prove my ability of working with python.

## Setup
To be able to use this project one must have following packages installed:
- **pygame**
- **mido**
- **numpy**

After the installation, users may use the application by running the file **generator.py**.
Users may change the path of input and output MIDI files by editing **MIDI_FILE_NAME** and **OUTPUT_FILE_NAME** in **generator.py** (Line 6 and 7).

## Usage

![UI](https://github.com/o0Yukikaze0o/demo_1/blob/main/UI_demo.PNG "a screenshot of the application")

- Button "||>": Play or pause the current track
- Button "RAND": Generate a short piece of random rhythm based on the current histogram
- Button "SAVE": Save this random rhythm
- Button "CLEAR": Reset the histogram
- Progress bar: Adjust the playback progress of the current track
