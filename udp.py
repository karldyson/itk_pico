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

    def start_listening(self, is_blocking: bool = False):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Logger.print(f"Listening to a", self._socket, self._port)
        self._socket.bind(('0.0.0.0', self._port))
        self._socket.setblocking(is_blocking)

    def stop_listening(self):
        self._socket.close()

    def read(self): # -> tuple[str?, str, int?]
        try:
            message, address_pair = self._socket.recvfrom(1024)
            addr, port = address_pair
            Logger.print(f"Received message: {message} from {addr}:{port}")
            return message, addr, port
        except Exception as e:
            return None, None, None
    
    def send(self, message: str, ip_address: str, port: int):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(message, (ip_address, port))
        Logger.print(f"UDP message: {message} is sent")
        udp_socket.close()
