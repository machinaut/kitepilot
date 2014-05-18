#!/usr/bin/env python

import serial

port = serial.Serial(port='/dev/ttyp0',
                     baudrate=19200,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS
                    )

while(1):
    data = port.read()
    for a in data:
        print hex(a)

