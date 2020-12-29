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

import logging
import os
from os import path
import socket
import sys

# Default values of configuration variables might be overriden by environment variables
defaults = {
    'dump_dir'          : '/tmp/airodumps',
    'dump_prefix'       : f'{socket.gethostname()}',
    'mac_excludes'      : [],
    'observ_interval'   : 300,
    'min_signal_level'  : -67,
    'api_url'           : 'http://sensorhub:8080/v1.0/',
    'log_level'         : logging.INFO,
    'datastream_id'     : 0 # Invalid value, shall start with 1
}

# The directory where all data gets dumped
try:
    DUMP_DIR = os.environ['DUMP_DIR']
except KeyError:
    DUMP_DIR = defaults['dump_dir']

# For distinguishing dumps by their hosts if stored together in one place (e.g. localhost)
try:
    DUMP_PREFIX = os.environ['DUMP_PREFIX']
except KeyError:
    DUMP_PREFIX = defaults['dump_prefix']

# List of MAC addresses to be ignored from collected data (empty by default)
try:
    MAC_EXCLUDES = os.environ['MAC_EXCLUDES'].split(',')
except:
    MAC_EXCLUDES = defaults['mac_excludes']

# Define time frame in seconds for observation (5 minutes by default)
try:
    OBSERV_INTERVAL = int(os.environ['OBSERV_INTERVAL'])
except:
    OBSERV_INTERVAL = defaults['observ_interval']

# Define minimal signal level to be considered near the sensor (-67 dBm by default)
try:
    MIN_SIGNAL_LEVEL = int(os.environ['MIN_SIGNAL_LEVEL'])
except:
    MIN_SIGNAL_LEVEL = defaults['min_signal_level']

# Set the URL to the OGC SensorThings API
try:
    API_URL = os.environ['API_URL']
except:
    API_URL = defaults['api_url']

# Choose the desired log levels
try:
    log_level = os.environ['LOG_LEVEL']
    if log_level.upper() == 'DEBUG':
        LOG_LEVEL = logging.DEBUG
    elif log_level.upper() == 'WARNING':
        LOG_LEVEL = logging.WARNING
    elif log_level.upper() == 'ERROR':
        LOG_LEVEL = logging.ERROR
    elif log_level.upper() == 'CRITICAL':
        LOG_LEVEL = logging.CRITICAL
    else:
        LOG_LEVEL = defaults['log_level']
except KeyError:
    LOG_LEVEL = logging.INFO

# Set the appropriate datastream ID to send observations to
try:
    DATASTREAM_ID = os.environ['DATASTREAM_ID']
except:
    DATASTREAM_ID = defaults['datastream_id']

# Configure the logging system
logging.basicConfig(
    filename=path.abspath(path.join(path.dirname(sys.argv[0]), os.pardir, 'log',
        path.splitext(path.basename(sys.argv[0]))[0] + '.log')),
    level=LOG_LEVEL,
    format="%(levelname)s:%(asctime)s:%(message)s"
)
