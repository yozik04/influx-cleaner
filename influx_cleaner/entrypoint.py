import argparse
import logging

from influxdb import InfluxDBClient

from influx_cleaner.cleaner import App
from influx_cleaner.ui import InteractiveUI, NoUI

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8086
DEFAULT_DBNAME = 'openhab2'

logger = logging.getLogger('cleaner').getChild(__name__)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='InfluxDB Cleaner')
    parser.add_argument('--host', type=str, required=False,
                        default=DEFAULT_HOST,
                        help='InfluxDB hostname')
    parser.add_argument('--port', '-p', type=int, required=False, default=DEFAULT_PORT,
                        help='InfluxDB port')
    parser.add_argument('--user', type=str, required=False, default='',
                        help='InfluxDB username')
    parser.add_argument('--password', type=str, required=False, default='',
                        help='InfluxDB password')
    parser.add_argument('--dbname', type=str, required=False, default=DEFAULT_DBNAME,
                        help='InfluxDB dbname')
    parser.add_argument('--measurement', '-m', type=str, required=False,
                        help='Specify measurement')
    parser.add_argument('--where', '-w', type=str, required=False,
                        help='Specify where query')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Say yes to all prompts')
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.DEBUG)

    args = parse_args()

    interactive = not (args.measurement and args.where)

    cleaner = App(
        db=InfluxDBClient(host=args.host, port=args.port, username=args.user, password=args.password,
                          database=args.dbname),
        ui=InteractiveUI() if interactive else NoUI(measurement=args.measurement, where=args.where, no_confirm=args.yes)
    )

    try:
        if interactive:
            while True:
                cleaner.clean()
        else:
            cleaner.clean()
    except KeyboardInterrupt:
        print('\nbye!')


if __name__ == '__main__':
    main()