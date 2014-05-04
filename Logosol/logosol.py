#!/usr/bin/env python

from construct import *
import serial

class Logosol():
    def __init__(self, serial_port = None):
        ser = serial.Serial(
            port = serial_port,
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )

        # This is the binary command string as a struct. Other functions use this to assemble their packets.
        # I will make another struct to parse the recieved data.
        self.TxPacket = Struct("TxData",
                               UBInt8("header"),
                               UBInt8("address"),
                               EmbeddedBitStruct( Nibble("datalen"),
                                                  Nibble("cmd")),
                               Array(lambda ctx: ctx.datalen, ULInt8("cmd_data")),
                               UBInt8("checksum"))

        # Construct has a feature for doing this. I should change over to their method
        # at some point.
        self.RxPacket = Struct("RxData",
                               UBInt8("length"),  # I am adding this length byte to this string
                               UBInt8("status"),
                               Array(lambda ctx: ctx.length, UBInt8("responce")),
                               UBInt8("checksum"))
        
        # All of the available commands
        self.Cmds = Enum( Byte("CMD"),
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
    def _make_packet(self, addr = 0, cmd = 'nop', data = []):
        # Convert the command to the cmd byte
        cmd = self.Cmds.build(cmd)
        
        nbytes = len(data)
         
        # command + nbytes shifted up a nibble makes up the actual command byte
        cksum = addr + (cmd + (nbytes * 16)) + bytearray([sum(data)])
        packet = self.TxPacket.build(Conatiner(header=0xAA, address = addr, command = cmd,
                                                cmd_data = data, checksum = cksum))
        return packet
        
    # Low level recieve function
    def _parse_packet(self, rx_data):
        length = len(rx_data)
        
        packet = bytearray(rx_data)
        
        lastbyte = packet.pop()
        checksum = sum(packet)
        
        # Check the checksum
        if lastbyte != checksum:
            raise ValueError("The checksum for the recieved data is wrong")

        # The data payload is two bytes less than the length of the packet
        data_len = length - 2
        
        # TODO: Replace this extra char with the proper construct way of having
        # variable length data fields!!!
        # Add on a char to so array knows how many data bytes to put into the array
        new_packet = chr(data_len) + rx_data
        
        return self.RxPacket.parse(new_packet)

    def ResetPositionCounter(self):
        packet = self._make_packet(addr = 0, cmd = 'reset_pos')
        ser.write(packet)
        
    
    def SetGains(self, P, V, I, I_lim, Out_lim, Current_lim, Pos_err_lim, Servo_rate_div, Dead_band):
            data_structure = Struct(UBInt16("P_gain"),
                                    UBInt16("V_gain"),
                                    UBInt16("I_gain"),
                                    UBInt16("Int_lim"),
                                    IBInt8("Out_lim"),
                                    IBInt8("Cur_lim"),
                                    IBInt16("Pos_err_lim"),
                                    IBInt8("Servo_rate_div"),
                                    IBInt8("Dead_band"))
                                    
            data_array = data_structure.build(P_gain = P,
                                              V_gain = V,
                                              I_gain = I,
                                              Int_lim = I_lim,
                                              Out_lim = Out_Lim,
                                              Cur_lim = Current_lim,
                                              Pos_err_lim = Pos_err_lim,
                                              Servo_rate_div = Servo_rate_div,
                                              Dead_band = Dead_band)
            
            packet = _make_packet(addr = 0, cmd = 'set_gain', data = data_array)
            
            ser.write(packet)


    def send_reset(self):
        packet = self._make_packet(addr = 0, cmd = 'nop')
        ser.write(packet)
        

