import csv
import json
import os
# from pprint import pprint
# from multiprocessing import Pool
from fuzzywuzzy import process
# from datetime import datetime
from find_job_titles import FinderPyaho
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher
# from multi_rake import Rake
from difflib import SequenceMatcher


def job_title_finder(finder, raw_position, ad_text):
    jobs_found = finder.findall(raw_position.title())
    if jobs_found:
        jobs = []
        for j in jobs_found:
            jobs.append(j.match)
        if len(jobs) > 1:
            if 'consultant' in jobs[0].lower():
                position = jobs[len(jobs) - 1].lower().strip()
            else:
                jobs_found_in_body = finder.findall(ad_text.title())
                if jobs_found_in_body:
                    jobs_in_body = []
                    occurrences = {}
                    job_match = False
                    for j in jobs_found_in_body:
                        jobs_in_body.append(j.match)
                    unique_jobs = set(jobs_in_body)
                    for job in jobs:
                        if job in unique_jobs:
                            job_match = True
                            occurrences[job] = jobs_in_body.count(job)
                    if job_match is False:
                        position = jobs[len(jobs) - 1].lower().strip()
                    else:
                        position = max(occurrences, key=occurrences.get)
                else:
                    position = jobs[len(jobs) - 1].lower().strip()
        else:
            position = jobs[len(jobs) - 1].lower().strip()
    else:
        jobs_in_body_found = finder.findall(ad_text.title())

        if jobs_in_body_found:
            position = jobs_in_body_found[0].match.lower().strip()
        else:
            position = None

    return position


def position_templates_exact_match_check(text, list_of_template_titles):
    position = None
    # print("list_of_template_titles", list_of_template_titles)
    for template_title in list_of_template_titles:
        if text.strip().lower() == template_title.strip().lower():
            position = template_title.strip().lower()
            break

    return position


def curated_lookup_csv_exact_match_check(text, lookup_list):
    position = None

    for pair in lookup_list:
        if text.lower().strip() == pair[0].lower().strip():
            position = pair[1]

    return position


def position_lookup_similar(position, positions_list, resolved_list, positions_searcher, fuzzy_process,
                            list_of_position_titles_with_templates):
    position_cleaned = position.lower().strip()
    if position_cleaned in list_of_position_titles_with_templates:
        return position_cleaned, None
    elif position_cleaned in resolved_list:
        position_index = resolved_list.index(position_cleaned)
        return position_cleaned, position_index
    elif position_cleaned in positions_list:
        position_index = positions_list.index(position_cleaned)
        resolved_position = resolved_list[position_index]
        return resolved_position, position_index
    else:
        position_found = positions_searcher.search(position_cleaned, 0.60)
        if position_found:
            if len(position_found) > 1:
                position_found = fuzzy_process.extractOne(position_cleaned, position_found)
                position_found = position_found[0]
            else:
                position_found = position_found[0]
            position_index = positions_list.index(position_found)
            resolved_position = resolved_list[position_index]
            return resolved_position, position_index
        else:
            return None, None


def get_reconciled_position_index(position, positions_list, resolved_list, positions_searcher, fuzzy_process):
    position_cleaned = position.lower().strip()
    if position_cleaned in positions_list:
        position_index = positions_list.index(position_cleaned)
        return position_index
    else:
        position_found = positions_searcher.search(position_cleaned, 0.60)
        if position_found:
            if len(position_found) > 1:
                position_found = fuzzy_process.extractOne(position_cleaned, position_found)
                position_found = position_found[0]
            else:
                position_found = position_found[0]
            position_index = positions_list.index(position_found)
            return position_index
        else:
            return None


def keyword_match(position, positions_list, resolved_list):
    raw_position_as_keywords = position.split(' ')
    # print(raw_position_as_keywords)
    possible_positions = []

    for position_l in positions_list:
        position_keywords = position_l.split(' ')
        match = 0
        for word in raw_position_as_keywords:
            for pword in position_keywords:
                if word.lower().strip() == pword.lower().strip():
                    match += 1

        if match >= 2:
            possible_positions.append([position_l, match])

    # print("possible_positions", possible_positions)
    if possible_positions:
        best_score = ['', 0]
        for i in possible_positions:
            if i[1] > best_score[1]:
                best_score = [i[0], i[1]]
        # print(best_score)

        position_cleaned = best_score[0].lower().strip()
        if position_cleaned in positions_list:
            position_index = positions_list.index(position_cleaned)
            resolved_position = resolved_list[position_index]
            return resolved_position
    else:
        return None


def match_sequence(position, positions_list, resolved_list):
    highest_score = ['', 0]
    for i in positions_list:
        score = SequenceMatcher(None, position, i).ratio()
        if score > highest_score[1]:
            highest_score = [i, score]
            if highest_score[1] >= 0.5:
                break

    position_cleaned = highest_score[0].lower().strip()

    if position_cleaned in positions_list:
        position_index = positions_list.index(position_cleaned)
        resolved_position = resolved_list[position_index]
        return resolved_position
    else:
        return None


def reconcile_position_flow(
        position,
        finder,
        list_of_position_titles_with_templates,
        curated_lookup_list,
        positions_list,
        resolved_list,
        positions_searcher,
        fuzzy_process,
        job_description):
    cleaned_position = position.lower().strip()

    status = "NO MATCH"

    found_jobtitlefinder_match_title = job_title_finder(finder, cleaned_position, job_description)

    # finds title in raw position then job desc - job_title_finder
    if found_jobtitlefinder_match_title:

        found_similar, found_index = position_lookup_similar(
            position=found_jobtitlefinder_match_title,
            positions_list=positions_list,
            resolved_list=resolved_list,
            positions_searcher=positions_searcher,
            fuzzy_process=fuzzy_process,
            list_of_position_titles_with_templates=list_of_position_titles_with_templates
        )
        print('found_similar:')
        print(found_similar)
        if found_similar and found_index is None:
            status = "EXACT MATCH"
            print(found_similar)
            print(status)
            return found_jobtitlefinder_match_title, found_similar.lower(), found_index, status
        elif found_similar:
            status = "SIMILAR MATCH"
            print(found_similar)
            print(status)
            return found_jobtitlefinder_match_title, found_similar.lower(), found_index, status
        else:
            pass

    # found_jobtitlefinder_match_description = job_title_finder(finder, cleaned_position, job_description)
    #
    # if found_jobtitlefinder_match_description:
    #
    #     found_similar, found_index = position_lookup_similar(
    #         position=found_jobtitlefinder_match_description,
    #         positions_list=positions_list,
    #         resolved_list=resolved_list,
    #         positions_searcher=positions_searcher,
    #         fuzzy_process=fuzzy_process,
    #         list_of_position_titles_with_templates=list_of_position_titles_with_templates
    #     )
    #
    #     if found_similar:
    #         status = "SIMILAR MATCH"
    #         return found_jobtitlefinder_match_title, found_similar.lower(), found_index, status
    #     else:
    #         pass

    # 2nd try job description - choose first item!

    found_exact_match = position_templates_exact_match_check(cleaned_position, list_of_position_titles_with_templates)

    if found_exact_match:

        position_index = get_reconciled_position_index(
            position=found_exact_match,
            positions_list=positions_list,
            resolved_list=resolved_list,
            positions_searcher=positions_searcher,
            fuzzy_process=fuzzy_process,
        )

        status = "EXACT MATCH"
        return found_jobtitlefinder_match_title, found_exact_match.lower(), position_index, status
    else:
        pass

    found_lookup_match = curated_lookup_csv_exact_match_check(cleaned_position, curated_lookup_list)

    if found_lookup_match:

        position_index = get_reconciled_position_index(
            position=found_lookup_match,
            positions_list=positions_list,
            resolved_list=resolved_list,
            positions_searcher=positions_searcher,
            fuzzy_process=fuzzy_process,
        )

        status = "CURATED LOOKUP MATCH"
        return found_jobtitlefinder_match_title, found_lookup_match.lower(), position_index, status
    else:
        pass

    found_similar, position_index = position_lookup_similar(
        position=cleaned_position,
        positions_list=positions_list,
        resolved_list=resolved_list,
        positions_searcher=positions_searcher,
        fuzzy_process=fuzzy_process,
        list_of_position_titles_with_templates=list_of_position_titles_with_templates
    )

    if found_similar:
        status = "SIMILAR MATCH"
        return found_jobtitlefinder_match_title, found_similar.lower(), position_index, status
    else:
        pass

    found_keyword_match = keyword_match(cleaned_position, positions_list, resolved_list)

    if found_keyword_match:

        position_index = get_reconciled_position_index(
            position=found_keyword_match,
            positions_list=positions_list,
            resolved_list=resolved_list,
            positions_searcher=positions_searcher,
            fuzzy_process=fuzzy_process,
        )

        status = "KEYWORD MATCH"
        return found_jobtitlefinder_match_title, found_keyword_match.lower(), position_index, status
    else:
        pass

    found_sequence_match = match_sequence(cleaned_position, positions_list, resolved_list)

    if found_sequence_match:

        position_index = get_reconciled_position_index(
            position=found_sequence_match,
            positions_list=positions_list,
            resolved_list=resolved_list,
            positions_searcher=positions_searcher,
            fuzzy_process=fuzzy_process,
        )

        status = "SEQUENCE MATCH"
        return found_jobtitlefinder_match_title, found_sequence_match.lower(), position_index, status
    else:
        return None, None, status


if __name__ == '__main__':

    list_of_positions_from_template_database = []

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'modules/cover_letter_v2/templates/cover_letter_sentences_v12_uk.json'),
              'r') as cv_templates:
        cover_letter_templates = json.load(cv_templates)

        for k, v in cover_letter_templates.items():
            list_of_positions_from_template_database.append(k)

    position_reconciler_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            'modules/cover_letter_v2/positions_reconciler_v2.tsv')

    positions_db = DictDatabase(CharacterNgramFeatureExtractor(3))
    positions_searcher = Searcher(positions_db, CosineMeasure())

    positions_list = []
    resolved_list = []

    with open(position_reconciler_file, 'r') as r:
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

    lookup_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'modules/cover_letter_v2/positions_lookup.csv')
    lookup_list = []

    with open(lookup_csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lookup_list.append([
                row['raw_position'].strip().lower(), row['reconciled_position'].strip().lower()
            ])

    finder = FinderPyaho()

    test_positions = [
        'Software Developer in Melbourne, Australia',
        'Software Developer',
        'software developer',
        'Java Developer',
        'Donkey trainer',
        'Horse trainer',
        'Graduate Software Development and Engineering',
        'Junior Software Engineer',
        'Graduate Front End Developer',
        'Web Developer',
        'Junior Web Developer/Content Publisher',
        'Junior Software Developer',
        'SaaS Software Developer - Graduate',
        'Software Developer',
        'Associate Software Developer',
        'Web Developer (React.js)',
        'Junior Web Developer - Full time - Preston VIC',
    ]

    counter = 0
    total = len(test_positions)
    score = total
    job_desc = 'test'
    for tp in test_positions:
        position_found_by_job_title_finder, position, position_index, status = reconcile_position_flow(
            tp,
            finder,
            list_of_positions_from_template_database,
            lookup_list,
            positions_list,
            resolved_list,
            positions_searcher,
            process,
            job_desc
        )
        if not position:
            score -= 1

        counter += 1

        print(str(counter), ": ", tp, " became ", position, ". Status: ", status)

    print(score, " out of ", total)
    print(round((score / total) * 100), "% reconciled.")
