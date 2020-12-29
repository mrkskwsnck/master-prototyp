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
from datetime import datetime, timezone
import json
import logging
from urllib import request, error
from urllib.parse import urljoin

def sendRequest(uri, method, data):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        json_str = json.dumps(data)
        logging.debug("Request: %s", uri)
        logging.debug("Method: %s", method)
        logging.debug("Data: %s", json_str)
        req = request.Request(uri, json_str.encode(), headers=headers, method=method)

        resp = request.urlopen(req)
        logging.debug("Response: %s", json.loads(resp.read()))
    except error.HTTPError as e:
        logging.critical("HTTP response code: %d", e.code)
        logging.critical("HTTP response reason: %s", e.reason)
        logging.debug("Response: %s", json.loads(e.read()))
        raise e

def sendStationCount(result, resultTime):
    logging.info("Attempting to send observation of %d spotted wireless stations", result)

    pt = datetime.now().astimezone().isoformat(timespec='milliseconds')
    rt = resultTime.astimezone().isoformat(timespec='milliseconds')
    iot_id = config.DATASTREAM_ID

    data = {
        "phenomenonTime": pt,
        "resultTime": rt,
        "result": result,
        "Datastream": {'@iot.id': config.DATASTREAM_ID}
    }

    uri = urljoin(config.API_URL, f"Observations")
    method = 'POST'
    sendRequest(uri, method, data)
    logging.info("Sent observation of %d spotted wireless stations", result)
