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

LogosolRxPacket = Struct("RxData",
                         UBInt8("length"),  # I am adding this length byte to this string
                         UBInt8("status"),
                         Array(lambda ctx: ctx.length, UBInt8("responce")),
                         UBInt8("checksum"))

LogosolCmds = Enum( Byte("CMD"),
                    reset_pos = 0x00,
                    set_addr  = 0x01,
                    def_stat  = 0x02,
                    read_stat = 0x03,
                    load_traj = 0x04,
                    start_mot = 0x05,
                    set_gain  = 0x06,
                    stp_motor = 0x07,
                    io_ctrl   = 0x08,
                    set_hm_md = 0x09,
                    set_baud  = 0x0A,
                    clear_stat= 0x0B,
                    save_home = 0x0C,
                    nop       = 0x0D,
                    nop2      = 0x0E,
                    hard_rst  = 0x0F)

# Low level send function
def LogosolSend(addr = 0, cmd = 0, data = []):
    
    # command + nbytes shifted up a nibble makes up the actual command byte
    cksum = addr + (cmd + (nbytes * 16)) + sum(data)
    packet = LogosolTxPacket.build(Conatiner(header=0xAA, address = addr, command = cmd,
                                            cmd_data = data, checksum = cksum))
    

def LogosolParse(rx_data):
    length = len(rx_data)
    
    packet = bytearray(rx_data)
    #for a in packet: print a
    
    lastbyte = packet.pop()
    checksum = sum(packet)

    if lastbyte != checksum:
        raise ValueError("The checksum for the recieved data is wrong")

    # The data payload is two bytes less than the length of the packet
    data_len = length - 2
    
    # Add on a char to so array knows how many data bytes to put into the array
    new_packet = chr(data_len) + rx_data
    
    return LogosolRxPacket.parse(new_packet)
    
print LogosolParse(bytearray([1,2,3,4,5,6,21]))

