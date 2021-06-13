
"""Utils for getting basic entity data.

For example, the
following information can be access about Colombo District.

.. code-block:: python

    >> from gig import ents
    >> ents.get_entity('district', 'LK-11')
    {'district_id': 'LK-11', 'name': 'Colombo', 'province_id': 'LK-1',
    'ed_id': 'EC-01', 'hasc': 'LK.CO', 'fips': 'CE23',
    'area': '642', 'population': '2324349'}

"""
import re
import json
from utils import db
from utils.cache import cache

from gig._constants import GIG_CACHE_NAME, GIG_CACHE_TIMEOUT
from gig._remote_data import _get_remote_tsv_data

from gig.ent_types import get_entity_type, ENTITY_TYPE


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entities(entity_type):
    """Get get all entity data, for entities of a particular type.

    Args:
        entity_type(str): entity type
    Returns:
        entity data

    .. code-block:: python

        >> from gig import ents
        >> entities = ents.get_entities('province')
        >> entities[0]
        {'province_id': 'LK-1', 'name': 'Western',
        'country_id': 'LK', 'fips': 'CE36', 'area': '3709',
        'capital': 'Colombo'}

    """

    def clean_types(d):
        if 'area' in d:
            d['area'] = (float)(d['area'])

        if 'population' in d:
            d['population'] = (int)(d['population'])

        if 'centroid_altitude' in d:
            try:
                d['centroid_altitude'] = (int)(d['centroid_altitude'])
            except ValueError:
                d['centroid_altitude'] = 0

        for k in ['centroid', 'subs', 'supers', 'ints', 'eqs']:
            if k in d:
                if d[k]:
                    d[k] = json.loads(d[k].replace('\'', '"'))
        return d

    return list(map(
        clean_types,
        list(filter(
            lambda x: x,
            _get_remote_tsv_data('%s.tsv' % (entity_type)),
        )),
    ))


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entity_index(entity_type):
    """Get all entity data, for entities of a particular type.

        Indexed by entity id.

    Args:
        entity_type(str): entity type
    Returns:
        entity data

    .. code-block:: python

        >> from gig import ents
        >> entity_index = ents.get_entity_index('province')
        >> entity_index['LK-2']
        {'province_id': 'LK-2', 'name': 'Central',
        'country_id': 'LK', 'fips': 'CE29', 'area': '5584', 'capital': 'Kandy'}

    """
    entities = get_entities(entity_type)
    id_key = db.get_id_key(entity_type)
    return dict(zip(
        list(map(
            lambda e: e[id_key],
            entities,
        )),
        entities,
    ))


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entity(entity_id):
    """Get entity by entity id.

    Args:
        entity_id(str): entity id
    Returns:
        entity (dict)

    .. code-block:: python

        >> from gig import ents
        >> ents.get_entity('LK-3')
        {'province_id': 'LK-3', 'name': 'Southern', 'country_id': 'LK',
        'fips': 'CE34', 'area': '5559', 'capital': 'Galle'}
    """
    entity_type = get_entity_type(entity_id)
    entity_index = get_entity_index(entity_type)
    return entity_index.get(entity_id, None)


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def multiget_entities(entity_ids):
    """Get multiple entities by entity id.

    Args:
        entity_ids(list of str): entity_ids id
    Returns:
        map of entity id to entity

    .. code-block:: python

        >> from gig import ents
        >> ents.multiget_entities(
            ['LK-1', 'LK-11', 'LK-1127', 'LK-1127015']
        )
        {'LK-1': {'province_id': 'LK-1', 'name': 'Western',
            'country_id': 'LK', 'fips': 'CE36', 'area': '3709',
            'capital': 'Colombo'},
        'LK-11': {'district_id': 'LK-11', 'name': 'Colombo',
            'province_id': 'LK-1', 'ed_id': 'EC-01',
            'hasc': 'LK.CO', 'fips': 'CE23', 'area': '642',
            'population': '2324349'},
        'LK-1127': {'dsd_id': LK-1127', 'name': 'Thimbirigasyaya',
            'hasc': 'LK.CO.TH','province_id': 'LK-1', 'district_id': 'LK-11',
            'area': '24', 'population': '238057'},
        'LK-1127015': {'gnd_id':'LK-1127015', 'name': 'Kurunduwatta',
            'province_id': 'LK-1', 'district_id': 'LK-11',
            'dsd_id': 'LK-1127', 'pd_id': 'EC-01C', 'gnd_num': 'None'}}
    """
    entity_map = {}
    for entity_id in entity_ids:
        entity_map[entity_id] = get_entity(entity_id)
    return entity_map


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entity_ids(entity_type):
    """Get all entity_ids of a particular entity type.

    Args:
        entity_type(str): entity type
    Returns:
        entity ids (list)

    .. code-block:: python

        >> from gig import ents
        >> ents.get_entity_ids('province')
        ['LK-1', 'LK-2', 'LK-3', 'LK-4', 'LK-5', 'LK-6',
        'LK-7', 'LK-8', 'LK-9']

    """
    return list(get_entity_index(entity_type).keys())


def get_fuzzy_fp(entity_name):
    """Get fuzzy fingerprint."""
    fuzzy_words = []
    for word in entity_name.split(' '):
        fuzzy_word = word.lower()
        if len(fuzzy_word) > 1:
            fuzzy_word = fuzzy_word.replace("th", 't')
            fuzzy_word = fuzzy_word.replace("w", 'v')
            fuzzy_word = fuzzy_word[0] + re.sub('[aeiou]', '', fuzzy_word[1:])
        fuzzy_words.append(fuzzy_word)
    return ' '.join(fuzzy_words)


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entities_by_name_buzzy(entity_name, limit=5):
    """Get entity by fuzzy name search.

    Args:
        entity_name(str): entity name
        limit (int): Maximum number of results to return
    Returns:
        entities (list) that approximately match the entity name
    """
    fp_search = get_fuzzy_fp(entity_name)
    matching_entities = []
    for entity_type in ENTITY_TYPE.list():
        entities = get_entities(entity_type)
        for entity in entities:
            fp_entity = get_fuzzy_fp(entity['name'])

            if fp_entity == fp_search:
                matching_entities.append(entity)
                if len(matching_entities) >= limit:
                    return matching_entities

    return matching_entities
