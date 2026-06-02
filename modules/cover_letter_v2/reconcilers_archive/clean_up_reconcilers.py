import csv
import json
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher

positions_db = DictDatabase(CharacterNgramFeatureExtractor(3))
position_searcher = Searcher(positions_db, CosineMeasure())

file1 = 'positions_reconciler.tsv' # left side titles are cover letter titles

file2 = 'positions_lookup (4).csv' # right side titles are cover letter titles

cover_letter_titles = []

raw_positions_from_file1_and_file2 = []

template_json_file = 'templates/cover_letter_sentences_v12_uk.json'

job_title_finder_positions = []

title_finder_file = 'titles_combined 4.txt'

with open(template_json_file, 'r') as cv_templates:
    cover_letter_templates = json.load(cv_templates)


for title, val in cover_letter_templates.items():
    cover_letter_titles.append(title.lower())

file1_reconciler = []
file2_reconciler = []

file1_positions = []
file2_positions = []

raw_positions = []

with open(file1, 'r') as r1:
    reader = csv.reader(r1, delimiter='\t')
    for row in reader:
        position = row[1].strip('\n').lower()
        reconciled = row[0].strip('\n').lower()
        if reconciled in cover_letter_titles:
            file1_reconciler.append([position, reconciled])
            file1_positions.append(position)
            positions_db.add(position.lower())
            raw_positions_from_file1_and_file2.append(position)

with open(file2, 'r') as r2:
    for row in r2:
        split = row.split(',')
        position = split[0].strip('\n').lower()
        reconciled = split[1].strip('\n').lower()
        if reconciled in cover_letter_templates:
            file2_reconciler.append([position, reconciled])
            file2_positions.append(position)
            positions_db.add(position.lower())
            raw_positions_from_file1_and_file2.append(position)

updated_reconciler = file1_reconciler + file2_reconciler

with open(title_finder_file, 'r') as title_finder_file:
    for row in title_finder_file:
        position = row.strip('\n').lower()
        if position not in raw_positions_from_file1_and_file2:
            position_found = position_searcher.search(position, 0.80)
            if position_found:
                position_found = position_found[0]
                if position_found.lower() in file1_positions:
                    index = file1_positions.index(position_found.lower())
                    position_and_reconciled = file1_reconciler[index]
                    updated_reconciler.append(position_and_reconciled)
                elif position_found.lower() in file2_positions:
                    index = file2_positions.index(position_found.lower())
                    position_and_reconciled = file2_reconciler[index]
                    updated_reconciler.append(position_and_reconciled)


with open('positions_reconciler_v2.tsv', 'w') as w:
    for item in updated_reconciler:
        position = item[0]
        reconciled = item[1]
        w.write(reconciled + '\t' + position + '\n')