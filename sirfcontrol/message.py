# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:51:20 2017

@author: CFord
"""

import struct

# How to decode the payload from the SiRF binary message
# ID, decription, fixed length part, repetion
message_decoder = {
    0x01 : ["Reference Navigation Data","", ""],
    0x02 : ["Measured Navigation Data",">BiiihhhBBBHIBBBBBBBBBBBBB", ""],
    0x03 : ["True Tracker Data","", ""],
    0x04 : ["Measured Tracking Data",">BhIB", "BBBHBBBBBBBBB"],
    0x05 : ["Raw Track Data","", ""],
    0x06 : ["SW Version","", ""],
    0x07 : ["Clock Status",">BHIBIII", ""],
    0x08 : ["50 BPS Subframe Data","", ""],
    0x09 : ["CPU Throughput",">BHHHH", ""],
    0x0A : ["Error ID","", ""],
    0x0B : ["Command Acknowledgment","", ""],
    0x0C : ["Command NAcknowledgment","", ""],
    0x0D : ["Visible List","", ""],
    0x0E : ["Almanac Data","", ""],
    0x0F : ["Ephemeris Data","", ""],
    0x10 : ["Test Mode 1","", ""],
    0x11 : ["Differential Corrections","", ""],
    0x12 : ["OkToSend",""],
    0x13 : ["Navigation Parameters","", ""],
    0x14 : ["Test Mode 2/3/4","", ""],
    0x1B : ["DGPS Status","", ""],
    0x1C : ["Nav. Lib. Measurement Data","", ""],
    0x1D : ["Nav. Lib. DGPS Data","", ""],
    0x1E : ["Nav. Lib. SV State Data","", ""],
    0x1F : ["Nav. Lib. Initialization Data","", ""],
    0x29 : ["Geodetic Navigation Data","", ""],
    0x2B : ["Queue Command Parameters","", ""],
    0x2D : ["Raw DR Data","", ""],
    0x2E : ["Test Mode 3/4/5/6 (GSW3 & SLC3)","", ""],
    0x30 : ["SiRF Dead Reckoning Class of Output Messages","", ""],
    0x31 : ["Test Mode 4 for SiRFLoc v2.x only","", ""],
    0x32 : ["SBAS Parameters","", ""],
    0x34 : ["1 PPS Time Message","", ""],
    0x37 : ["Test Mode 4","", ""],
    0x38 : ["Extended Ephemeris Data","", ""],
    0x3F : ["Test Mode Output","", ""],
    0x40 : ["Auxilary Time Management","", ""],
    0xE1 : ["SiRF internal message","", ""],
    0xFF : ["Development Data","", ""]
}

class Message(object):
    def __init__(self, message):
        self.id = message[0]
        self.data = None
        self.repeated = None
        if self.id in message_decoder:
            if len(message_decoder[self.id][1]) > 0:
                offset = 0
                read = struct.calcsize(message_decoder[self.id][1])
                self.data = struct.unpack_from(message_decoder[self.id][1], message, offset)
                offset += read
                while ( read + offset ) < len(message):
                    self.data += struct.unpack_from(message_decoder[self.id][2], message, offset)
                    offset += struct.calcsize(message_decoder[self.id][2])
        else:
            print("Unknown message: %d" % self.id )
            
    def description(self):
        if self.id in message_decoder:
            return message_decoder[self.id][0]
            