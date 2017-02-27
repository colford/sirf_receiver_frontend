# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:59:29 2017

@author: CFord
"""

import sys, math, signal
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from collections import deque
from sirfcontrol.sirf import SirfMessageReader

# Globals to begin with
port = "COM7"
baud = 38400

class SirfMeasuredTracker(QtGui.QWidget):
    def __init__(self):
        super(SirfMeasuredTracker, self).__init__()
        self.width = 450
        self.height = 350
        self.message = None
        self.cno = []
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, self.width, self.height)
        self.setWindowTitle('SiRF Measurment Tracker')        
        self.show()
        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawTracker(qp)
        qp.end()
        
    def drawHeaders(self,qp):
        font_metrics = QWidget.fontMetrics(self)
        font_height = font_metrics.height()
        qp.rotate(-90)
        x = -130
        y = 15
        qp.drawText( x, y, "SVID" )
        y += font_height + 15
        qp.drawText( x, y, "Azimuth" )
        y += font_height + 15       
        qp.drawText( x, y, "Elevation" )
        y += font_height + 15
        qp.drawText( x, y, "(Re)Acquistion success" )
        y += font_height + 4
        qp.drawText( x, y, "Carrier phase vaild" )
        y += font_height + 4
        qp.drawText( x, y, "Bit sync complete" )
        y += font_height + 4        
        qp.drawText( x, y, "Subframe sync complete" )
        y += font_height + 4        
        qp.drawText( x, y, "Carrier pullin complete" )
        max_width = font_metrics.width("Carrier pullin complete")
        y += font_height + 4        
        qp.drawText( x, y, "Code locked" )        
        y += font_height + 4        
        qp.drawText( x, y, "Acquistion failed" )        
        y += font_height + 4        
        qp.drawText( x, y, "Ephemeris data avail" )        
        qp.rotate(90)
        x -= 110
        y = max_width + 24
        qp.drawText( -x, y, "Carrier to Noise (dB-Hz)" )
    
    def drawLED(self,qp,x,y,height,on):
        if on:
            qp.fillRect( x, y-height, 5, height, QColor("green" ))
        else:
            qp.drawRect( x, y-height, 5, height ) 
    
    def drawData(self,qp):
        if self.message == None:
            return
        font_metrics = QWidget.fontMetrics(self)
        font_height = font_metrics.height()
        box_height = font_height/2+1
        startx = 5
        y = 150

        # Assume channel number fixed
        if len(self.cno) == 0:
            for i in range(0,self.message[3]):
                self.cno.append(deque(10*[0]*10,10*10))

        # Add in the new C/No data
        for i in range(0,self.message[3]):
            self.cno[i].append(self.message[(i+8)+(12*i)])
        
        for channels in range(0,self.message[3]):
            qp.setPen(QColor("black"))
            x = startx
            index = (channels+4)+(12*channels)
            qp.drawText( x, y, str(self.message[index]))
            x += 29
            qp.drawText( x, y, str(self.message[index+1]))
            x += 29
            qp.drawText( x, y, str(self.message[index+2]))
            x += 29
            self.drawLED(qp,x,y,box_height,self.message[index+3] & 0x01)
            x += font_height + 4
            self.drawLED(qp,x,y,box_height,self.message[index+3] & 0x02)
            x += font_height + 4
            self.drawLED(qp,x,y,box_height,self.message[index+3] & 0x04)
            x += font_height + 4
            self.drawLED(qp,x,y,box_height,self.message[index+3] & 0x08)
            x += font_height + 4
            self.drawLED(qp,x,y,box_height,self.message[index+3] & 0x10)
            x += font_height + 4
            self.drawLED(qp,x,y,box_height,self.message[index+3] & 0x20)
            x += font_height + 4
            self.drawLED(qp,x,y,box_height,self.message[index+3] & 0x40)
            x += font_height + 4
            self.drawLED(qp,x,y,box_height,self.message[index+3] & 0x80)
            x += font_height + 16
            scale = max(self.cno[channels])
            for i in range(0,len(self.cno[channels])):
                if self.cno[channels][i] == 0:
                    qp.setPen(QColor("red"))
                    qp.drawLine(x, y, x, y-1)
                else:
                    qp.setPen(QColor("green"))
                    qp.drawLine(x, y, x, y-int(box_height/scale*self.cno[channels][i]))
                x += 2
            y += font_height + 2
    
    def drawTracker(self,qp):
        self.drawHeaders(qp)
        self.drawData(qp)
        
    def newMessage(self,data):
        self.message = data.data
        self.repaint()

class SirfMessageProcessor(QThread):
    def __init__(self,parent = None):
        super(SirfMessageProcessor, self).__init__()
        self.reader = SirfMessageReader(port,baud)
        self.exiting = False
        self.start()
    
    def __del__(self):    
        self.exiting = True
        self.wait()    
    
    def run(self):
        while not self.exiting:
            self.message = self.reader.read_message()
            if self.message.id == 4:
                self.emit(SIGNAL("messageID4"), self.message)

class Sirf(object):
    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QtGui.QApplication(sys.argv)
        sirf_ui = SirfMeasuredTracker()
        sirf_processor = SirfMessageProcessor()
        QtCore.QObject.connect(sirf_processor, SIGNAL("messageID4"), sirf_ui.newMessage)
        sirf_ui.show()
        app.exec_()