# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:51:20 2017

@author: CFord
"""

import struct

# How to decode the payload from the SiRF binary message
# ID, decription, fixed length part, number_of_subids, [repetion|subid], subid1, subid2...]
message_decoder = {
    0x01 : ["Reference Navigation Data","", 0, ""],
    0x02 : ["Measured Navigation Data",">BiiihhhBBBHIBBBBBBBBBBBBB", 0, ""],
    0x03 : ["True Tracker Data","", ""],
    0x04 : ["Measured Tracking Data",">BhIB", 0, "BBBHBBBBBBBBB"],
    0x05 : ["Raw Track Data","", 0, ""],
    0x06 : ["SW Version",">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB", 0, ""],
    0x07 : ["Clock Status",">BHIBIII", 0, ""],
    0x08 : ["50 BPS Subframe Data","", 0, ""],
    0x09 : ["CPU Throughput",">BHHHH", 0, ""],
    0x0A : ["Error ID","", 0, ""],
    0x0B : ["Command Acknowledgment","", 0, ""],
    0x0C : ["Command NAcknowledgment","", 0, ""],
    0x0D : ["Visible List","", 0, ""],
    0x0E : ["Almanac Data","", 0, ""],
    0x0F : ["Ephemeris Data","", 0, ""],
    0x10 : ["Test Mode 1","", 0, ""],
    0x11 : ["Differential Corrections","", 0, ""],
    0x12 : ["OkToSend", "", 0, ""],
    0x13 : ["Navigation Parameters","", 0, ""],
    0x14 : ["Test Mode 2/3/4","", 0, ""],
    0x1B : ["DGPS Status","", 0, ""],
    0x1C : ["Nav. Lib. Measurement Data","", 0, ""],
    0x1D : ["Nav. Lib. DGPS Data","", 0, ""],
    0x1E : ["Nav. Lib. SV State Data","", 0, ""],
    0x1F : ["Nav. Lib. Initialization Data","", 0, ""],
    0x29 : ["Geodetic Navigation Data","", 0, ""],
    0x2B : ["Queue Command Parameters","", 0, ""],
    0x2D : ["Raw DR Data","", 0, ""],
    0x2E : ["Test Mode 3/4/5/6 (GSW3 & SLC3)","", 0, ""],
    0x30 : ["SiRF Dead Reckoning Class of Output Messages","", 0, ""],
    0x31 : ["Test Mode 4 for SiRFLoc v2.x only","", 0, ""],
    0x32 : ["SBAS Parameters","", 0, ""],
    0x34 : ["1 PPS Time Message","", 0, ""],
    0x37 : ["Test Mode 4","", 0, ""],
    0x38 : ["Extended Ephemeris Data","", 0, ""],
    0x3F : ["Test Mode Output","", 0, ""],
    0x40 : ["Auxilary Time Management","", 0, ""],
    0x4B : ["Ack/Nack/Error Notification", ">B", 2, "B", "BBBBB", "BBB"],
    0xE1 : ["SiRF internal message","", 0, ""],
    0xFF : ["Development Data","", 0, ""]
}

class Message(object):
    def __init__(self, message):
        self.id = message[0]
        if self.id == 6:
            print(message)
        self.data = None
        self.repeated = None
        if self.id in message_decoder:
            if len(message_decoder[self.id][1]) > 0:
                offset = 0
                read = struct.calcsize(message_decoder[self.id][1])
                self.data = struct.unpack_from(message_decoder[self.id][1], message, offset)
                offset += read
                while ( read + offset ) < len(message):
                    if message_decoder[self.id][2] > 0:
                        # Read as sub ids
                        print(message)
                        subid = struct.unpack_from(message_decoder[self.id][3], message, offset)[0]
                        data = struct.unpack_from(message_decoder[self.id][3+subid], message, offset)
                        print(subid,data)
                        offset += 1 + struct.calcsize(message_decoder[self.id][3+subid])
                    else:
                        # Read as repeated
                        self.data += struct.unpack_from(message_decoder[self.id][3], message, offset)
                        offset += struct.calcsize(message_decoder[self.id][3])
        else:
            print("Unknown message: %d" % self.id )
            
    def description(self):
        if self.id in message_decoder:
            return message_decoder[self.id][0]
            