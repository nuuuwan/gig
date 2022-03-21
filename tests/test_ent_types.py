import unittest

from gig.ent_types import ENTITY_TYPE, get_entity_type


class TestEntityTypes(unittest.TestCase):
    def test_get_entity_type(self):
        for [input, expected_output] in [
            ['LK', ENTITY_TYPE.COUNTRY],
            ['LK-1', ENTITY_TYPE.PROVINCE],
            ['LK-11', ENTITY_TYPE.DISTRICT],
            ['LK-1127', ENTITY_TYPE.DSD],
            ['LK-1127025', ENTITY_TYPE.GND],
            ['XX-112702512', ENTITY_TYPE.UNKNOWN],
            ['EC-11', ENTITY_TYPE.ED],
            ['EC-11A', ENTITY_TYPE.PD],
            ['LG-12345', ENTITY_TYPE.LG],
            ['MOH-12345', ENTITY_TYPE.MOH],
            ['XX-1234', ENTITY_TYPE.UNKNOWN],
        ]:
            self.assertEqual(
                get_entity_type(input),
                expected_output,
            )
