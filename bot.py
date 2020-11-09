import sys
import logging
import zipfile
from pathlib import Path
from configparser import ConfigParser
import tweepy
from os import environ

#################################
# config
#################################

# logging 
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

#################################
# functions
#################################

class WordGenerator():
    """
    Word generator : loads words from a text file and saves last word read
    """
    zip_txt_file = "words.txt"
    last_pos = 0

    def __init__(self, words_file: Path, last_pos_file: Path):
        
        self.words_file = words_file
        self.last_pos_file = last_pos_file

        last_pos = self.load_last_pos()
        self.cur_pos = last_pos + 1

    def load_last_pos(self):

        if self.last_pos_file.is_file():
            with open(str(self.last_pos_file), "r") as f_last_pos:
                try:
                    last_pos = int(f_last_pos.read())
                except:
                    logging.debug("last pos is not an integer")
                    last_pos = -1

        else:
            logging.debug("last pos file does not exists")
            last_pos = -1
        
        logging.debug("last pos : %s" % last_pos)
        return last_pos

    def save_last_pos(self):
        with open(str(self.last_pos_file), "w") as f_last_pos:
            f_last_pos.write(str(self.cur_pos))

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
    config.read('bot.ini')

    tweet_template =config["bot"]["tweet_template"]

    script_dir = Path(__file__).resolve().parent
    words_file     = script_dir / Path(config["bot"]["words_file"])
    last_post_file = script_dir / Path(config["bot"]["last_pos_file"])

    # twitter auth
    auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
    auth.set_access_token(environ["ACCESS_KEY"], environ["ACCESS_SECRET"])

    api = tweepy.API(auth)

    # get last tweeted word
    word_gen = WordGenerator(words_file, last_post_file)
    next_word = word_gen.get_next_word()

    # post tweet
    api.update_status(tweet_template.format(next_word))

    # save pos
    word_gen.save_last_pos()

if __name__ == "__main__":
    main()
