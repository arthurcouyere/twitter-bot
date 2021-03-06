import logging
from pathlib import Path
from configparser import ConfigParser
from redis import Redis
import tweepy
import redis
from os import environ
from dotenv import load_dotenv

#################################
# config
#################################

config_file = "bot.ini"

# load .env file
load_dotenv()

# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#################################
# functions
#################################

class Context():
    last_pos_prop = "twitter-bot.last_pos"

    def __init__(self, r: Redis) -> None:
        self.r = r

    def get_last_pos(self)-> int:
        last_pos = self.r.get(self.last_pos_prop)
        if last_pos == None:
            last_pos = -1
        else:
            last_pos = int(last_pos.decode('utf8'))

        return last_pos

    def save_last_pos(self, last_pos: int) -> None:
        self.r.set(self.last_pos_prop, last_pos)

class WordGenerator():
    """
    Word generator : loads words from a text file and saves last word read
    """
    zip_txt_file = "words.txt"
    last_pos = 0

    def __init__(self, words_file: Path, r: Redis) -> None:

        self.context = Context(r)

        self.words_file = words_file
        self.cur_pos = self.context.get_last_pos() + 1

    def save_last_pos(self):
        self.context.save_last_pos(self.cur_pos)

    def get_next_word(self):
        f = open(str(self.words_file), 'r', encoding='utf8')
        logging.debug("reading text file %s" % f.name)
        for i, line in enumerate(f):
            if i == self.cur_pos:
                return line.strip()

#################################
# main
#################################

def main():

    # config
    config = ConfigParser()
    config.read(config_file)

    tweet_template =config["bot"]["tweet_template"]

    script_dir = Path(__file__).resolve().parent
    words_file     = script_dir / Path(config["bot"]["words_file"])

    # redis connect
    r = redis.from_url(environ["REDIS_URL"])

    # twitter auth
    auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
    auth.set_access_token(environ["ACCESS_KEY"], environ["ACCESS_SECRET"])

    api = tweepy.API(auth)

    # get last tweeted word
    word_gen = WordGenerator(words_file, r)
    next_word = word_gen.get_next_word()

    # post tweet
    status = tweet_template.format(next_word)
    logging.info("tweeting status [%s]" % status)
    api.update_status(status)

    # save pos
    word_gen.save_last_pos()

if __name__ == "__main__":
    main()
