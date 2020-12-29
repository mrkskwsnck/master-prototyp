#!/usr/bin/env python3

# Copyright (C) 2020  Markus Kwaśnicki
#
# This file is part of the prototype.
#
# This prototype is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This prototype is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this prototype.  If not, see <https://www.gnu.org/licenses/>.

import config
from datetime import datetime, timedelta

def within_time_frame(station, now, seconds=config.OBSERV_INTERVAL):
    d = timedelta(seconds=seconds)
    then = now - d
    last_time_seen = datetime.fromisoformat(station[3])

    if last_time_seen <= now and last_time_seen >= then:
        return True
    else:
        return False

def in_range(station, signal_level=config.MIN_SIGNAL_LEVEL):
    if station[4] not in [0, -1] and station[4] >= signal_level:
        return True
    else:
        return False
