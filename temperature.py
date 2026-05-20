# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.
#

import machine
import onewire
import ds18x20
import time
from .logger import Logger
import binascii

class TemperatureSensor:
    _pin: int = 0
    _one_wire: onewire.OneWire
    _sensor: ds18x20.DS18X20
    _devices = []

    def __init__(self, pin: int) -> None:
        self._pin = pin
        self._one_wire = onewire.OneWire(machine.Pin(pin))
        self._sensor = ds18x20.DS18X20(self._one_wire)
        Logger.print(f"Scanning for devices on pin {pin}...")
        self._devices = self._sensor.scan()
        Logger.print("Found devices:", self._devices)
        if not self._devices:
            raise RuntimeError("No DS18B20 found!")
        else:
            for device in self._devices:
                friendly = self.friendly_name(device)
                Logger.print(f"Device: {device}; Friendly: {friendly}")
        Logger.print("Initialisation complete")

    def get_temperature(self):
        for device in self._devices:
            self._sensor.convert_temp()
            time.sleep(1)
            temp = self._sensor.read_temp(device)
            Logger.print("Temperature:", temp)
            return temp

    # returns a dictionary of sensor temperatures indexed by the
    # ascii friendly name. copes with multiple sensors on the same
    # GPIO pin
    def get_temperatures(self):
        temps = {}
        for device in self._devices:
            self._sensor.convert_temp()
            time.sleep(1)
            temp = self._sensor.read_temp(device)
            friendly_name = self.friendly_name(device)
            Logger.print(f"Device: {friendly_name}; Temperature: {temp}")
            temps[friendly_name] = temp
        return temps

    # returns a friendier ascii device name
    def friendly_name(self, device):
        string = binascii.hexlify(device)
        return string.decode('ascii')

    # returns a dictionary of sensor friendly names
    def get_device_friendly_names(self):
        names = {}
        for device in self._devices:
            names[self.friendly_name(device)] = {}
        return names
