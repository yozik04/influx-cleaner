# influx-cleaner
A command line tool to remove invalid data from InfluxDB.

I am using some openhab2 bindings that from time to time produce invalid data. This invalid data gets into InfluxDB. It is complicated to clean it.

Tool is not meant to delete a large amount of data. No deletion performance optimization is done. Index is being rebuild after every deleted row.

## Installation
From Pypi
```
pip install influx-cleaner
```
This will install `influx-cleaner` command line tool to your path.

## Usage
Run
```
influx-cleaner
```

###
Arguments
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

clean() { influx-cleaner --host 192.168.1.2 --dbname openhab2 -m $1 -w $2; }

clean BogusHumidity "value < 0"
clean BogusTemperature "value < -100"
```
