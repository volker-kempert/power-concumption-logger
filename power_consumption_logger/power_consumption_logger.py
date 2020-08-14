"""Main module."""
import requests
import datetime
import sys
from pathlib import Path
import time


def read_from_web(host='cmatic-xxxxx'):
    """Read the data from the host interface (pure function)

    Parameters
    ----------

    Returns
    -------
    - example {
        "StatusSNS": {
            "Time": "2018-11-11T13:46:56",
            "COUNTER": {
                "C1": 109,
                "C2": 8,
                "C3": 6,
                "C4": 14
                }
            }
        }

    """
    try:
        r = requests.get('http://' + host + '/cm?cmnd=Status 10')
        data = r.json()
        return String.format('{} {} {} {} {}\n',
            data['StatusSNS']['Time'],
            data['StatusSNS']['COUNTER']['C1'],
            data['StatusSNS']['COUNTER']['C2'],
            data['StatusSNS']['COUNTER']['C3'],
            data['StatusSNS']['COUNTER']['C4']
        )
    except requests.exceptions.ConnectionError as err:
        print('Connection error: {}'.format(err))
        sys.exit(1)


class Writer:

    def __init__(self, dirname, host):
        self.dirname = dirname
        # make sure file exists and is writeable or throw an io exception
        try:
            path=Path(self.dirname)
            path.mkdir(parents=True, exist_ok=True)
        except EnvironmentError:
            # parent of IOError, OSError *and* WindowsError where available
            print('Cannot create storage location {}'.format(self.dirname))
            sys.exit(1)
        self.filename = os.path.join(self.dirname, 'cmatic-{}'.format(datetime.date.today()))

    def _write_data(self, data):
        """Write data to file persistently.

        TODO add more

        Parameters:
        -----------

        data: structure like:
        "StatusSNS": {
            "Time": "2018-11-11T13:46:56",
            "COUNTER": {
                "C1": 109,
                "C2": 8,
                "C3": 6,
                "C4": 14
                }
            }
        }


        """
        try:
            with open(self.filename, 'a') as f:
                f.write(data)
        except EnvironmentError:
            # parent of IOError, OSError *and* WindowsError where available
            print('Cannot write data to file {}'.format(file_name))
            sys.exit(2)

    def record(period_in_sec: int):
        """Record a dataset continuously

        In a single thread, block while sleeping
        Never return
        """
        while True:
            self._write_data(read_from_web(self.url))
            time.sleep(period_in_sec)

