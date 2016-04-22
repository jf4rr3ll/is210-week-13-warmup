#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Task 01 Module"""


import csv
import json

GRADES = {
    'A': float(1.00),
    'B': float(0.90),
    'C': float(0.80),
    'D': float(0.70),
    'F': float(0.60),
    }


def get_score_summary(filename):
    """Defines a function to read and interpret the data in a file.

    Args:
        filename (str): the filename of the file which will be read.

    Returns:
        dictionary: keyed by boro, with values of a tuple for the number
        of restaurants, and their scores.

    Examples:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417,
    """
    data = {}
    fhandler = open(filename, 'r')
    csvdata = csv.reader(fhandler)
    for row in csvdata:
        if row[10] not in ['P', '', 'GRADE']:
            data[row[0]] = [row[1], row[10]]
            data.update(data)
    fhandler.close()

    review = {}
    for value in data.itervalues():
        if value[0] not in review.iterkeys():
            val1 = 1
            val2 = GRADES[value[1]]
        else:
            val1 = review[value[0]][0] + 1
            val2 = review[value[0]][1] + GRADES[value[1]]
        review[value[0]] = (val1, val2)
        review.update(review)

    results = {}
    for key in review.iterkeys():
        val1 = review[key][0]
        val2 = review[key][1]/review[key][0]
        results[key] = (val1, val2)
    return results


def get_market_density(filename):
    """Defines a function that

    """
    fhandler = open(filename, 'r')
    jsondata = json.load(fhandler)
    alldata = jsondata['data']
    datatotal = {}
    fhandler.close()
    for data in alldata:
        data[8] = data[8].strip()
        if data[8] not in datatotal.iterkeys():
            val = 1
        else:
            val = datatotal[data[8]] + 1
        datatotal[data[8]] = val
        datatotal.update(datatotal)
    return datatotal


def correlate_data(filename1='inspection_results.csv',
                   filename2='green_markets.json',
                   filename3='correlationdata.csv'):
    """Defines a function to

    Args:
        filename1 (str)
        filename2 (str)
        filename3 (str)

    Returns:
        dictionary:
    """
    scoredata = get_score_summary(filename1)
    marketdata = get_market_density(filename2)
    dataresult = {}
    for key2 in marketdata.iterkeys():
        for key1 in scoredata.iterkeys():
            if key1 == str(key2).upper():
                val1 = scoredata[key1][1]
                val2 = float(marketdata[key2])/(scoredata[key1][0])
                dataresult[key2] = (val1, val2)
                dataresult.update(dataresult)
    jdata = json.dumps(dataresult)
    fhandler = open(filename3, 'w')
    fhandler.write(jdata)
    fhandler.close