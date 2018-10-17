# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 03:06:19 2018

@author: Joshua Major

This module contains the REF class for the Instrulab 4201c reference probe.
It has methods to establish the serial communication with the probe and to
take temperature measurements 

git test


"""

import serial
import sys

class REF(object):
    
    def __init__(self):
        self.name = 'Instrulab 4201c'
        
    
    def establish_REF_com(self, REF_port):
    
        ser = serial.Serial(
                    port = REF_port,
                    baudrate=9600,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    bytesize = serial.EIGHTBITS
                )
        ser.timeout = 2
        ser.flushInput()
        ser.write(b'S\n')
        REF_stat = str(ser.readline())
        if REF_stat == "b'U\\r\\n'" or REF_stat == "b'>\\r\\n'":
            print('\nSerial communication established with REF on port:', REF_port)
            return ser
    
        else:         
            print('Error: Serial communication could not be estableshed for the REF',
                  '\nPlease douple check the port number and change in __main__\n')
            sys.exit()
            
            
    def measure_REF_temp(self, REF_com):
        while True:
            REF_com.flushInput()
            REF_com.write(b'T\n')
            temp = str(REF_com.readline())
            if temp == "b'>\\r\\n'":
                temp = str(REF_com.readline())
            try:
                temp = float(temp.lstrip("b'+").rstrip("C1\\r\\n'"))
                return temp
                break
            except ValueError:
               REF_com.flushInput()