import csv
import os
import csv
import json
import os
from pprint import pprint
from multiprocessing import Pool
from fuzzywuzzy import process
from datetime import datetime
from find_job_titles import FinderPyaho
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher
from multi_rake import Rake
from difflib import SequenceMatcher
templates_path = r"C:\Users\danny\Documents\Programming\docgen_api\modules\cover_letter_v2\templates\cover_letter_sentences_v12_uk.json"
positions_path = r"C:\Users\danny\Documents\Programming\docgen_api\modules\cover_letter_v2\positions_reconciler_v2.tsv"
positions_list = []
resolved_list = []
positions_db = DictDatabase(CharacterNgramFeatureExtractor(3))
positions_searcher = Searcher(positions_db, CosineMeasure())
with open(positions_path, 'r') as r:
    reader = csv.reader(r, delimiter='\t')
    for ind, row in enumerate(reader):
        resolved_list.append(row[0].strip('\n'))
        try:
            positions_list.append(row[1].strip('\n'))
        except:
            print(row[0])
            print(ind - 1)
        try:
            positions_db.add(row[1].strip('\n'))
        except:
            print(row[0])
            print(ind - 1)


with open(templates_path) as file:
    data = json.load(file)

positions_with_templates = []
# pprint(data)
for k, v in data.items():
    print(k)
    positions_with_templates.append(k.lower().strip())

# print(len(positions_with_templates))

missing_positions = []
reconciled_positions = []

for position in resolved_list:
    if position.lower().strip() in positions_with_templates:
        reconciled_positions.append(position)
    else:
        missing_positions.append(position)

print("missing_positions: ",len(missing_positions))
print("reconciled_positions: ",len(reconciled_positions))