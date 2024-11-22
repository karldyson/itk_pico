# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.

import network
import time
from .logger import Logger

class WiFi:
    _wlan = network.WLAN(network.STA_IF)
    _wlan.active(True)
    _ssid = ""
    _password = ""

    def connect(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        self._wlan.connect(ssid, password)
        seconds = 1
        while not self._wlan.isconnected():
            seconds += 1
            Logger.print(f"Connecting to Wi-Fi... {seconds}")
            time.sleep(1)
        Logger.print("Connected to Wi-Fi:", self._wlan.ifconfig())

    def try_reconnect_if_lost(self):
        if self._wlan.isconnected():
            pass
        else:
            Logger.print("WiFi connection lost. Reconnecting!")
            self._wlan.disconnect()
            self.connect(self._ssid, self._password)  

    def get_mac_address(self):
        mac_address = self._wlan.config('mac')  
        mac_address_formatted = ':'.join(f'{b:02x}' for b in mac_address)
        Logger.print("MAC Address:", mac_address_formatted)
        return mac_address_formatted
