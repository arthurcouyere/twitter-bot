import argparse
import logging
from pathlib import Path
from typing import Tuple
from tqdm import tqdm
import mlconjug3

#################################
# config
#################################

# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#################################
# main
#################################

class VerbConjugator():
    """
    Conjugates a verb at differents moods (default=all)
    """

    def __init__(self, lang="fr") -> None:
        self.conjugator = mlconjug3.Conjugator(language=lang)

    def conjugate_verb(self, verb:str, moods:Tuple[str]=None) -> Tuple[str]:

        if not self.conjugator.conjug_manager.is_valid_verb(verb):
            return None

        conjugated_list = []
        try:
            conjugated_verb = self.conjugator.conjugate(verb)
            if conjugated_verb == None:
                return None

            for conjugate_form in conjugated_verb.iterate():
                conjugated = conjugate_form[-1]
                if conjugated != verb and conjugated not in conjugated_list:
                    mood = conjugate_form[0]
                    if (moods == None) or (moods != None and (mood in moods)):
                        conjugated_list.append(conjugated)

            return conjugated_list

        except:
            return None

def main():

    # args
    parser = argparse.ArgumentParser(description='list tweets from Twitter API')
    parser.add_argument('-v', '--verbose',  action='store_true', help="verbose mode")
    args = parser.parse_args()
    logging.debug(args)

    script_dir = Path(__file__).resolve().parent

    # load verbs
    print("loading verbs")
    verbs_file = script_dir / Path("data/verbs.txt")
    with open(str(verbs_file), "r") as f:
        verbs = [line.rstrip() for line in f]

    # load nouns
    print("loading nouns")
    nouns_file = script_dir / Path("data/nouns.txt")
    with open(str(nouns_file), "r") as f:
        nouns = [line.rstrip() for line in f]

    # conjugate verbs
    print("conjugating verbs")
    conjugator = VerbConjugator("fr")
    moods = ['Indicatif', 'Conditionnel', 'Subjonctif']
    conjugated_verbs = []
    not_conjugated_verbs = []
    for verb in tqdm(verbs):
        conjugated_list = conjugator.conjugate_verb(verb, moods)
        if conjugated_list != None:
            conjugated_verbs += conjugated_list
        else:
            not_conjugated_verbs.append(verb)

    if len(not_conjugated_verbs) > 0:
        logging.warning("warning : could not conjugate following verbs: {}".format(", ".join(not_conjugated_verbs)))

    # load words
    print("loading words")
    words_file = script_dir / Path("../data/words.txt")
    with open(str(words_file), "r") as f:
        words = [line.rstrip() for line in f]
        
    # process words
    print("filtering words")
    words_filtered = []
    words_filtered_file = script_dir / Path("../data/words_filtered.txt")
    with open(str(words_filtered_file), "w") as f:
        for word in tqdm(words):
            if (word not in conjugated_verbs) or (word in nouns):
                f.write("{}\n".format(word))

    print("#%s words found" % len(words))


if __name__ == "__main__":
    main()
