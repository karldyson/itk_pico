import machine
import onewire
import ds18x20
import time

class TemperatureSensor:
    _pin: int = 0
    _one_wire: onewire.OneWire
    _sensor: ds18x20.DS18X20
    _devices = []

    def __init__(self, pin: int) -> None:
        self._pin = pin
        self._one_wire = onewire.OneWire(machine.Pin(pin))  
        self._sensor = ds18x20.DS18X20(self._one_wire)
        devices = self._sensor.scan()
        self._sensor.convert_temp() # !!!! <- Double check it
        print("Found devices:", devices)
        if not devices:
            raise RuntimeError("No DS18B20 found!")

    def get_temperature(self):
        while True:
            # self._sensor.convert_temp()
            # time.sleep(1)  # Wait for the conversion to complete

            for device in self._devices:
                temp = self._sensor.read_temp(device)
                print("Temperature:", temp, "°C")
                return temp