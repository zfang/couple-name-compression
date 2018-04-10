import argparse
import json
from operator import itemgetter
from collections import OrderedDict

from couple_name_compression import get_prefix, get_suffix, load_name_db, compute_reconstruction_cost

parser = argparse.ArgumentParser(description='Get couple name compression')
parser.add_argument('--female', required=True, help='female name')
parser.add_argument('--male', required=True, help='male name')
args = parser.parse_args()

name_db = load_name_db()
female_name_db = name_db['female']
male_name_db = name_db['male']

result = {}
for key1, key2 in [('female', 'male'), ('male', 'female')]:
    result_key = '{}_{}'.format(key1, key2)
    db1 = name_db[key1]
    db2 = name_db[key2]
    names = []
    for arg1, arg2 in [(True, False), (False, True), (True, True)]:
        name = (get_prefix(args.__dict__[key1], db1, end_with_vowel=arg1) + get_suffix(args.__dict__[key2], db2, start_with_vowel=arg2)).capitalize()
        names.append(OrderedDict({
            'name': name,
            'reconstruction_cost': len(compute_reconstruction_cost(name, db1, db2)),
        }))
    names = sorted(names, key=itemgetter('reconstruction_cost'))
    result[result_key] = names

print(json.dumps(result, indent=4))
