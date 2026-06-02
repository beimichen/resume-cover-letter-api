import csv
import json
import os
import random
import gender_guesser.detector as gender
from modules.cover_letter_v2.skill_lookups import extract_skills_from_text, \
    find_normalized_skill_type, normalize_raw_skill, extract_hard_skills_from_text, \
    find_closest_representation_of_raw_skill
from modules.cover_letter_v2.generic_skill_sentences import generate_skills_sentence, recruitment_titles
from modules.cover_letter_v2.process_template import process_template, extract_and_categorize_all_sentences
from modules.cover_letter_v2.custom_cover_letter_template_paragraphs_and_sentences import create_custom_body_paragraphs, \
    create_custom_intro_paragraph, create_custom_outro_paragraph
from modules.cover_letter_v2.similar_positions import find_similar_positions
from modules.cover_letter_v2.cover_letter_html import create_cv_html
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher
from multi_rake import Rake
from fuzzywuzzy import fuzz


# import logging
#
# logname = 'docgen_backend_api'
#
# logging.basicConfig(filename=logname,
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)


class CoverLetterCreator:

    def __init__(
            self,
            reconciled_position=None,
            raw_position=None,
            insertable_position=None,
            user_name=None,
            employer_name=None,
            company_name=None,
            ad_text=None,
            resume=None,
            searched_skills=None,
            contact_number=None,
            user_email=None,
            raw_resume=None,
            date=None,
            cover_letter_templates=None,
            generic_ability_type_sentences=None,
            generic_knowledge_type_sentences=None,
            skill_search_instance=None,
            hard_skills_search_instance=None,
            skill_entities=None,
            skill_normalizer=None,
            rake_instance=None,
            skill_categories=None,
            skill_cat_types=None,
            pre_compiled_coverletter=None
    ):

        self.reconciled_position = reconciled_position
        self.raw_position = raw_position
        self.insertable_position = insertable_position
        self.user_name = user_name  # user name from API or chat
        self.employer_name = employer_name
        self.contact_number = contact_number
        self.user_email = user_email
        self.company_name = company_name  # from API or chat
        self.alternative_positions = find_similar_positions(reconciled_position)
        self.ad_text = ad_text  # from the API or the chat
        self.resume = resume  # from the API or the chat
        self.searched_skills = searched_skills
        self.raw_resume = raw_resume
        self.cover_letter_templates = cover_letter_templates
        self.date = date
        self.generic_ability_type_sentences = generic_ability_type_sentences,
        self.generic_knowledge_type_sentences = generic_knowledge_type_sentences
        self.skill_search_instance = skill_search_instance,
        self.hard_skill_search_instance = hard_skills_search_instance
        self.skill_entities = skill_entities,
        self.skill_normalizer = skill_normalizer,
        self.rake_instance = rake_instance,
        self.skill_categories = skill_categories,
        self.skill_cat_types = skill_cat_types
        self.pre_compiled_coverletter = pre_compiled_coverletter

    def extract_position_template(self, position):
        # print("extract_position_template: ", position)
        try:
            position_cover_letter_template = self.cover_letter_templates[position]
            # print("position_cover_letter_template: ", position_cover_letter_template) # this is passing ok
            template = process_template(position_cover_letter_template)
            return template
        except Exception as e:
            # logging.debug(e)
            print(e)
            return None

    def extract_skills_from_ad_text(self, rake_instance, skill_categories, skill_cat_types, skill_search_instance,
                                    hard_skill_search_instance,
                                    skill_entities, skill_normalizer):
        knowledge_and_abilities_and_their_types = []
        hard_skills_only = []

        if self.ad_text:

            skills_found = extract_skills_from_text(self.ad_text, rake_instance, skill_search_instance, skill_entities,
                                                    skill_normalizer)

            hard_skills_only = extract_hard_skills_from_text(self.ad_text, rake_instance, hard_skill_search_instance)

            print('hard skills found in ad:')
            print(hard_skills_only)

            if skills_found:

                for skill in skills_found:
                    knowledge_and_abilities_and_their_types.append(
                        find_normalized_skill_type(skill, skill_categories, skill_cat_types))

        return knowledge_and_abilities_and_their_types, hard_skills_only

    def extract_skills_from_resume(self, skill_search_instance, hard_skills_search_instance, skill_entities,
                                   skill_normalizer, skill_categories,
                                   skill_cat_types):

        if self.resume:
            skills = self.resume['personal']['skills']
            skills_for_sent_normalized = []
            skills_only = []
            skills_and_skill_types = []
            for skill in skills:
                skill_for_sent_found = normalize_raw_skill(skill.lower(), skill_search_instance, skill_entities,
                                                           skill_normalizer)
                skill_found = find_closest_representation_of_raw_skill(skill.lower(), hard_skills_search_instance)
                if skill_for_sent_found:
                    skills_for_sent_normalized.append(skill_for_sent_found)
                if skill_found:
                    skills_only.append(skill_found)
            if skills_for_sent_normalized:
                deduped_normalized_skills = list(set(skills_for_sent_normalized))
                for skill in deduped_normalized_skills:
                    skill_and_skill_type_found = find_normalized_skill_type(skill, skill_categories, skill_cat_types)
                    if skill_and_skill_type_found:
                        skills_and_skill_types.append(
                            find_normalized_skill_type(skill, skill_categories, skill_cat_types))
            return skills_and_skill_types, skills_only
        else:
            return [], []

    def extract_skills_from_searched_skills(self, skill_search_instance, hard_skills_search_instance, skill_entities,
                                            skill_normalizer,
                                            skill_categories,
                                            skill_cat_types,
                                            searched_skills):
        # print('Searched skills')
        # print(searched_skills)
        if searched_skills:
            skills_for_sent_normalized = []
            skills_only = []
            skills_and_skill_types = []
            for skill in searched_skills:
                skill_for_sent_found = normalize_raw_skill(skill.lower(), skill_search_instance, skill_entities,
                                                           skill_normalizer)
                skill_found = find_closest_representation_of_raw_skill(skill.lower(), hard_skills_search_instance)
                # print('hard skill found')
                # print(skill_found)
                if skill_for_sent_found:
                    skills_for_sent_normalized.append(skill_for_sent_found.lower())
                if skill_found:
                    skills_only.append(skill_found.lower())
            if skills_for_sent_normalized:
                skills_and_skill_types = []
                deduped_normalized_skills = list(set(skills_for_sent_normalized))
                for _skill in deduped_normalized_skills:
                    skill_and_skill_type_found = find_normalized_skill_type(_skill.lower(), skill_categories,
                                                                            skill_cat_types)
                    if skill_and_skill_type_found:
                        skills_and_skill_types.append(
                            skill_and_skill_type_found)
            # print('Search skills normalized')
            # print(skills_only)
            return skills_and_skill_types, skills_only
        else:
            return [], []

    def identify_intersecting_skills_with_types(self, user_skills, ad_skills):
        inter_skills = list(set(user_skills) & set(ad_skills))
        return inter_skills

    def identify_intersecting_skills(self, user_skills, ad_skills):
        inter_skills = list(set(user_skills) & set(ad_skills))
        for skill in user_skills:
            if skill not in inter_skills:
                for _skill in ad_skills:
                    if _skill not in inter_skills:
                        match_ratio = fuzz.ratio(skill, _skill)
                        if match_ratio >= 86:
                            inter_skills.append(skill)
        deduped_inter_skills = list(set(inter_skills))
        return deduped_inter_skills

    def insert_entities_into_template(self, template, company, position, user_name, education_institutions, degrees,
                                      fields):
        if company:
            # TODO:
            pass

    def insert_custom_education_sentence(self, template):
        pass

    def create_custom_skill_sentence_and_find_intersecting_skills(
            self,
            _generic_ability_type_sentences,
            _generic_knowledge_type_sentences,
            _skill_search_instance,
            _hard_skill_search_instance,
            _skill_entities,
            _skill_normalizer,
            _rake_instance,
            _skill_categories,
            _skill_cat_types,
            _searched_skills):

        print('creating custom skill sentences and extracting skills')

        if self.resume:
            print('extracting skills from resume')
            skills_for_sent_found_in_resume, hard_skills_found_in_resume = self.extract_skills_from_resume(
                _skill_search_instance,
                _hard_skill_search_instance,
                _skill_entities,
                _skill_normalizer,
                _skill_categories,
                _skill_cat_types)
        else:
            skills_for_sent_found_in_resume = []
            hard_skills_found_in_resume = []

        print('extracting skills from ad')
        skills_found_in_ad, hard_skills_found_in_ad = self.extract_skills_from_ad_text(_rake_instance,
                                                                                       _skill_categories,
                                                                                       _skill_cat_types,
                                                                                       _skill_search_instance,
                                                                                       _hard_skill_search_instance,
                                                                                       _skill_entities,
                                                                                       _skill_normalizer)

        if self.searched_skills:
            print('normalizing skills from search skills')
            skills_for_sent_found_from_searched_skills, hard_skills_found_from_searched_skills = self.extract_skills_from_searched_skills(
                _skill_search_instance,
                _hard_skill_search_instance,
                _skill_entities, _skill_normalizer,
                _skill_categories,
                _skill_cat_types,
                _searched_skills)
        else:
            skills_for_sent_found_from_searched_skills = []
            hard_skills_found_from_searched_skills = []

        skills_from_ad_cleaned_with_types = []
        skills_from_ad_for_sent = []
        skills_from_ad = []

        aggregate_users_skills_list = []

        for skill in skills_found_in_ad:
            if skill is not None:
                skills_from_ad_cleaned_with_types.append(skill)
                skills_from_ad_for_sent.append(skill[0])

        for skill in hard_skills_found_in_ad:
            skills_from_ad.append(skill)

        skills_from_resume_cleaned_with_types = []
        skills_from_searched_cleaned_with_types = []

        for skill in skills_for_sent_found_in_resume:
            if skill is not None:
                aggregate_users_skills_list.append(skill[0])
                skills_from_resume_cleaned_with_types.append(skill)

        for skill in skills_for_sent_found_from_searched_skills:
            if skill is not None:
                if skill not in skills_for_sent_found_in_resume:
                    aggregate_users_skills_list.append(skill[0])
                    skills_from_searched_cleaned_with_types.append(skill)

        if self.resume:
            raw_skills_from_resume = self.resume['skills']
            for raw_skill in raw_skills_from_resume:
                if raw_skill not in aggregate_users_skills_list:
                    aggregate_users_skills_list.append(raw_skill)
        else:
            raw_skills_from_resume = []

        if self.searched_skills:
            for raw_skill in self.searched_skills:
                aggregate_users_skills_list.append(raw_skill.lower())

        if skills_from_resume_cleaned_with_types and skills_from_ad_cleaned_with_types:
            intersecting_skills_with_types = self.identify_intersecting_skills_with_types(
                skills_from_resume_cleaned_with_types,
                skills_from_ad_cleaned_with_types)
        elif skills_from_searched_cleaned_with_types and skills_from_ad_cleaned_with_types:
            intersecting_skills_with_types = self.identify_intersecting_skills_with_types(
                skills_from_searched_cleaned_with_types,
                skills_from_ad_cleaned_with_types)
        else:
            intersecting_skills_with_types = []

        intersecting_skills_global = []

        abilities = []
        knowledge = []
        hard_skills = hard_skills_found_in_resume + hard_skills_found_from_searched_skills

        if hard_skills:
            hard_skills = list(set(hard_skills))
            for skill in hard_skills:
                aggregate_users_skills_list.append(skill)

        if aggregate_users_skills_list and skills_from_ad:
            deduped_aggregate_user_skills_list = list(set(aggregate_users_skills_list))
            intersecting_skills = self.identify_intersecting_skills(deduped_aggregate_user_skills_list, skills_from_ad)
            print('skills from ad')
            print(skills_from_ad)
            print('aggregate user skills')
            print(aggregate_users_skills_list)
            print('intersecting skills')
            print(intersecting_skills)
            if intersecting_skills:
                for skill in intersecting_skills:
                    intersecting_skills_global.append(skill)

        print('creating skill sentences')
        if intersecting_skills_with_types:
            for skill in intersecting_skills_with_types:
                skill_type = skill[1]
                skill = skill[0]
                if skill_type == 'skill':
                    abilities.append(skill)
                elif skill_type == 'knowledge':
                    knowledge.append(skill)
        elif skills_from_resume_cleaned_with_types:
            for skill in skills_from_resume_cleaned_with_types:
                skill_type = skill[1]
                skill = skill[0]
                if skill_type == 'skill':
                    abilities.append(skill)
                elif skill_type == 'knowledge':
                    knowledge.append(skill)
        elif raw_skills_from_resume:
            if len(raw_skills_from_resume) >= 5:
                for skill in raw_skills_from_resume[:5]:
                    knowledge.append(skill)
            else:
                for skill in raw_skills_from_resume:
                    knowledge.append(skill)
        elif skills_from_ad_cleaned_with_types:
            for skill in skills_from_ad_cleaned_with_types:
                skill_type = skill[1]
                skill = skill[0]
                if skill_type == 'skill':
                    abilities.append(skill)
                elif skill_type == 'knowledge':
                    knowledge.append(skill)

        print('creating knowledge/ability sentence')
        topics_of_interest_extracted_from_ad = abilities + knowledge

        if abilities:
            abilities_sentence = generate_skills_sentence(abilities, 'skills', self.company_name,
                                                          _generic_ability_type_sentences,
                                                          _generic_knowledge_type_sentences)
        else:
            abilities_sentence = []

        if knowledge:
            knowledge_sentence = generate_skills_sentence(knowledge, 'knowledge', self.company_name,
                                                          _generic_ability_type_sentences,
                                                          _generic_knowledge_type_sentences)
        else:
            knowledge_sentence = []

        print('finished creating knowledge/ability sentence')

        knowledge_and_abilities_dict = {'abilities': abilities,
                                        'knowledge': knowledge,
                                        'hard_skills': hard_skills}

        return abilities_sentence, knowledge_sentence, knowledge_and_abilities_dict, \
               aggregate_users_skills_list, \
               topics_of_interest_extracted_from_ad, \
               skills_from_ad, \
               intersecting_skills_global

    #
    # def generate_sentence_with_skills(self, skills, skills_type):
    #     sentence = generate_skills_sentence(skills, skills_type,)
    #     return sentence

    def job_ad_text_match_skills(
            self,
            skill_search_instance=None,
            hard_skills_search_instance=None,
            rake_instance=None,
            generic_ability_type_sentences=None,
            generic_knowledge_type_sentences=None,
            skill_entities=None,
            skill_normalizer=None,
            skill_categories=None,
            skill_cat_types=None):

        if self.searched_skills:
            searched_skills = self.searched_skills
            if self.resume:
                if 'skills' in self.resume:
                    searched_skills = searched_skills + self.resume['skills']
            print('searched skills:')
            print(searched_skills)
            abilities_sentence, knowledge_sentence, intersecting_knowledge_and_abilities, \
            aggregate_users_skills_list, topics_of_interest_extracted_from_ad, skills_extracted_from_ad, intersecting_skills = \
                self.create_custom_skill_sentence_and_find_intersecting_skills(
                    generic_ability_type_sentences, generic_knowledge_type_sentences, skill_search_instance,
                    hard_skills_search_instance,
                    skill_entities,
                    skill_normalizer,
                    rake_instance,
                    skill_categories,
                    skill_cat_types,
                    searched_skills)
        else:
            print('no searched skill')
            abilities_sentence = None
            knowledge_sentence = None
            intersecting_skills = []
            topics_of_interest_extracted_from_ad = []
            intersecting_knowledge_and_abilities = []
            aggregate_users_skills_list = []
            skills_extracted_from_ad = []

        return intersecting_skills, aggregate_users_skills_list, skills_extracted_from_ad, topics_of_interest_extracted_from_ad

    def write_cover_letter(self, skill_search_instance, hard_skills_search_instance, rake_instance,
                           pre_compiled_coverletter,
                           generic_ability_type_sentences, generic_knowledge_type_sentences, skill_entities,
                           skill_normalizer,
                           skill_categories,
                           skill_cat_types
                           ):

        # print(self.raw_position)

        relative_match_position_templates = []

        vowels = ['a', 'e', 'i', 'o', 'u']

        repetitive_keywords = ['your team']

        # standard_intro only where name is supplied
        standard_intro = "Dear {},\n"

        # intro_if_no_name_provided only for empty name, as it uses "recruitment manager at COMPANY" instead
        intro_if_no_name_provided = "Dear {} at {},\n"

        if self.employer_name:
            # number of names must be >= 1
            number_of_names = len(self.employer_name.split())

            pre_intro = ""

            if number_of_names == 1:
                names_seperated = self.employer_name.split()
                first_name = names_seperated[0]
                pre_intro = standard_intro.format(first_name.title())

            else:
                # number of names must be > 1
                # in the case of a name with 5 words, always take only first and last name

                names_seperated = self.employer_name.split()
                first_name = names_seperated[0].title()
                last_name = names_seperated[-1].title()
                ms = "Ms. "
                mr = "Mr. "
                output = get_last_name_and_gender_prefix(first_name, last_name, ms, mr)
                pre_intro = standard_intro.format(output)

        else:
            recruitment_title = random.choice(recruitment_titles)
            pre_intro = intro_if_no_name_provided.format(recruitment_title, self.company_name)

        # intro_paragraph = ""
        # body_paragraphs = []
        # outro_paragraph = ""

        sign_offs = [
            "Sincerely,\n",
            "Yours Sincerely,\n",
            "Kind Regards,\n",
            "Kindest Regards,\n",
            "Warm Regards,\n",
            "Warmest Regards,\n"
        ]

        """ Set up variables for resume components that are used to write sentences """
        if self.resume:

            try:
                skills_from_resume = self.resume['skills']
            except KeyError as e:
                print(e)
                skills_from_resume = None

            try:
                degrees_from_resume = self.resume['education']['degrees']
                # for degree in degrees_from_resume:
                #     degrees.append(degree)
            except KeyError as e:
                print(e)
                degrees_from_resume = None

            try:
                fields_of_study_from_resume = self.resume['education']['fields']
                # for field in fields_of_study_from_resume:
                #     fields.append(field)
            except KeyError as e:
                print(e)
                fields_of_study_from_resume = None

            try:
                education_institutions_from_resume = self.resume['education']['education_institution']
                # for field in fields_of_study_from_resume:
                #     fields.append(field)
            except KeyError as e:
                print(e)
                education_institutions_from_resume = None

            try:
                experiences_from_resume = self.resume['experiences']
            except KeyError as e:
                print(e)
                experiences_from_resume = None
        else:
            print('no resume')
            degrees_from_resume = None
            experiences_from_resume = None
            education_institutions_from_resume = None
            fields_of_study_from_resume = None
            skills_from_resume = None

        if self.user_name != '[user_name]':
            print('creating sign offs with user name')
            print(self.user_name)
            sign_off = random.choice(sign_offs) + self.user_name.title()
        else:
            print('creating sign offs with no user name')
            sign_off = random.choice(sign_offs) + "[user_name]"

        # find skills from ad and match

        if self.searched_skills:
            searched_skills = self.searched_skills
            if self.resume:
                if 'skills' in self.resume:
                    searched_skills = searched_skills + self.resume['skills']
            print('searched skills:')
            print(searched_skills)
            abilities_sentence, knowledge_sentence, intersecting_knowledge_and_abilities, \
            aggregate_users_skills_list, topics_of_interest_extracted_from_ad, skills_extracted_from_ad, intersecting_skills = \
                self.create_custom_skill_sentence_and_find_intersecting_skills(
                    generic_ability_type_sentences, generic_knowledge_type_sentences, skill_search_instance,
                    hard_skills_search_instance,
                    skill_entities,
                    skill_normalizer,
                    rake_instance,
                    skill_categories,
                    skill_cat_types,
                    searched_skills)
        else:
            print('no searched skill')
            abilities_sentence = None
            knowledge_sentence = None
            intersecting_skills = []
            topics_of_interest_extracted_from_ad = []
            intersecting_knowledge_and_abilities = []
            aggregate_users_skills_list = []
            skills_extracted_from_ad = []

        exact_match_position_template = self.extract_position_template(self.reconciled_position)
        # print("exact_match_position_template: ", exact_match_position_template)
        # unordered_categorized_sentences_exact_match_template_sentences = exact_match_position_template[0]

        if exact_match_position_template:
            ordered_uncategorized_sentences_exact_match_template_sentences = exact_match_position_template[1]
            exact_match_position_template_num_of_pars = exact_match_position_template[2]
            exact_match_position_template_num_of_chars = exact_match_position_template[3]
        else:
            ordered_uncategorized_sentences_exact_match_template_sentences = None
            exact_match_position_template_num_of_pars = None
            exact_match_position_template_num_of_chars = None

        print('relative positions:')
        print(self.alternative_positions)

        if self.alternative_positions:
            for position in self.alternative_positions:
                try:
                    relative_position_template = self.extract_position_template(position)
                    # print('relative position template')
                    # print(relative_position_template)
                except Exception as e:
                    # logging.debug(e)
                    print(e)
                    relative_position_template = None

                if relative_position_template:
                    relative_match_position_templates.append(relative_position_template)

            if relative_match_position_templates:
                all_relative_position_intro_sentences, \
                all_relative_position_body_sentences, \
                all_relative_position_outro_sentences = extract_and_categorize_all_sentences(
                    relative_match_position_templates)
            else:
                all_relative_position_intro_sentences = None
                all_relative_position_body_sentences = None
                all_relative_position_outro_sentences = None
        else:
            all_relative_position_intro_sentences = None
            all_relative_position_body_sentences = None
            all_relative_position_outro_sentences = None

        """ Search for alternative position templates """
        if all_relative_position_body_sentences:

            print('there are alternative position template sentences')

            relative_match_position_templates.append(exact_match_position_template)

            # If the exact match template is weak (3 or under paragraphs and under 850 characters in length)

            # template reset
            template = ''
            # create intro par using pertinent data
            print('creating custom intro')
            intro_paragraph = create_custom_intro_paragraph(education_institutions_from_resume,
                                                            degrees_from_resume,
                                                            fields_of_study_from_resume,
                                                            self.insertable_position,
                                                            self.company_name,
                                                            self.user_name) + '\n'

            if '[degree]' in intro_paragraph:
                degree_present = True
            else:
                degree_present = False

            # create body pars using pertinent data
            print('creating custom body paragraphs')
            body_paragraphs = create_custom_body_paragraphs(all_relative_position_body_sentences,
                                                            abilities_sentence, knowledge_sentence,
                                                            experiences_from_resume, degree_present)
            # create outro par using pertinent data
            print('creating custom outro paragraphs')
            outro_paragraph = create_custom_outro_paragraph(self.insertable_position) + '\n'
            print('finished creating custom outro par')
            template += pre_intro + intro_paragraph
            for body_par in body_paragraphs:
                template += body_par

            template += outro_paragraph + sign_off

            """ If resulting template from relative positions isn't good enough"""
            if exact_match_position_template_num_of_chars:
                if len(template) < exact_match_position_template_num_of_chars:

                    print(
                        'custom created template is weaker than the exact match template. restarting create cover letter')

                    intro_paragraph = ""
                    body_paragraph = ""
                    outro_paragraph = ""

                    for sentence in ordered_uncategorized_sentences_exact_match_template_sentences['intro'][
                        'parsed_sentences']:
                        intro_paragraph += sentence.strip() + " "

                    # intro_paragraph += '\n'

                    if 'a [position]' in intro_paragraph and any(v in self.insertable_position[:1] for v in vowels):
                        intro_paragraph = intro_paragraph.replace('a [position]', 'an ' + self.insertable_position)
                    elif 'an [position]' in intro_paragraph and any(
                            v not in self.insertable_position[:1] for v in vowels):
                        intro_paragraph = intro_paragraph.replace('an [position]', 'a ' + self.insertable_position)
                    else:
                        intro_paragraph = intro_paragraph.replace('[position]', self.insertable_position)

                    if self.user_name:
                        intro_paragraph = intro_paragraph.replace('[user_name]', self.user_name)
                    if self.company_name:
                        intro_paragraph = intro_paragraph.replace('[org]', self.company_name)
                    if education_institutions_from_resume:
                        intro_paragraph = intro_paragraph.replace('[edu_institution]',
                                                                  education_institutions_from_resume[-1])
                    if degrees_from_resume:
                        intro_paragraph = intro_paragraph.replace('[degree]', degrees_from_resume[-1])
                    if fields_of_study_from_resume:
                        intro_paragraph = intro_paragraph.replace('[field]', fields_of_study_from_resume[-1])

                    body_paragraphs = []

                    for key, val in ordered_uncategorized_sentences_exact_match_template_sentences['body'].items():
                        for sentence in val['parsed_sentences']:
                            body_paragraph += sentence + ' '
                        body_paragraph += '\n\n'
                        body_paragraphs.append(body_paragraph)

                    for sentence in ordered_uncategorized_sentences_exact_match_template_sentences['outro'][
                        'parsed_sentences']:
                        outro_paragraph += sentence.strip() + " "

                    # outro_paragraph += '\n'

                    if 'a [position]' in body_paragraph and any(v in self.insertable_position[:1] for v in vowels):
                        body_paragraph = body_paragraph.replace('a [position]', 'an ' + self.insertable_position)
                    elif 'an [position]' in body_paragraph and any(
                            v not in self.insertable_position[:1] for v in vowels):
                        body_paragraph = body_paragraph.replace('an [position]', 'a ' + self.insertable_position)
                    else:
                        body_paragraph = body_paragraph.replace('[position]', self.insertable_position)

                    if 'a [position]' in outro_paragraph and any(v in self.insertable_position[:1] for v in vowels):
                        outro_paragraph = outro_paragraph.replace('a [position]', 'an ' + self.insertable_position)
                    elif 'an [position]' in outro_paragraph and any(
                            v not in self.insertable_position[:1] for v in vowels):
                        outro_paragraph = outro_paragraph.replace('an [position]', 'a ' + self.insertable_position)
                    else:
                        outro_paragraph = outro_paragraph.replace('[position]', self.insertable_position)

                    template = pre_intro + intro_paragraph + body_paragraph + outro_paragraph + sign_off

        else:

            print('there are no alternative position template sentences')

            intro_paragraph = ""
            body_paragraph = ""
            outro_paragraph = ""

            if ordered_uncategorized_sentences_exact_match_template_sentences:
                for sentence in ordered_uncategorized_sentences_exact_match_template_sentences['intro'][
                    'parsed_sentences']:
                    intro_paragraph += sentence.strip() + " "

                intro_paragraph += '\n\n'

                if 'a [position]' in intro_paragraph and any(v in self.insertable_position[:1] for v in vowels):
                    intro_paragraph = intro_paragraph.replace('a [position]', 'an ' + self.insertable_position)
                elif 'an [position]' in intro_paragraph and any(v not in self.insertable_position[:1] for v in vowels):
                    intro_paragraph = intro_paragraph.replace('an [position]', 'a ' + self.insertable_position)
                else:
                    intro_paragraph = intro_paragraph.replace('[position]', self.insertable_position)

                if self.user_name:
                    intro_paragraph = intro_paragraph.replace('[user_name]', self.user_name)

                body_paragraphs = []

                for key, val in ordered_uncategorized_sentences_exact_match_template_sentences['body'].items():
                    for sentence in val['parsed_sentences']:
                        body_paragraph += sentence + ' '
                    body_paragraph += '\n\n'
                    body_paragraphs.append(body_paragraph)

                # print(body_paragraphs)

                if self.company_name:
                    intro_paragraph = intro_paragraph.replace('[org]', self.company_name)

                for sentence in ordered_uncategorized_sentences_exact_match_template_sentences['outro'][
                    'parsed_sentences']:
                    outro_paragraph += sentence.strip() + " "

                outro_paragraph += '\n\n'

                if 'a [position]' in body_paragraph and any(v in self.insertable_position[:1] for v in vowels):
                    body_paragraph = body_paragraph.replace('a [position]', 'an ' + self.insertable_position)
                elif 'an [position]' in body_paragraph and any(v not in self.insertable_position[:1] for v in vowels):
                    body_paragraph = body_paragraph.replace('an [position]', 'a ' + self.insertable_position)
                else:
                    body_paragraph = body_paragraph.replace('[position]', self.insertable_position)

                if 'a [position]' in outro_paragraph and any(v in self.insertable_position[:1] for v in vowels):
                    outro_paragraph = outro_paragraph.replace('a [position]', 'an ' + self.insertable_position)
                elif 'an [position]' in outro_paragraph and any(v not in self.insertable_position[:1] for v in vowels):
                    outro_paragraph = outro_paragraph.replace('an [position]', 'a ' + self.insertable_position)
                else:
                    outro_paragraph = outro_paragraph.replace('[position]', self.insertable_position)

                template = pre_intro + intro_paragraph + body_paragraph + outro_paragraph + sign_off
            else:
                template = None

        return template, \
               intersecting_knowledge_and_abilities, intersecting_skills, aggregate_users_skills_list, skills_extracted_from_ad, topics_of_interest_extracted_from_ad


def get_last_name_and_gender_prefix(first_name, last_name, female_prefix, male_prefix):
    """
    return person's title (Mr. / Mrs etc) based on their name using a trained ML classifier
    gender-guesser library : https://pypi.org/project/gender-guesser/
    """
    g = gender.Detector()
    gender_checked = g.get_gender(first_name)
    if gender_checked == "female":
        title = female_prefix + last_name.title()
    elif gender_checked == "male":
        title = male_prefix + last_name.title()
    else:
        title = first_name + " " + last_name

    return title

# if __name__ == '__main__':
#
#     # Instantiate files & lookups for cover letter generator
#
#     print("Instantiating Lookups!!")
#     # coverletter templates
#     template_json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                       'templates/cover_letter_sentences_v12_uk.json')
#
#     with open(template_json_file, 'r') as cv_templates:
#         cover_letter_templates = json.load(cv_templates)
#
#     # generic sentences
#     file1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                          'generic_sentences/insert_skills_ability_type_sentences.csv')
#     file2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                          'generic_sentences/insert_skills_knowledge_type_sentences.csv')
#
#     generic_ability_type_sentences = []
#     generic_knowledge_type_sentences = []
#
#     with open(file1, 'r') as r1:
#         for row in r1:
#             generic_ability_type_sentences.append(row.strip('\n'))
#
#     with open(file2, 'r') as r2:
#         for row in r2:
#             generic_knowledge_type_sentences.append(row.strip('\n'))
#
#     # SKILL LOOKUPS
#     rake = Rake()
#     skills_db = DictDatabase(CharacterNgramFeatureExtractor(3))
#     skill_searcher = Searcher(skills_db, CosineMeasure())
#     skills_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skills_normalizer.tsv')
#     skills_cat_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skills_categorization.tsv')
#     template_json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                       'templates/cover_letter_sentences_v12_uk.json')
#
#     # print(skills_file)
#     skill_entities = []
#     skill_normalizer = []
#
#     with open(skills_file, 'r', encoding='utf-8-sig') as h_skills:
#         reader = csv.reader(h_skills, delimiter='\t')
#         for row in reader:
#             skill_entities.append(row[0].strip('\n').lower())
#             skill_normalizer.append(row[1].strip('\n').lower())
#             skills_db.add(row[0].strip('\n').lower())
#
#     skill_categories = []
#     skill_cat_types = []
#
#     print("Instantiating complete!!")
#
#     reconciled_position = 'etl developer'
#     raw_position = 'academic advisor'
#     # reconciled_position = 'Academic Advisor'
#     # raw_position = 'Academic Advisor'
#
#     user_name = 'Jane Doe'
#
#     resume = None
#
#     company_name = 'Boeing'
#
#     employer_name = 'John Micheals'
#
#     ad_text = None
#
#     # resume = {
#     #     'education': {
#     #         'degrees': ['Bachelor degree', 'Master degree'],
#     #         'fields': ['Computer Science', 'IT'],
#     #         'education_institutions': ['Stanford University', 'Harvard']
#     #     },
#     #     'experiences': None,
#     #     'skills': ['Aircraft maintenance', 'electronic systems', 'drilling', 'cutting']
#     # }
#     # Let's change this to original django model - means convention is unified:
#
#     cv = CoverLetterCreator(
#         reconciled_position=reconciled_position,
#         raw_position=raw_position,
#         user_name=user_name,
#         employer_name=employer_name,
#         company_name=company_name,
#         ad_text=ad_text,
#         resume=resume,
#         cover_letter_templates=cover_letter_templates,
#         generic_ability_type_sentences=generic_ability_type_sentences,
#         generic_knowledge_type_sentences=generic_knowledge_type_sentences,
#         skill_search_instance=skill_searcher,
#         skill_entities=skill_entities,
#         skill_normalizer=skill_normalizer,
#         rake_instance=rake,
#         skill_categories=skill_categories,
#         skill_cat_types=skill_cat_types
#     )
#
#     cover_letter, cover_letter_html_no_styling, cover_letter_html_full_styling, intersecting_knowledge_and_abilities, \
#     intersecting_skills, aggregate_users_skills_list, skills_extracted_from_ad = cv.write_cover_letter(skill_searcher,
#                                                                                                        rake, None)
#     # template, html_template, full_html_template_with_inline_css, \
#     #                      intersecting_knowledge_and_abilities,intersecting_skills, aggregate_users_skills_list, skills_extracted_from_ad
#     # cover_letter, cover_letter_html_no_styling, cover_letter_html_full_styling = cv.write_cover_letter(
#     #     generic_ability_type_sentences,
#     #     generic_knowledge_type_sentences,
#     #     skill_search_instance,
#     #     skill_entities,
#     #     skill_normalizer,
#     #     rake_instance,
#     #     skill_categories,
#     #     skill_cat_types)
#
#     # print("cover_letter")
#     # print(cover_letter)
