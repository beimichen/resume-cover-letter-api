import csv
import json
import os
from pprint import pprint
# from multiprocessing import Pool
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, jsonify, make_response
# from flask_restful import Api, Resource, reqparse
import logging
from flask_restx import Resource, Api, reqparse
import html2text
from flask_sqlalchemy import SQLAlchemy

from modules.cover_letter_v2.cover_letter_generator import CoverLetterCreator
from datetime import datetime

from modules.cover_letter_v2.cover_letter_html import create_cv_html
from modules.cover_letter_v2.default_cover_letter_generator import generate_default_coverletter
from modules.cover_letter_v2.skill_lookups import extract_skills_from_text
from find_job_titles import FinderPyaho

from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher
from multi_rake import Rake
from fuzzywuzzy import process

from modules.stylize_resume.pdf_generation_resume import default_template_resume_pdf
from position_reconciler import reconcile_position_flow, job_title_finder

# from playsound import playsound

import logging
import sys

# log = open("docgen_errors.log", "a")
# sys.stdout = log

print("Initation begin")
print("--------")

print("1 INITIATE: Jobtitle finder")
finder = FinderPyaho()

print("2 INITIATE: Flask App")
latest_chrome_app_version = "0.0.4"
force_users_to_update = False
force_update_message = "Hi! We have recently updated DocGen, and require all users to update to the latest version of our app. " \
                       "We're always making improvements and trying to make applying for jobs the best possible experience for you. Thanks for your continued support and feedback!"
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
parser = reqparse.RequestParser()

print("3 INITIATE: Flask App")
# logging.basicConfig(level=logging.INFO)
name_space_1 = api.namespace('api/v1', description='resume & cover letter api v1')

# Instantiate files & lookups for cover letter generator

print("4 INITIATE: Position database")

list_of_positions_from_template_database = []

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'modules/cover_letter_v2/templates/cover_letter_sentences_v12_uk.json'), 'r') as cv_templates:
    cover_letter_templates = json.load(cv_templates)

    for k, v in cover_letter_templates.items():
        list_of_positions_from_template_database.append(k.lower().strip())

print("5 INITIATE: Coverletter Template database")
# coverletter templates
template_json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'modules/cover_letter_v2/templates/cover_letter_sentences_v12_uk.json')

with open(template_json_file, 'r') as cv_templates:
    cover_letter_templates = json.load(cv_templates)

# default coverletter templates
########### generic_body_pre_bullet_point_sentences

generic_body_pre_bullet_point_sentences = []

generic_body_pre_bullet_point_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                            'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(generic_body_pre_bullet_point_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        generic_body_pre_bullet_point_sentences.append(row[0])

########### generic_closing_intro_sentences
generic_closing_intro_sentences = []

generic_closing_intro_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(generic_closing_intro_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        generic_closing_intro_sentences.append(row[0])

########### generic_closing_outro_sentences
generic_closing_outro_sentences = []

generic_closing_outro_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(generic_closing_outro_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        generic_closing_outro_sentences.append(row[0])

########### generic_followup_outro_sentences
generic_followup_outro_sentences = []
generic_followup_outro_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                     'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(generic_followup_outro_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        generic_followup_outro_sentences.append(row[0])

########### generic_intro_education_sentences
generic_intro_education_sentences = []
generic_intro_education_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(generic_intro_education_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        generic_intro_education_sentences.append(row[0])
###########  generic_intro_followup_sentences
generic_intro_followup_sentences = []
generic_intro_followup_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                     'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(generic_intro_followup_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        generic_intro_followup_sentences.append(row[0])
########### generic_intro_opening_sentences
generic_intro_opening_sentences = []
generic_intro_opening_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(generic_intro_opening_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        generic_intro_opening_sentences.append(row[0])
###########  generic_opening_outro_sentences
generic_opening_outro_sentences = []
generic_opening_outro_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(generic_opening_outro_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        generic_opening_outro_sentences.append(row[0])
########### insert_skills_ability_type_sentences
insert_skills_ability_type_sentences = []
insert_skills_ability_type_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(insert_skills_ability_type_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        insert_skills_ability_type_sentences.append(row[0])
########### insert_skills_knowledge_type_sentences
insert_skills_knowledge_type_sentences = []
insert_skills_knowledge_type_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                           'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(insert_skills_knowledge_type_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        insert_skills_knowledge_type_sentences.append(row[0])
###########  position_specific_generic_discrete_intro_sentences
position_specific_generic_discrete_intro_sentences = []
position_specific_generic_discrete_intro_sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                       'modules/cover_letter_v2/generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

with open(position_specific_generic_discrete_intro_sentences_file, encoding="utf-8") as tsv_file:
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        position_specific_generic_discrete_intro_sentences.append(row[0])

print("6 INITIATE: Generic Sentences")
# generic sentences
file1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'modules/cover_letter_v2/generic_sentences/insert_skills_ability_type_sentences.csv')
file2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'modules/cover_letter_v2/generic_sentences/insert_skills_knowledge_type_sentences.csv')

generic_ability_type_sentences = []
generic_knowledge_type_sentences = []

with open(file1, 'r') as r1:
    for row in r1:
        generic_ability_type_sentences.append(row.strip('\n'))

with open(file2, 'r') as r2:
    for row in r2:
        generic_knowledge_type_sentences.append(row.strip('\n'))

print("7 INITIATE: Skills")
# SKILL LOOKUPS
rake = Rake()
skills_db = DictDatabase(CharacterNgramFeatureExtractor(3))
skills_db2 = DictDatabase(CharacterNgramFeatureExtractor(3))
skill_searcher = Searcher(skills_db, CosineMeasure())
skill_searcher2 = Searcher(skills_db2, CosineMeasure())
skills_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules/cover_letter_v2/skills_normalizer.tsv')
skills_file2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules/cover_letter_v2/hard_skills.tsv')
skills_cat_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'modules/cover_letter_v2/skills_categorization.tsv')
template_json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'modules/cover_letter_v2/templates/cover_letter_sentences_v12_uk.json')

print(skills_file)
skill_entities = []
skill_normalizer = []

with open(skills_file, 'r', encoding='utf-8-sig') as h_skills:
    reader = csv.reader(h_skills, delimiter='\t')
    for row in reader:
        skill_entities.append(row[0].strip('\n').lower())
        skill_normalizer.append(row[1].strip('\n').lower())
        skills_db.add(row[0].strip('\n').lower())

with open(skills_file2, 'r', encoding='utf-8-sig') as h_skills2:
    for row in h_skills2:
        skills_db2.add(row.strip().strip('\n').lower())

skill_categories = []
skill_cat_types = []

with open(skills_cat_file, 'r', encoding='utf-8-sig') as skills_cat:
    reader = csv.reader(skills_cat, delimiter='\t')
    for row in reader:
        skill_categories.append(row[1].lower())
        skill_cat_types.append(row[2].lower())

with open(template_json_file, 'r') as cv_templates:
    cover_letter_templates = json.load(cv_templates)

print("7 INITIATE: Position Reconciler")
# POSITION RECONCILER
position_reconciler_file = 'modules/cover_letter_v2/positions_reconciler_v2.tsv'

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

print("INITIALISATION COMPLETE")


# END

# user model for business partners (later!)
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # all values unique
    name = db.Column(db.String(100), nullable=False)  # must have information
    email = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User(name = {name}, email = {email}"


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/apply")
def apply():
    return render_template('apply.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@app.route("/register")
def register():
    return render_template('dashboard.html')


@app.route("/login")
def login():
    return render_template('dashboard.html')


@api.route('/hello-world')
class HelloWorld(Resource):

    def get(self):
        return "Welcome to the Resume & Cover Letter API Sandbox."

    def post(self):
        data = api.payload
        print(data)
        # json = request.get_json()
        return jsonify({'response': data})


@api.route('/settings')
class HelloWorld(Resource):

    def get(self):
        return "Welcome to the Resume & Cover Letter API Sandbox."

    def post(self):
        data = api.payload
        print(data)
        if data['key'] == 'h3&8s92jf^&@#0hf78d6s987df987sd3^^&*^@)*&^@df876sdfbahb78cw786kmznxcbq0p':
            data = {
                "min_sleep_time": 5
            }
            return jsonify({'response': data})
        else:
            return 500


def convert_resume_doc_to_parsed(resume_file_link):
    # TODO: add resume doc / docx parsing here
    pass


def extract_skills_from_resume(parsed_resume):
    resume = json.loads(parsed_resume, indent=4)
    skills = resume['skills']
    tools = resume['tools']
    return skills + tools


def get_job_match_for_api(searched_skills=None,
                          raw_job_title=None,
                          job_ad_description=None,
                          list_of_position_titles_with_templates=None,
                          fuzzy_process=None,
                          parsed_resume=None,
                          resume_file_link=None,
                          pre_compiled_coverletter=None,
                          hash_id=None,
                          source_url=None,
                          ):
    if raw_job_title:

        unprocessed_job_title_found = job_title_finder(finder, raw_job_title, job_ad_description)

        position_found_by_job_title_finder, reconciled_job_title, position_index, status = reconcile_position_flow(
            position=raw_job_title.lower().strip(),
            finder=finder,
            list_of_position_titles_with_templates=list_of_position_titles_with_templates,
            curated_lookup_list=lookup_list,
            positions_list=positions_list,
            resolved_list=resolved_list,
            positions_searcher=positions_searcher,
            fuzzy_process=fuzzy_process,
            job_description=job_ad_description
        )
        if unprocessed_job_title_found:
            position_found_by_job_title_finder = unprocessed_job_title_found
        else:
            position_found_by_job_title_finder = position_found_by_job_title_finder
        print('job title found:')
        print(position_found_by_job_title_finder)
        print('reconciled:')
        print(reconciled_job_title)

    else:
        position_found_by_job_title_finder = None
        reconciled_job_title = None
        position_index = None

    if parsed_resume:
        resume = parsed_resume

    elif resume_file_link:
        resume = convert_resume_doc_to_parsed(resume_file_link)
        # for now, convert doc can create a json object in same format as parsed resume -
        # it will only extract skills and fill skills field. in future when we can extract more fields
        # accurately we can add. this way we keep resume objects uniform

    else:
        resume = None

    if reconciled_job_title:

        inserted_position = position_found_by_job_title_finder

        job_match_obj = CoverLetterCreator(
            reconciled_position=reconciled_job_title,
            raw_position=raw_job_title,
            insertable_position=position_found_by_job_title_finder,
            user_name=None,
            employer_name=None,
            company_name=None,
            ad_text=job_ad_description,
            resume=resume,
            searched_skills=searched_skills,
            cover_letter_templates=cover_letter_templates,
            generic_ability_type_sentences=generic_ability_type_sentences,
            generic_knowledge_type_sentences=generic_knowledge_type_sentences,
            pre_compiled_coverletter=pre_compiled_coverletter
        )
        print("job_match_obj: ",job_match_obj)

        try:
            intersecting_skills, aggregate_users_skills_list, skills_extracted_from_ad, topics_of_interest_extracted_from_ad = job_match_obj.job_ad_text_match_skills(
                skill_searcher,
                skill_searcher2,
                rake,
                generic_ability_type_sentences,
                generic_knowledge_type_sentences,
                skill_entities,
                skill_normalizer,
                skill_categories,
                skill_cat_types
            )
        except:
            skills_extracted_from_ad = []
            topics_of_interest_extracted_from_ad = []
            aggregate_users_skills_list = []
            intersecting_skills = None

        if aggregate_users_skills_list:
            aggregate_users_skills_list = list(set(aggregate_users_skills_list))

    else:
        skills_extracted_from_ad = []
        topics_of_interest_extracted_from_ad = []
        aggregate_users_skills_list = []
        intersecting_skills = None

    print('intersecting skills')
    print(intersecting_skills)

    if intersecting_skills and searched_skills:
        matched_skills, number_skills_matched, match_score = job_matching(reconciled_job_title,
                                                                          aggregate_users_skills_list,
                                                                          searched_skills,
                                                                          intersecting_skills)
    elif intersecting_skills and resume['skills']:
        searched_skills = resume['skills']
        matched_skills, number_skills_matched, match_score = job_matching(reconciled_job_title,
                                                                          aggregate_users_skills_list,
                                                                          searched_skills,
                                                                          intersecting_skills)
    else:
        matched_skills = []
        number_skills_matched = 0
        match_score = 1

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    response_data = {
        "timestamp": timestamp,
        "skills_extracted_from_ad": skills_extracted_from_ad,
        "topics_of_interest_extracted_from_ad": topics_of_interest_extracted_from_ad,
        "matched_skills": matched_skills,  # returns empty list if none matched
        "match_score": match_score,
        "number_matched": number_skills_matched,
        "hash_id": hash_id,
        "source_url": source_url,
    }

    return response_data


def job_matching(reconciled_position, aggregate_users_skills_list, searched_skills, intersecting_skills):
    # TODO: Later extend this to include VERY similar skills - maybe if users want that. they may prefer
    #  exact match only. or we give them option to include similar skills in the match.

    number_matched = len(intersecting_skills)

    # Job Match Score

    """     
    3 levels - Green, Yellow, and Red

    if the skill is found in the position title - then Green
    if no matched skills - red
    if only 1 searched skill - only either red or green
    if 2 searched skills - 2 found = green, 1 found = yellow , zero found = red
    if 3-4 searched skills - >2 found = green, 1 found = yellow , zero found = red
    if 5 > searched skills - >3 found = green, 1 found = yellow , zero found = red

    dont discriminate between soft and hard


    etc.
    user search > 5 - then match 3 or above - green.


    """

    number_of_skills_to_match = len(searched_skills)

    golden_match = False

    for skill in intersecting_skills:
        # TODO: should we be checking the raw position instead of reconciled? to avoid mis-matches.
        # example if facebook designer resolves to social media designer, and user searches for facebook as a skill
        if skill in reconciled_position:
            golden_match = True

    # if searched skill is actually in the position title
    if golden_match:
        match_score = 3

    elif number_matched == 0:
        match_score = 1

    # 1 searched skill
    elif number_of_skills_to_match == 1 and number_matched >= 1:
        match_score = 3

    # 2 searched skills
    elif number_of_skills_to_match == 2 and number_matched == 1:
        match_score = 2

    elif number_of_skills_to_match == 2 and number_matched > 1:
        match_score = 3

    # above 3

    elif number_of_skills_to_match >= 3 and number_of_skills_to_match < 5 and number_matched == 1:
        match_score = 2

    elif number_of_skills_to_match >= 3 and number_of_skills_to_match < 5 and number_matched > 1:
        match_score = 3

    # 5 and above

    elif number_of_skills_to_match >= 5 and number_matched > 2:
        match_score = 3

    elif number_of_skills_to_match >= 5 and number_matched >= 1 and number_matched <= 2:
        match_score = 2

    else:
        match_score = 1

    print("intersecting_skills: ", intersecting_skills)
    print("number_matched: ", number_matched)
    print("match_score: ", match_score)
    return intersecting_skills, number_matched, match_score


def create_cover_letter_and_job_match_for_api(
        candidate_name=None,
        parsed_resume=None,
        resume_file_link=None,
        hiring_manager_name=None,
        raw_job_title=None,
        job_ad_description=None,
        company_name=None,
        hash_id=None,
        source_url=None,
        searched_skills=None,
        include_resume_skills_in_match=None,
        list_of_position_titles_with_templates=None,
        fuzzy_process=None,
        pre_compiled_coverletter=None

):
    if raw_job_title:

        unprocessed_job_title_found = job_title_finder(finder, raw_job_title, job_ad_description)

        position_found_by_job_title_finder, reconciled_job_title, position_index, status = reconcile_position_flow(
            position=raw_job_title.lower().strip(),
            finder=finder,
            list_of_position_titles_with_templates=list_of_position_titles_with_templates,
            curated_lookup_list=lookup_list,
            positions_list=positions_list,
            resolved_list=resolved_list,
            positions_searcher=positions_searcher,
            fuzzy_process=fuzzy_process,
            job_description=job_ad_description
        )
        if unprocessed_job_title_found:
            position_found_by_job_title_finder = unprocessed_job_title_found
        else:
            position_found_by_job_title_finder = position_found_by_job_title_finder
        print('job title found:')
        print(position_found_by_job_title_finder)
        print('reconciled:')
        print(reconciled_job_title)

    else:
        position_found_by_job_title_finder = None
        reconciled_job_title = None
        position_index = None

    if parsed_resume:
        resume = parsed_resume

    elif resume_file_link:
        resume = convert_resume_doc_to_parsed(resume_file_link)
        # for now, convert doc can create a json object in same format as parsed resume -
        # it will only extract skills and fill skills field. in future when we can extract more fields
        # accurately we can add. this way we keep resume objects uniform

    else:
        resume = None

    if reconciled_job_title:
        print("reconciled")
        if not candidate_name:
            candidate_name = "[user_name]"

        inserted_position = position_found_by_job_title_finder
        cv = CoverLetterCreator(
            reconciled_position=reconciled_job_title,
            raw_position=raw_job_title,
            insertable_position=position_found_by_job_title_finder,
            user_name=candidate_name,
            employer_name=hiring_manager_name,
            company_name=company_name,
            ad_text=job_ad_description,
            resume=resume,
            searched_skills=searched_skills,
            cover_letter_templates=cover_letter_templates,
            generic_ability_type_sentences=generic_ability_type_sentences,
            generic_knowledge_type_sentences=generic_knowledge_type_sentences,
            pre_compiled_coverletter=pre_compiled_coverletter
        )
        try:
            template, \
            intersecting_knowledge_and_abilities, intersecting_skills, aggregate_users_skills_list, skills_extracted_from_ad, topics_of_interest_extracted_from_ad = cv.write_cover_letter(
                skill_searcher, skill_searcher2, rake,
                pre_compiled_coverletter,
                generic_ability_type_sentences,
                generic_knowledge_type_sentences,
                skill_entities,
                skill_normalizer,
                skill_categories,
                skill_cat_types
            )
        except:
            template = generate_default_coverletter(hiring_manager_name)
            html_template = None
            skills_extracted_from_ad = []
            full_html_template_with_inline_css = None
            topics_of_interest_extracted_from_ad = []
            aggregate_users_skills_list = []
            intersecting_skills = None
            intersecting_knowledge_and_abilities = None
            inserted_position = None

        if aggregate_users_skills_list:
            aggregate_users_skills_list = list(set(aggregate_users_skills_list))

        # intersecting_skills_dict:
        # {'abilities': abilities,
        #  'knowledge': knowledge}
    else:
        template = generate_default_coverletter(hiring_manager_name)
        html_template = None
        skills_extracted_from_ad = []
        full_html_template_with_inline_css = None
        topics_of_interest_extracted_from_ad = []
        aggregate_users_skills_list = []
        intersecting_skills = None
        intersecting_knowledge_and_abilities = None
        inserted_position = None

    print('intersecting skills')
    print(intersecting_skills)

    if intersecting_skills and searched_skills:
        matched_skills, number_skills_matched, match_score = job_matching(reconciled_job_title,
                                                                          aggregate_users_skills_list,
                                                                          searched_skills,
                                                                          intersecting_skills)
    elif intersecting_skills and resume['skills']:
        searched_skills = resume['skills']
        matched_skills, number_skills_matched, match_score = job_matching(reconciled_job_title,
                                                                          aggregate_users_skills_list,
                                                                          searched_skills,
                                                                          intersecting_skills)
    else:
        matched_skills = []
        match_score = 1

    now = datetime.now()
    timestamp = datetime.timestamp(now)

    # log data

    if template:
        template = template.splitlines()
        print('success creating template')
    else:
        if hiring_manager_name:
            template = generate_default_coverletter(hiring_manager_name)
        else:
            template = generate_default_coverletter(None)
        print('default template generated')

    response_data = {
        "timestamp": timestamp,
        "skills_extracted_from_ad": skills_extracted_from_ad,
        "topics_of_interest_extracted_from_ad": topics_of_interest_extracted_from_ad,
        "matched_skills": matched_skills,  # returns empty list if none matched
        "match_score": match_score,
        "coverletter_text": template,  # returns null if not coverletter not reconcilied
        "coverletter_html_no_styling": None,  # returns null if not coverletter not reconcilied
        "coverletter_html_full_styling": None,
        "raw_job_title": raw_job_title,
        "reconciled_job_title": reconciled_job_title,
        "reconciled_job_index": position_index,
        "company_name": company_name,
        # "job_ad": job_ad_description.splitlines(keepends=True),
        "hash_id": hash_id,
        "source_url": source_url,
        "position_inserted": inserted_position
    }

    return response_data


def convert_job_ad_description(job_ad_description):
    if type(job_ad_description) == list:
        output = ' '.join(job_ad_description)
    else:
        output = job_ad_description

    is_html = bool(BeautifulSoup(output, "html.parser").find())
    if is_html:
        output = html2text.html2text(job_ad_description)
    else:
        pass

    return output


@api.route('/create-job-application')
class CreateJobApplication(Resource):

    def get(self):
        return {'test': 'test'}

    def post(self):

        data = api.payload
        payload_type = type(data)

        if payload_type is str:
            data = json.loads(data)
        elif payload_type is dict:
            pass
        else:
            data = None

        # pprint(data, indent=4, width=1000)
        # print("TYPE is: ")
        # print(type(data))

        if data:
            print(data["chrome_app_version"])
            if data["chrome_app_version"] != latest_chrome_app_version and force_users_to_update:
                response_data = {
                    "force_update_message": "force_update_message"
                }
                return response_data, 402

            else:
                print("chrome app version CORRECT")
                # user info
                candidate_name = data['candidate_name']
                parsed_resume = data['parsed_resume']

                # name_space_1.logger.info(parsed_resume)
                resume_file_link = data['resume_file_link']

                # job info
                hiring_manager_name = data['hiring_manager_name']
                raw_job_title = data['raw_job_title']
                job_ad_description = data['job_ad_description']

                job_ad_description = convert_job_ad_description(job_ad_description)

                company_name = data['company_name']
                hash_id = data['hash_id']
                source_url = data['source_url']

                # job search
                searched_skills = data['searched_skills']
                include_resume_skills_in_match = data['include_resume_skills_in_match']  # Bool

                pre_compiled_coverletter = data['pre_compiled_coverletter']

                try:
                    response_data = create_cover_letter_and_job_match_for_api(
                        candidate_name=candidate_name,
                        parsed_resume=parsed_resume,
                        resume_file_link=resume_file_link,
                        hiring_manager_name=hiring_manager_name,
                        raw_job_title=raw_job_title,
                        job_ad_description=job_ad_description,
                        company_name=company_name,
                        hash_id=hash_id,
                        source_url=source_url,
                        searched_skills=searched_skills,
                        include_resume_skills_in_match=include_resume_skills_in_match,
                        list_of_position_titles_with_templates=list_of_positions_from_template_database,
                        fuzzy_process=process,
                        pre_compiled_coverletter=pre_compiled_coverletter
                    )

                    # print(response_data)
                    print("success creating cover letter")

                except Exception as e:
                    logging.debug(e)
                    print(e)
                    print("error")
                    response_data = {'error': 'no_cover_letter'}

                return response_data, 200
        else:
            return {
                       "message": "no data provided. check data is being sent as a json object in the body of the request - not as a url parameter"}, 409


@api.route('/job-match')
class GetJobMatch(Resource):

    def get(self):
        return {'test': 'test'}

    def post(self):

        data = api.payload
        payload_type = type(data)

        if payload_type is str:
            data = json.loads(data)
        elif payload_type is dict:
            pass
        else:
            data = None

        # pprint(data, indent=4, width=1000)
        # print("TYPE is: ")
        # print(type(data))

        # expected json fields:
        # "chrome_app_version"

        # get
        # reconciled_position, aggregate_users_skills_list, searched_skills, intersecting_skills

        # returns
        # matched_skills, number_skills_matched, match_score

        # job_matching(reconciled_position, aggregate_users_skills_list, searched_skills, intersecting_skills)

        if data:
            print(data["chrome_app_version"])
            if data["chrome_app_version"] != latest_chrome_app_version and force_users_to_update:
                response_data = {
                    "force_update_message": "force_update_message"
                }
                return response_data, 402

            else:
                print("chrome app version CORRECT")
                # user info
                # candidate_name = data['candidate_name']
                parsed_resume = data['parsed_resume']

                # name_space_1.logger.info(parsed_resume)
                resume_file_link = data['resume_file_link']

                # job info
                # hiring_manager_name = data['hiring_manager_name']
                raw_job_title = data['raw_job_title']
                job_ad_description = data['job_ad_description']

                job_ad_description = convert_job_ad_description(job_ad_description)
                print("job ad converted: ", job_ad_description)
                # company_name = data['company_name']
                hash_id = data['hash_id']
                source_url = data['source_url']

                # job search
                searched_skills = data['searched_skills']
                # include_resume_skills_in_match = data['include_resume_skills_in_match']  # Bool

                pre_compiled_coverletter = data['pre_compiled_coverletter']

                try:

                    response_data = get_job_match_for_api(searched_skills=searched_skills,
                                          raw_job_title=raw_job_title,
                                          job_ad_description=job_ad_description,
                                          list_of_position_titles_with_templates=list_of_positions_from_template_database,
                                          fuzzy_process=process,
                                          parsed_resume=parsed_resume,
                                          resume_file_link=resume_file_link,
                                          pre_compiled_coverletter=pre_compiled_coverletter,
                                          hash_id=hash_id,
                                          source_url=source_url,
                                          )

                    # print(response_data)
                    print("success creating cover letter")

                except Exception as e:
                    logging.debug(e)
                    print(e)
                    print("error")
                    response_data = {'error': 'no_cover_letter'}

                return response_data, 200
        else:
            return {
                       "message": "no data provided. check data is being sent as a json object in the body of the request - not as a url parameter"}, 409


@api.route('/coverletter_as_html')
class CoverletterHtml(Resource):

    def get(self):
        return {'test': 'test'}

    def post(self):

        data = api.payload
        payload_type = type(data)

        if payload_type is str:
            data = json.loads(data)
        elif payload_type is dict:
            pass
        else:
            data = None

        # pprint(data, indent=4, width=1000)
        # print("TYPE is: ")
        # print(type(data))

        if data:
            # user info
            raw_job_title = data['raw_job_title']
            company_name = data['company_name']
            candidate_name = data['candidate_name']
            sign_off = data['sign_off']  # pass in as null
            contact_number = data['contact_number']
            date = data['date']
            pre_intro = data['pre_intro']  # pass in as null
            email = data['email']
            intro_paragraph = data['intro_paragraph']  # pass in as null
            body_paragraphs = data['body_paragraphs']  # pass in as null
            outro_paragraph = data['outro_paragraph']  # pass in as null
            pre_compiled_coverletter = data['pre_compiled_coverletter_text']
            user_name_present = data['user_name_present']

            if not candidate_name:
                candidate_name = "[user_name]"

            html_template, full_html_template_with_inline_css = create_cv_html(
                insertable_position=raw_job_title,
                company=company_name,
                user_name=candidate_name,
                sign_off=sign_off,
                contact_number=contact_number,
                date=date,
                pre_intro=pre_intro,
                email=email,
                intro_paragraph=intro_paragraph,
                body_paragraphs=body_paragraphs,
                outro_paragraph=outro_paragraph,
                user_name_present=user_name_present,
                pre_compiled_coverletter_text=pre_compiled_coverletter
            )

            now = datetime.now()
            timestamp = datetime.timestamp(now)

            response_data = {
                "timestamp": timestamp,
                "coverletter_html_no_styling": html_template,  # returns null if not coverletter not reconcilied
                "coverletter_html_full_styling": full_html_template_with_inline_css,
            }

            # name_space_1.logger.info(response_data)
            return response_data, 200
        else:
            return {
                       "message": "no data provided. check data is being sent as a json object in the body of the request - not as a url parameter"
                   }, 409


@api.route('/mass-create-job-applications')
class MassCreateJobApplication(Resource):

    def get(self):
        return {'test': 'test'}

    def post(self):

        data = api.payload
        payload_type = type(data)

        if payload_type is str:
            data = json.loads(data)
        elif payload_type is dict:
            pass
        else:
            data = None

        if data:

            ad_response_objects = []

            for job_ad_object in data["job_ads"]:
                # TODO: pass into celery queue

                # print(type(job_ad_object))
                # pprint(job_ad_object, width=1000)
                # user info
                candidate_name = job_ad_object['candidate_name']
                parsed_resume = job_ad_object['parsed_resume']
                # pprint(parsed_resume)
                # name_space_1.logger.info(parsed_resume)
                resume_file_link = job_ad_object['resume_file_link']

                # job info
                hiring_manager_name = job_ad_object['hiring_manager_name']
                raw_job_title = job_ad_object['raw_job_title']

                job_ad_description = job_ad_object['job_ad_description']
                job_ad_description = convert_job_ad_description(job_ad_description)

                company_name = job_ad_object['company_name']
                hash_id = job_ad_object['hash_id']
                source_url = job_ad_object['source_url']

                # job search
                searched_skills = job_ad_object['searched_skills']
                include_resume_skills_in_match = job_ad_object['include_resume_skills_in_match']  # Bool

                response_data = create_cover_letter_and_job_match_for_api(
                    candidate_name=candidate_name,
                    parsed_resume=parsed_resume,
                    resume_file_link=resume_file_link,
                    hiring_manager_name=hiring_manager_name,
                    raw_job_title=raw_job_title,
                    job_ad_description=job_ad_description,
                    company_name=company_name,
                    hash_id=hash_id,
                    source_url=source_url,
                    searched_skills=searched_skills,
                    include_resume_skills_in_match=include_resume_skills_in_match,
                    list_of_position_titles_with_templates=list_of_positions_from_template_database,
                    fuzzy_process=process
                )

                ad_response_objects.append(response_data)

                # name_space_1.logger.info(response_data)

            mass_applications = {
                "number_of_applications": len(ad_response_objects),
                "applications": ad_response_objects
            }
            return mass_applications, 200
        else:
            return {
                       "message": "no data provided - or provided in wrong format. check data is being sent as a json object in the body of the request - not as a url parameter"}, 409


@api.route('/register_coverletter_changes')
class RegisterCoverletterChanges(Resource):
    def get(self):
        return {'test': 'test'}

    def post(self):
        json = request.get_json()
        # push to S3 bucket

        return {'response': 'data'}, 200


@api.route('/stylize_resume')
class SytlizeResume(Resource):
    def get(self):
        return {'test': 'test'}

    def post(self):

        data = api.payload
        payload_type = type(data)

        if payload_type is str:
            data = json.loads(data)
        elif payload_type is dict:
            pass
        else:
            data = None

        pprint(data, indent=4, width=1000)
        print("TYPE is: ")
        print(type(data))

        if data:

            error = ""
            try:
                html_resume = default_template_resume_pdf(data)
            except Exception as e:
                html_resume = ""
                print("RESUME ERROR: ", e)
                error = e

            # current date and time
            now = datetime.now()
            timestamp = datetime.timestamp(now)

            response_data = {
                "timestamp": timestamp,
                "resume_stylized": html_resume,
                "error_message": error
            }

            return response_data


@api.route('/resume_advice')
class ResumeAdvice(Resource):
    def get(self):
        return {'test': 'test'}

    def post(self, request):
        json = request.get_json()

        return {'response': 'data'}


# business partners
# api.add_resource(CreateJobApplication, "/api/coverletter/create_job_application")
# split up universal and personal fields - keep universal (personal fields are stored when django api is called)

# api.add_resource(ResumeAdvice, "/api/resume/resume_advice")
# api.add_resource(IndustryKnowledge, "/api/resume/ai_industry_insights")

# chrome extension

# both

# api.add_resource(CreateJobApplication, "/api/coverletter/create_coverletter_and_tailor_resume")
# api.add_resource(MassCreateCoverletters, "/api/coverletter/mass_create_coverletters")
# api.add_resource(MassCreateCoverletters, "/api/coverletter/mass_create_coverletters_tailored_resumes")
# api.add_resource(RegisterCoverletterChanges, "/api/coverletter/send_coverletter_changes")
# api.add_resource(SytlizeResume, "/api/resume/stylize_resume")
# api.add_resource(ResumeAdvice, "/api/resume/resume_advice")
# api.add_resource(ResumeAdvice, "/api/search/external_apply")
# load page

# extract external apply link (use script)

if __name__ == '__main__':
    app.run(debug=False)
