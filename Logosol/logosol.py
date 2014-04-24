#!/usr/bin/env python

from construct import *

LogosolTxPacket = Struct("TxData",
                         UBInt8("header"),
                         UBInt8("address"),
                         #UBInt8("command"),
                         #BitStruct("command", Nibble("datalen"), Nibble("cmd")),
                         EmbeddedBitStruct( Nibble("datalen"),
                                            Nibble("cmd")),
                         Array(lambda ctx: ctx.datalen, UBInt8("cmd_data")),
                         UBInt8("checksum"))

example_packet = LogosolTxPacket.build(Container(header = 170, address= 3,
datalen = 2, cmd = 1, cmd_data = [1,2], checksum = 128))

print map(hex,map(ord,example_packet))

