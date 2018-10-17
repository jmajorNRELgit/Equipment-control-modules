# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:22:03 2018

@author: Joshua Major

This module contains the class for the Fluke 6330 calibration bath over rs232 using a serial to usb adapter
It has methods for establishing comunication, reading the current set temp, setting the set temp, and 
reading the current temperature as measured by the bath. 
"""
import serial
import sys


class bath(object):
    
    def __init__(self):
        self.name = 'Fluke 6330 calibration bath'
        
    def establish_bath_com(self, bath_port):
        '''This function establishes communication with the bath.
        It requires an argument string stating the com port.'''
        
        ser = serial.Serial(
            port= bath_port,
            baudrate=2400,
            parity= serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            
        )
        
        ser.timeout = 2
        
        ser.flushInput()
        ser.write(b'*IDN?\r')
        IDN = ser.readline()
        IDN = str(ser.readline())
        print(IDN)
        if IDN == "b'HART,2100,0,4.01\\r\\n'":
            print('\nSerial communication established with bath on port:', bath_port)
            self.bath_com =  ser
        
        else:         
            print('Error: Serial communication could not be estableshed for the bath',
                  '\nPlease douple check the port number and change in __main__\n')
            sys.exit()

    def read_bath_setpoint(self):
        
        self.bath_com.flushInput()
        self.bath_com.write(b's\r')
        self.bath_com.readline()
        setpoint = str(self.bath_com.readline()).lstrip("b'set:   ").rstrip("\\r\\n'")
        return setpoint
    
    def set_bath_setpoint(self, setpoint):
        
        self.bath_com.flushOutput()
        self.setpoint = setpoint
        self.setpoint = 's = {0}\r'.format(self.setpoint)
        self.setpoint = self.setpoint.encode()
        self.bath_com.write(self.setpoint)
        
        
        
    def read_bath_temp(self):
          
        self.bath_com.flushInput()
        self.bath_com.write(b't\r')
        self.bath_com.readline()
        bath_temp = str(self.bath_com.readline()).lstrip("b't:   ").rstrip(" C\\r\\n'")
        return bath_temp  
    
    def close_bath(self):
        self.bath_com.close()