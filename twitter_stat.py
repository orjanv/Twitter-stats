#!/usr/bin/env python
"""
    A python script that takes the Twitter archive export file as input
    and from it extract some usage statistics that might be useful.

        1. Request your Twitter archive here in your Twitter settings:
            - https://twitter.com/settings/account
        2. Once downloaded, unzip the archive into the same folder as this script
        3. Run script like this: 
            $ python twitter_stat.py
    Written by Orjan Vollestad (hoyd@twitter)
    
"""
from __future__ import division
import csv
import datetime
import matplotlib.pyplot as plt
import sys
import webbrowser
from calendar import TimeEncoding, day_name, day_abbr
from collections import defaultdict, OrderedDict
SOURCE = 'tweets.csv' # old version took sys.argv[-1]
WEBPAGE = 'tweets.html'
TWEETDAYSPNG = 'by-days-of-week.png'


def csvtodict(_dict):
    """Function to convert CSV file from input to a Python dictionary
    """
    with open(SOURCE) as _file:
        # Create a reader which represents rows in a dictionary form
        reader = csv.DictReader(_file)
        # This will read a row as {column1: value1, column2: value2,...}
        for row in reader:
            # Go over each column name and value
            for (keys, values) in row.items():
                _dict[keys].append(values)
    return _dict


def get_day_name(day_no, locale, short=False):
    with TimeEncoding(locale) as encoding:
        if short:
            s = day_abbr[day_no]
        else:
            s = day_name[day_no]
        if encoding is not None:
            s = s.decode(encoding)
        return s
        
def daycount(_dict):
    """Function to get count of tweets grouped on weekday
    """
    weekdays = []
    for weekday in _dict['timestamp']:
        wdate = weekday[:10]
        date = datetime.datetime.strptime(wdate, '%Y-%m-%d')
        day = datetime.datetime.isoweekday(date)
        day = get_day_name(day-1, "en_GB.UTF-8", True)
        weekdays.append(day)

    # Build a dictionary to store the number of tweets per day
    daynumbers = {u'Mon':0, u'Tue':0, u'Wed':0, u'Thu':0, u'Fri':0, u'Sat':0, u'Sun':0}
    for k, v in daynumbers.iteritems():
        daynumbers[k] = weekdays.count(k)

    add_to_webpage("You have tweeted most often on a %s" % (maxdictvalue(daynumbers)))

    # plot the data using pyplot
    plot_data(daynumbers)

def generic_stat(_dict):
    """Function to generate some generic Twitter stats
    """
    weekdays = []
    for weekday in _dict['timestamp']:
        day = weekday[:10]
        weekdays.append(day)
    date_first_tweet = datetime.datetime.strptime(weekdays[0], '%Y-%m-%d')
    date_last_tweet = datetime.datetime.strptime(weekdays[-1], '%Y-%m-%d')
    date_beginning = datetime.datetime.strptime('2006-03-21', '%Y-%m-%d') # The first tweet ever posted to Twitter
    # Do some calculations
    twitter_length = date_first_tweet - date_last_tweet
    years, remainder = divmod(twitter_length.days, 365)
    average = len(weekdays) / twitter_length.days
    pioneer = date_last_tweet - date_beginning
    p_year, p_days = divmod(pioneer.days, 365)
    # Write the results to webpage    
    add_to_webpage("You have been tweeting for %s years and %s day(s)" % (years, remainder))
    add_to_webpage("Your first tweet was posted %s years and %s days after the first tweet posted ever to Twitter" % (p_year, p_days))
    add_to_webpage("Total number of tweets in archive: %s" % (len(weekdays)))
    add_to_webpage("On an average, you have tweeted %.2f tweets each day" % (round(average, 2)))


def plot_data(D):
    '''Take in a dict and plot it
    '''
    plt.title('Tweets by Day of Week')
    plt.bar(range(len(D)), D.values(), align='center', color='green', edgecolor='green')
    plt.xticks(range(len(D)), D.keys())
    plt.savefig(TWEETDAYSPNG, bbox_inches=0)
    add_to_webpage('<h2>Tweets by days of week</h2>\n<img src="%s" width="420px" />' % TWEETDAYSPNG)
    #plt.show()

def add_to_webpage(tekst):
    '''Function to add inn <p> tags with text as argument
    '''
    f = open(WEBPAGE,'a')
    f.write('<p>\n%s\n</p>\n' % tekst)
    f.close()
    
def create_webpage():
    '''Set up the html file with a header
    '''
    f = open(WEBPAGE, 'w')
    f.write('<h1>Twitter statistics</h1>\n')
    f.close()

def maxdictvalue(_dict):
    """Return key of dict that has the biggest value
    """
    values = list(_dict.values())
    keys = list(_dict.keys())
    return keys[values.index(max(values))]


def main():
    """Create the dict with a list as value
    """
    create_webpage()
    _dict = defaultdict(list)
    csvtodict(_dict)
    tekst = generic_stat(_dict)
    daycount(_dict)
    
    webbrowser.open(WEBPAGE)


if __name__ == "__main__":
    main()
