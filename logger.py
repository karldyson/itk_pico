# Author: Eugene Tkachenko https://www.youtube.com/@itkacher
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# See the LICENSE file for the full text of the license.

class Logger:
    _is_enabled: bool = False

    @staticmethod
    def set_enabled(is_enabled: bool):
        Logger._is_enabled = is_enabled

    @staticmethod
    def print(*args, **kwargs):
        if (Logger._is_enabled):
            print(*args, **kwargs)
