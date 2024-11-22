# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.

import urequests
from .logger import Logger

class Http:

    def get(self, url: str):
        response = urequests.get(url)
        text = response.text
        response.close()
        Logger.print(f"Received: {text}")
        return text

    def post(self, url: str, data):
        response = urequests.post(url, json=data)
        text = response.text
        Logger.print(f" Received: {text}")
        response.close()
        return text