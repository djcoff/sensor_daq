#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 14:45:22 2017

@author: derek
"""

import abc
#import asyncio
#from OmegaExpansion import onionI2C
import time
from datetime import datetime
import json
import random # for Dummy class


class Environmental_Sensor(metaclass=abc.ABCMeta):

    def __init__(self):

        # init data dictionaries
        self.data = {}
        self.metadata = {}

        self.metadata['Name'] = 'TRH_Sensor'
        self.metadata['Type'] = 'Temperature_RH'
        self.metadata['Mfg'] = None
        self.metadata['Model'] = None
        self.metadata['SerialNum'] = None
        self.metadata['MeasurementList'] = None
       
        print("Name: ", self.metadata['Name'])
        
        
        #info = InstrumentInfo()
        #interface = Interface()
        #self.loop = asyncio.get_event_loop()
        #self.task_list = []
        
    @abc.abstractmethod
    def configure(self):
        pass

    def _add_timestamp(self):
        self.data['DateTime'] = datetime.utcnow().isoformat(timespec='seconds')
        
#    def get_temperature(self):
#        return self.data['Temperature']
#
#    def _set_temperature(self, temp): # temp is a dictionary
#        self.data['Temperature'] = temp
#        
#    def _set_temperature_value(self, tempval): # tempval is a float
#        self.data['Temperature']['value'] = tempval
#
#    def get_rh(self):
#        return self.data['RH']
#
#    def _set_rh(self, rh): # rh is a dictionary
#        self.data['RH'] = rh
#
#    def _set_rh_value(self, rhval): # rhval is a float
#        self.data['RH']['value'] = rhval

 
    
    def _valid_param(self,param):
        if param in self.metadata['MeasurementList']:
            return True
        else:
            return False
        
    # define data of type param using values(dictionary)
    def _set_param(self,param,values):
        if (self._valid_param(param)):
            self.data[param] = values
        
    # define "value' field of type param using value  
    # do I want to check for valid entry?
    def _set_param_value(self,param,value):
        # param is in self.metadata['MeasurementList']
        if (self._valid_param(param)):
            self.data[param]['value'] = value


    @abc.abstractmethod
    def read(self):
        pass

    def get_data(self, format='json'):
        
        if (format=='json'):
            return json.dumps(self.data)
        else:
            return json.dumps(self.data) # default
        
    def get_metadata(self):
        return json.dumps(self.metadata)
    

class DummyTRHP(Environmental_Sensor):

    def __init__(self):
        super().__init__()
        self.metadata['Name'] = 'Dummy'
        self.metadata['Type'] = 'Temperature_RH_Pressure'
        self.metadata['Mfg'] = 'ACME'
        self.metadata['Model'] = 'Dummy'
        self.metadata['MeasurementList'] = ['Temperature','RH','Pressure']
        
        print("Name: ", self.metadata['Name'])
        
        # Get I2C bus
        #self.i2c = onionI2C.OnionI2C()
        
        rh={}
        rh['value']=-9999.0
        rh['units'] = '%'
        rh['error'] = 2
        self._set_param('RH',rh)

        temp={}
        temp['value']=-9999.0
        temp['units'] = 'C'
        temp['error'] = 0.5
        self._set_param('Temperature',temp)

        p={}
        p['value']=-9999.0
        p['units'] = 'mb'
        p['error'] = 0.5
        self._set_param('Pressure',p)
        
        
    def configure(self):
        pass
    
    
    
    def read(self,format='json'):

        # SHT31 address, 0x44(68)
        # Send measurement command, 0x2C(44)
        #		0x06(06)	High repeatability measurement
        data = [0x06]
        #self.i2c.writeBytes(0x44, 0x2C, data)

        time.sleep(0.5)

        # SHT31 address, 0x44(68)
        # Read data back from 0x00(00), 6 bytes
        # Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
#        data = self.i2c.readBytes(0x44, 0x00, 6)
#        
#        # Convert the data
#        temp = data[0] * 256 + data[1]
#        cTemp = -45 + (175 * temp / 65535.0)
#        #fTemp = -49 + (315 * temp / 65535.0)
#        rh = 100 * (data[3] * 256 + data[4]) / 65535.0
        
        #should do CRC check but have to figure that out.

        cTemp = 25 + random.randrange(0,100)/100
        rh = 60 + random.randrange(0,100)/100
        p = 1010 + random.randrange(0,100)/50
        

        # set data values
        self._set_param_value('RH',rh)
        self._set_param_value('Temperature',cTemp)
        self._set_param_value('Pressure',p)
        self._add_timestamp()
        
        print(self.data['DateTime'])
        
        #return json.dumps(self.data)
        return self.get_data()

    
class SHT31(Environmental_Sensor):

    def __init__(self):
        super().__init__()
        self.metadata['Name'] = 'SHT31'
        self.metadata['Type'] = 'Temperature_RH'
        self.metadata['Mfg'] = 'ACME'
        self.metadata['Model'] = 'SHT31-D'
        self.metadata['MeasurementList'] = ['Temperature','RH']
        
        print("Name: ", self.metadata['Name'])
        
        # Get I2C bus
        self.i2c = onionI2C.OnionI2C()
        
        rh={}
        rh['value']=-9999.0
        rh['units'] = '%'
        rh['error'] = 2
        self._set_param('RH',rh)
        #self._set_rh(rh)

        temp={}
        temp['value']=-9999.0
        temp['units'] = 'C'
        temp['error'] = 0.5
        self._set_param('Temperature',temp)
        #self._set_temperature(temp)
        
        #self.data['RH'] = rh
        #self.data['Temperature'] = temp
        #print(self.data)
        
    def configure(self):
        pass
    
    
    
    def read(self,format='json'):

        # SHT31 address, 0x44(68)
        # Send measurement command, 0x2C(44)
        #		0x06(06)	High repeatability measurement
        data = [0x06]
        self.i2c.writeBytes(0x44, 0x2C, data)

        time.sleep(0.5)

        # SHT31 address, 0x44(68)
        # Read data back from 0x00(00), 6 bytes
        # Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        data = self.i2c.readBytes(0x44, 0x00, 6)
        
        # Convert the data
        temp = data[0] * 256 + data[1]
        cTemp = -45 + (175 * temp / 65535.0)
        #fTemp = -49 + (315 * temp / 65535.0)
        rh = 100 * (data[3] * 256 + data[4]) / 65535.0
        
        #should do CRC check but have to figure that out.

        # set data values
        self._set_param_value('RH',rh)
        #self._set_rh_value(rh)
        self._set_param_value('Temperature',cTemp)
        #self._set_temperature_value(cTemp)
        self._add_timestamp()
        
        # return formatted data string (defaults to 'json')
        #self.data['RH']['value']=rh
        #self.data['Temperature']['value']=cTemp
        #self.data['DateTime'] = datetime.utcnow().isoformat(timespec='seconds')
        print(self.data['DateTime'])
        
        #return json.dumps(self.data)
        return self.get_data()


class HumiChip(Environmental_Sensor):

    def __init__(self):
        super().__init__()
        self.metadata['Name'] = 'HumiChip'
        self.metadata['Type'] = 'Temperature_RH'
        self.metadata['Mfg'] = 'Samyoung S&C / ncd.com'
        self.metadata['Model'] = 'HCPA_5V_U3'
        self.metadata['MeasurementList'] = ['Temperature','RH']
        
        print("Name: ", self.metadata['Name'])
        
        # Get I2C bus
        self.i2c = onionI2C.OnionI2C()
        
        rh={}
        rh['value']=-9999.0
        rh['units'] = '%'
        rh['error'] = 3
        self._set_param('RH',rh)
        #self._set_rh(rh)

        temp={}
        temp['value']=-9999.0
        temp['units'] = 'C'
        temp['error'] = 0.3
        self._set_param('Temperature',temp)
        #self._set_temperature(temp)
        
        #self.data['RH'] = rh
        #self.data['Temperature'] = temp
        #print(self.data)
        
    def configure(self):
        pass
    
    
    
    def read(self,format='json'):

        # Code from https://github.com/ControlEverythingCommunity/HCPA-5V-U3/blob/master/Onion%20Omega%20Python/HCPA_5V_U3.py
        # HCPA_5V_U3 address, 0x28(40)
        # Send start command, 0x80(128)
        data = [0x80]
        self.i2c.write(0x28, data)
        
        time.sleep(0.5)
        
        # HCPA_5V_U3 address, 0x28(40)
        # Read data back, 4 bytes
        # humidity msb, humidity lsb, cTemp msb, cTemp lsb
        data = self.i2c.readBytes(0x28, 0x00, 4)
        
        # Convert the data to 14-bits
        rh = (((data[0] & 0x3F) * 256) + data[1]) / 16384.0 * 100.0
        cTemp = (((data[2] * 256) + (data[3] & 0xFC)) / 4) / 16384.0 * 165.0 - 40.0
        fTemp = (cTemp * 1.8) + 32
        
        #should do CRC check but have to figure that out.

        # set data values
        self._set_param_value('RH',rh)
        #self._set_rh_value(rh)
        self._set_param_value('Temperature',cTemp)
        #self._set_temperature_value(cTemp)
        self._add_timestamp()
        
        # return formatted data string (defaults to 'json')
        #self.data['RH']['value']=rh
        #self.data['Temperature']['value']=cTemp
        #self.data['DateTime'] = datetime.utcnow().isoformat(timespec='seconds')
        print(self.data['DateTime'])
        
        #return json.dumps(self.data)
        return self.get_data()
         