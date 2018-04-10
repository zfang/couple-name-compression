import os
from collections import defaultdict, OrderedDict

current_dir = os.path.dirname(os.path.abspath(__file__))

FILES = {
    'last': 'dist.all.last',
    'female': 'dist.female.first',
    'male': 'dist.male.first',
}

vowels = 'aeiouy'


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


def get_prefix(original_name, names_dict, end_with_vowel=False):
    original_name = original_name.lower()
    name = None
    cost = len(names_dict)

    for i in range(1, len(original_name)):
        candidate = original_name[:-i]
        if end_with_vowel != ends_with_vowel(candidate):
            continue

        current_cost = 0
        for key in names_dict.keys():
            if key.startswith(candidate):
                current_cost += 1

        if current_cost <= cost:
            name = candidate
            cost = current_cost

    return name


def get_suffix(original_name, names_dict, start_with_vowel=False):
    original_name = original_name.lower()
    name = None
    cost = len(names_dict)

    for i in range(1, len(original_name)):
        candidate = original_name[i:]
        if start_with_vowel != starts_with_vowel(candidate):
            continue

        current_cost = 0
        for key in names_dict.keys():
            if key.endswith(candidate):
                current_cost += 1

        if current_cost <= cost:
            name = candidate
            cost = current_cost

    return name


def compute_reconstruction_cost(compressed_name, prefix_dict, suffix_dict):
    compressed_name = compressed_name.lower()
    tuples = []

    for i in range(1, len(compressed_name)):
        prefix = compressed_name[:i]
        possible_names_with_prefix = [key for key in prefix_dict.keys() if key.startswith(prefix)]
        suffix = compressed_name[i:]
        possible_names_with_suffix = [key for key in suffix_dict.keys() if key.endswith(suffix)]

        for p in possible_names_with_prefix:
            for s in possible_names_with_suffix:
                tuples.append((p, s))

    return tuples


def count_syllables(text):
    return len([c for c in text.lower() if c in vowels])


def ends_with_vowel(text):
    return len(text) > 0 and text[-1] in vowels


def starts_with_vowel(text):
    return len(text) > 0 and text[0] in vowels
