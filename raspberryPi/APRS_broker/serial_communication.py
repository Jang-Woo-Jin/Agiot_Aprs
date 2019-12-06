import serial

ser = serial.Serial('/dev/ttyUSB1',9600)
ser.write('1')
