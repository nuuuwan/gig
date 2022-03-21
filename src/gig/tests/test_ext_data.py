import unittest

from gig import ext_data
from gig.ent_types import ENTITY_TYPE

TEST_ATTR_GROUP = 'census'
TEST_TABLE_ID = 'total_population'
TEST_FIELD_ID = 'total_population'


class TestGIGExtData(unittest.TestCase):
    def test_get_table(self):
        table = ext_data._get_table(TEST_ATTR_GROUP, TEST_TABLE_ID)
        self.assertTrue(len(table) > 100)
        self.assertEqual(table[0]['entity_id'][:2], 'EC')

    def test_get_table_index(self):
        table_index = ext_data._get_table_index(TEST_ATTR_GROUP, TEST_TABLE_ID)
        self.assertEqual(table_index['LK'][TEST_FIELD_ID], 20357776.0)

    def test_get_data_for_table_and_entity(self):
        data = ext_data.get_table_data(
            TEST_ATTR_GROUP,
            TEST_TABLE_ID,
            entity_ids=['LK'],
        )
        self.assertEqual(
            data['LK'][TEST_FIELD_ID],
            20357776.0,
        )

        data = ext_data.get_table_data(
            TEST_ATTR_GROUP,
            TEST_TABLE_ID,
            entity_type=ENTITY_TYPE.PROVINCE,
        )
        self.assertEqual(
            len(data.values()),
            9,
        )
        self.assertEqual(
            data['LK-1'][TEST_FIELD_ID],
            5850745,
        )
