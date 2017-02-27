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
        self.coldstartpayload = bytearray(b'\x80\xFF\xD7\x00\xF9\xFF\xBE\x52\x66\x00\x3A\xC5\x7A\x00\x01\x24\xF8\x00\x83\xD6\x00\x03\x9C\x0C\x0e')
        self.coldstartmessage = self.startbytes + \
                                    len(self.coldstartpayload).to_bytes(2,byteorder='big') + \
                                    self.coldstartpayload + \
                                    self.calc_crc(self.coldstartpayload).to_bytes(2,byteorder='big') + \
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
                        
    def cold_start(self):
        # Wtire the cold start message
        print(self.coldstartmessage)
        print(self.com.write(self.coldstartmessage))