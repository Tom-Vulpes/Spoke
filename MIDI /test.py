# SPOKE Main Board - Default Code with Debounce & Stability Fixes
import time
import board
import touchio
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import neopixel
from rainbowio import colorwheel

# MIDI note numbers corresponding to each touch pin
midi_notes = [98, 96, 93, 91, 88, 86, 84, 81, 79, 76, 74, 72, 69, 67, 64, 62, 60, 57, 55, 52, 50, 48, 45, 43, 40, 38, 36]

# Define the touch pins
touch_pins = [
    board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8,
    board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16,
    board.GP17, board.GP18, board.GP19, board.GP20, board.GP21, board.GP22, board.GP23, board.GP24,
    board.GP25, board.GP28, board.VOLTAGE_MONITOR
]

# --- DEBOUNCE SETTINGS ---
# How many consecutive reads must agree before a state change is accepted.
# Increase this if you still get bouncing; decrease if response feels sluggish.
DEBOUNCE_COUNT = 3

# Minimum time (seconds) between a note-off and the next note-on for the same pad.
# Prevents rapid re-triggering. 0.03 = 30ms.
RETRIGGER_LOCKOUT = 0.03

# Initialize touch sensors
# Board is powered on with a short settling delay so auto-calibration
# captures a clean baseline (nothing touching the pads).
print("Waiting for sensor calibration to settle...")
time.sleep(0.5)

touch_sensors = []
for pin in touch_pins:
    try:
        touch_sensors.append(touchio.TouchIn(pin))
    except ValueError:
        print(f"No pulldown resistor found on pin {pin}, skipping...")

# Let CircuitPython's touchio finish its auto-threshold calculation
# before we start reading. Without this pause the thresholds can be
# set too low if any nearby hand capacitance is present at boot.
time.sleep(0.3)
print("Calibration complete.")

# MIDI setup
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# State tracking
note_played        = [False] * len(touch_pins)   # is note currently on?
debounce_counter   = [0]     * len(touch_pins)   # consecutive same-state reads
last_release_time  = [0.0]   * len(touch_pins)   # time of last note-off

# NeoPixel setup
num_pixels = len(touch_sensors)
pixels = neopixel.NeoPixel(board.GP0, num_pixels, brightness=0.03, auto_write=True)

# Startup animation
def rainbow(speed, duration, step_size=10):
    start_time = time.monotonic()
    while time.monotonic() - start_time < duration:
        for j in range(0, 256, step_size):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels + j) % 256
                pixels[i] = colorwheel(pixel_index)
            pixels.show()
            if time.monotonic() - start_time >= duration:
                return
            time.sleep(speed)

def all_blue():
    pixels.fill((0, 0, 255))
    pixels.show()

rainbow(0.01, 2, step_size=10)
all_blue()

# Main loop
while True:
    now = time.monotonic()

    for i, touch_sensor in enumerate(touch_sensors):
        raw_touched = touch_sensor.value

        # --- DEBOUNCE ---
        # Increment counter if reading matches the pending new state,
        # reset it if the reading flips back.
        if raw_touched != note_played[i]:
            debounce_counter[i] += 1
        else:
            debounce_counter[i] = 0

        # Only act once the reading has been stable for DEBOUNCE_COUNT loops
        if debounce_counter[i] < DEBOUNCE_COUNT:
            continue

        debounce_counter[i] = 0  # reset after acting

        if raw_touched and not note_played[i]:
            # --- RETRIGGER LOCKOUT ---
            # Ignore note-on if we just released this pad very recently
            if (now - last_release_time[i]) < RETRIGGER_LOCKOUT:
                continue

            midi.send(NoteOn(midi_notes[i], 120))
            note_played[i] = True
            pixels[i] = (255, 0, 255)

        elif not raw_touched and note_played[i]:
            midi.send(NoteOff(midi_notes[i], 120))
            note_played[i] = False
            last_release_time[i] = now
            pixels[i] = (0, 0, 255)
