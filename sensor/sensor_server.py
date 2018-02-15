#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 12:57:57 2017

@author: derek
"""
import asyncio
import sys
import logging
import time
#import encodings.idna
#from trh_sensor import SHT31
#from trh_sensor import HumiChip
from environmental_sensor import DummyTRHP

#SERVER_ADDRESS = ('192.168.86.177', 8199)
SERVER_ADDRESS = ('127.0.0.1', 8199)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')


class SensorServer(asyncio.Protocol):
    
    clients={}
    def __init__(self):
        self.buffer = ""    

    def connection_made(self,transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log = logging.getLogger(
            'SensorServer_{}_{}'.format(*self.address)
        )
        self.log.debug('connection accepted')
        SensorServer.clients[self.address] = self.transport
        print(SensorServer.clients)
        
    def data_received(self,data):
        self.log.debug('received {!r}'.format(data))
        self.transport.write(data)
        self.log.debug('sent {!r}'.format(data))
        #self.broadcast(data)
        
    def eof_received(self):
        self.log.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()
        
    def connection_lost(self,error):
        if error:
            self.log.error('ERROR: {}'.format(error))
        else:
            self.log.debug('closing')

        del SensorServer.clients[self.address]
        print(SensorServer.clients)
        super().connection_lost(error)

    def send_to_clients(msg):    
        #print ("clients:" + clients)
        for k,v in SensorServer.clients.items():
            #print(v)
            w=v
            #w.write((msg+'\n').encode('idna'))
            w.write((msg+'\r\n').encode())


async def read_sensor(srv,sensor):
    while True:
	# write to clients	
        #print("T=25.0,RH=34.5")
        #srv.send_to_clients("T=25.0,RH=34.5")
        start = time.time()
        srv.send_to_clients(sensor.read())
        end = time.time()
        delta = end-start
        while (delta > 1):
            delta -= 1.0
        #print('delta = %3.2f, sleep = %3.2f' % (delta, (1-delta)))    
        #print("read_sensor")
        await asyncio.sleep(1.0-delta)
        #await asyncio.sleep(.5)
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
    sensor = DummyTRHP()
    event_loop = asyncio.get_event_loop()
    factory = event_loop.create_server(SensorServer, *SERVER_ADDRESS)
    #server = asyncio.ensure_future(factory)
    server = event_loop.run_until_complete(factory)
    
    task = asyncio.ensure_future(read_sensor(SensorServer,sensor))
    task_list = asyncio.Task.all_tasks()
    
    try:
        event_loop.run_until_complete(asyncio.wait(task_list))
        #event_loop.run_forever()
    except KeyboardInterrupt:
        print('closing server')
        server.close()
        event_loop.run_until_complete(server.wait_closed())       
        
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
