import serial
import time

port = serial.Serial("COM4", timeout = 10)

time.sleep(2) # waits for the port to initialize

port.write(b'54')
