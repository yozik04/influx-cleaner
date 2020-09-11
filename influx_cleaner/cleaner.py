import json
import logging
from typing import List

from influxdb.client import ResultSet

from influx_cleaner.ui import UI

logger = logging.getLogger('cleaner').getChild(__name__)


class MeasurementEntry:
    def __init__(self, name, row):
        self.name = name
        self.time = row['time']
        self.value = row['value']

    def __repr__(self):
        return f"{self.name}\t{self.time}\t{self.value}"


class Cleaner:
    def __init__(self, db):
        self.db = db
        self.entries: List[MeasurementEntry] = []

    def has_entries(self):
        return len(self.entries) > 0

    def print_measurement_entries(self):
        if len(self.entries) == 0:
            logger.warning('Empty result')
            return

        print("measurement_name\ttime\tvalue")
        for entry in self.entries:
            print(entry)

    def fetch_measurement_entries(self, measurement, where):
        if not measurement or not where:
            raise ValueError('measurement or where is not set')

        query_where = 'select * from ' + measurement + ' where ' + where + ';'
        logger.debug(f'Fetching: {query_where}')

        result = self.db.query(query_where)  # type: ResultSet

        self.entries = list([MeasurementEntry(measurement, row) for row in result.get_points(measurement)])

    def remove_measurement_entries(self):
        for item in self.entries:
            self._remove_measurement_entry(item)

    def _remove_measurement_entry(self, item: MeasurementEntry):
        delete_query = 'DELETE FROM ' + item.name + ' WHERE time = $time;'
        self.db.query(delete_query, params={'params': json.dumps({'time': item.time})})
        print(f"{item} removed")

        # delete_query = 'DELETE FROM ' + measurement_name + ' WHERE '
        # where = []
        # where_params = {}
        # for nr, item in enumerate(data):
        #     where.append(f"time = $time{nr}")
        #     where_params[f'time{nr}'] = item['time']
        #
        # query = delete_query + " OR ".join(where) + ";"
        # result = client.query(query, bind_params=where_params, method="post")
        #
        # print(f'Removed {len(data)} lines')


class App:
    def __init__(self, db, ui: UI):
        self.cleaner = Cleaner(db)
        self.ui: UI = ui

    def clean(self):
        measurement = self.ui.get_measurement()
        where = self.ui.get_where()

        self.cleaner.fetch_measurement_entries(measurement, where)

        self.cleaner.print_measurement_entries()

        if self.cleaner.has_entries():
            if self.ui.get_removal_confirmation():
                self.cleaner.remove_measurement_entries()

                print(f'Removed {len(self.cleaner.entries)} lines')
            else:
                print(f'Not removing')


