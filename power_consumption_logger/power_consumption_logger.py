"""Main module."""
import requests
import datetime
import time
import sys
from pathlib import Path
import os


def read_from_web_sim():
    timestamp = datetime.datetime.now().isoformat(timespec='seconds')
    return [timestamp, 1, 2, 3, 4]


def read_from_web(host='cmatic-xxxxx'):
    """Read the data from the host interface

    Reads a JSON struct like {
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
    from a web CDN

    Parameters
    ----------

    Returns
    -------

    array of [timestamp: string, c1: int c2: int, c3: int, c4: int]


    Exception:
    ----------
    in case of read error it exits the program with code 1

    """
    if host == 'simulate':
        # shortcut for testing
        return read_from_web_sim()
    try:
        url = 'http://' + host + '/cm'
        # param = {'cmnd': 'Status 10'.encode("utf-8")}
        param = '?cmnd=Status%2010'
        print('{} param {}'.format(url, param))
        r = requests.get(url + param)
        data = r.json()
        print(data)
        return [
            data['StatusSNS']['Time'],
            data['StatusSNS']['COUNTER']['C1'],
            data['StatusSNS']['COUNTER']['C2'],
            data['StatusSNS']['COUNTER']['C3'],
            data['StatusSNS']['COUNTER']['C4']
        ]
    except requests.exceptions.ConnectionError as err:
        print('Connection error: {}'.format(err))
        sys.exit(1)


def reset_counter(host='cmatic-xxxxx'):
    """Reset all counters of cmatic

    Parameters
    ----------

    host (str):
        The host to call

    """
    if host == 'simulate':
        # shortcut for testing
        return
    try:
        url = 'http://' + host + '/cm'
        for i in range(1,5):
            param = f"?cmnd=Counter{i}%200"
            print('{} param {}'.format(url, param))
            requests.get(url + param)
    except requests.exceptions.ConnectionError as err:
        print('Connection error: {}'.format(err))
        sys.exit(1)


def data_to_str(data):
    return '{};{};{};{};{}'.format(data[0], data[1], data[2], data[3], data[4])

class Writer:

    def __init__(self, dirname, host):
        self.dirname = dirname
        self.host = host
        self.iso_date = "2021-02-04"
        # make sure file exists and is writeable or throw an io exception
        try:
            path = Path(self.dirname)
            path.mkdir(parents=True, exist_ok=True)
        except EnvironmentError:
            # parent of IOError, OSError *and* WindowsError where available
            print('Cannot create storage location {}'.format(self.dirname))
            sys.exit(2)

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
        iso_date = data[0][:10]  # 1st 10 letters form iso format are the date
        filename = os.path.join(self.dirname, 'cmatic_' + iso_date + '.csv')

        try:
            with open(filename, 'a') as f:
                f.write(data_to_str(data) + '\n')
        except EnvironmentError:
            # parent of IOError, OSError *and* WindowsError where available
            print('Cannot write data to file {}'.format(filename))
            sys.exit(2)

    def record(self, period_in_sec: int):
        """Record a dataset continuously

        Args:
            period_in_sec: delay for different readings
        In a single thread, block while sleeping
        Never return
        """
        if period_in_sec == 0:
            self._record_single()
        else:
            while True:
                self._record_single()
                time.sleep(period_in_sec)

    def _record_single(self):
        """Record a single dataset"""
        data = read_from_web(self.host)
        iso_date = iso_date = data[0][:10]
        if self.iso_date != iso_date:
            self.iso_date = iso_date
            reset_counter(self.host)
        else:
            self._write_data(data)
