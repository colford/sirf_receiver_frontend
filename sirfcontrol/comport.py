# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:32:45 2017

@author: CFord
"""

import serial
import struct

class Comport(object):
    def __init__(self,port,baud,timeout=1):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.crc_mask = pow(2,15) - 1
        self.com = None
    
    def isopen(self):
        return self.com != None
    
    def open(self):
        self.com = serial.Serial(self.port, self.baud, timeout=self.timeout)
        
    def check_crc(self,payload,crc):
        return ( sum(payload) & self.crc_mask ) == crc

    def hunt_for(self,value):
        if ord(self.com.read(1)) == value:
            return True

    def hunt_for_start(self):
        while 1:
            if self.hunt_for(0xA0) and self.hunt_for(0xA2):
                return True
        
    def read_message(self):
        # We need to hunt for 0xA0 0xA2 which is the start of the message
        # then there is a 2 byte length of the payload followed by
        # the payload and then two byte checksum followed by 0xB0 0xB3
        while True:
            if self.hunt_for_start():
                length = struct.unpack('>H', self.com.read(2))[0]
                payload = self.com.read(length)
                crc = struct.unpack('>H', self.com.read(2))[0]
                end = struct.unpack('>H',self.com.read(2))[0]
                if end == 0xB0B3:
                    if self.check_crc(payload,crc):
                        return payload