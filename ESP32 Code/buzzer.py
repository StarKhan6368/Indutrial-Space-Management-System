import time
from rtttl import RTTTL
from machine import PWM, Pin

class BuzzerPlayer():

    def __init__(self, pin):
        self.buzzer_pin = PWM(Pin(pin, Pin.OUT), freq=1047, duty=0)

    def tone(self, freq, duration=0, duty=30):
        if freq != 0:
            self.buzzer_pin.freq(int(freq))
            self.buzzer_pin.duty(duty)
        else:
            self.buzzer_pin.duty(0)
        time.sleep_us(int(duration * 0.9 * 1000))
        self.buzzer_pin.duty(0)
        time.sleep_us(int(duration * 0.1 * 1000))        

    def play_rtttl(self, input, duty=30):
        tune = RTTTL(input)    
        for freq, msec in tune.notes():
            self.tone(freq, msec, duty)
