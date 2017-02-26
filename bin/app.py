# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:14:48 2017

@author: CFord
"""

import sys
import os.path

# Add our paths in so they can be found.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Below is the SiRF control application
from sirfcontrol.sirfui import Sirf

if __name__ == "__main__":
    Sirf()
    
