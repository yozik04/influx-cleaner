from setuptools import setup

setup(
    name='influx-cleaner',
    version='1.0.0',
    packages=['influx_cleaner'],
    url='https://github.com/yozik04/influx-cleaner',
    license='LGPL3',
    author='Jevgeni Kiski',
    author_email='yozik04@gmail.com',
    description='InfluxDB Measurement data cleaner',
    entry_points={
        "console_scripts": [
            "influx-cleaner = influx_cleaner.entrypoint:main"
        ]
    },
    install_requires=['influxdb']
)
