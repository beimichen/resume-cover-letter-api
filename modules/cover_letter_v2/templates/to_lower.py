import json

with open('cover_letter_sentences_v12.json') as f:
    data = json.load(f)

output = {}
c = 0
for k,v in data.items():
    print(k)
    c += 1
    print(c)
    low = k.lower().strip()
    output[low] = v

import csv

with open('lowered.json', 'w', newline='', encoding='utf-8') as f:
    json.dump(output, f, indent=4)



