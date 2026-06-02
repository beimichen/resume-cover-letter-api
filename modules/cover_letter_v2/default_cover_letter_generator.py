import csv
import os
import random
from pprint import pprint
from modules.cover_letter_v2.generic_templates import conclusion_sentences, \
    outro_sentences, recruitment_titles, intro_sentences, body_sentences, sign_offs

def generate_default_coverletter(hiring_manager_name):

    coverletter = []

    if hiring_manager_name:
        intro_1 = "Dear John, "
    else:
        intro_1 = "Dear " + random.choice(recruitment_titles)

    coverletter.append(intro_1)

    intro2 = random.choice(intro_sentences)
    coverletter.append(intro2)

    chosen_body_sentences = random.choices(body_sentences, k=4)


    body = ""
    for i in chosen_body_sentences:
        body = body + i + " "

    coverletter.append(body)

    outro_1 = random.choice(outro_sentences)
    coverletter.append(outro_1)
    outro_2 = random.choice(conclusion_sentences)
    coverletter.append(outro_2)
    sign_off = random.choice(sign_offs)
    coverletter.append(sign_off)

    pprint(coverletter)

    return "\n".join(coverletter)

if __name__ == '__main__':
    pprint(generate_default_coverletter("John Doe"), width=1000)

