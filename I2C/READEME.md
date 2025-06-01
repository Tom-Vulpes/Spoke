A quick note on the I2C usage on the SPOKE board.

Due to the architecture of the RP2040 chip, when you use the i2c pins on GP26 and GP27, it disbales the use of GP28 and GP29 as a touch sensor. 
