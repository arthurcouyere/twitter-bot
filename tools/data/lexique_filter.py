#!/usbin/bin/env python3
import re
import logging
from pathlib import Path
import csv
from tqdm import tqdm

"""
Import du lexique récupéré depuis https://github.com/WhiteFangs/BotDuCul
et converti en csv (depuis le "INSERT INTO" mysql)
"""

#################################
# config
#################################

input_file = "lexique.csv"
output_file = "lexique.txt"

# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#################################
# main
#################################

def main():
    script_dir = Path(__file__).resolve().parent
    words_file = script_dir / Path(input_file)
    words_filtered_file = script_dir / Path(output_file)

    # count csv rows
    logging.info("loading csv words file : {}".format(str(words_file)))
    with open(str(words_file), encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile)
        row_count = sum(1 for row in csvreader)

    # parse csv file
    logging.info("parsing words")
    words = {}
    with open(str(words_file), encoding="utf8") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in tqdm(csvreader, total=row_count, desc="filtering words"):
            word = row["ortho"]

            if word not in words.keys() and (
                (row["cgram"] == "NOM" and row["nombre"] in ["",  "s"]) or
                (row["cgram"] == "ADJ" and row["nombre"] in ["",  "s"] and row["genre"] in ["",  "m", "f"]) or
                (row["cgram"] == "VER" and row["infover"] in ["inf"]) or
                (row["cgram"] == "ADV")
            ):
                words[word] = 1;

    logging.info("writing words to file {}".format(str(words_filtered_file)))
    with open(str(words_filtered_file), "w", encoding="utf8") as f:
        for word in words.keys():
            f.write("{}\n".format(word))
    
if __name__ == "__main__":
    main()