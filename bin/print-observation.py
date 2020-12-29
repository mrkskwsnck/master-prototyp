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
from datetime import datetime
import dumpprocessor
from helper import in_range, within_time_frame
import logging
import os

if __name__ == '__main__':
    logging.debug("Starting up withing working directory '%s'", os.getcwd())

    all_stations = dumpprocessor.getStations()

    stations_wtf = [station for station in all_stations if within_time_frame(station, datetime.now(), config.OBSERV_INTERVAL)]
    stations_ir = [station for station in stations_wtf if in_range(station, config.MIN_SIGNAL_LEVEL)]
    evaled_stations = stations_ir

    if evaled_stations:
        for station in evaled_stations:
            print(station)
        logging.info("Spotted %d wireless clients in past %d seconds", len(evaled_stations), config.OBSERV_INTERVAL)
    else:
        logging.info('No data to print')
