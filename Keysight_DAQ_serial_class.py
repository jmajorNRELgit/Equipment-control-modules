# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 03:06:19 2018

@author: Joshua Major

This module contains the DAQ class for the Keysight 34970A.
The methods in this clas allow you to establish communication with the DAQ, check which
chanels have thermocouples attached, and take temperature measurements.

"""
import serial
import sys
import numpy as np
import time

class DAQ(object):

    def __init__(self):
        self.name = 'Keysight 34970A'



    def establish_DAQ_com(self, DAQ_port):

        self.ser = serial.Serial(
                    port = DAQ_port,
                    baudrate=9600,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    bytesize = serial.EIGHTBITS
                )
        self.ser.timeout = 2
        self.ser.flushInput()
        self.ser.write(b'*IDN?\n')
        if str(self.ser.readline()) == "b'HEWLETT-PACKARD,34970A,0,13-2-2\\r\\n'":
            print('\nSerial communication established with DAQ on port:', DAQ_port)
            return self.ser

        else:
            print('Error: Serial communication could not be estableshed for the REF',
                  '\nPlease douple check the port number and change in __main__\n')
            sys.exit()


    def check_for_thermocouples(self):

        #Takes measurements on each of the 20 chanels
        self.ser.write(b'MEAS:TEMP? TCouple, K, (@101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120)\n')

        time.sleep(.5)

        #Reads measurements into a variable
        temps = self.ser.readline()

        #Turns the temperature reading into a list of temps
        temps = list(map(float, str(temps).lstrip("b'").rstrip("\\r\\n'").split(',')))

        temps = np.array(temps)

        #Empty thermocouple chanels read very large negative numbers so this finds where
        #the chanel readings are above -100 degrees
        #Add 1 because the chanels start at 101 and not 100
        thermocuople_locations = np.where(temps > -100)[0] +1

        print('\nThermocouples found on chanels: {0}'.format(str(thermocuople_locations)))

        self.chanles = list(thermocuople_locations)
        
        return list(thermocuople_locations)


    def measure_thermocouples(self, chanels = None):
        #print('Reading temperatures from DAQ')
        if chanels == None:
            chanels = self.chanles
        chanel_list = []
        for location in chanels:
            if int(location) <10:
                chanel_list.append('10{0}'.format(str(location)))
            else:
                chanel_list.append('1{0}'.format(str(location)))

        chanel_list = str(chanel_list).rstrip(']').lstrip('[').replace("'", "")
        command = 'MEAS:TEMP? TCouple, K, (@{0})\n'.format(chanel_list)
        #print('\nReading chanels: {0}'.format(chanel_list))
        self.ser.write(command.encode())
        temp_bytes = self.ser.readline()
        temp_list = list(map(float, str(temp_bytes).lstrip("b'").rstrip("\\r\\n'").split(',')))
        #print('\n',temp_list)
        return temp_list
        
if __name__ == '__main__':
    obj = DAQ()
    