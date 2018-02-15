#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 13:00:34 2018

@author: derek
"""

import asyncio
import sys
import logging
import time
import json

#SERVER_ADDRESS = ('127.0.0.1', 8199)
SERVER_ADDRESS = ('192.168.86.177', 8199)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')


class SensorClient(asyncio.Protocol):
       
    def __init__(self):
        self.buffer = None
        self.data_ready = False
        #self.loop = loop

    def connection_made(self,transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log = logging.getLogger(
            'SensorServer_{}_{}'.format(*self.address)
        )
        self.log.debug('connection accepted')
#        SensorServer.clients[self.address] = self.transport
#        print(SensorServer.clients)
        
    def data_received(self,data):
        #self.log.debug('received {!r}'.format(data))
        #self.transport.write(data)
        #self.log.debug('sent {!r}'.format(data))
        #self.broadcast(data)
        #print('Data received: {!r}'.format(data.decode()))
        self.buffer = json.loads(data)
        self.data_ready = True
        
#    def eof_received(self):
#        self.log.debug('received EOF')
#        if self.transport.can_write_eof():
#            self.transport.write_eof()
   
    def connection_lost(self,error):
#        if error:
#            self.log.error('ERROR: {}'.format(error))
#        else:
#            self.log.debug('closing')
#
#        del SensorServer.clients[self.address]
#        print(SensorServer.clients)
#        super().connection_lost(error)
        print('The server closed the connection')
        print('Stop the event loop')
        #self.loop.stop()
        
    def data_is_ready(self):
        return self.data_ready
    
    def get_buffer(self):
        buffer = self.buffer
        #self.buffer = None
        self.data_ready = False    
        return buffer
 

async def read_buffer(sensors):
    while True:

        for sensor in sensors:
            #print(sensor.data_ready())
            if (sensor.data_is_ready()):
                data = sensor.get_buffer()              
                #print(data)
                #print('T = %5.2f, RH = %6.2f, p = %7.2f' % 
                #      (data['Temperature']['value'],data['RH']['value'],data['Pressure']['value']))
                print('T = %5.2f, RH = %6.2f' % 
                      (data['Temperature']['value'],data['RH']['value']))
                
        await asyncio.sleep(.25)
        #yield from asyncio.sleep(1)

def shutdown():
    tasks = asyncio.Task.all_tasks()
    for t in tasks:
        t.cancel()
    print("Tasks canceled")
    asyncio.get_event_loop().stop()
    #await asyncio.sleep(1)
    
if __name__ == "__main__":

    #sensor = SHT31()
    #sensor = HumiChip()
    #sensor = DummyTRHP()
    event_loop = asyncio.get_event_loop()
#    factory = event_loop.create_server(SensorServer, *SERVER_ADDRESS)
    sensors = []
    sensor = SensorClient()
    sensors.append(sensor)
    print('%r' % (sensor.data_is_ready()))
    factory = event_loop.create_connection(lambda: sensor, *SERVER_ADDRESS)
    #server = asyncio.ensure_future(factory)
    client = event_loop.run_until_complete(factory)
    
    task = asyncio.ensure_future(read_buffer(sensors))
    task_list = asyncio.Task.all_tasks()
    
    try:
        event_loop.run_until_complete(asyncio.wait(task_list))
        #event_loop.run_forever()
    except KeyboardInterrupt:
        print('closing server')
        #client.close()
        #event_loop.run_until_complete(client.wait_closed())       
        
        shutdown()
#        for task in task_list:
#            print("cancel task")
#            task.cancel()
        #server.close()
        event_loop.run_forever()
        #event_loop.run_until_complete(asyncio.wait(asyncio.ensure_future(shutdown)))
        
    finally:
        
        print('closing event loop')
        event_loop.close()
