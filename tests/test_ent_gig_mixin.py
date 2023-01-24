import unittest

from gig import Ent, GIGTable

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


class TestEntGIGMixin(unittest.TestCase):
    def test_gig(self):
        gig_table = GIGTable('population-ethnicity', 'regions', '2012')
        ent = Ent.for_id('LK-1')
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
