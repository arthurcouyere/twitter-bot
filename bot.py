import sys
import logging
import zipfile
from pathlib import Path
from configparser import ConfigParser
import tweepy

#################################
# config
#################################


# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

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
            with open(self.last_pos_file, "r") as f_last_pos:
                try:
                    last_pos = int(f_last_pos.read())
                except:
                    logging.debug(f"last pos is not an integer")
                    last_pos = -1

        else:
            logging.debug(f"last pos file does not exists")
            last_pos = -1
        
        logging.debug(f"last pos : {last_pos}")
        return last_pos

    def save_last_pos(self):
        with open(self.last_pos_file, "w") as f_last_pos:
            f_last_pos.write(f"{self.cur_pos}")

    def get_next_word(self):
        f = open(self.words_file, 'r', encoding='utf8')
        logging.debug(f"reading text file {f.name}")
        for i, line in enumerate(f):
            if i == self.cur_pos:
                return line.strip()

#################################
# main
#################################

def main():

    # config file
    config = ConfigParser()
    config.read('bot.ini')

    script_dir = Path(__file__).resolve().parent
    words_file = script_dir / Path(config["bot"]["words_file"])
    last_post_file = script_dir / Path(config["bot"]["last_pos_file"])

    word_gen = WordGenerator(words_file, last_post_file)
    print(word_gen.get_next_word())
    word_gen.save_last_pos()

    # Authenticate to Twitter
    # auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
    auth = tweepy.OAuthHandler(config["twitter"]["api_key"], config["twitter"]["api_secret_key"])
    # auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")
    auth.set_access_token(config["twitter"]["access_token"], config["twitter"]["access_token_secret"])

    # Create API object
    api = tweepy.API(auth)

    # Post a tweet
    api.update_status("Hello")

if __name__ == "__main__":
    main()