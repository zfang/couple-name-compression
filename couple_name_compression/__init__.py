import os
from collections import defaultdict, OrderedDict

current_dir = os.path.dirname(os.path.abspath(__file__))

FILES = {
    'last': 'dist.all.last',
    'female': 'dist.female.first',
    'male': 'dist.male.first',
}

vowels = 'aeiouy'

digraphs = ('ch', 'sh', 'th', 'wh', 'ph')


def load_name_db():
    name_db = defaultdict(OrderedDict)
    for key, file_path in FILES.items():
        with open('/'.join((current_dir, file_path)), 'r', encoding='utf-8') as f:
            for line in f:
                name, freq_percentage, cumulative_freq_percentage, rank = line.split()
                name_db[key][name.lower()] = {
                    'freq_percentage': float(freq_percentage),
                    'cumulative_freq_percentage': float(cumulative_freq_percentage),
                    'rank': int(rank),
                }
    return name_db


def get_prefixes(original_name, names_dict, end_with_vowel=False):
    names = []

    for i in range(1, len(original_name)):
        candidate = original_name[:-i]
        if end_with_vowel != ends_with_vowel(candidate):
            continue

        if original_name[-i - 1:-i + 1 or len(original_name)] in digraphs:
            continue

        current_cost = 0
        for key, data in names_dict.items():
            if key != original_name and key.startswith(candidate):
                current_cost += data['freq_percentage']

        names.append((candidate, current_cost))

    return names


def get_suffixes(original_name, names_dict, start_with_vowel=False):
    names = []

    for i in range(1, len(original_name)):
        candidate = original_name[i:]
        if start_with_vowel != starts_with_vowel(candidate):
            continue

        if original_name[i - 1:i + 1] in digraphs:
            continue

        current_cost = 0
        for key, data in names_dict.items():
            if key != original_name and key.endswith(candidate):
                current_cost += data['freq_percentage']

        names.append((candidate, current_cost))

    return names


def compute_reconstruction_cost(compressed_name, name1, name2, prefix_dict, suffix_dict):
    tuples = []

    for i in range(1, len(compressed_name)):
        prefix = compressed_name[:i]
        possible_names_with_prefix = [(key, data['freq_percentage'])
                                      for key, data in prefix_dict.items()
                                      if key != name1 and key.startswith(prefix)]
        suffix = compressed_name[i:]
        possible_names_with_suffix = [(key, data['freq_percentage'])
                                      for key, data in suffix_dict.items()
                                      if key != name2 and key.endswith(suffix)]

        for p, freq1 in possible_names_with_prefix:
            for s, freq2 in possible_names_with_suffix:
                tuples.append((p, s, freq1 * freq2))

    return tuples


def count_syllables(text):
    return len([c for c in text.lower() if c in vowels])


def ends_with_vowel(text):
    return len(text) > 0 and text[-1] in vowels


def starts_with_vowel(text):
    return len(text) > 0 and text[0] in vowels
