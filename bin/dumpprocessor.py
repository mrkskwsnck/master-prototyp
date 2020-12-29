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
import logging
import os
from os import path
import sys
from lxml import etree

def getMostRecentDumpPath():
    try:
        return [getAllDumpPaths()[-1]]
    except IndexError as e:
        logging.error("No dump files present for DUMP_PREFIX='%s'", config.DUMP_PREFIX)
        sys.exit(1)

def getAllDumpPaths():
    # Get absolute path to ALL THE dump files in netxml format created by airodump-ng
    logging.debug("Attempting to collect dump files from folder '%s'", config.DUMP_DIR)
    try:
        dump_paths = [path.abspath(path.join(config.DUMP_DIR, name)) for name in os.listdir(config.DUMP_DIR)
                    if path.isfile(path.join(config.DUMP_DIR, name))
                    # Hostname shalt be considered case-insensitive
                    and name.lower().startswith(config.DUMP_PREFIX.lower())
                    and name.endswith("netxml")]
        dump_paths.sort()
        return dump_paths
    except FileNotFoundError as e:
        logging.error("Cannot read dump directory")
        logging.error(e)
        sys.exit(1)

def getStations():
    stations = set()

    dump_paths = getMostRecentDumpPath()
    for dump_path in dump_paths:
            logging.info("Processing dump file '%s'", dump_path)

            with open(dump_path) as f:
                distinct_stations = 0
                first_station_seen = None
                last_station_seen = None

                try:
                    # Parse hard through broken XML
                    parser = etree.XMLParser(recover=True)
                    tree = etree.parse(f, parser)
                    root = tree.getroot()

                    nodes = root.findall('wireless-network/wireless-client')
                    if len(nodes) > 0:
                        for node in nodes:
                            mac_address = node.find("client-mac").text

                            # Skip the sensor's own MAC addresses
                            if mac_address in config.MAC_EXCLUDES:
                                continue

                            manufacturer = node.find("client-manuf").text
                            
                            first_time = datetime.strptime(node.get("first-time"), "%a %b %d %H:%M:%S %Y")
                            if not first_station_seen or first_station_seen > first_time:
                                first_station_seen = first_time
                            
                            last_time = datetime.strptime(node.get("last-time"), "%a %b %d %H:%M:%S %Y")
                            if not last_station_seen or last_station_seen < last_time:
                                last_station_seen = last_time

                            last_signal_level = int(node.find("snr-info/last_signal_dbm").text)    # Signal level [dBm]
                            logging.debug("Spotted: %s\t%s\t%s\t%s\t%d", mac_address, manufacturer, first_time.isoformat(), last_time.isoformat(), last_signal_level)
                            distinct_stations += 1

                            # Store sensor data for station
                            station = (mac_address, manufacturer, first_time.isoformat(), last_time.isoformat(), last_signal_level)
                            stations.add(station)

                        d = last_station_seen - first_station_seen
                        hours = d.seconds // 3600
                        minutes = (d.seconds // 60) % 60
                        seconds = d.seconds - (hours * 3600 + minutes * 60)
                        logging.info("Processed %d distinct stations during runtime of %d days, %d hours, %d minutes and %d seconds",
                            distinct_stations, d.days, hours, minutes, seconds)
                    else:
                        logging.info('No stations were spotted')
                except etree.XMLSyntaxError as e:
                    logging.debug("XML parse error: '%s'", e)
                    logging.warning("Dump file '%s' is not parsable, skipping", dump_path)

    return sorted(stations, key=lambda station: station[3])
