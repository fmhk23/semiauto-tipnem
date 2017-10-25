# -*- coding: utf-8 -*-

# Usage
# Please find Readme on github.
# python auto_tipnem.py <account list csv> <amount> <mosaic name>

# Libraries
import configparser
import datetime
import pandas as pd
import sys
import time

from requests_oauthlib import OAuth1Session

# Functions
def post_tiptweet(name, ammount, mosaic, twitter):
    tweet_time = datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S')

    tweet = '@tipnem tip ' + name + ' ' + ammount + ' ' + mosaic + ' automatically tweeted at ' + tweet_time
    params = {'status': tweet}

    req = twitter.post('https://api.twitter.com/1.1/statuses/update.json', params = params)
    time.sleep(60)

    if req.status_code == 200:
        return('Tweeted to' + name + ' ! Check Reply from @tipnem')
    else:
        return('Failed to send to ' + name + ': %d' % req.status_code)

def main():
    # Read Tokens and Secrets from config
    config = configparser.ConfigParser()
    config.read('config.ini')
    CK = config['keys']['CK']
    CS = config['keys']['CS']
    AS = config['keys']['AS']
    AT = config['keys']['AT']

    # Get arguments
    csv = sys.argv[1]
    amount = sys.argv[2]
    mosaic = sys.argv[3]

    # Read account list from csv
    accounts_pd = pd.read_csv(csv)
    accounts = list(accounts_pd['name'])

    # Generate OAuth1Session
    twitter = OAuth1Session(CK, CS, AT, AS)

    # Tip
    [post_tiptweet(x, amount, mosaic, twitter) for x in accounts]

if __name__ == '__main__':
    main()
