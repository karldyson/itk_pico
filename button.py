from machine import Pin
import time

class Button:

    _button_pin: Pin

    def __init__(self, pin: int) -> None:
        self._button_pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)  

    def is_pressed(self) -> bool: 
        button_state = self._button_pin.value()  # Read the button state (0 or 1)
        if button_state:
            time.sleep(0.1)  # Small delay to avoid bouncing issues
            return True
        else:
            return False
        