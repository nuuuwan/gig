import unittest

from test_ent_base import TEST_D

from gig import Ent, EntType

TEST_EXPECTED_SUBS = [
    'EC-01H',
    'EC-01I',
    'EC-01J',
    'EC-01K',
    'EC-01M',
    'EC-01N',
    'EC-01O',
    'LG-11031',
    'LG-11090',
    'LG-11121',
    'LG-11210',
    'LG-11240',
    'LG-11301',
    'LG-11330',
    'LK-1106',
    'LK-1109',
    'LK-1121',
    'LK-1124',
    'LK-1133',
    'LK-1136',
    'MOH-11031',
    'MOH-11060',
    'MOH-11212',
    'MOH-11330',
]


class TestEntLoadMixin(unittest.TestCase):
    def test_from_dict(self):
        ent = Ent.from_dict(TEST_D)
        self.assertEqual(ent.id, 'LK-11')
        self.assertEqual(ent.name, 'Colombo')
        self.assertEqual(ent.area, 642.00)
        self.assertEqual(ent.population, 2323964)
        self.assertEqual(ent.centroid_altitude, 8)
        self.assertEqual(ent.centroid, [6.869636028857, 80.01959786729992])

        self.assertEqual(ent.lnglat, [80.01959786729992, 6.869636028857])
        self.assertEqual(
            ent.subs,
            TEST_EXPECTED_SUBS,
        )
        self.assertEqual(ent.supers, ['LK'])
        self.assertEqual(ent.eqs, ['LK-1'])
        self.assertEqual(ent.ints, [])

    def test_list_from_type(self):
        ent_list = Ent.list_from_type(EntType.PROVINCE)
        self.assertEqual(len(ent_list), 9)
        self.assertEqual(ent_list[0].id, 'LK-1')

    def test_idx_from_type(self):
        ent_idx = Ent.idx_from_type(EntType.PROVINCE)
        self.assertEqual(len(ent_idx), 9)
        self.assertEqual(ent_idx['LK-1'].id, 'LK-1')
        self.assertEqual(ent_idx['LK-1'].name, 'Western')

    def test_from_id(self):
        ent = Ent.from_id('LK-1')
        self.assertEqual(ent.id, 'LK-1')
        self.assertEqual(ent.name, 'Western')

    def test_list_from_id_list(self):
        for id_list in [['LK-1'], ['LK-11', 'LK-12']]:
            ent_list = Ent.list_from_id_list(id_list)
            self.assertEqual(len(ent_list), len(id_list))

            for id, ent in zip(id_list, ent_list):
                self.assertEqual(id, ent.id)

    def test_ids_from_type(self):
        id_list = Ent.ids_from_type(EntType.PROVINCE)
        self.assertEqual(
            id_list,
            [
                'LK-1',
                'LK-2',
                'LK-3',
                'LK-4',
                'LK-5',
                'LK-6',
                'LK-7',
                'LK-8',
                'LK-9',
            ],
        )

    def test_list_by_name_fuzzy(self):
        for expected_id, name_fuzzy, filter_ent_type, filter_parent_id in [
            ['LK-11', 'Colombo', None, None],
            ['LK-11', 'Colombo', EntType.DISTRICT, None],
            ['LK-11', 'Colombo', EntType.DISTRICT, 'LK-1'],
            ['LK-11', 'Colombi', None, None],
            ['LK-1103', 'Colombo', EntType.DSD, None],
            ['LG-11001', 'Colombo MC', EntType.LG, None],
            ['LK-23', 'Nuwara Eliya', EntType.DISTRICT, None],
            ['LK-23', 'Nuwara-Eliya', EntType.DISTRICT, None],
            ['LK-23', 'NuwaraEliya', EntType.DISTRICT, None],
        ]:
            ents = Ent.list_from_name_fuzzy(
                name_fuzzy, filter_ent_type, filter_parent_id
            )
            ent = ents[0]
            self.assertEqual(ent.id, expected_id)

    def test_list_by_name_fuzzy_limit(self):
        ents = Ent.list_from_name_fuzzy(
            'Colombo', limit=10, min_fuzz_ratio=10
        )
        self.assertEqual(len(ents), 10)
