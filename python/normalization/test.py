from normalizer import Normalizer, phrase_equals_abbreviation, phrases_equal
import unittest
import json
from normalize import read_input, normalize_samples


class TestNormalizer(unittest.TestCase):

    def test_normalize_suite(self):
        self.assertEqual(Normalizer.normalize_suite('Sterling Suite 6'), 'sterling suite 6')
        self.assertEqual(Normalizer.normalize_suite('Empire Suite 235'), 'empire suite 235')
        self.assertEqual(Normalizer.normalize_suite('Suite 221	'), 'suite 221')
        self.assertEqual(Normalizer.normalize_suite('Emc Suite Left 20	'), 'emc suite left 20')
        self.assertEqual(Normalizer.normalize_suite('Green Monster Sro	'), 'green monster sro')

    def test_extract_section_features(self):
        normalizer = Normalizer()
        self.assertEqual(normalizer.extract_section_features('136'), generate_feature(d='136'))
        self.assertEqual(normalizer.extract_section_features('Reserve 40	'), generate_feature(pp="reserve", d='40'))
        self.assertEqual(normalizer.extract_section_features('Top Deck 6	'), generate_feature(pp="top deck", d='6'))
        self.assertEqual(normalizer.extract_section_features('31RS	'), generate_feature(d='31', s='rs'))
        self.assertEqual(normalizer.extract_section_features('Left Field Pavilion 311'),
                         generate_feature(pp='left field pavilion', d='311'))
        self.assertEqual(normalizer.extract_section_features('Infield Reserve IFR7	'),
                         generate_feature(pp='infield reserve', p='ifr', d='7'))
        self.assertEqual(normalizer.extract_section_features('311PL'), generate_feature(d='311', s='pl'))
        self.assertEqual(normalizer.extract_section_features('F9'), generate_feature(p='f', d='9'))
        self.assertEqual(normalizer.extract_section_features('L36'), generate_feature(p='l', d='36'))

    def test_normalize_row(self):
        normalizer = Normalizer()
        self.assertEqual(normalizer.normalize_row('a'), 'a')
        self.assertEqual(normalizer.normalize_row('B'), 'b')
        self.assertEqual(normalizer.normalize_row('1'), '1')
        self.assertEqual(normalizer.normalize_row('Row C'), 'c')
        self.assertEqual(normalizer.normalize_row('row 12'), '12')
        self.assertEqual(normalizer.normalize_row('r31'), '31')
        self.assertEqual(normalizer.normalize_row('Cc'), 'cc')
        self.assertEqual(normalizer.normalize_row('37Wc '), '37')
        self.assertEqual(normalizer.normalize_row('A-Z	'), 'a-z')
        self.assertEqual(normalizer.normalize_row('AA-XX	'), 'aa-xx')
        self.assertEqual(normalizer.normalize_row('1-10	'), '1-10')

    def test_phrase_equals_abbreviation(self):
        self.assertTrue(phrase_equals_abbreviation('reserve', 'rs'))
        self.assertTrue(phrase_equals_abbreviation('left field pavilion', 'pl'))
        self.assertTrue(phrase_equals_abbreviation('right field pavilion', 'pr'))

    def test_phrase_equal(self):
        self.assertTrue(phrases_equal('right field pavilion', 'pavilion'))

    def test_mets(self):
        invalid_matches = get_invalid_matches(
            manifest='../../manifests/citifield_sections.csv',
            input='../../samples/metstest.csv'
        )
        for match in invalid_matches:
            print(json.dumps(match))
        self.assertEqual(len(invalid_matches), 0)

    def test_dodgers(self):
        invalid_matches = get_invalid_matches(
            manifest='../../manifests/dodgerstadium_sections.csv',
            input='../../samples/dodgertest.csv'
        )
        for match in invalid_matches:
            print(json.dumps(match))
        self.assertEqual(len(invalid_matches), 0)

    def test_redsox(self):
        invalid_matches = get_invalid_matches(
            manifest='../../gradesamples/fenwaypark_sections.csv',
            input='../../gradesamples/redsoxgrade.csv'
        )
        for match in invalid_matches:
            print(json.dumps(match))
        self.assertEqual(len(invalid_matches), 0)


def generate_feature(pp='', p='', d='', s='', fp=''):
    """util function to generate feature dict"""
    return {
        'preceding_phrase': pp,
        'prefix': p,
        'digits': d,
        'suffix': s,
        'following_phrase': fp
    }


def get_invalid_matches(manifest, input):
    """util function to return any invalid matches when running through a test file"""
    normalizer = Normalizer()
    normalizer.read_manifest(manifest)
    samples = read_input(input)

    matched = normalize_samples(normalizer, samples, verbose=False)

    invalid_matches = [match for match in matched if match['expected'] != match['output']]

    return invalid_matches


if __name__ == '__main__':
    unittest.main()
