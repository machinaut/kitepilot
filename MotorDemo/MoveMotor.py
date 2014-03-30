import serial
from time import sleep
from random import randint
ser = serial.Serial('COM7', 9600)

#wait for arduino to reset
sleep(2)

#send a newline to tell arduino to start
ser.write('\n')
    
#wait for GO (calibration done)
while "GO" not in ser.readline():
    pass

while True:
    pos = str(randint(0,1023))
    print pos
    ser.write(pos + '\n')
    sleep(1)
    
#this never happens
ser.close()
