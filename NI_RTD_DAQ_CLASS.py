# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:43:15 2018

This is a class module for the NI USB DAQ with eight 3 wire RTD's 

@author: jmajor
"""

import nidaqmx
from nidaqmx.constants import ExcitationSource, TemperatureUnits, ResistanceConfiguration

class DAQ(object):
    
    '''Sets up the DAQ task and assigns 8 RTD channels to it'''
    def __init__(self):
        self.name = 'NI USB RTD DAQ'
        
        self.task = nidaqmx.Task()
        
        self.channels = [0,1,2,3,4,5,6,7] #RTD channels. 
        
        for i in self.channels:
        
            self.task.ai_channels.add_ai_rtd_chan('cDAQ1Mod1/ai{0}'.format(i), ###open the program NIMAX to see channel names###
                                     current_excit_source=ExcitationSource.INTERNAL,
                                     resistance_config = ResistanceConfiguration.THREE_WIRE,
                                     units=TemperatureUnits.DEG_C,
                                     current_excit_val= .001)
        
    
        
        
    '''Reads all RTD channels assigned in __init__ and returns a list of the readout'''    
    def read_DAQ_temps(self):
        
        temperatures = self.task.read(1)
        
        flat = [item for sublist in temperatures for item in sublist] #takes the list of lists and flattens it
        flat = [round(num, 4) for num in flat] #rounds each float in the list
        return flat
    
    '''Closes the task'''
    def close_NI_RTD_DAQ(self):
        self.task.close()
 
        
    def set_channels(self,channels):
        self.task2 = nidaqmx.Task()
        
        self.channels2 = channels #RTD channels. 
        
        for i in self.channels2:
        
            self.task2.ai_channels.add_ai_rtd_chan('cDAQ1Mod1/ai{0}'.format(i), ###open the program NIMAX to see channel names###
                                     current_excit_source=ExcitationSource.INTERNAL,
                                     resistance_config = ResistanceConfiguration.THREE_WIRE,
                                     units=TemperatureUnits.DEG_C,
                                     current_excit_val= .001)

    def read_channels(self):
        temperatures2 = self.task2.read(1)
        
        flat = [item for sublist in temperatures2 for item in sublist] #takes the list of lists and flattens it
        flat = [round(num, 4) for num in flat] #rounds each float in the list
        return flat
    
    
if __name__ == '__main__':
    daq = DAQ()
    daq.set_channels([2,4,5,7])
    daq.read_channels()