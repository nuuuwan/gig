import time
import unittest

from utils import db

from gig import ents
from gig.ent_types import ENTITY_TYPE


class TestGig(unittest.TestCase):
    def test_get_entities(self):
        for entity_type in ENTITY_TYPE.list():
            entities = ents.get_entities(entity_type)
            self.assertTrue(len(entities) >= 9)

    def test_get_entity_index(self):
        for entity_type in ENTITY_TYPE.list():
            entity_index = ents.get_entity_index(entity_type)
            first_entity_id = (list(entity_index.keys()))[0]
            first_entity = entity_index[first_entity_id]
            first_entity_id2 = first_entity[db.get_id_key(entity_type)]
            self.assertEqual(first_entity_id, first_entity_id2)

    def test_get_entity_ids(self):
        for entity_type in ENTITY_TYPE.list():
            entity_index = ents.get_entity_index(entity_type)
            entity_ids = ents.get_entity_ids(entity_type)
            self.assertEqual(list(entity_index.keys()), entity_ids)

    def test_get_entity(self):
        for entity_type in ENTITY_TYPE.list():
            entity_ids = ents.get_entity_ids(entity_type)
            first_entity_id = entity_ids[0]
            entity = ents.get_entity(first_entity_id)
            id_key = db.get_id_key(entity_type)
            self.assertEqual(entity[id_key], first_entity_id)
            if 'centroid_altitude' in entity:
                self.assertTrue(0 <= entity['centroid_altitude'] <= 2600)

    def test_multiget_entities(self):
        entity_map = ents.multiget_entities(['LK', 'LK-1', 'LK-11'])
        self.assertEqual(
            list(entity_map.keys()),
            ['LK', 'LK-1', 'LK-11'],
        )

    def test_perf(self):
        delta_t_total = 0
        for entity_type in ENTITY_TYPE.list():
            ents.get_entities(entity_type)

            t_start = time.time()
            entities = ents.get_entities(entity_type)
            delta_t = (time.time() - t_start) * 1000
            delta_t_total += delta_t

            first_entity = entities[0]
            self.assertTrue(db.get_id_key(entity_type) in first_entity)
            self.assertTrue('name' in first_entity)
        delta_t_mean = delta_t_total / len(ENTITY_TYPE.list())
        self.assertTrue(delta_t_mean < 200, delta_t_mean)

    def test_get_entities_by_name_buzzy(self):
        for [entity_name, expected_entity_names] in [
            [
                'Colombu',
                ['Colombo', 'Colombo', 'Colombo'],
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
            actual_entities = ents.get_entities_by_name_fuzzy(entity_name)
            actual_entity_names = list(
                map(
                    lambda entity: entity['name'],
                    actual_entities,
                )
            )
            self.assertListEqual(expected_entity_names, actual_entity_names)

        # with filters
        self.assertEqual(
            'LK-11',
            ents.get_entities_by_name_fuzzy(
                'Colombo',
                filter_entity_type='district',
            )[0]['id'],
        )

        self.assertEqual(
            'EC-01A',
            ents.get_entities_by_name_fuzzy(
                'Colombo North',
                filter_parent_id='EC-01',
            )[0]['id'],
        )
