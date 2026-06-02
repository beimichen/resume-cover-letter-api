import os
import random
import csv
# test
custom_template_intro = \
"""
{generic_intro_opening_sentence}{generic_intro_followup_sentence}{generic_intro_education_sentence}{generic_intro_closing_sentence}
"""

custom_template_outro = \
"""
{generic_opening_outro_sentence}{generic_followup_outro_sentence}{generic_closing_outro_sentence}
"""

custom_body_template = ""

file1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/generic_closing_intro_sentences.tsv')
file2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/generic_closing_outro_sentences.tsv')
file3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/generic_followup_outro_sentences.tsv')
file4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/generic_intro_education_sentences.tsv')
file5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/generic_intro_followup_sentences.tsv')
file6 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/generic_intro_opening_sentences.tsv')
file7 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/generic_opening_outro_sentences.tsv')
file8 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/insert_skills_ability_type_sentences.csv')
file9 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/insert_skills_knowledge_type_sentences.csv')
file10 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/position_specific_generic_discrete_intro_sentences.tsv')
file11 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generic_sentences/generic_body_pre_bullet_point_sentences.tsv')

generic_opening_outro_sentences = []
generic_followup_outro_sentences = []
generic_closing_outro_sentences = []

generic_intro_opening_sentences = []
generic_intro_education_sentences = []
generic_intro_followup_sentences = []
generic_closing_intro_sentences = []

insert_skills_ability_type_sentences = []
insert_skills_knowledge_type_sentences = []
position_specific_generic_discrete_intro_sentences = []
positions_of_position_specific_sentences = []
generic_body_pre_bullet_point_sentences = []

with open(file1, 'r') as r1:
    for row in r1:
        generic_closing_intro_sentences.append(row.strip('\n'))

with open(file2, 'r') as r2:
    for row in r2:
        generic_closing_outro_sentences.append(row.strip('\n'))

with open(file3, 'r') as r3:
    for row in r3:
        generic_followup_outro_sentences.append(row.strip('\n'))

with open(file4, 'r') as r4:
    for row in r4:
        generic_intro_education_sentences.append(row.strip('\n'))

with open(file5, 'r') as r5:
    for row in r5:
        generic_intro_followup_sentences.append(row.strip('\n'))

with open(file6, 'r') as r6:
    for row in r6:
        generic_intro_opening_sentences.append(row.strip('\n'))

with open(file7, 'r') as r7:
    for row in r7:
        generic_opening_outro_sentences.append(row.strip('\n'))

with open(file8, 'r') as r8:
    for row in r8:
        insert_skills_ability_type_sentences.append(row.strip('\n'))

with open(file9, 'r') as r9:
    for row in r9:
        insert_skills_knowledge_type_sentences.append(row.strip('\n'))

with open(file10, 'r') as r10:
    reader = csv.reader(r10, delimiter='\t')
    for row in reader:
        positions_of_position_specific_sentences.append(row[0])
        position_specific_generic_discrete_intro_sentences.append(row[4])

with open(file11, 'r') as r11:
    for row in r11:
        generic_body_pre_bullet_point_sentences.append(row.strip('\n'))


# generic_body_pre_bullet_point_sentences
def generate_skills_sentence(skills, sent_tyoe):
    generic_ability_type_sentences = []
    generic_knowledge_type_sentences = []
    if sent_tyoe == 'skill':
        skills_dropin_replacement = ""
        for skill in skills:
            skills_dropin_replacement += ' ' + skill + ','
        skills_dropin_replacement_formatted = skills_dropin_replacement[1:-1]
        chosen_sent = random.choice(generic_ability_type_sentences)
        updated_skills_sentence = chosen_sent.replace('[skills]', skills_dropin_replacement_formatted)
        return updated_skills_sentence
    elif sent_tyoe == 'knowledge':
        skills_dropin_replacement = ""
        for skill in skills:
            skills_dropin_replacement += ' ' + skill + ','
        skills_dropin_replacement_formatted = skills_dropin_replacement[1:-1]
        chosen_sent = random.choice(generic_knowledge_type_sentences)
        updated_skills_sentence = chosen_sent.replace('[skills]', skills_dropin_replacement_formatted)
        return updated_skills_sentence


def create_custom_intro_paragraph(education_institutions, degrees, fields_of_study, position, company, user_name):
    custom_intro = custom_template_intro
    generic_intro_opening_sentence = random.choice(generic_intro_opening_sentences)
    generic_intro_followup_sentence = random.choice(generic_intro_followup_sentences)
    generic_intro_education_sentence = random.choice(generic_intro_education_sentences)
    generic_closing_intro_sentence = random.choice(generic_closing_intro_sentences)
    custom_intro = custom_intro.replace('{generic_intro_opening_sentence}', generic_intro_opening_sentence.strip() + ' ')
    custom_intro = custom_intro.replace('{generic_intro_followup_sentence}', generic_intro_followup_sentence.strip() + ' ')
    custom_intro = custom_intro.replace('{generic_intro_education_sentence}', generic_intro_education_sentence.strip() + ' ')
    custom_intro = custom_intro.replace('{generic_intro_closing_sentence}', generic_closing_intro_sentence.strip() + ' ')

    if education_institutions:
        if '[edu_institution]' in custom_intro:
            custom_intro = custom_intro.replace('[edu_institution]', education_institutions[-1])
    if degrees and fields_of_study:
        if '[degree]' in custom_intro and '[field]' in custom_intro:
            custom_intro = custom_intro.replace('[degree]', degrees[-1])
            custom_intro = custom_intro.replace('[field]', fields_of_study[-1])
        elif '[degree]' in custom_intro:
            custom_intro = custom_intro.replace('[degree]', degrees[-1])
    elif degrees and not fields_of_study:
        if '[degree]' in custom_intro:
            custom_intro = custom_intro.replace('[degree]', degrees[-1])
    if position:
        if '[position]' in custom_intro:
            custom_intro = custom_intro.replace('[position]', position)
    if company:
        if '[org]' in custom_intro:
            custom_intro = custom_intro.replace('[org]', company)
    if user_name:
        if '[user_name]' in custom_intro:
            custom_intro = custom_intro.replace('[user_name]', user_name)
    return custom_intro


def create_custom_outro_paragraph(position):
    print('creating outro sentences')
    custom_outro = custom_template_outro
    generic_opening_outro_sentence = random.choice(generic_opening_outro_sentences)
    generic_followup_outro_sentence = random.choice(generic_followup_outro_sentences)
    generic_closing_outro_sentence = random.choice(generic_closing_outro_sentences)
    custom_outro = custom_outro.replace('{generic_opening_outro_sentence}', generic_opening_outro_sentence.strip() + ' ')
    custom_outro = custom_outro.replace('{generic_followup_outro_sentence}', generic_followup_outro_sentence.strip() + ' ')
    custom_outro = custom_outro.replace('{generic_closing_outro_sentence}', generic_closing_outro_sentence.strip() + ' ')
    if position:
        custom_outro = custom_outro.replace('[position]', position)
    return custom_outro


def create_custom_body_paragraphs(body_sentences, abilities_sentence, knowledge_sentence, experiences_from_resume, degree_present):

    blacklist_sentences = ['I look forward to discussing the position with you in more detail.']

    education_body_sentences = []

    conjunction_body_sentences = []
    conjunction_body_preceding_sentences = []

    conjunction_insertable_skills_body_sentences = []
    conjunction_insertable_skills_body_preceding_sentences = []

    conjunction_generic_skill_body_sentence = []
    conjunction_generic_skill_preceding_body_sentence = []

    pre_bullet_pnt_body_sentences = []

    bullet_pnt_body_sentences = []

    generic_skill_body_sentences = []

    personal_skills_body_sentences = []

    personal_experience_body_sentences = []

    insertable_skills_body_sentences = []

    discrete_body_sentences = []

    sentences_seen = set()

    # print('BODY SENTENCES:')
    # print(body_sentences)

    print('education_body_sentences')
    if body_sentences['education_body_sentences']:
        # print('education_body_sentences')
        # print(body_sentences['education_body_sentences'])
        for sent in body_sentences['education_body_sentences']:
            # print(sent)
            if sent[1] not in sentences_seen:
                if degree_present and '[degree]' not in sent[0]:
                    education_body_sentences.append(sent[0].strip())
                    sentences_seen.add(sent[1].strip())

    print('conjunction_body_sentences')
    if body_sentences['conjunction_body_sentences']:
        # print('conjunction_body_sentences')
        # print(body_sentences['conjunction_body_sentences'])
        for sent in body_sentences['conjunction_body_sentences']:
            # print(sent)
            if sent[0][0][1] not in sentences_seen:
                conjunction_body_preceding_sentences.append(sent[0][1].strip())
                conjunction_body_sentences.append(sent[0][0][0].strip())
                sentences_seen.add(sent[0][0][1].strip())
    print('conjunction_insertable_skills_body_sentences')
    if body_sentences['conjunction_insertable_skills_body_sentences']:
        # print('conjunction_insertable_skills_body_sentences')
        # print(body_sentences['conjunction_insertable_skills_body_sentences'])
        for sent in body_sentences['conjunction_insertable_skills_body_sentences']:
            # print(sent)
            if sent[0][0][1] not in sentences_seen:
                conjunction_insertable_skills_body_preceding_sentences.append(sent[0][1].strip())
                conjunction_insertable_skills_body_sentences.append(sent[0][0][0].strip())
                sentences_seen.add(sent[0][0][1].strip())
    print('conjunction_skill_body_sentences')
    if body_sentences['conjunction_skill_body_sentences']:
        # print('conjunction_skill_body_sentences')
        # print(body_sentences['conjunction_skill_body_sentences'])
        for sent in body_sentences['conjunction_skill_body_sentences']:
            # print(sent)
            if sent[0][0][1] not in sentences_seen:
                conjunction_generic_skill_preceding_body_sentence.append(sent[0][1].strip())
                conjunction_generic_skill_body_sentence.append(sent[0][0][0].strip())
                sentences_seen.add(sent[0][0][1].strip())
    print('pre_bullet_pnt_body_sentences')
    if body_sentences['pre_bullet_pnt_body_sentences']:
        # print('pre_bullet_pnt_body_sentences')
        # print(body_sentences['pre_bullet_pnt_body_sentences'])
        for sent in body_sentences['pre_bullet_pnt_body_sentences']:
            # print(sent)
            if sent[1] not in sentences_seen:
                pre_bullet_pnt_body_sentences.append(sent[0].strip())
                sentences_seen.add(sent[1].strip())
    print('generic_skill_body_sentences')
    if body_sentences['generic_skill_body_sentences']:
        # print('generic_skill_body_sentences')
        # print(body_sentences['generic_skill_body_sentences'])
        for sent in body_sentences['generic_skill_body_sentences']:
            # print(sent)
            if sent[1] not in sentences_seen:
                generic_skill_body_sentences.append(sent[0].strip())
                sentences_seen.add(sent[1].strip())
    print('personal_skills_body_sentences')
    if body_sentences['personal_skills_body_sentences']:
        # print('personal_skills_body_sentences')
        # print(body_sentences['personal_skills_body_sentences'])
        for sent in body_sentences['personal_skills_body_sentences']:
            # print(sent)
            if sent[1] not in sentences_seen:
                personal_skills_body_sentences.append(sent[0].strip())
                sentences_seen.add(sent[1].strip())
    print('personal_experience_body_sentences')
    if body_sentences['personal_experience_body_sentences']:
        # print('personal_experience_body_sentences')
        # print(body_sentences['personal_experience_body_sentences'])
        for sent in body_sentences['personal_experience_body_sentences']:
            # print(sent)
            if len(sent[0]) > 10:
                if sent[1] not in sentences_seen:
                    personal_experience_body_sentences.append(sent[0].strip())
                    sentences_seen.add(sent[1].strip())
    print('insertable_skills_body_sentences')
    if body_sentences['insertable_skills_body_sentences']:
        # print('insertable_skills_body_sentences')
        # print(body_sentences['insertable_skills_body_sentences'])
        for sent in body_sentences['insertable_skills_body_sentences']:
            # print(sent)
            if sent[1] not in sentences_seen:
                insertable_skills_body_sentences.append(sent[0].strip())
                sentences_seen.add(sent[1].strip())
    print('discrete_body_sentences')
    if body_sentences['discrete_body_sentences']:
        # print('discrete_body_sentences')
        # print(body_sentences['discrete_body_sentences'])
        for sent in body_sentences['discrete_body_sentences']:
            # print(sent)
            if sent[1] not in sentences_seen:
                if 'I look forward to discussing the position with you in more detail.' not in sent[0] and degree_present and '[degree]' not in sent[0]:
                    if len(sent[0]) > 10:
                # if any(s in sent[0] for s in blacklist_sentences):
                        discrete_body_sentences.append(sent[0].strip())
                        sentences_seen.add(sent[1].strip())
                # else:
                #     discrete_body_sentences.append(sent[0].strip())
    print('bullet_pnt_body_sentences')
    if body_sentences['bullet_pnt_body_sentences']:
        # print('bullet_pnt_body_sentences')
        # print(body_sentences['bullet_pnt_body_sentences'])
        for bullet_pnt_collection in body_sentences['bullet_pnt_body_sentences']:
            bullet_points = []
            if bullet_pnt_collection:
                for sent in bullet_pnt_collection:
                    # print(sent)
                    if sent:
                        if sent[1] not in sentences_seen:
                            bullet_points.append(sent[0].strip())
                            sentences_seen.add(sent[1].strip())
                if bullet_points:
                    bullet_pnt_body_sentences.append(bullet_points)

    print('finished filtering body sentences')

    body_first_paragraph = ""

    if education_body_sentences and degree_present is False:
        random_sent = random.choice(education_body_sentences)
        education_body_sentences.remove(random_sent)
        body_first_paragraph += random_sent + ' '
    print('finished choosing random education body sentence')

    if len(discrete_body_sentences) >= 3:
        for i in range(3):
            random_sent = random.choice(discrete_body_sentences)
            discrete_body_sentences.remove(random_sent)
            body_first_paragraph += random_sent + ' '
    elif len(discrete_body_sentences) == 2:
        for i in range(2):
            random_sent = random.choice(discrete_body_sentences)
            discrete_body_sentences.remove(random_sent)
            body_first_paragraph += random_sent + ' '
    elif len(discrete_body_sentences) == 1:
        body_first_paragraph += discrete_body_sentences[0] + ' '
    print('finished choosing random discrete body sentence')

    if conjunction_generic_skill_body_sentence:
        random_sent = random.choice(conjunction_generic_skill_body_sentence)
        preceding_random_sent_index = conjunction_generic_skill_body_sentence.index(random_sent)
        conjunction_generic_skill_body_sentence.remove(random_sent)
        preceding_random_sent = conjunction_generic_skill_preceding_body_sentence[preceding_random_sent_index]
        body_first_paragraph += preceding_random_sent + ' '
        body_first_paragraph += random_sent + ' '
    elif conjunction_body_sentences:
        random_sent = random.choice(conjunction_body_sentences)
        preceding_random_sent_index = conjunction_body_sentences.index(random_sent)
        conjunction_body_sentences.remove(random_sent)
        preceding_random_sent = conjunction_body_preceding_sentences[preceding_random_sent_index]
        body_first_paragraph += preceding_random_sent + ' '
        body_first_paragraph += random_sent + ' '
    print('finished choosing random generic body sentence')

    if generic_skill_body_sentences:
        random_sent = random.choice(generic_skill_body_sentences)
        generic_skill_body_sentences.remove(random_sent)
        body_first_paragraph += random_sent + ' '
    elif personal_skills_body_sentences:
        random_sent = random.choice(personal_skills_body_sentences)
        personal_skills_body_sentences.remove(random_sent)
        body_first_paragraph += random_sent + ' '
    elif personal_experience_body_sentences:
        random_sent = random.choice(personal_experience_body_sentences)
        personal_experience_body_sentences.remove(random_sent)
        body_first_paragraph += random_sent + ' '
    print('finished choosing random generic skill body sentence')

    if not abilities_sentence and not knowledge_sentence:
        if conjunction_insertable_skills_body_sentences:
            random_sent = random.choice(conjunction_insertable_skills_body_sentences)
            preceding_random_sent_index = conjunction_insertable_skills_body_sentences.index(random_sent)
            conjunction_insertable_skills_body_sentences.remove(random_sent)
            preceding_random_sent = conjunction_insertable_skills_body_preceding_sentences[preceding_random_sent_index]
            body_first_paragraph += preceding_random_sent + ' '
            body_first_paragraph += random_sent + ' '
        elif insertable_skills_body_sentences:
            random_sent = random.choice(insertable_skills_body_sentences)
            insertable_skills_body_sentences.remove(random_sent)
            body_first_paragraph += random_sent + ' '
    else:
        if abilities_sentence:
            # print('abilities_sentence')
            # print(abilities_sentence)
            body_first_paragraph += abilities_sentence + ' '
        if knowledge_sentence:
            # print('knowledge_sentence')
            # print(knowledge_sentence)
            body_first_paragraph += knowledge_sentence + ' '

    print('finished choosing random abilities and knowledge body sentence')

    body_first_paragraph = body_first_paragraph + '\n\n'

    body_second_paragraph = ""

    if experiences_from_resume:
        all_dot_points = []
        for exp in experiences_from_resume:
            if '•' in exp:
                exp_dot_points = exp.split('•')
                for dot_pnt in exp_dot_points:
                    all_dot_points.append(dot_pnt)
    else:
        all_dot_points = None

    if all_dot_points:
        random_sent = random.choice(generic_body_pre_bullet_point_sentences)
        body_second_paragraph += random_sent + '\n'
        for dot_pnt in all_dot_points:
            body_second_paragraph += '•' + dot_pnt + '\n'
    else:
        print('no bullet points from resume. choosing random bullet points from templates')
        if pre_bullet_pnt_body_sentences and bullet_pnt_body_sentences:
            random_sent = random.choice(pre_bullet_pnt_body_sentences)
            body_second_paragraph += random_sent + '\n'
            bullet_pnt_index = pre_bullet_pnt_body_sentences.index(random_sent)
            bullet_points = bullet_pnt_body_sentences[bullet_pnt_index]
            for bullet_pnt in bullet_points:
                body_second_paragraph += '•' + bullet_pnt + '\n'
            print('finished choosing random pre point sentences')

    body_second_paragraph = body_second_paragraph

    return [body_first_paragraph, body_second_paragraph]
