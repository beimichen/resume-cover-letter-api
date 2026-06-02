# def is_camel_case(s):
#     return s != s.lower() and s != s.upper() and "_" not in s
#
#
# def has_numbers(input):
#     return any(char.isdigit() for char in input)
#
#
# file = 'hard_skills.tsv'
#
# from nltk.corpus import wordnet as wn
#
# skills = []
#
# with open(file, 'r') as r:
#     for row in r:
#         position = row.strip('\n')
#         if len(position.split(' ')) == 1:
#             if is_camel_case(position) is False and has_numbers(
#                     position) is False and position.isupper() is False and '-' not in position:
#                 skills.append(row.strip('\n'))
#
# all_skills = []
#
# with open(file, 'r') as r2:
#     for row in r2:
#         position = row.strip('\n')
#         all_skills.append(position)
#
# pos_all = dict()
# for w in skills:
#     pos_l = set()
#     for tmp in wn.synsets(w):
#         if tmp.name().split('.')[0] == w:
#             pos_l.add(tmp.pos())
#     if w[-3:] != 'ing' and w[-3:] != 'try' and w[-3:] != 'ics' and w[:-3] != 'ogy' and w[-3:] != 'ery' and w[
#                                                                                                            -3:] != 'phy':
#         pos_all[w] = pos_l
#
# filtered = []
#
# for key, val in pos_all.items():
#     if len(val) > 0:
#         if 'n' in val and 'v':
#             _key = key[-3:]
#             if _key != 'ing' and _key != 'try' and _key != 'ics' and _key != 'ogy' and _key != 'ery' and _key != 'phy' \
#                     and _key != 'dia' and _key != 'apy' and _key != 'thy' and _key != 'sis' and key != 'scrum' and \
#                     _key != 'opy' and 'medicine' not in key and key != 're':
#                 filtered.append(key)
#
# # {'v'} {'s'} {'a'}
# print(filtered)
#
#
# with open('updated_hard_skills.tsv', 'w') as w:
#     for skill in all_skills:
#         if skill not in filtered:
#             w.write(skill + '\n')
#
# # accounting
#
#
# # amuse
# # alba
# # attempt
# # alba
# # argument
# # balance
# # bargain
# # bristle
# # bristles
# # board
# # cameras
# # craft
# # controllers
# # current
# # casts
# # chip
# # detect
# # dies
# # diet
# # fiction
# # filters
# # flint
# # helmet
# # helmets
