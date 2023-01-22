import unittest

from gig import GIGTableRow

TEST_D = {
    'entity_id': 'LK-1',
    'a': '100',
    'b': '200',
    'c': '300.456',
    'total_population': '600.456',
}
TEST_GIG_TABLE_ROW = GIGTableRow(TEST_D)


class TestGIGTableRow(unittest.TestCase):
    def test_id(self):
        self.assertEqual(TEST_GIG_TABLE_ROW.id, 'LK-1')

    def test_get_attr(self):
        self.assertEqual(TEST_GIG_TABLE_ROW.a, 100)
        self.assertEqual(TEST_GIG_TABLE_ROW.b, 200)
        self.assertEqual(TEST_GIG_TABLE_ROW.c, 300.456)

    def test_dict(self):
        self.assertEqual(
            TEST_GIG_TABLE_ROW.dict,
            {
                'a': 100,
                'b': 200,
                'c': 300.456,
            },
        )

    def test_total(self):
        self.assertEqual(TEST_GIG_TABLE_ROW.total, 600.456)

    def test_str(self):
        self.assertEqual(
            str(TEST_GIG_TABLE_ROW)[:20],
            "{'id': 'LK-1', 'cell",
        )
