#!/usr/bin/env python

from construct import *

# This is the binary command string as a struct. Other functions use this to assemble their packets.
# I will make another struct to parse the recieved data.
LogosolTxPacket = Struct("TxData",
                         UBInt8("header"),
                         UBInt8("address"),
                         EmbeddedBitStruct( Nibble("datalen"),
                                            Nibble("cmd")),
                         Array(lambda ctx: ctx.datalen, UBInt8("cmd_data")),
                         UBInt8("checksum"))

# Checking that I have put the struct together correctly!!!!
example_packet = LogosolTxPacket.build(Container(header = 170, address= 3,
datalen = 2, cmd = 1, cmd_data = [1,2], checksum = 128))

# Print Hex 
print map(hex,map(ord,example_packet))

