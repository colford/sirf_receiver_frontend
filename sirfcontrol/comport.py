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
        self.startbytes = bytearray(b'\xa0\xa2')
        self.endbytes = bytearray(b'\xb0\xb3')
        self.warm_payload = bytearray(b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0C\x02')
        self.warm_message = self.startbytes + \
                                len(self.warm_payload).to_bytes(2,byteorder='big') + \
                                self.warm_payload + \
                                self.calc_crc(self.warm_payload).to_bytes(2,byteorder='big') + \
                                self.endbytes
        self.coldstart_payload = bytearray(b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0C\x84')
        self.coldstart_message = self.startbytes + \
                                   len(self.coldstart_payload).to_bytes(2,byteorder='big') + \
                                   self.coldstart_payload + \
                                   self.calc_crc(self.coldstart_payload).to_bytes(2,byteorder='big') + \
                                   self.endbytes
        self.hotstart_payload = bytearray(b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0C\x00')
        self.hotstart_message = self.startbytes + \
                                   len(self.hotstart_payload).to_bytes(2,byteorder='big') + \
                                   self.hotstart_payload + \
                                   self.calc_crc(self.hotstart_payload).to_bytes(2,byteorder='big') + \
                                   self.endbytes                                 
        self.sw_poll_payload = bytearray(b'\x84\x00')
        self.sw_poll_message = self.startbytes + \
                                   len(self.sw_poll_payload).to_bytes(2,byteorder='big') + \
                                   self.sw_poll_payload + \
                                   self.calc_crc(self.sw_poll_payload).to_bytes(2,byteorder='big') + \
                                   self.endbytes
    
    def isopen(self):
        return self.com != None
    
    def open(self):
        self.com = serial.Serial(self.port, self.baud, timeout=self.timeout)
        
    def calc_crc(self,payload):
        return ( sum(payload) & self.crc_mask )       
        
    def check_crc(self,payload,crc):
        return self.calc_crc(payload) == crc

    def hunt_for(self,value):
        valstring = self.com.read(1)
        return ( len(valstring) > 0 and ord(valstring) == value )

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
                        
    def cold_start(self):
        # Wtire the cold start message
        print(self.coldstart_message)
        print(self.com.write(self.coldstart_message))
        
    def warm_start(self):
        # Wtire the warm start message
        print(self.warm_payload)
        print(self.com.write(self.warm_payload))
        
    def hot_start(self):
        # Wtire the hot start message
        print(self.hotstart_payload)
        print(self.com.write(self.hotstart_payload))
        
    def sw_poll(self):
        # Poll for the software version
        print(self.sw_poll_message)
        print(self.com.write(self.sw_poll_message))