import math
import time
from machine import ADCBlock, ADC

class MQ135(object):
    # The load resistance on the board
    RLOAD = 3.0
    # Calibration resistance at atmospheric CO2 level
    RZERO = 76.63
    # Parameters for calculating ppm of CO2 from sensor resistance
    PARA = 116.6020682
    PARB = 2.769034857
    # Parameters to model temperature and humidity dependence
    CORA = 0.00035
    CORB = 0.02718
    CORC = 1.39538
    CORD = 0.0018
    CORE = -0.003333333
    CORF = -0.001923077
    CORG = 1.130128205
    # Atmospheric CO2 level for calibration purposes
    ATMOCO2 = 415.58
    
    def __init__(self, pin):
        self.pin = pin
        self.adc_block = ADCBlock(1, bits=10)
        self.adc = self.adc_block.connect(self.pin)
        self.value = 1

    def get_correction_factor(self, temperature, humidity):
        return self.CORE * temperature + self.CORF * humidity + self.CORG

    def get_resistance(self):
        value = ADC(self.pin).read()
        if not value:
            value = self.value
        self.value = value
        return ((1023./value) - 1.) * self.RLOAD

    def get_corrected_resistance(self, temperature, humidity):
        return self.get_resistance()/ self.get_correction_factor(temperature, humidity)

    def get_ppm(self):
        return self.PARA * (self.get_resistance()/ self.RZERO)**-self.PARB

    def get_corrected_ppm(self, temperature, humidity):
        return self.PARA * (self.get_corrected_resistance(temperature, humidity)/ self.RZERO)**-self.PARB

    def get_rzero(self):
        return self.get_resistance() * math.pow((self.ATMOCO2/self.PARA), (1./self.PARB))

    def get_corrected_rzero(self, temperature, humidity):
        return self.get_corrected_resistance(temperature, humidity) * math.pow((self.ATMOCO2/self.PARA), (1./self.PARB))
