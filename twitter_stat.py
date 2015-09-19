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
from calendar import TimeEncoding, day_name, day_abbr
from collections import defaultdict, OrderedDict, Counter
import csv, re, datetime, sys, webbrowser
import matplotlib.pyplot as plt
import numpy as np

SOURCE = 'tweets.csv' # old version took sys.argv[-1]
WEBPAGE = 'tweets.html'
BYDAYSPNG = 'by-days-of-week.png'
HASHTAGPNG = 'most-common-hashtags.png'
MENTIONPNG = 'most-common-mentions.png'
HEADER = ["tweet_id","in_reply_to_status_id","in_reply_to_user_id","timestamp","source","text",\
        "retweeted_status_id","retweeted_status_user_id","retweeted_status_timestamp","expanded_urls"]
HEADER_DICT = dict( (name,i) for i, name in enumerate(HEADER) )
DEBUG = False
            
def get_words(tweet_text):
    return [word.lower() for word in re.findall('\w+', tweet_text) if len(word) > 3]

def load_tweets():
    tweets = []
    file_path = SOURCE
    with open(file_path,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        csvreader.next() # Skip header
        for row in csvreader:
            tweets.append(row)

    #print 'Loaded %d tweets' % len(tweets)

    #print tweets[:10]

    return tweets
    
def word_frequency(tweets):
    hash_c = Counter()
    at_c = Counter()  
    
    for tweet in tweets:
        for word in re.findall('@\w+', tweet[ HEADER_DICT['text'] ]):
            at_c[ word.lower() ] += 1
        for word in re.findall('\#[\d\w]+', tweet[ HEADER_DICT['text'] ]):
            hash_c[ word.lower() ] += 1
    
    hash_d = dict(hash_c.most_common(10))
    
    if DEBUG:
        print hash_d
    plot_data(hash_d, "10 most common hashtags", HASHTAGPNG)
    
    at_d = dict(at_c.most_common(10))
    
    if DEBUG:
        print at_d
    plot_data(at_d, "10 most common mention", MENTIONPNG)
        
def csvtodict(_dict):
    """Function to convert CSV file from input to a Python dictionary
    """
    with open(SOURCE) as _file:
        # Create a reader which represents rows in a dictionary form
        reader = csv.DictReader(_file)
        # This will read a row as {column1: value1, column2: value2,...}
        tweets = 0
        for row in reader:
            # Go over each column name and value
            for (keys, values) in row.items():
                _dict[keys].append(values)
            tweets += 1
    #print 'Loaded %d tweets' % tweets
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
        day = get_day_name(day-1, "en_GB.UTF-8", False)
        weekdays.append(day)

    # Build a dictionary to store the number of tweets per day
    daynumbers = {u'Monday':0, u'Tuesday':0, u'Wednesday':0, u'Thursday':0, u'Friday':0, u'Saturday':0, u'Sunday':0}
    for k, v in daynumbers.iteritems():
        daynumbers[k] = weekdays.count(k)

    add_to_webpage("<li>You have tweeted most often on a %s</li></ul>" % (maxdictvalue(daynumbers)))
    
    if DEBUG:
        print daynumbers
    # plot the data using pyplot
    plot_data(daynumbers, "Tweets by days of week", BYDAYSPNG)

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
    add_to_webpage("<ul><li>You have been tweeting for %s years and %s day(s)</li>" % (years, remainder))
    add_to_webpage("<li>Your first tweet was posted %s years and %s days after the first tweet posted ever to Twitter</li>" % (p_year, p_days))
    add_to_webpage("<li>Total number of tweets in archive: %s</li>" % (len(weekdays)))
    add_to_webpage("<li>On an average, you have tweeted %.2f tweets each day</li>" % (round(average, 2)))

def plot_data(D, title, _file):
    '''Take in a dict and plot it
    '''
    # Size of plot
    fig = plt.figure(figsize=(12, 6))
    
    # Plot settings and values
    plt.title(title)
    plt.barh(range(len(D)), D.values(), align='center', color='green', edgecolor='green')
    plt.margins(right=0.1)
    plt.subplots_adjust(left=0.20)
    plt.yticks(range(len(D)), list(D.keys()))

    # Save to file
    plt.savefig(_file, bbox_inches=0)
    add_to_webpage('<h2>%s</h2>\n<img src="%s" width="700px" />' % (title, _file))

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
    generic_stat(_dict)
    daycount(_dict)

    # Taken from https://github.com/laurenarcher/twitter-archive-analysis
    tweets = load_tweets()
    word_frequency(tweets)

    webbrowser.open(WEBPAGE)

if __name__ == "__main__":
    main()
