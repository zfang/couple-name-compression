import argparse
import json
from collections import OrderedDict
from operator import itemgetter

from couple_name_compression import get_prefixes, get_suffixes, load_name_db, compute_reconstruction_cost

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
    name1 = args.__dict__[key1].lower()
    name2 = args.__dict__[key2].lower()
    names = []
    for arg1 in (True, False):
        for arg2 in (False, True):
            prefixes = get_prefixes(name1, db1, end_with_vowel=arg1)
            suffixes = get_suffixes(name2, db2, start_with_vowel=arg2)
            for prefix, cost1 in prefixes:
                for suffix, cost2 in suffixes:
                    name = prefix + suffix
                    if name == name1 or name == name2:
                        continue
                    compressed_name = name.capitalize()
                    names.append(OrderedDict({
                        'name': compressed_name,
                        'total_cost': cost1 + cost2,
                        'reconstruction_cost': sum(
                            freq for _, _, freq in compute_reconstruction_cost(name, name1, name2, db1, db2)),
                    }))
    names = sorted(names, key=itemgetter('total_cost', 'reconstruction_cost'))
    result[result_key] = names

print(json.dumps(result, indent=4))
