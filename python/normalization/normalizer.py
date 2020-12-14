import csv
from operator import itemgetter
from difflib import SequenceMatcher
from itertools import chain, combinations
from pprint import pprint


class Normalizer(object):
    def __init__(self):
        self.manifest_dict = {}

    def read_manifest(self, manifest):
        """reads a manifest file

        manifest should be a CSV containing the following columns
            * section_id
            * section_name
            * row_id
            * row_name

        Arguments:
            manifest {[str]} -- /path/to/manifest
        """

        self.manifest_dict.clear()

        with open(manifest, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for i, csv_row in enumerate(csv_reader):
                if i > 0:
                    section_id, section_name, row_id, row_name = csv_row

                    if section_id and section_name:
                        sl_section_name = section_name.strip().lower()

                        if not row_id and not row_name:
                            self.manifest_dict[sl_section_name] = {'section_id': int(section_id), 'rows': None}

                        elif row_id and row_name:
                            n_row_name = self.normalize_row(row_name)

                            if sl_section_name in self.manifest_dict:
                                section_data = self.manifest_dict[sl_section_name]

                                if 'section_id' not in section_data:
                                    section_data['section_id'] = int(section_id)

                                if 'rows' not in section_data or not section_data['rows']:
                                    section_data['rows'] = {n_row_name: int(row_id)}
                                else:
                                    section_data['rows'][n_row_name] = int(row_id)
                            else:
                                self.manifest_dict[sl_section_name] = {
                                    'section_id': int(section_id),
                                    'rows': {
                                        n_row_name: int(row_id)
                                    }
                                }
                    else:
                        raise ValueError('Invalid CSV file format.')

    def normalize(self, section, row):
        """normalize a single (section, row) input

        Given a (Section, Row) input, returns (section_id, row_id, valid)
        where
            section_id = int or None
            row_id = int or None
            valid = True or False

        Arguments:
            section {[type]} -- [description]
            row {[type]} -- [description]
        """

        if not row:  # suite section
            n_section = self.normalize_suite(section)
            if n_section in self.manifest_dict:
                section_data = self.manifest_dict[n_section]
                section_id = section_data['section_id']

                return section_id, None, True

            return None, None, False

        # normal section
        existing_section = self.query_section(section)
        if existing_section:
            section_data = self.manifest_dict[existing_section]
            section_id = section_data['section_id']

            existing_row = self.query_section_row(existing_section, row)
            if existing_row and section_data['rows']:
                rows = section_data['rows']
                row_id = rows[existing_row]
                return section_id, row_id, True

            return section_id, None, False

        return None, None, False

    def query_section(self, section_name):
        sl_section_name = section_name.strip().lower()
        for section in self.manifest_dict:
            if self.sections_equal(section, sl_section_name):
                return section
        return None

    def sections_equal(self, s1, s2):
        if s1 == s2:
            return True

        dict_attrs = (
            'preceding_phrase',
            'prefix',
            'digits',
            'suffix',
            'following_phrase',)

        features1 = self.extract_section_features(s1)
        preceding_phrase1, prefix1, digits1, suffix1, following_phrase1 = itemgetter(*dict_attrs)(features1)
        features2 = self.extract_section_features(s2)
        preceding_phrase2, prefix2, digits2, suffix2, following_phrase2 = itemgetter(*dict_attrs)(features2)

        # first check that extracted digits matches
        if digits1 == digits2:

            # if one of the sections only feature is the digits return true
            if (not preceding_phrase1 and not prefix1 and not suffix1 and not following_phrase1) or \
                    (not preceding_phrase2 and not prefix2 and not suffix2 and not following_phrase2):
                return True

            for phrase1 in [preceding_phrase1, following_phrase1]:
                for phrase2 in [preceding_phrase2, following_phrase2]:
                    if phrase1 and phrase2 and phrases_equal(phrase1, phrase2):
                        return True
                for abr2 in [prefix2, suffix2]:
                    if phrase1 and abr2 and phrase_equals_abbreviation(phrase1, abr2):
                        return True

            for abr1 in [prefix1, suffix1]:
                for phrase2 in [preceding_phrase2, following_phrase2]:
                    if abr1 and phrase2 and phrase_equals_abbreviation(phrase2, abr1):
                        return True
                for abr2 in [prefix2, suffix2]:
                    if abr1 and abr2 and abbreviations_equal(abr1, abr2):
                        return True
        return False

    def extract_section_features(self, section):
        features = {'preceding_phrase': '', 'prefix': '', 'digits': '', 'suffix': '', 'following_phrase': ''}

        # separate by white spaces
        chunks = section.strip().lower().split()
        found_digit = False
        preceding_words = []
        following_words = []

        # find first chunk with digits
        for chunk in chunks:
            if found_digit:
                following_words.append(chunk)
            else:
                if any(char.isdigit() for char in chunk):
                    prefix, digits, suffix = self.extract_word_features(chunk)
                    features['prefix'] = prefix
                    features['digits'] = digits
                    features['suffix'] = suffix
                    found_digit = True
                else:
                    preceding_words.append(chunk)

        features['preceding_phrase'] = ' '.join(preceding_words)
        features['following_phrase'] = ' '.join(following_words)

        return features

    @staticmethod
    def extract_word_features(word):
        prefix = []
        digits = []
        suffix = []
        # find first contiguous string of digits
        found_first_digit = False
        for c in word:
            if c.isdigit():
                digits.append(c)
                found_first_digit = True
            elif found_first_digit:
                suffix.append(c)
            else:
                prefix.append(c)

        return ''.join(prefix), ''.join(digits), ''.join(suffix)

    def query_section_row(self, section, row_name):
        assert section in self.manifest_dict
        section_data = self.manifest_dict[section]
        if 'rows' not in section_data or not section_data['rows']:
            return None
        rows = section_data['rows']
        for row in rows:
            if self.rows_equal(row, row_name):
                return row
        return None

    def rows_equal(self, row1, row2):
        return self.normalize_row(row1) == self.normalize_row(row2)

    @staticmethod
    def normalize_suite(suite):
        """normalizes a suite section by stripping white space and converting to lowercase"""
        return suite.strip().lower()

    def normalize_row(self, row):
        row = row.strip().lower()

        # exclude any ranges
        if '-' in row:
            return row

        chunks = row.split()

        # find first chunk that is either all digits, or one/two letters
        for chunk in chunks:
            if all(char.isdigit() for char in chunk):  # all digits
                return chunk
            elif len(chunk) <= 2 and all(char.isalpha() for char in chunk):  # one/two letters
                return chunk
            elif any(char.isdigit() for char in chunk):  # 37wc case
                _, digits, _ = self.extract_word_features(chunk)
                return digits

        # fall back on returning original string
        return row


def generate_acronym(phrase):
    return ''.join(s[0].lower() for s in phrase.split())


def phrase_equals_abbreviation(phrase, abr, strict=False):
    acronym = generate_acronym(phrase)
    if acronym == abr:
        return True

    if not strict:
        sequence = SequenceMatcher(None, acronym, abr)
        # print(acronym, abr, sequence.ratio())
        if sequence.ratio() >= .6:
            return True

        # handle case where abbreviation is shortened/missing letters and/or switched around
        # ex: left field pavilion === pl, right field pavilion === pr
        ordered_perms = ordered_permutations(acronym)
        # print(list(ordered_perms))
        if tuple(abr) in ordered_perms:
            return True

        r_ordered_perms = ordered_permutations(reversed(acronym))
        # print(list(r_ordered_perms))
        if tuple(abr) in r_ordered_perms:
            return True

    words = phrase.split()
    i = 0
    for word in words:
        for j, c in enumerate(word):
            if i >= len(abr):
                break
            # the first letter of a word must be matched
            if c == abr[i]:
                i += 1
            else:
                if strict and j == 0:
                    return False

    return i == len(abr)


def phrases_equal(phrase1, phrase2, strict=False):
    if not strict:
        if phrase1 in phrase2 or phrase2 in phrase1:
            return True

    sequence = SequenceMatcher(None, phrase1, phrase2)
    return sequence.ratio() >= 0.75


def abbreviations_equal(abr1, abr2):
    sequence = SequenceMatcher(None, abr1, abr2)
    return sequence.ratio() >= 0.8


def powerset(iterable):
    lst = list(iterable)
    return chain.from_iterable(combinations(lst, r) for r in range(1, len(lst) + 1))


def ordered_permutations(iterable):
    pset = powerset(iterable)
    s = set()
    for x in pset:
        s.add(tuple(sorted(x)))
    return s
