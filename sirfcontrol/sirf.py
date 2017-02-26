# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:34:10 2017

@author: CFord
"""

from sirfcontrol.comport import Comport
from sirfcontrol.message import Message

class SirfMessageReader(object):
    def __init__(self,port,baud):
        self.com = Comport(port,baud)
        self.connect()
    
    def connect(self):
        self.com.open()
    
    def read_message(self):
        return Message(self.com.read_message())
            
        
