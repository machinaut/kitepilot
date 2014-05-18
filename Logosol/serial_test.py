#!/usr/bin/env python

import os
import sys
import logosol
import time

if len(sys.argv) != 2:
    print "Provide the serial device as the first and only arguement!"
    print "Ex:"
    print "    serial_test.py /dev/tty01" 

mc = logosol.Logosol(serial_port = sys.argv[1])

res = mc.send_reset()
#res = mc.ser.read(size=5)

print 'Response:'
for a in res:
    print hex(ord(a))
