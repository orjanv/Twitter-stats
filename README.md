Twitter-stats
=============

A small python script that takes the Twitter archive export file as input and from it extract some usage statistics.

1. Request your Twitter archive here in your Twitter settings:
    * https://twitter.com/settings/account
2. Once downloaded, extract the tweets.csv file from the archive into the same folder as this script
3. Then, run the script like this: 

```
$ python twitter_stat.py
```

Features
--------
- Plots amount of tweets against days a week using pyplot from matplotlib
- Writes the outout to a html file 'tweets.html' and then opens it in a webbrowser

![alt text][plot]

Suggestions:
------------
- Most used words using pytagcloud

[logo]: https://github.com/orjanv/Twitter-stats/blob/master/by-days-of-week.png "Tweets by days of week"
