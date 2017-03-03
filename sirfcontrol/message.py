# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:51:20 2017

@author: CFord
"""

import struct

# How to decode the payload from the SiRF binary message
# ID, Description, Class-Handler
message_decoder = {
    0x01 : ["Reference Navigation Data",""],
    0x02 : ["Measured Navigation Data","Message_02"],
    0x03 : ["True Tracker Data",""],
    0x04 : ["Measured Tracking Data","Message_04"],
    0x05 : ["Raw Track Data",""],
    0x06 : ["SW Version","Message_06"],
    0x07 : ["Clock Status","Message_07"],
    0x08 : ["50 BPS Subframe Data",""],
    0x09 : ["CPU Throughput","Message_09"],
    0x0A : ["Error ID",""],
    0x0B : ["Command Acknowledgment",""],
    0x0C : ["Command NAcknowledgment",""],
    0x0D : ["Visible List",""],
    0x0E : ["Almanac Data",""],
    0x0F : ["Ephemeris Data",""],
    0x10 : ["Test Mode 1",""],
    0x11 : ["Differential Corrections",""],
    0x12 : ["OkToSend", ""],
    0x13 : ["Navigation Parameters",""],
    0x14 : ["Test Mode 2/3/4",""],
    0x1B : ["DGPS Status",""],
    0x1C : ["Nav. Lib. Measurement Data",""],
    0x1D : ["Nav. Lib. DGPS Data",""],
    0x1E : ["Nav. Lib. SV State Data",""],
    0x1F : ["Nav. Lib. Initialization Data",""],
    0x29 : ["Geodetic Navigation Data",""],
    0x2B : ["Queue Command Parameters",""],
    0x2D : ["Raw DR Data",""],
    0x2E : ["Test Mode 3/4/5/6 (GSW3 & SLC3)",""],
    0x30 : ["SiRF Dead Reckoning Class of Output Messages",""],
    0x31 : ["Test Mode 4 for SiRFLoc v2.x only",""],
    0x32 : ["SBAS Parameters",""],
    0x34 : ["1 PPS Time Message",""],
    0x37 : ["Test Mode 4",""],
    0x38 : ["Extended Ephemeris Data",""],
    0x3F : ["Test Mode Output",""],
    0x40 : ["Auxilary Time Management",""],
    0x4B : ["Ack/Nack/Error Notification", "Message_4B"],
    0x5D : ["TCX0 Learning output response", "Message_5D"],
    0xE1 : ["SiRF internal message",""],
    0xFF : ["Development Data",""]
}

class Message_02(object):
    def __init__(self, mid, description, message):
        self.id = mid
        self.message = message
        self.fixed = ">BiiihhhBBBHIBBBBBBBBBBBBB"
        self.data = None
        self.decode()
        
    def decode(self):
        # Read the fixed part of the message
        self.data = struct.unpack_from(self.fixed, self.message, 0)

class Message_04(object):
    def __init__(self, mid, description, message):
        self.id = mid
        self.message = message
        self.fixed = ">BhIB"
        self.repeated = "BBBHBBBBBBBBB"
        self.repeated_size = struct.calcsize(self.repeated)
        self.data = None
        self.decode()
        
    def decode(self):
        # Read the fixed part
        offset = 0
        read = struct.calcsize(self.fixed)
        self.data = struct.unpack_from(self.fixed, self.message, offset)
        offset += read
        
        while ( read + offset ) < len(self.message):
            # Read as repeated
            self.data += struct.unpack_from(self.repeated, self.message, offset)
            offset += self.repeated_size

class Message_06(object):
    def __init__(self, mid, description, message):
        self.id = mid
        self.message = message
        self.fixed = ">BBB"
        self.data = None
        self.decode()
        
    def decode(self):
        # Read the fixed part of the message
        self.data = struct.unpack_from(self.fixed, self.message, 0)
        ver_length = self.data[1]
        self.sirf_version = self.message[3:ver_length+3-1]
        self.customer_version = self.message[3+ver_length:-1]
        print(self.sirf_version,self.customer_version)
        
class Message_07(object):
    def __init__(self, mid, description, message):
        self.id = mid
        self.message = message
        self.fixed = ">BHIBIII"
        self.data = None
        self.decode()
        
    def decode(self):
        # Read the fixed part of the message
        self.data = struct.unpack_from(self.fixed, self.message, 0)
        
class Message_09(object):
    def __init__(self, mid, description, message):
        self.id = mid
        self.message = message
        self.fixed = ">BHHHH"
        self.data = None
        self.decode()
        
    def decode(self):
        # Read the fixed part of the message
        self.data = struct.unpack_from(self.fixed, self.message, 0)

class Message_4B(object):
    def __init__(self, mid, description, message):
        self.id = mid
        self.message = message
        self.fixed = ">BB"
        self.sub1 = "BBBBB"
        self.sub2 = "BBB"
        self.data = None
        self.decode()
        
    def decode(self):
        # Keep track of where we are in the message
        offset = 0
        
        # Read the fixed part of the message
        read = struct.calcsize(self.fixed)
        self.data = struct.unpack_from(self.fixed, self.message, offset)
        self.subid = self.data[1]
        offset += read
        
        # Consume the repeating variable part
        if self.subid == 1:
            self.data += struct.unpack_from(self.sub1, self.message, offset)
        elif self.subid == 2:
            self.data += struct.unpack_from(self.sub2, self.message, offset)
        else:
            print("Message 0x4B error unknown subid:", self.subid)

class Message_5D(object):
    def __init__(self, mid, description, message):
        self.id = mid
        self.message = message
        self.fixed = ">BB"
        self.submap = {
            0x01: "BBBBiHHBBBB",
            0x02: "IhhhHHHBbBB",
            0x04: "IHBBBBB",
            0x05: "IIIHHHH",
            0x06: "IIIHH",
            0x07: "IIIIIHHIIIiIHH",
            0x09: "BBBII",
            0x0A: "BBBII",
            0x0B: "BBIIiIHH",
            0x0C: "IIIHHHHHHHHBBI",
            0x0D: "IIIIIIHiiH"
        }
        self.data = None
        self.decode()
        
    def decode(self):
        # Keep track of where we are in the message
        offset = 0
        
        # Read the fixed part of the message
        read = struct.calcsize(self.fixed)
        self.data = struct.unpack_from(self.fixed, self.message, offset)
        self.subid = self.data[1]
        print(self.subid)
        print(self.message)
        offset += read
        
        # Consume the subtype part
        if self.subid in self.submap:
            self.data += struct.unpack_from(self.submap[self.subid], self.message, offset)
        else:
            print("Message 0x4B error unknown subid:", self.subid)


class Message(object):
    def __init__(self, message):
        self.id = message[0]
        if self.id in message_decoder:
            if len(message_decoder[self.id][1]) > 0:
                eval_string = '%s( %d, "%s", %s)' % (message_decoder[self.id][1],self.id,message_decoder[self.id][0],message)
                self.decoded = eval(eval_string)
        else:
            print("Unknown message: %d" % self.id )
    
    def description(self):
        if self.id in message_decoder:
            return message_decoder[self.id][0]
     