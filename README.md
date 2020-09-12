# influx-cleaner
A command line tool to remove invalid data from InfluxDB.

I am using some Openhab2 bindings that from time to time produce invalid data. This invalid data gets into InfluxDB. It is complicated to clean it.

Tool is not meant to delete a large amount of data. No deletion performance optimization is done. Index is being rebuild after every deleted row.

## Installation
From Pypi
```
pip install influx-cleaner
```
This will install `influx-cleaner` command line tool to your path.

## Usage in interactive mode
Run
```
influx-cleaner --host 192.168.1.2 --dbname myinfluxdb
```
The tool will ask you for measurement name and query
```
Measurement name(): TestMeasurement
WHERE value < -100
DEBUG:cleaner.influx_cleaner.cleaner:Fetching: select * from TestMeasurement where value < -100;
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): 192.168.1.2:8086
DEBUG:urllib3.connectionpool:http://192.168.1.2:8086 "GET /query?q=select+%2A+from+TestMeasurement+where+value+%3C+-100%3B&db=myinfluxdb HTTP/1.1" 200 None
measurement_name        time    value
TestMeasurement         2020-06-22T08:14:23.741000Z     -3276.8
TestMeasurement         2020-06-22T08:29:16.077000Z     -3276.8
TestMeasurement         2020-06-22T19:46:03.348000Z     -3276.8
TestMeasurement         2020-09-10T21:01:44.536000Z     -3276.8
TestMeasurement         2020-09-11T03:00:58.966000Z     -3276.8
TestMeasurement         2020-09-11T03:01:00.886000Z     -3276.8
remove (y/N)y
DEBUG:urllib3.connectionpool:http://192.168.1.2:8086 "GET /query?params=%7B%22time%22%3A+%222020-06-22T08%3A14%3A23.741000Z%22%7D&q=DELETE+FROM+TestMeasurement+WHERE+time+%3D+%24time%3B&db=myinfluxdb HTTP/1.1" 200 None
TestMeasurement   2020-06-22T08:14:23.741000Z     -3276.8 removed
DEBUG:urllib3.connectionpool:http://192.168.1.2:8086 "GET /query?params=%7B%22time%22%3A+%222020-06-22T08%3A29%3A16.077000Z%22%7D&q=DELETE+FROM+TestMeasurement+WHERE+time+%3D+%24time%3B&db=myinfluxdb HTTP/1.1" 200 None
TestMeasurement   2020-06-22T08:29:16.077000Z     -3276.8 removed
DEBUG:urllib3.connectionpool:http://192.168.1.2:8086 "GET /query?params=%7B%22time%22%3A+%222020-06-22T19%3A46%3A03.348000Z%22%7D&q=DELETE+FROM+TestMeasurement+WHERE+time+%3D+%24time%3B&db=myinfluxdb HTTP/1.1" 200 None
TestMeasurement   2020-06-22T19:46:03.348000Z     -3276.8 removed
DEBUG:urllib3.connectionpool:http://192.168.1.2:8086 "GET /query?params=%7B%22time%22%3A+%222020-09-10T21%3A01%3A44.536000Z%22%7D&q=DELETE+FROM+TestMeasurement+WHERE+time+%3D+%24time%3B&db=myinfluxdb HTTP/1.1" 200 None
TestMeasurement   2020-09-10T21:01:44.536000Z     -3276.8 removed
DEBUG:urllib3.connectionpool:http://192.168.1.2:8086 "GET /query?params=%7B%22time%22%3A+%222020-09-11T03%3A00%3A58.966000Z%22%7D&q=DELETE+FROM+TestMeasurement+WHERE+time+%3D+%24time%3B&db=myinfluxdb HTTP/1.1" 200 None
TestMeasurement   2020-09-11T03:00:58.966000Z     -3276.8 removed
DEBUG:urllib3.connectionpool:http://192.168.1.2:8086 "GET /query?params=%7B%22time%22%3A+%222020-09-11T03%3A01%3A00.886000Z%22%7D&q=DELETE+FROM+TestMeasurement+WHERE+time+%3D+%24time%3B&db=myinfluxdb HTTP/1.1" 200 None
TestMeasurement   2020-09-11T03:01:00.886000Z     -3276.8 removed
Removed 6 lines

```

### Arguments
```                                                                                                                                                                                                               (master|●7…)
usage: influx-cleaner [-h] [--host HOST] [--port PORT] [--user USER]
                      [--password PASSWORD] [--dbname DBNAME]
                      [--measurement MEASUREMENT] [--where WHERE] [--yes]

InfluxDB Cleaner

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           InfluxDB hostname
  --port PORT, -p PORT  InfluxDB port
  --user USER           InfluxDB username
  --password PASSWORD   InfluxDB password
  --dbname DBNAME       InfluxDB dbname
  --measurement MEASUREMENT, -m MEASUREMENT
                        Specify measurement
  --where WHERE, -w WHERE
                        Specify where query
  --yes, -y             Say yes to all prompts
```

## Usage in scripts

```bash clean.sh

clean() { influx-cleaner --host 192.168.1.2 --dbname myinfluxdb -m $1 -w $2; }

clean TestMeasurement "value < -100"
clean BogusHumidity "value < 0"
clean BogusTemperature "value < -100"
```

You can add `-y` parameter if you do not want to confirm every clean
