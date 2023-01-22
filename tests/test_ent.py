import unittest

from gig import Ent, EntType, GIGTable

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


class TestGig(unittest.TestCase):
    def test_class_ent_base(self):
        ent = Ent(TEST_D)
        self.assertEqual(ent.id, 'LK-11')
        self.assertEqual(ent.name, 'Colombo')
        self.assertTrue(ent.is_parent_id('LK-1'))
        self.assertFalse(ent.is_parent_id('LK-1125'))

        self.assertEqual(len(str(ent)), 519)
        self.assertEqual(str(ent)[:10], "{'id': 'LK")

    def test_from_dict(self):
        ent = Ent.from_dict(TEST_D)
        self.assertEqual(ent.id, 'LK-11')
        self.assertEqual(ent.name, 'Colombo')
        self.assertEqual(ent.area, 642.00)
        self.assertEqual(ent.population, 2323964)
        self.assertEqual(ent.centroid_altitude, 8)
        self.assertEqual(ent.centroid, [6.869636028857, 80.01959786729992])
        self.assertEqual(
            ent.subs,
            [
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
            ],
        )
        self.assertEqual(ent.supers, ['LK'])
        self.assertEqual(ent.eqs, ['LK-1'])
        self.assertEqual(ent.ints, [])

    def test_load_list_for_type(self):
        ent_list = Ent.load_list_for_type(EntType.PROVINCE)
        self.assertEqual(len(ent_list), 9)
        self.assertEqual(ent_list[0].id, 'LK-1')

    def test_load_idx_for_type(self):
        ent_idx = Ent.load_idx_for_type(EntType.PROVINCE)
        self.assertEqual(len(ent_idx), 9)
        self.assertEqual(ent_idx['LK-1'].id, 'LK-1')
        self.assertEqual(ent_idx['LK-1'].name, 'Western')

    def test_load_for_id(self):
        ent = Ent.load_for_id('LK-1')
        self.assertEqual(ent.id, 'LK-1')
        self.assertEqual(ent.name, 'Western')

    def test_load_list_for_id_list(self):
        for id_list in [['LK-1'], ['LK-11', 'LK-12']]:
            ent_list = Ent.load_list_for_id_list(id_list)
            self.assertEqual(len(ent_list), len(id_list))

            for id, ent in zip(id_list, ent_list):
                self.assertEqual(id, ent.id)

    def test_load_ids_for_type(self):
        id_list = Ent.load_ids_for_type(EntType.PROVINCE)
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

    def test_load_list_by_name_fuzzy(self):
        for [ent_name, expected_ent_names] in [
            [
                'Colombo',
                [
                    'Colombo',
                    'Colombo',
                    'Colombo',
                    'Colombo MC',
                ],
            ],
            [
                'Nuware Eliya',
                [
                    'Nuwara Eliya',
                    'Nuwara Eliya',
                    'Nuwaraeliya',
                    'Nuwara-Eliya',
                    'Nuwara Eliya PS',
                ],
            ],
            [
                'Trincomali',
                [
                    'Trincomalee',
                    'Trincomalee',
                    'Trincomalee',
                ],
            ],
            [
                'Galla',
                ['Galwala', 'Galdola', 'Gallala', 'Gallewa', 'Gallawa'],
            ],
        ]:
            ent_list = Ent.load_list_for_name_fuzzy(ent_name)
            actual_ent_names = list(
                map(
                    lambda ent: ent.name,
                    ent_list,
                )
            )
            self.assertListEqual(expected_ent_names, actual_ent_names)

    def test_gig(self):
        gig_table = GIGTable('population-ethnicity', 'regions', '2012')
        ent = Ent.load_for_id('LK-1')
        gig_row = ent.gig(gig_table)
        self.assertEqual(
            gig_row.total,
            5_850_745,
        )

        self.assertEqual(
            gig_row.dict,
            {
                'sinhalese': 4925402,
                'sl_tamil': 339233,
                'ind_tamil': 56614,
                'sl_moor': 460545,
                'burgher': 25277,
                'malay': 27853,
                'sl_chetty': 4806,
                'bharatha': 1297,
                'other_eth': 9718,
            },
        )

        self.assertEqual(
            list(gig_row.dict.keys()),
            [
                'sinhalese',
                'sl_moor',
                'sl_tamil',
                'ind_tamil',
                'malay',
                'burgher',
                'other_eth',
                'sl_chetty',
                'bharatha',
            ],
        )
