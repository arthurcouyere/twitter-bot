import argparse
import logging
import tweepy
from datetime import datetime
from os import environ
from dotenv import load_dotenv
from tqdm import tqdm

#################################
# config
#################################

# load .env file
load_dotenv()

# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#################################
# main
#################################

def main():

    # args
    parser = argparse.ArgumentParser(description='list tweets from Twitter API')
    parser.add_argument('-v', '--verbose',  action='store_true', help="verbose mode")
    parser.add_argument('-f', '--from-date', help="get tweets after date")
    args = parser.parse_args()
    logging.debug(args)
    
    # twitter auth
    auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
    auth.set_access_token(environ["ACCESS_KEY"], environ["ACCESS_SECRET"])
    api = tweepy.API(auth)

    user = api.me()
    logging.info("current user: {1} [{0}]".format(user.id, user.screen_name))

    # init
    nb_status = 0
    if args.from_date:
        date_bound = datetime.strptime(args.from_date, "%Y-%m-%d %H:%M:%S")
    else:
        date_bound = None
    first_status = last_status = None
    tqdm_disabled = (args.verbose == True)

    # loop on statuses
    status_cursor = tweepy.Cursor(api.user_timeline).items()
    for status in tqdm(status_cursor, total=user.statuses_count, desc="Loading tweets", disable=tqdm_disabled):
        if date_bound == None or (date_bound !=None and status.created_at  > date_bound):
            if args.verbose:
                logging.info("[{1}] [{0}] [{2}] ".format(status.id, status.created_at, status.text))
            nb_status += 1
            if first_status == None:
                first_status = status
            last_status = status

    logging.info("tweets found: #{0}".format(nb_status))
    logging.info("first status: [{1}] [{0}] [{2}] ".format(first_status.id, first_status.created_at, first_status.text))
    logging.info("last  status: [{1}] [{0}] [{2}] ".format(last_status.id, last_status.created_at, last_status.text))

if __name__ == "__main__":
    main()
