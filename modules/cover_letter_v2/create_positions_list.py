file = 'positions_lookup.csv'
file2 = 'positions.tsv'

positions = []

with open(file, 'r') as r:
    for row in r:
        _positions = row.split(',')
        positions.append(_positions[0])

positions2 = []

with open(file2, 'r') as r2:
    for row in r2:
        positions2.append(row.strip('\n'))

position_all = positions + positions2

with open('positions2.tsv', 'w') as w:
    for p in position_all:
        w.write(p + '\n')