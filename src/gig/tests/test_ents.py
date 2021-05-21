'''Test gig_data.'''
import unittest
import time

from utils import db

from gig import ents
from gig.ent_types import ENTITY_TYPE


class TestGig(unittest.TestCase):
    '''Test.'''

    def test_get_entities(self):
        '''Test.'''
        for entity_type in ENTITY_TYPE.list():
            entities = ents.get_entities(entity_type)
            self.assertTrue(len(entities) >= 9)

    def test_get_entity_index(self):
        '''Test.'''
        for entity_type in ENTITY_TYPE.list():
            entity_index = ents.get_entity_index(entity_type)
            first_entity_id = (list(entity_index.keys()))[0]
            first_entity = entity_index[first_entity_id]
            first_entity_id2 = first_entity[db.get_id_key(entity_type)]
            self.assertEqual(first_entity_id, first_entity_id2)

    def test_get_entity_ids(self):
        '''Test.'''
        for entity_type in ENTITY_TYPE.list():
            entity_index = ents.get_entity_index(entity_type)
            entity_ids = ents.get_entity_ids(entity_type)
            self.assertEqual(list(entity_index.keys()), entity_ids)

    def test_get_entity(self):
        '''Test.'''
        for entity_type in ENTITY_TYPE.list():
            entity_ids = ents.get_entity_ids(entity_type)
            first_entity_id = entity_ids[0]
            entity = ents.get_entity(first_entity_id)
            id_key = db.get_id_key(entity_type)
            self.assertEqual(entity[id_key], first_entity_id)

    def test_multiget_entities(self):
        '''Test.'''
        self.assertEqual(
            ents.multiget_entities(['LK', 'LK-1', 'LK-11']),
            {
                'LK': {
                  'id': 'LK',
                  'name': 'Sri Lanka',
                  'country_id': 'LK',
                  'area': 65611.0,
                  'population': 20359054,
                  'hasc': 'LK',
                  'fips': 'CE'
                },
                'LK-1': {
                  'id': 'LK-1',
                  'name': 'Western',
                  'country_id': 'LK',
                  'province_id': 'LK-1',
                  'area': 3709.0,
                  'population': 5850745,
                  'province_capital': 'Colombo',
                  'fips': 'CE36'
                },
                'LK-11': {
                  'id': 'LK-11',
                  'name': 'Colombo',
                  'country_id': 'LK',
                  'province_id': 'LK-1',
                  'district_id': 'LK-11',
                  'ed_id': 'EC-01',
                  'area': 642.0,
                  'population': 2323964,
                  'hasc': 'LK.CO',
                  'fips': 'CE23'
                },
            },
        )

    def test_perf(self):
        '''Test.'''
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
