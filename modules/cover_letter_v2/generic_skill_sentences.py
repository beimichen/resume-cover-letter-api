import os
import random

recruitment_titles = [
    'recruitment manager',
    'head of recruitment',
    'employment manager'
]


def generate_skills_sentence(skills, sent_type, company, generic_ability_type_sentences,
                             generic_knowledge_type_sentences):
    if sent_type == 'skill':
        skills_dropin_replacement = ""
        for skill in skills:
            skills_dropin_replacement += ' ' + skill + ','
        skills_dropin_replacement_formatted = skills_dropin_replacement[1:-1]
        chosen_sent = random.choice(generic_ability_type_sentences)
        updated_skills_sentence = chosen_sent.replace('[skills]', skills_dropin_replacement_formatted)
        updated_skills_sentence = updated_skills_sentence.replace('[org]', company)
        return updated_skills_sentence
    elif sent_type == 'knowledge':
        skills_dropin_replacement = ""
        for skill in skills:
            skills_dropin_replacement += ' ' + skill + ','
        skills_dropin_replacement_formatted = skills_dropin_replacement[1:-1]
        chosen_sent = random.choice(generic_knowledge_type_sentences)
        updated_skills_sentence = chosen_sent.replace('[skills]', skills_dropin_replacement_formatted)
        updated_skills_sentence = updated_skills_sentence.replace('[org]', company)
        return updated_skills_sentence
