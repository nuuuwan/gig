import unittest

from gig import Ent

TEST_SUBS = '''
    ['EC-01H', 'EC-01I', 'EC-01J', 'EC-01K', 'EC-01M',
    'EC-01N', 'EC-01O', 'LG-11031', 'LG-11090', 'LG-11121',
    'LG-11210', 'LG-11240', 'LG-11301', 'LG-11330', 'LK-1106',
    'LK-1109', 'LK-1121', 'LK-1124', 'LK-1133', 'LK-1136',
    'MOH-11031', 'MOH-11060', 'MOH-11212', 'MOH-11330']
'''

TEST_D = dict(
    id='LK-11',
    name='Colombo',
    area='642.00',
    population='2323964',
    centroid_altitude='8',
    centroid='[6.869636028857, 80.01959786729992]',
    subs=TEST_SUBS,
    supers="['LK']",
    eqs="['LK-1']",
    ints="[]",
)


class TestEntBase(unittest.TestCase):
    def test_init(self):
        ent = Ent(TEST_D)
        self.assertEqual(ent.id, 'LK-11')
        self.assertEqual(ent.name, 'Colombo')
        self.assertTrue(ent.is_parent_id('LK-1'))
        self.assertFalse(ent.is_parent_id('LK-1125'))

        self.assertEqual(len(str(ent)), 519)
        self.assertEqual(str(ent)[:10], "{'id': 'LK")

    def test_acronym_and_short_name(self):
        for id, expected_acronym, expected_short_name in [
            ['LK-11', 'C', 'Clmb'],
            ['LG-11001', 'CMC', 'Clmb MC'],
            ['LG-11005', 'HPS', 'Hmgm PS'],
            ['LG-11009', 'SJKMC', 'Sr Jywrdnpr Ktt MC'],
            ['LG-11010', 'DMLMC', 'Dhwl MtLvn MC'],
        ]:
            ent = Ent.from_id(id)
            self.assertEqual(ent.acronym, expected_acronym)
            self.assertEqual(ent.short_name, expected_short_name)
