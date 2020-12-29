# Prototyp

Prototyp der Masterarbeit des berufsbegleitenden Masterstudiengangs Geoinformatik M.Eng. an der Hochschule Mainz

## Beschreibung

Der Prototyp basiert auf einem [Raspberry Pi (Zero W)](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) und wird mit [Kali Linux](https://www.kali.org/), als Sensor, betrieben.
Er hat zur Aufgabe, die WLAN-Umgebung (später auch Bluetooth) nach Clients abzuscannen.
Die Scanergebnisse werden im NetXML-Format ([Kismet](https://www.kismetwireless.net/)) zur weiteren Auswertung (temporär) geschrieben, um daraus die Personenanzahl (dank Smartphones u.a. Wearables) in unmittelbarer Nähe abzuschätzen.
Abschließend werden alle ermittelten Sensorwerte, mittels [OGC SensorThings API](http://docs.opengeospatial.org/is/15-078r6/15-078r6.html), an einen Zentralen Server, zwecks Historisierung sowie Visualisierung, übermittelt.

## Voraussetzungen

* Kali Linux incl. Re4son Kernel
* Python 3.7

### Entwicklungsumgebung

* [pyenv](https://github.com/pyenv/pyenv)

```bash
apt-get install -y build-essential curl git libbz2-dev libffi-dev liblzma-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libssl-dev llvm python3-lxml python3-openssl tk-dev wget xz-utils zlib1g-dev
```

## Ersteinrichtung

**Projekt klonen**

```bash
git clone https://github.com/mrkskwsnck/master-prototyp.git /opt/prototyp
```

**Dienste installieren**

…damit diese nach jedem Systemneustart auomatisch gestartet werden.

```bash
cd /opt/prototyp
for S in systemd/*.{service,timer}; do ln -sf "$PWD/$S" /etc/systemd/system; done
systemctl daemon-reload
systemctl enable monitor-mode.service wifi-observation.service
```

**Dienste konfigurieren (optional)**

Ggf. Umgebungsvariablen innerhalb der Service-Unit-Datei überschreiben, um diese an die eigene Umgebung anzupassen.

```bash
systemctl edit monitor-mode.service
systemctl edit wifi-observation.service
```

**HINWEIS:** Die überschriebenen Zeilen werden im Drop-In-Verzeichnis der jeweiligen Service-Unit-Datei geschrieben! Etwa `/etc/systemd/system/monitor-mode.service.d/override.conf` für `/etc/systemd/system/monitor-mode.service` usw.

**Dienste (manuell) starten**

```bash
systemctl start monitor-mode.service wifi-observation.service
```

**Dienste (manuell) stoppen**

```bash
systemctl stop monitor-mode.service wifi-observation.service
```

## Umgebungsvariablen

Die bereitgestellten Programme bzw. Skripten können mittels Umgebungsvariablen konfiguriert werden, indem die Säumniswerte (vor Programmausführung) zu überschreiben sind.

**DUMP_DIR=** Das Verzeichnis, indem die flüchtigen (keine Persistenz) Daten geschrieben werden.

```bash
DUMP_DIR='/tmp/airodumps'
```
**DUMP_PREFIX=** Zur Unterscheidung gesammelter Daten verschiedener Hosts, falls diese gemeinsam an einem Ort gespeichert sind (z.B. `localhost`).

```bash
DUMP_PREFIX='<LOCAL_HOSTNAME>'
```

**WRITE_INTERVAL=** Legt das Schreibinterval der Sensordaten, in Sekunden, fest.
Betrifft das Programm `airodump-ng`, welches die Sensordaten des Prototyps erhebt.
Dieser Wert sollte nicht zu niedrig gesetzt werden, da sonst der Sensor möglicherweise nicht mit dem Schreiben neuer Daten nachkommt!
Hinsweis: Das Interval zur Auswertung der Sensordaten (siehe `OBSERV_INTERVAL`) sollte auf das Schreibinterval abgestimmt sein.

```bash
WRITE_INTERVAL=30
```

**MAC_EXCLUDES=** Liste der MAC-Adressen, die aus den gesammelten Daten zu ignorieren bzw. herauszufiltern sind (säumnismäßig leer).

```bash
MAC_EXCLUDES='0A:1B:2C:3D:4E:5F,01:23:45:AB:CD:EF,...'
```

**OBSERV_INTERVAL=** Definiert das Zeitfenster in Sekunden für die Beobachtung (säumnismäßig 5 Minuten).

```bash
OBSERV_INTERVAL=300
```

**MIN_SIGNAL_LEVEL=** Definiert den minimalen Signalpegel, für den ein Draht-loser Client, als in unmittelbarer Nähe zum Sensor angenommen wird (säumnismäßig -67 dBm).

```bash
MIN_SIGNAL_LEVEL=-67
```

**API_URL=** Setzt die Adresse (URI) zur OGC SensorThings API (z.B. ['http://sensorhub:8080/v1.0/']('http://sensorhub:8080/v1.0/')).

```bash
API_URL='http://sensorhub:8080/v1.0/'
```

**LOG_LEVEL=** Die gewünschte Protokollebene für Debugging-Zwecke (säumnismäßig `INFO`).

```bash
LOG_LEVEL='<DEBUG|INFO|WARNING|ERROR|CRITICAL>'
```

**DATASTREAM_ID** Setzt die entsprechende Datenstrom-ID der OGC SensorThings API zum Übermitteln von Beobachtungen.

```
DATASTREAM_ID=1
```

### Datenerfassung

Das für den WLAN-Sensor zugrunde liegende Programm `airodump-ng` schreibt dessen akkumulierte Daten ausschließlich in Intervallen.
Zwar kann das Intervall Sekunden-genau konfiguriert werden, jedoch erschwert dieser Umstand die Implementierung eines kontinuierlichen Datenstroms.

## Visualisierung

Die Visualisierung auf einer zweidimensionalen Karte des OpenStreetMap-Dienstes ist als Einzelseiten-Webanwendung implementiert und muss von einem Web-Server ausgeliefert werden.

```bash
user@localhost:~$ cd /opt/master-prototyp/web
user@localhost:/opt/master-prototyp/web$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Lokal zu erreichen unter: http://localhost:8000/map.html

## Lizensierung

> Prototype to sense nearby people approximately using wireless technology  
> Copyright (C) 2020  Markus Kwaśnicki
>
> This prototype is free software: you can redistribute it and/or modify  
> it under the terms of the GNU General Public License as published by  
> the Free Software Foundation, either version 3 of the License, or  
> (at your option) any later version.
>
> This prototype is distributed in the hope that it will be useful,  
> but WITHOUT ANY WARRANTY; without even the implied warranty of  
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License  
> along with this prototype.  If not, see <https://www.gnu.org/licenses/>.
