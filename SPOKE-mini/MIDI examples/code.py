# This is the code for USB-MIDI. In this code we assign a midi value to each pin, and when the board senses that the pin has been touched it will send a NoteOn message. When the pin is released, it sends a NoteOff message.

import time
import board
import touchio
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# Define the touch pins
touch_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19, board.GP20, board.GP21, board.GP22, board.GP26, board.GP27, board.GP28]

touch_sensors = []
for pin in touch_pins:
    try:
        touch_sensors.append(touchio.TouchIn(pin))
    except ValueError:
        print(f"No pulldown resistor found on pin {pin}, skipping...")


# MIDI setup - If you want to assign the midi device to a specific channel or port then just change the values in this line.
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# MIDI note numbers corresponding to each touch pin - change these to whatever midi note you prefer. 
midi_notes = [36, 38, 40, 43, 45, 48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72, 74, 76, 79, 81, 84, 86, 88, 91, 93, 96] 

# State variables to track if a note has been played for each touch pin
note_played = [False] * len(touch_pins)

# Setup LED toggling
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Main loop
while True:
    for i, touch_sensor in enumerate(touch_sensors):
        # Capacitive touch sensing
        if touch_sensor.value:
            # Check if the note has already been played
            if not note_played[i]:
                # Send MIDI note on message when touch is detected. The Velocity is set to 120, change the value if you want to.
                midi.send(NoteOn(midi_notes[i], 120))
    		led.value = True
                note_played[i] = True  # Update state variable
        else:
            # Check if the note has been played and turn it off
            if note_played[i]:
                # Send MIDI note off message when touch is released
                midi.send(NoteOff(midi_notes[i], 120))
		led.value = False
                note_played[i] = False  # Update state variable
