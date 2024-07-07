
<img src="[https://your-image-url.type](https://github.com/Tom-Vulpes/Spoke/assets/165816078/3fd4bdc1-7e99-401a-b058-55a4bf390c39)" width="100" height="100"> 

SPOKE is a 26 pin capacative touch board using the Raspberry Pi Pico microcontroller.

The board is able to do lots of things and can be adapted to your own needs.

The two main examples provided are USB-MIDI and as a Keyboard emulator.

Both are run using Circuitpython, head here to download the latest version: https://circuitpython.org/board/raspberry_pi_pico/

You will also need to copy and paste some libraries to the device if they're not already there. The libaries can be downloaded here: https://circuitpython.org/libraries

On your CIRCUITPY device there is a folder that says lib. You will need to just copy/paste the following libraries form the bundle into that folder.

For USB MIDI you will need the folder that says adafruit_midi.

For the Keyboard emulator you will need the folder that says adafruit_hid.

It is fine to have both libraries in the lib folder at the same time.

