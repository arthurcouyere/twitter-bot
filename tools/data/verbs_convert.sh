#!/bin/bash
wget https://github.com/Einenlum/french-verbs-list/raw/master/verbs.json
cat verbs.json | jq -r ".verbs[][]" > verbs.txt