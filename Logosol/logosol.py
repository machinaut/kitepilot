#!/usr/bin/env python

from construct import *
import serial
import pdb
import time

class Logosol():
    def __init__(self, serial_port = None):
        self.ser = serial.Serial(
            port = serial_port,
            baudrate=19200,
            timeout = 0.5,
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
        cksum = (addr + ord(cmd) + (nbytes * 16) + sum(data)) & 0xFF
        packet = self.TxPacket.build(Container(header=170, address = addr,
                                     datalen = nbytes, cmd = ord(cmd),
                                     cmd_data = data, checksum = cksum))
        return packet
        
    # Low level recieve function
    def _parse_packet(self, rx_data):
        length = len(rx_data)
        
        packet = bytearray(rx_data)
        
        lastbyte = packet.pop()
        checksum = sum(packet) & 0xFF
        
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
	
	
    def _logosol_rw(self, data):
	# Clear the RX buffer
	self.ser.flushInput()
	
	#Write the data
	self.ser.write(data)
	
	# Wait for at least 10ms, just in case the logosol is busy
	time.sleep(0.010)
	
	# Get the number of bytes available
	nBytes = self.ser.inWaiting()

	# Read back the available bytes
	rxData = self.ser.read(nBytes)
	
	# We should parse the response here!!!
	return rxData
	
    def ResetPositionCounter(self):
        packet = self._make_packet(addr = 0, cmd = 'reset_pos')
        self.ser.write(packet)
        
    
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
            
            self.ser.write(packet)

    
    def SetTrajectory(self, pos = None, vel = None, acc = None, PWM = None,
                            mode = "PWM", profile = "TRAP", start = False):

	# Start at one (for the control byte!)
	ndatabytes = 1
	if pos not None:
		pos_set = 1
		# Servo Mode
		servo_mode = 1
		ndatabytes += 4
	else:
		pos_set = 0
		# PWM Mode
		servo_mode = 0

	if vel not None:
		# Setting velocity 
		vel_set = 1
		ndatabytes += 4	
	else:
		# Not Setting Velocity
		vel_set = 0

	if acc not None:
		# Set Acceleration
		acc_set = 1
		ndatabytes += 4
	else:
		# Not Setting Acceleration
		acc_set = 0

	if PWM not None:
		PWM_set = 1
		# PWM Mode
		servo_mode = 0
		ndatabytes += 1
	else:
		PWM_set = 0
		# Position Servo
		servo_MODE = 1
	
	# This byte tells the Logosol what is being set, and the # of data bytes to expect
	control_byte = BitStruct('control',
				 BitField('pos'),
				 BitField('vel'),
				 BitField('acc'),
				 BitField('pwm'),
				 BitField('servo'),
				 BitField('profile'),
				 BitField('vel_pwm'),
				 BitField('start?'))

	control_data = control_byte.build(pos = pos_set, vel = vel_set, acc = acc_set, pwm = PWM_set, vel_pwm = servo_mode, start = start)
				     
	# Put the command data into a struct.
	# The optional macros will leave out all of their data if the value to build is None.
	trajectory_struct = Struct(Optional(UBInt32('Position')),
				   Optional(UBInt32('Velocity')),
				   Optional(UBInt32('Acceleration')),
				   Optional(UBInt8('PWM')))
	
	trajectory_data = trajectory_struct.build(Position = pos, Velocity = vel, Acceleration = acc, PWM = PWM)
	
	
	# The control byte + trajectory bytes = the data bytes
	data = control_data + trajectory_data
	
	# Make a packet out of all this stuff
	packet = self._make_packet(addr = 0, cmd = 'load_traj', data = data)
	
	# Write da packet
	self._logosol_rw(packet)
	
    def send_reset(self):
        packet = self._make_packet(addr = 0, cmd = 'nop') 
        print 'Command:'
        self.print_hex(packet)
	
	# Write da packet
	return self._logosol_rw(packet)
        
    def print_hex(self, data):
        for c in data:
            print hex(ord(c)),
        print '\n'


