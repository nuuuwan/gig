import unittest

from gig import Ent
from tests.test_ent_base import TEST_D


class TestEntJSONMixin(unittest.TestCase):
    def test_to_json(self):
        ent1 = Ent(TEST_D)
        json_str = ent1.to_json()
        self.assertIsInstance(json_str, str)
        ent2 = Ent.from_json(json_str)
        self.assertEqual(ent1, ent2)
