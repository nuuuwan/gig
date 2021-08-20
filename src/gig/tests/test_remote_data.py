"""Test data."""
import unittest

from gig._remote_data import _get_remote_json_data, _get_remote_tsv_data


class TestGigData(unittest.TestCase):
    """Test."""

    def test_get_remote_json_data(self):
        """Test."""
        TEST_FILE = 'census/meta.json'
        data = _get_remote_json_data(TEST_FILE)
        self.assertTrue('total_population' in data)

    def test_get_remote_tsv_data(self):
        """Test."""
        TEST_FILE = 'province.tsv'
        data = _get_remote_tsv_data(TEST_FILE)
        self.assertEqual(len(data), 9)
        self.assertEqual(data[0]['province_id'], 'LK-1')
