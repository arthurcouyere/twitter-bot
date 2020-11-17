import argparse
import logging
from datetime import timedelta
import dateparser
from pathlib import Path
from configparser import ConfigParser
import clock

#################################
# config
#################################

config_file = "bot.ini"

# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#################################
# main
#################################

def main():

   # config
    config = ConfigParser()
    config.read(config_file)

    # args
    parser = argparse.ArgumentParser(description='calculate end date for twitter bot', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('start_date', help="start date of bot, in human readable format :\n" +
                                           "2020-11-16\n" +
                                           "2020-11-16 16:30\n" +
                                           "17 nov 2020\n" +
                                           "today\n" +
                                           "(see python dateparse doc for more information)")
    parser.add_argument('-v', '--verbose',  action='store_true', help="verbose mode")
    args = parser.parse_args()
    logging.debug(args)

    script_dir = Path(__file__).resolve().parent
    words_file = script_dir / Path(config["bot"]["words_file"])

    # load words
    print("loading words")
    word_count = 0
    with open(str(words_file), "r") as f:
        for i, line in enumerate(f):
            word_count += 1
    
    print("words found : {}".format(word_count))

    # tweet period
    print("run period in minutes : {}".format(clock.run_period_in_minutes))

    start_date = dateparser.parse(args.start_date)
    print("start date : {}".format(start_date))
    
    duration_in_minutes = clock.run_period_in_minutes * word_count
    end_date = start_date + timedelta(minutes=duration_in_minutes)
    print("calculated end date : {}".format(end_date))

if __name__ == "__main__":
    main()
