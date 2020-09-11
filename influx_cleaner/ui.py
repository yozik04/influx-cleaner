from abc import ABC


class UI(ABC):
    measurement = ''
    where = ''
    removal_confirmation = False

    def get_measurement(self):
        return self.measurement

    def get_where(self):
        return self.where

    def get_removal_confirmation(self):
        return self.removal_confirmation


class InteractiveUI(UI):
    def __init__(self):
        self.previous_measurement = ''

    def get_measurement(self):
        measurement_name = ''
        while not measurement_name:
            measurement_name = input("Measurement name(%s): " % self.previous_measurement)
            if measurement_name == '':
                measurement_name = self.previous_measurement

        return measurement_name

    def get_where(self):
        return input("WHERE ")

    def get_removal_confirmation(self):
        remove = input('remove (y/N)')
        return remove.lower() == 'y'


class NoUI(UI):
    def __init__(self, measurement, where, no_confirm=True):
        self.measurement = measurement
        self.where = where
        self.no_confirm = no_confirm

    def get_measurement(self):
        return self.measurement

    def get_where(self):
        return self.where

    def get_removal_confirmation(self):
        if self.no_confirm:
            return True
        else:
            remove = input('remove (y/N)')
            return remove.lower() == 'y'
