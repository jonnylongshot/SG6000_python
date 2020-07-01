#!python
#
# sg6000.py
#
# Python interface to SG6000 Signal Generator made by DS Instruments
#   https://www.dsinstruments.com
#
# May be compatibile with other models but not tested.
#
#
# (C)2020 Jonathan Horne
#
import serial
import io
import time

#Define the commands for the SG6000 as listed in the documentation here:
# https://www.dsinstruments.com/support/dsi-scpi-command-list/
class SG6000cmd:
    IDN     = "*IDN"        #Return the SCPI identification string
    RESET   = "*RST"        #Reset instrument
    FREQ    = "FREQ:CW"     #Frequency in Hz
    DBM     = "POWER"       #Output power level in dBm
    RFOUT   = "OUTP:STAT"   #RF output "on" or "off"


#Utility class for controlling the ERAsynth Micro
class SG6000:
    #Back-to-back serial commands don't work without a pause.
    # This delay fixes the problem.
    SEND_DELAY = 0.1    #pause this many seconds after sending

    #Class Initializer
    # Main purpose is to open the serial port
    def __init__(self, serial_device):
        self.ser = serial.Serial(serial_device, 115200, timeout=1, rtscts=0)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

    #Destructor
    def __del__(self):
        self.ser.close()

    #Send a command without a response
    def send_cmd(self, cmd):
        self.sio.write(f"{cmd}\r")
        self.sio.flush()
        time.sleep(self.SEND_DELAY)

    #Send a command and return the response
    def send_cmd_resp(self, cmd):
        self.sio.write(f"{cmd}\r")
        self.sio.flush()
        response = self.sio.readline()
        resp_clean = response.strip()
        return(resp_clean)

    #read device IDN
    def get_idn(self):
        idn = self.send_cmd_resp(f"{SG6000cmd.IDN}?")
        return idn

    #issue reset
    def reset(self):
        self.send_cmd(f"{SG6000cmd.RESET}")

    #get synthesizer frequency
    def get_freq(self):
        freq = self.send_cmd_resp(f"{SG6000cmd.FREQ}?")
        return freq

    #set synthesizer frequency
    def set_freq(self, freq):
        ifreq = int(freq)
        self.send_cmd(f"{SG6000cmd.FREQ} {ifreq}")


    #get output power in dBm
    def get_dbm(self):
        dbm = self.send_cmd_resp(f"{SG6000cmd.DBM}?")
        return dbm

    #set output power in dBm
    def set_dbm(self, dbm):
        fdbm = float(dbm)
        self.send_cmd(f"{SG6000cmd.DBM} {fdbm}")


    #get RF output enaable status
    def get_rfout(self):
        onoff_str = self.send_cmd_resp(f"{SG6000cmd.RFOUT}?")
        return onoff_str

    #set RF output enaable ("on" or "off")
    def set_rfout(self, onoff_str):
        self.send_cmd(f"{SG6000cmd.RFOUT} {onoff_str}")






# Sample usage provided if called from the command line
if __name__ ==  '__main__':
    #Set serial port device for synthesizer here
    serial_dev = '/dev/cu.usbserial-DM01PS7W'

    #Open device with default serial port
    synth = SG6000(serial_dev)

    #reset device (not necessarily needed, included here as demo)
    synth.reset()
    
    #display status
    idn = synth.get_idn()
    print(f"IDN = {idn}")

    #get output frequency
    freq = synth.get_freq()
    print(f"freq = {freq}") #Hz is part of the returned string
        
    #Set output frequency in Hz
    synth.set_freq(500e6)

    #get output power in dBm
    dbm = synth.get_dbm()
    print(f"Power = {dbm} dBm")    

    #Set output amplitude in dBm
    synth.set_dbm(-15)

    #Enable the output, pause, then disable
    synth.set_rfout("on")
    time.sleep(2)
    synth.set_rfout("off")
