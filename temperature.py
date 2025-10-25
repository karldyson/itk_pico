# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.
#
# Modified by Karl Dyson in October 2025

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

    # modified by Karl Dyson in October 2025
    # added a little extra debug at initialisation to include
    # the friendly name of the sensor
    def __init__(self, pin: int) -> None:
        self._pin = pin
        self._one_wire = onewire.OneWire(machine.Pin(pin))
        self._sensor = ds18x20.DS18X20(self._one_wire)
        Logger.print("Initialised on pin:", self._pin)
        Logger.print("Scanning for devices...")
        self._devices = self._sensor.scan()
        Logger.print("Found devices:", self._devices)
        for device in self._devices:
            friendly = self.friendly_name(device)
            Logger.print(f"Device: {device}; Friendly Name: {friendly}")
        if not self._devices:
            raise RuntimeError("No DS18B20 found!")
        Logger.print("Initialisation complete")

    # modified by Karl Dyson in October 2025
    # loops through all connected sensors and returns a dictionary
    # of temperatures indexed by the friendly ASCII name of the sensor
    def get_temperature(self):
        temps = {}
        for device in self._devices:
            self._sensor.convert_temp()
            time.sleep(1)
            temp = self._sensor.read_temp(device)
            device_string = self.friendly_name(device)
            Logger.print(f"Device: {device_string}; Temperature: {temp} celcius")
            temps[device_string] = temp
        return temps

    # added by Karl Dyson in October 2025
    # turns the device ID into a friendly ASCII ID
    def friendly_name(self, device):
        string = binascii.hexlify(device)
        return string.decode('ascii')

    # added by Karl Dyson in October 2025
    # returns a dictionary of friendly names
    def get_device_friendly_names(self):
        names = {}
        for device in self._devices:
            names[self.friendly_name(device)] = {}
        return names

