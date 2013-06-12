#!/usr/bin/env python
"""
    A python script that takes the Twitter archive export file as input
    and from it extract some usage statistics that might be useful.

        1. Request your Twitter archive here in your Twitter settings:
            - https://twitter.com/settings/account
        2. Once downloaded, store in the same folder as this script
        3. Run script like this: 
            $ python twitter_stat.py tweets.csv
    Written by Orjan Vollestad (orjanv@gmail.com)
"""
from __future__ import division
import csv
import datetime
import sys
import calendar
from collections import defaultdict
FILENAME = sys.argv[-1]


def csvtodict(_dict):
    """Function to convert CSV file from input to a Python dictionary"""
    with open(FILENAME) as _file:
        # Create a reader which represents rows in a dictionary form
        reader = csv.DictReader(_file)
        # This will read a row as {column1: value1, column2: value2,...}
        for row in reader:
            # Go over each column name and value
            for (keys, values) in row.items():
                _dict[keys].append(values)
    return _dict


def daycount(_dict):
    """Function to get count of tweets grouped on weekday"""
    weekdays = []
    for weekday in _dict['timestamp']:
        wdate = weekday[:10]
        date = datetime.datetime.strptime(wdate, '%Y-%m-%d')
        day = datetime.datetime.isoweekday(date)
        weekdays.append(day)

    # Build a dictionary to store the number of tweets per day
    daynumbers = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    for day in range(1, 8):
        daynumbers[day] = weekdays.count(day)
    tday = maxdictvalue(daynumbers)-1
    print "You have tweeted most often on a %s" % (calendar.day_name[tday])
    

def generic_stat(_dict):
    """Function to generate some generic Twitter stats  """
    weekdays = []
    for weekday in _dict['timestamp']:
        day = weekday[:10]
        weekdays.append(day)
    date_first_tweet = datetime.datetime.strptime(weekdays[0], '%Y-%m-%d')
    date_last_tweet = datetime.datetime.strptime(weekdays[-1], '%Y-%m-%d')
    # Do some calculations
    twitter_length = date_first_tweet - date_last_tweet
    years, remainder = divmod(twitter_length.days, 365)
    average = len(weekdays) / twitter_length.days
    # Print the results
    print "You have been tweeting for %s years and %s day(s)" % \
        (years, remainder)
    print "Total number of tweets in archive: %s" % (len(weekdays))
    print "On an average, you have tweeted %.2f tweets each day" % \
        (round(average, 2))

    
def maxdictvalue(_dict):
    """Return key of dict that has the biggest value"""
    values = list(_dict.values())
    keys = list(_dict.keys())
    return keys[values.index(max(values))]


def main():
    """Create the dict with a list as value"""
    _dict = defaultdict(list)
    csvtodict(_dict)
    generic_stat(_dict)
    daycount(_dict)


if __name__ == "__main__":
    main()
