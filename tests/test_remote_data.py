import unittest

from gig._remote_data import _get_remote_tsv_data


class TestGigData(unittest.TestCase):
    def test_get_remote_tsv_data(self):
        TEST_FILE = 'ents/province.tsv'
        data = _get_remote_tsv_data(TEST_FILE)
        self.assertEqual(len(data), 9)
        self.assertEqual(data[0]['province_id'], 'LK-1')
