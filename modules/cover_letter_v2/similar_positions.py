import os

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'similar_positions_v2.csv')

similar_positions = []
positions = []
positions_indices = []


with open(file, 'r') as r:
    for i, row in enumerate(r):
        _positions = row.strip('\n').split(',')
        similar_positions.append(_positions)
        for position in _positions:
            positions_indices.append(i)
            positions.append(position)


def find_similar_positions(position):
    if position.lower() in positions:
        index_of_found_position = positions.index(position.lower())
        index_of_similar_positions = positions_indices[index_of_found_position]
        similar_positions_found = similar_positions[index_of_similar_positions]
        return similar_positions_found
    else:
        return None


if __name__ == '__main__':
    similar_positions = find_similar_positions('A And P Mechanic')
    print(similar_positions)