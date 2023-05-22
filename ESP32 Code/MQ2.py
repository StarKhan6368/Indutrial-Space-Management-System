from machine import ADC
from micropython import const
from utime import sleep_ms
from math import exp, log

class MQ2(object):
    
    MQ2_RO_BASE = float(9.83)
    MQ_SAMPLE_TIMES = const(5)
    MQ_SAMPLE_INTERVAL = const(5000)

    def __init__(self, pinData, boardResistance = 10.0, baseVoltage = 3.3):      
        self._ro = -1       
        self._baseVoltage = baseVoltage
        self.pinData = ADC(pinData)
        self._boardResistance = boardResistance
        self.last_vrl = 1
        
    def calibrate(self, ro=-1):
        if ro == -1:
            ro = 0
            for i in range(0,MQ2.MQ_SAMPLE_TIMES + 1):        
                print("Step {0}".format(i))
                ro += self.__calculateResistance__(self.pinData.read())
                sleep_ms(self.MQ_SAMPLE_INTERVAL)        
            ro = ro/(self.MQ2_RO_BASE * self.MQ_SAMPLE_TIMES )
        self._ro = ro
        
    def __calculateResistance__(self, rawAdc):
        vrl = rawAdc*(self._baseVoltage / 4095)
        if vrl == 0:
            vrl = self.last_vrl
        self.last_vrl = vrl
        return (self._baseVoltage - vrl)/vrl*self._boardResistance
    
    def readRatio(self):
        return self.__calculateResistance__(self.pinData.read())/self._ro
    
    def readLPG(self):
        return exp((log(self.readRatio())-2.95)/-0.45)
    
    def readMethane(self):
        return exp((log(self.readRatio())-3.21)/-0.38)
    
    def readSmoke(self):
        return exp((log(self.readRatio())-3.54)/-0.42)       
     
    def readHydrogen(self):
        return exp((log(self.readRatio())-3.32)/-0.48)
