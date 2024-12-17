# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.

import time
from machine import Pin

# 28byj 48 Uln2003 5v Stepper Motor Uln2003 Driver
class StepperMotor:
    _pin1: Pin
    _pin2: Pin
    _pin3: Pin
    _pin4: Pin
    _pins = []
    _steps = []
    _steps_per_revolution: int

    _current_step = 0

    def __init__(self, pin1: int = 21, pin2: int = 20, pin3: int = 19, pin4: int = 18, steps_per_revolution: int = 2048) -> None:
        self._pin1 = Pin(pin1, Pin.OUT)
        self._pin2 = Pin(pin2, Pin.OUT)
        self._pin3 = Pin(pin3, Pin.OUT)
        self._pin4 = Pin(pin4, Pin.OUT)
        self._pins = [self._pin1, self._pin2, self._pin3, self._pin4]
        self._steps_per_revolution = steps_per_revolution

        self._steps = [
            [self._pin1],
            [self._pin1, self._pin2],
            [self._pin2],
            [self._pin2, self._pin3],
            [self._pin3],
            [self._pin3, self._pin4],
            [self._pin4],
            [self._pin4, self._pin1],
        ]
        self._set_pins_low()

    def _set_pins_low(self):
        """Set all pins to LOW"""
        for pin in self._pins:
            pin.low()

    def _set_pins_high(self, high_pins):
        """Set specific pins to HIGH"""
        for pin in high_pins:
            pin.high()

    def step(self, direction: int):
        high_pins = self._steps[self._current_step] 
        self._set_pins_low()                
        self._set_pins_high(high_pins)   
        self._current_step = (self._current_step + direction) % len(self._steps)

    def release(self):
        self._set_pins_low()

    def default_sleep(self):
        time.sleep(0.001)
    
    def rotate(self, direction: int = 1, fraction: float = 1):
        steps = int(self._steps_per_revolution * fraction)
        for _ in range(steps):
            self.step(direction)
            self.default_sleep()
        self.release()