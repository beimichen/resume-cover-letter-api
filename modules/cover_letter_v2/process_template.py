# from pprint import pprint
import os
import json

def process_template(template):
    number_of_paragraphs = 0
    number_of_characters = 0

    ### INTRO SENTENCES ###

    job_application_intro_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    conjunction_intro_sentences = {
        'original': [],
        'parsed': [],
        'id': [],
        'preceding_original': [],
        'preceding_parsed': []
    }

    discrete_intro_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    job_application_personal_intro_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    insertable_skills_intro_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    education_intro_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    personal_intro_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    ### BODY SENTENCES ###

    discrete_body_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    conjunction_body_sentences = {
        'original': [],
        'parsed': [],
        'id': [],
        'preceding_original': [],
        'preceding_parsed': []
    }

    conjunction_insertable_skills_body_sentences = {
        'original': [],
        'parsed': [],
        'id': [],
        'preceding_original': [],
        'preceding_parsed': []
    }

    conjunction_skill_body_sentence = {
        'original': [],
        'parsed': [],
        'id': [],
        'preceding_original': [],
        'preceding_parsed': []
    }

    pre_bullet_pnt_body_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    bullet_pnt_body_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    generic_skill_body_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    education_body_sentence = {
        'original': [],
        'parsed': [],
        'id': []
    }

    personal_skills_body_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    personal_experience_body_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    insertable_skills_body_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    ### OUTRO SENTENCES ###

    insertable_skills_list_outro_sentence = {
        'original': [],
        'parsed': [],
        'id': []
    }  # outro_insertable_skills_list_sentence

    outro_sentences = {
        'original': [],
        'parsed': [],
        'id': []
    }

    ### Template with unorganized sentences###

    template_with_uncategorized_sentences = {
        'intro': {
            'original_sentences': [],
            'parsed_sentences': [],
            'id': []
        },
        'body': dict(),
        'outro': {
            'original_sentences': [],
            'parsed_sentences': [],
            'id': []
        }
    }

    template_intro = template['intro']
    template_body = template['body']
    template_outro = template['outro']

    for key, val in template.items():
        par_counter = 0
        if key == 'total_num_of_par':
            number_of_paragraphs = val
        if key == 'total_num_of_char':
            number_of_characters = val
        if key == 'intro':
            for _key, _val in val.items():
                if 'paragraph_' in _key:
                    par_counter += 1
                    preceding_par_ind = par_counter - 1
                    sent_counter = 0
                    for __ind, (__key, __val) in enumerate(_val.items()):
                        # par_index = _key.split('_')[1]
                        if 'sent' in __key and not '_sent' in __key:
                            sent_counter += 1
                            preceding_sentence_index = sent_counter - 1
                            template_with_uncategorized_sentences['intro']['original_sentences'].append(
                                __val['original_sentence_text'])
                            template_with_uncategorized_sentences['intro']['parsed_sentences'].append(
                                __val['parsed_sentence_text'])
                            template_with_uncategorized_sentences['intro']['id'].append(
                                __val['sentence_hash'])
                            if __val['sentence_type'] == 'intro_job_application_sentence':
                                job_application_intro_sentences['original'].append(
                                    __val['original_sentence_text'])
                                job_application_intro_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                job_application_intro_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'intro_job_application_personal_sentence':
                                job_application_personal_intro_sentences['original'].append(
                                    __val['original_sentence_text'])
                                job_application_personal_intro_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                job_application_personal_intro_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'intro_insertable_skills_list_sentence':
                                insertable_skills_intro_sentences['original'].append(
                                    __val['original_sentence_text'])
                                insertable_skills_intro_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                insertable_skills_intro_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'intro_education_sentence':
                                education_intro_sentences['original'].append(
                                    __val['original_sentence_text'])
                                education_intro_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                education_intro_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'intro_personal_sentence':
                                personal_intro_sentences['original'].append(
                                    __val['original_sentence_text'])
                                personal_intro_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                personal_intro_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'intro_conjunction_sentence':
                                conjunction_intro_sentences['original'].append(
                                    __val['original_sentence_text'])
                                conjunction_intro_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                if preceding_sentence_index != 0:
                                    conjunction_intro_sentences['preceding_original'].append(
                                        val[_key]['sent' + str(preceding_sentence_index)]['original_sentence_text'])
                                    conjunction_intro_sentences['preceding_parsed'].append(
                                        val[_key]['sent' + str(preceding_sentence_index)]['parsed_sentence_text'])
                                else:
                                    if par_counter != 1:
                                        preceding_par_key = 'paragraph_' + str(preceding_par_ind)
                                        if preceding_par_key in _val:
                                            preceding_section_key = 'body'
                                            last_sent_object = list(template_body[preceding_par_key].values())[-1]
                                        else:
                                            preceding_section_key = 'intro'
                                            last_par = list(template_intro.values())[-1]
                                            last_sent_object = list(last_par.values())[-1]
                                        conjunction_intro_sentences['preceding_original'].append(
                                            last_sent_object['original_sentence_text'])
                                        conjunction_intro_sentences['preceding_parsed'].append(
                                            last_sent_object['parsed_sentence_text'])
                                conjunction_intro_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'discrete_intro_sentence':
                                discrete_intro_sentences['original'].append(
                                    __val['original_sentence_text'])
                                discrete_intro_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                discrete_intro_sentences['id'].append(
                                    __val['sentence_hash'])

        if key == 'body':
            for _ind, (_key, _val) in enumerate(val.items()):
                if 'paragraph_' in _key:
                    par_counter += 1
                    preceding_par_ind = par_counter - 1
                    sent_counter = 0
                    if _key not in template_with_uncategorized_sentences['body']:
                        template_with_uncategorized_sentences['body'][_key] = dict()
                        template_with_uncategorized_sentences['body'][_key]['original_sentences'] = []
                        template_with_uncategorized_sentences['body'][_key]['parsed_sentences'] = []
                        template_with_uncategorized_sentences['body'][_key]['id'] = []
                    for __ind, (__key, __val) in enumerate(_val.items()):
                        if 'sent' in __key and not '_sent' in __key:
                            sent_counter += 1
                            preceding_sentence_index = sent_counter - 1
                            template_with_uncategorized_sentences['body'][_key]['original_sentences'].append(
                                __val['original_sentence_text'])
                            template_with_uncategorized_sentences['body'][_key]['parsed_sentences'].append(
                                __val['parsed_sentence_text'])
                            template_with_uncategorized_sentences['body'][_key]['id'].append(
                                __val['sentence_hash'])
                            if __val['sentence_type'] == 'body_conjunction_sentence':
                                conjunction_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                conjunction_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                if preceding_sentence_index != 0:
                                    conjunction_body_sentences['preceding_original'].append(
                                        val[_key]['sent' + str(preceding_sentence_index)]['original_sentence_text'])
                                    conjunction_body_sentences['preceding_original'].append(
                                        val[_key]['sent' + str(preceding_sentence_index)]['original_sentence_text'])
                                    conjunction_body_sentences['preceding_parsed'].append(
                                        val[_key]['sent' + str(preceding_sentence_index)]['parsed_sentence_text'])
                                else:
                                    preceding_par_key = 'paragraph_' + str(preceding_par_ind)
                                    if preceding_par_key in _val:
                                        preceding_section_key = 'body'
                                        last_sent_object = list(template_body[preceding_par_key].values())[-1]
                                    else:
                                        preceding_section_key = 'intro'
                                        # print(template_intro)
                                        last_par = list(template_intro.values())[-1]
                                        last_sent_object = list(last_par.values())[-1]
                                    conjunction_body_sentences['preceding_original'].append(
                                        last_sent_object['original_sentence_text'])
                                    conjunction_body_sentences['preceding_parsed'].append(
                                        last_sent_object['parsed_sentence_text'])
                                conjunction_body_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'body_education_sentence':
                                education_body_sentence['original'].append(__val['original_sentence_text'])
                                education_body_sentence['parsed'].append(__val['parsed_sentence_text'])
                                education_body_sentence['id'].append(__val['sentence_hash'])
                            elif __val['sentence_type'] == 'body_conjunction_insertable_skills_list_sentence':
                                conjunction_insertable_skills_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                conjunction_insertable_skills_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                if preceding_sentence_index != 0:
                                    conjunction_insertable_skills_body_sentences['preceding_original'].append(
                                        val[_key]['sent' + str(preceding_sentence_index)]['original_sentence_text'])
                                    conjunction_insertable_skills_body_sentences['preceding_parsed'].append(
                                        val[_key]['sent' + str(preceding_sentence_index)]['parsed_sentence_text'])
                                else:
                                    if par_counter != 1:
                                        preceding_par_key = 'paragraph_' + str(preceding_par_ind)
                                        if preceding_par_key in _val:
                                            preceding_section_key = 'body'
                                            last_sent_object = list(template_body[preceding_par_key].values())[-1]
                                        else:
                                            preceding_section_key = 'intro'
                                            last_par = list(template_intro.values())[-1]
                                            last_sent_object = list(last_par.values())[-1]
                                        conjunction_insertable_skills_body_sentences['preceding_original'].append(
                                            last_sent_object['original_sentence_text'])
                                        conjunction_insertable_skills_body_sentences['preceding_parsed'].append(
                                            last_sent_object['parsed_sentence_text'])
                                conjunction_insertable_skills_body_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'body_conjunction_skill_sentence':
                                if preceding_sentence_index != 0:
                                    conjunction_skill_body_sentence['original'].append(
                                        __val['original_sentence_text'])
                                    conjunction_skill_body_sentence['parsed'].append(
                                        __val['parsed_sentence_text'])
                                    if preceding_sentence_index != 0:
                                        conjunction_skill_body_sentence['preceding_original'].append(
                                            val[_key]['sent' + str(preceding_sentence_index)]['original_sentence_text'])
                                        conjunction_skill_body_sentence['preceding_parsed'].append(
                                            val[_key]['sent' + str(preceding_sentence_index)]['parsed_sentence_text'])
                                    else:
                                        if par_counter != 1:
                                            preceding_par_key = 'paragraph_' + str(preceding_par_ind)
                                            if preceding_par_key in _val:
                                                preceding_section_key = 'body'
                                                last_sent_object = list(template_body[preceding_par_key].values())[-1]
                                            else:
                                                preceding_section_key = 'intro'
                                                last_par = list(template_intro.values())[-1]
                                                last_sent_object = list(last_par.values())[-1]
                                            conjunction_skill_body_sentence['preceding_original'].append(
                                                last_sent_object['original_sentence_text'])
                                            conjunction_skill_body_sentence['preceding_parsed'].append(
                                                last_sent_object['parsed_sentence_text`'])
                                    conjunction_skill_body_sentence['id'].append(
                                        __val['sentence_hash'])
                            elif __val['sentence_type'] == 'body_skills_personal_sentence':
                                personal_skills_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                personal_skills_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                personal_skills_body_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'body_personal_experience_sentence':
                                personal_experience_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                personal_experience_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                personal_experience_body_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'body_insertable_skills_list_sentence':
                                insertable_skills_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                insertable_skills_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                insertable_skills_body_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'body_skills_generic_sentence':
                                generic_skill_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                generic_skill_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                generic_skill_body_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'pre_bullet_point':
                                pre_bullet_pnt_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                pre_bullet_pnt_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                pre_bullet_pnt_body_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'bullet_point':
                                bullet_pnt_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                bullet_pnt_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                bullet_pnt_body_sentences['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'body_discrete_sentence':
                                discrete_body_sentences['original'].append(
                                    __val['original_sentence_text'])
                                discrete_body_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                discrete_body_sentences['id'].append(
                                    __val['sentence_hash'])

        if key == 'outro':
            for _key, _val in val.items():
                if 'paragraph_' in _key:
                    par_counter += 1
                    preceding_par_ind = par_counter - 1
                    sent_counter = 0
                    for __ind, (__key, __val) in enumerate(_val.items()):
                        if 'sent' in __key and not '_sent' in __key:
                            sent_counter += 1
                            if __val['original_sentence_text']:
                                template_with_uncategorized_sentences['outro']['original_sentences'].append(
                                    __val['original_sentence_text'])
                            if __val['parsed_sentence_text']:
                                template_with_uncategorized_sentences['outro']['parsed_sentences'].append(
                                    __val['parsed_sentence_text'])
                            template_with_uncategorized_sentences['outro']['id'].append(
                                __val['sentence_hash'])
                            if __val['sentence_type'] == 'outro_insertable_skills_list_sentence':
                                insertable_skills_list_outro_sentence['original'].append(
                                    __val['original_sentence_text'])
                                insertable_skills_list_outro_sentence['parsed'].append(
                                    __val['parsed_sentence_text'])
                                insertable_skills_list_outro_sentence['id'].append(
                                    __val['sentence_hash'])
                            elif __val['sentence_type'] == 'outro_closing_sentence':
                                outro_sentences['original'].append(
                                    __val['original_sentence_text'])
                                outro_sentences['parsed'].append(
                                    __val['parsed_sentence_text'])
                                outro_sentences['id'].append(
                                    __val['sentence_hash'])

    ### Template with labelled/categorized sentences ###

    template_with_sentences_categorized = {
        'intro': {
            'job_application_intro_sentences': job_application_intro_sentences,
            'conjunction_intro_sentences': conjunction_intro_sentences,
            'insertable_skills_intro_sentences': insertable_skills_intro_sentences,
            'education_intro_sentences': education_intro_sentences,
            'personal_intro_sentences': personal_intro_sentences,
            'discrete_intro_sentences': discrete_intro_sentences
        },
        'body': {
            'conjunction_body_sentences': conjunction_body_sentences,
            'conjunction_insertable_skills_body_sentences': conjunction_insertable_skills_body_sentences,
            'conjunction_skill_body_sentence': conjunction_skill_body_sentence,
            'pre_bullet_pnt_body_sentences': pre_bullet_pnt_body_sentences,
            'bullet_pnt_body_sentences': bullet_pnt_body_sentences,
            'generic_skill_body_sentences': generic_skill_body_sentences,
            'personal_skills_body_sentences': personal_skills_body_sentences,
            'personal_experience_body_sentences': personal_experience_body_sentences,
            'insertable_skills_body_sentences': insertable_skills_body_sentences,
            'discrete_body_sentences': discrete_body_sentences
        },
        'outro': {
            'insertable_skills_list_outro_sentence': insertable_skills_list_outro_sentence,
            'outro_sentences': outro_sentences
        }
    }

    templates = (template_with_sentences_categorized, template_with_uncategorized_sentences, number_of_paragraphs,
                 number_of_characters)

    return templates


def extract_and_categorize_all_sentences(templates):
    ### INTRO SENTENCES ###
    job_application_intro_sentences = []
    conjunction_intro_sentences = []
    insertable_skills_intro_sentences = []
    education_intro_sentences = []
    personal_intro_sentences = []
    discrete_intro_sentences = []

    ### BODY SENTENCES ###
    conjunction_body_sentences = []
    conjunction_insertable_skills_body_sentences = []
    conjunction_skill_body_sentences = []
    pre_bullet_pnt_body_sentences = []
    bullet_pnt_body_sentences = []
    generic_skill_body_sentences = []
    personal_skills_body_sentences = []
    personal_experience_body_sentences = []
    insertable_skills_body_sentences = []
    discrete_body_sentences = []
    education_body_sentences = []

    ### OUTRO SENTENCES ###
    insertable_skills_list_outro_sentences = []
    outro_sentences = []

    for template in templates:
        bullet_points = []
        for key, val in template[0].items():
            if key == 'intro':
                for _key, _val in val.items():
                    sentences = _val['parsed']
                    ids = _val['id']
                    if _key == 'job_application_intro_sentences':
                        for id_ind, sent in enumerate(sentences):
                            job_application_intro_sentences.append((sent, ids[id_ind]))
                    elif _key == 'conjunction_intro_sentences':
                        for sent_ind, sent in enumerate(sentences):
                            preceding_sent = _val['preceding_parsed'][sent_ind]
                            conjunction_intro_sentences.append(((sent, ids[sent_ind]), preceding_sent))
                    elif _key == 'insertable_skills_intro_sentences':
                        for id_ind, sent in enumerate(sentences):
                            insertable_skills_intro_sentences.append((sent, ids[id_ind]))
                    elif _key == 'education_intro_sentences':
                        for id_ind, sent in enumerate(sentences):
                            education_intro_sentences.append((sent, ids[id_ind]))
                    elif _key == 'personal_intro_sentences':
                        for id_ind, sent in enumerate(sentences):
                            personal_intro_sentences.append((sent, ids[id_ind]))
                    elif _key == 'discrete_intro_sentences':
                        for id_ind, sent in enumerate(sentences):
                            discrete_intro_sentences.append((sent, ids[id_ind]))

            elif key == 'body':
                for _key, _val in val.items():
                    sentences = _val['parsed']
                    ids = _val['id']
                    if _key == 'conjunction_body_sentences':
                        for sent_ind, sent in enumerate(sentences):

                            if _val['preceding_parsed']:
                                # print("AHHHH OK: ", _val['preceding_parsed'])
                                preceding_sent = _val['preceding_parsed'][sent_ind]
                                conjunction_body_sentences.append(((sent, ids[sent_ind]), preceding_sent))

                    elif _key == 'conjunction_insertable_skills_body_sentences':
                        for sent_ind, sent in enumerate(sentences):
                            preceding_sent = _val['preceding_parsed'][sent_ind]
                            conjunction_insertable_skills_body_sentences.append(((sent, ids[sent_ind]), preceding_sent))
                    elif _key == 'conjunction_skill_body_sentence':
                        for sent_ind, sent in enumerate(sentences):
                            preceding_sent = _val['preceding_parsed'][sent_ind]
                            conjunction_skill_body_sentences.append(((sent, ids[sent_ind]), preceding_sent))
                    elif _key == 'body_education_sentence':
                        for id_ind, sent in enumerate(sentences):
                            education_body_sentences.append((sent, ids[id_ind]))
                    elif _key == 'pre_bullet_pnt_body_sentences':
                        for id_ind, sent in enumerate(sentences):
                            pre_bullet_pnt_body_sentences.append((sent, ids[id_ind]))
                    elif _key == 'bullet_pnt_body_sentences':
                        for id_ind, sent in enumerate(sentences):
                            bullet_points.append((sent, ids[id_ind]))
                    elif _key == 'generic_skill_body_sentences':
                        for id_ind, sent in enumerate(sentences):
                            generic_skill_body_sentences.append((sent, ids[id_ind]))
                    elif _key == 'personal_skills_body_sentences':
                        for id_ind, sent in enumerate(sentences):
                            personal_skills_body_sentences.append((sent, ids[id_ind]))
                    elif _key == 'personal_experience_body_sentences':
                        for id_ind, sent in enumerate(sentences):
                            personal_experience_body_sentences.append((sent, ids[id_ind]))
                    elif _key == 'insertable_skills_body_sentences':
                        for id_ind, sent in enumerate(sentences):
                            insertable_skills_body_sentences.append((sent, ids[id_ind]))
                    elif _key == 'discrete_body_sentences':
                        for id_ind, sent in enumerate(sentences):
                            discrete_body_sentences.append((sent, ids[id_ind]))
            elif key == 'outro':
                for _key, _val in val.items():
                    sentences = _val['parsed']
                    ids = _val['id']
                    if _key == 'insertable_skills_list_outro_sentence':
                        for id_ind, sent in enumerate(sentences):
                            insertable_skills_list_outro_sentences.append((sent, ids[id_ind]))
                    elif _key == 'outro_sentences':
                        for id_ind, sent in enumerate(sentences):
                            outro_sentences.append((sent, ids[id_ind]))

        bullet_pnt_body_sentences.append(bullet_points)

    intro_sentences = {
        'job_application_intro_sentences': job_application_intro_sentences,
        'conjunction_intro_sentences': conjunction_intro_sentences,
        'insertable_skills_intro_sentences': insertable_skills_intro_sentences,
        'education_intro_sentences': education_intro_sentences,
        'personal_intro_sentences': personal_intro_sentences,
        'discrete_intro_sentences': discrete_intro_sentences
    }

    body_sentences = {
        'education_body_sentences': education_body_sentences,
        'conjunction_body_sentences': conjunction_body_sentences,
        'conjunction_insertable_skills_body_sentences': conjunction_insertable_skills_body_sentences,
        'conjunction_skill_body_sentences': conjunction_skill_body_sentences,
        'pre_bullet_pnt_body_sentences': pre_bullet_pnt_body_sentences,
        'bullet_pnt_body_sentences': bullet_pnt_body_sentences,
        'generic_skill_body_sentences': generic_skill_body_sentences,
        'personal_skills_body_sentences': personal_skills_body_sentences,
        'personal_experience_body_sentences': personal_experience_body_sentences,
        'insertable_skills_body_sentences': insertable_skills_body_sentences,
        'discrete_body_sentences': discrete_body_sentences
    }

    outro_sentences = {
        'insertable_skills_list_outro_sentences': insertable_skills_list_outro_sentences,
        'outro_sentences': outro_sentences
    }

    return intro_sentences, body_sentences, outro_sentences