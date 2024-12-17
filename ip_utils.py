# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.

def ip_to_int(ip: str):
    octets = ip.split('.')
    return (int(octets[0]) << 24) + (int(octets[1]) << 16) + (int(octets[2]) << 8) + int(octets[3])

def int_to_ip(int_ip: str):
    return '.'.join([str((int_ip >> (i << 3)) & 0xFF) for i in range(3, -1, -1)])

def get_broadcast_address(ip: str, subnet_mask: str):
    ip_int = ip_to_int(ip)
    subnet_mask_int = ip_to_int(subnet_mask)
    broadcast_int = ip_int | (~subnet_mask_int & 0xFFFFFFFF)
    return int_to_ip(broadcast_int)

def ip_2_broadcast(ip_address: str) -> str:
    print("OLD IP", ip_address, "NEW IP",".".join(ip_address.split(".")[:-1] + ["255"]))
    return ".".join(ip_address.split(".")[:-1] + ["255"])