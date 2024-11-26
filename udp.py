# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.

import socket
import time
from .logger import Logger

class Udp:
    _socket: socket
    _port: int

    def __init__(self, port: int):
        self._port = port

    def start_listening(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(('0.0.0.0', self._port))

    def stop_listening(self):
        self._socket.close()

    def read(self):
        message, addr = self._socket.recvfrom(1024)  # Buffer size of 1024 bytes
        Logger.print(f"Received message: {message} from {addr}")
        return message, addr
    
    def send(self, message: str, ip_address: str, port: int):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(message, (ip_address, port))
        udp_socket.close()
