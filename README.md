
<img src="https://github.com/Tom-Vulpes/Spoke/assets/165816078/3fd4bdc1-7e99-401a-b058-55a4bf390c39.png" width="100" height="100"> 

SPOKE is a 27 pin capacative touch board using the RP2040 IC from raspberry Pi.

The board is able to do lots of things and can be adapted to your own needs.

The two main examples provided are USB-MIDI and as a Keyboard emulator.

Both are run using Circuitpython, if you are setting up your own device, or trying out a factory reset, then head here to download the latest version and follow the steps to flash it onto the board: https://circuitpython.org/board/raspberry_pi_pico/

You will also need to copy and paste some libraries to the device if they're not already there. The libaries can be downloaded here: https://circuitpython.org/libraries

On your CIRCUITPY device there is a folder that says lib. You will need to just **copy/paste the following libraries** from the bundle into that folder.

For USB MIDI you will need the folder that says **adafruit_midi.**
For the Keyboard emulator you will need the folder that says **adafruit_hid.**
You will also need the **neopixel.mpy** file for any LED controls.
