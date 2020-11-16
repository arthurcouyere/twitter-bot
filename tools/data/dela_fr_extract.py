#!/usbin/bin/env python3
import re
import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from tqdm import tqdm

"""
Extrait les noms depuis le dictionnaire xml
récupéré depuis https://infolingu.univ-mlv.fr/DonneesLinguistiques/Dictionnaires/telechargement.html

"""

#################################
# config
#################################

input_file = "dela-fr-public-u8.dic.xml"
ouput_file = "nouns.txt"

# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#################################
# main
#################################

def main():
    script_dir = Path(__file__).resolve().parent
    words_file = script_dir / Path(input_file)

    pattern = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ]+$")

    nouns_file = script_dir / Path(ouput_file)
    with open(str(nouns_file), "w") as f:
        logging.info("loading xml file : {}".format(str(nouns_file)))
        tree = ET.parse(str(words_file))
        root = tree.getroot()

        logging.info("extracting nouns")
        for child in root:
            if child.tag == "entry":
                for elem in child.findall("pos"):
                    if elem.attrib["name"] == "noun":
                        for elem in child.findall("inflected"):
                            for form in elem.findall("form"):
                                noun = form.text
                                if pattern.match(noun):
                                    f.write("{}\n".format(noun))
    
if __name__ == "__main__":
    main()