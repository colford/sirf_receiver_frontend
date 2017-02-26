# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 16:14:10 2017

@author: CFord
"""

from nose.tools import *
from sirfcontrol.comport import Comport

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

def test_comport():
    comport = Comport("COM7", 38400)
    assert_equal("COM7",comport.port)
    assert_equal(38400,comport.baud)
    assert_equal(1,comport.timeout)
    assert_equal(comport.isopen(),False)