#!/usr/bin/env python

"""Tests for `power_consumption_logger` package."""

import pytest
import tempfile
import os
import responses
import requests


import power_consumption_logger.power_consumption_logger as pcl


@pytest.fixture(scope="module")
def temp_dir ():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname  # provide the fixture value


def helper_entry_available(filename, entry, line_no):
    with open(filename) as f:
        content = f.read().splitlines()
        print(content)
        return content[line_no] == pcl.data_to_str(entry)

def test_create_storage_dir__and_fail():
    """ we do not have create access rights on / root dir so it fails"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        pcl.Writer('/Z:/', 'simulate')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def test_create_storage_dir__ok(temp_dir):
    """ must be able to create something inside temp dir """
    new_dir = os.path.join(temp_dir, 'new')
    sut = pcl.Writer(new_dir, 'simulate')
    assert sut.dirname == new_dir
    assert os.path.isdir(new_dir)

def test_create_new_measurement_file__one_line(temp_dir):
    data = ['2020-08-19T22:55:00', 1, 1, 1, 1]
    sut = pcl.Writer(temp_dir, 'simulate')
    expected_file = os.path.join(temp_dir, 'cmatic_2020-08-19.csv')
    sut._write_data(data)
    assert os.path.isfile(expected_file)
    assert helper_entry_available(expected_file, data, 0)

def test_create_new_measurement_file__three_line(temp_dir):
    data1 = ['2020-08-20T08:55:00', 1, 1, 1, 1]
    data2 = ['2020-08-20T08:56:00', 1, 1, 1, 1]
    data3 = ['2020-08-20T08:57:00', 1, 1, 1, 1]
    sut = pcl.Writer(temp_dir, 'simulate')
    expected_file = os.path.join(temp_dir, 'cmatic_2020-08-20.csv')
    sut._write_data(data1)
    sut._write_data(data2)
    sut._write_data(data3)
    assert os.path.isfile(expected_file)
    assert helper_entry_available(expected_file, data1, 0)
    assert helper_entry_available(expected_file, data2, 1)
    assert helper_entry_available(expected_file, data3, 2)


@responses.activate
def test_web_response__ok():
    responses.add(responses.GET, 'http://cmatic-d9cd14/cm?cmnd=Status%2010',
        json={
            "StatusSNS": {
                "Time": "2018-11-11T13:46:56",
                "COUNTER": {
                    "C1": 109,
                    "C2": 8,
                    "C3": 6,
                "C4": 14
                }
            }
        }, status=200)

    expected_response = ['2018-11-11T13:46:56',  109, 8, 6, 14]
    assert pcl.read_from_web('D9CD14') == expected_response

@responses.activate
def test_web_response__connection_error():
    """ we do not have create access rights on / root dir so it fails"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        pcl.read_from_web('D9CD14')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
