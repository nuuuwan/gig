
"""Utils for getting basic entity data.

For example, the
following information can be access about Colombo District.

.. code-block:: python

    >> from gig import entities
    >> entities.get_entity('district', 'LK-11')
    {'district_id': 'LK-11', 'name': 'Colombo', 'province_id': 'LK-1',
    'ed_id': 'EC-01', 'hasc': 'LK.CO', 'fips': 'CE23',
    'area': '642', 'population': '2324349'}

"""

from utils import db
from utils.cache import cache

from gig._constants import GIG_CACHE_NAME
from gig._remote_data import _get_remote_tsv_data

from gig.ent_types import get_entity_type


@cache(GIG_CACHE_NAME)
def get_entities(entity_type):
    """Get get all entity data, for entities of a particular type.

    Args:
        entity_type(str): entity type
    Returns:
        entity data

    .. code-block:: python

        >> from gig import entities
        >> ents = entities.get_entities('province')
        >> ents[0]
        {'province_id': 'LK-1', 'name': 'Western',
        'country_id': 'LK', 'fips': 'CE36', 'area': '3709',
        'capital': 'Colombo'}

    """
    return list(filter(
        lambda x: x,
        _get_remote_tsv_data('%s.tsv' % (entity_type)),
    ))


@cache(GIG_CACHE_NAME)
def get_entity_index(entity_type):
    """Get all entity data, for entities of a particular type.
        Indexed by entity id.

    Args:
        entity_type(str): entity type
    Returns:
        entity data

    .. code-block:: python

        >> from gig import entities
        >> entity_index = entities.get_entity_index('province')
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


@cache(GIG_CACHE_NAME)
def get_entity(entity_id):
    """Get entity by entity id.

    Args:
        entity_id(str): entity id
    Returns:
        entity (dict)

    .. code-block:: python

        >> from gig import entities
        >> entities.get_entity('LK-3')
        {'province_id': 'LK-3', 'name': 'Southern', 'country_id': 'LK',
        'fips': 'CE34', 'area': '5559', 'capital': 'Galle'}
    """
    entity_type = get_entity_type(entity_id)
    entity_index = get_entity_index(entity_type)
    return entity_index.get(entity_id, None)


@cache(GIG_CACHE_NAME)
def get_entity_ids(entity_type):
    """Get all entity_ids of a particular entity type.

    Args:
        entity_type(str): entity type
    Returns:
        entity ids (list)

    .. code-block:: python

        >> from gig import entities
        >> entities.get_entity_ids('province')
        ['LK-1', 'LK-2', 'LK-3', 'LK-4', 'LK-5', 'LK-6',
        'LK-7', 'LK-8', 'LK-9']

    """
    return list(get_entity_index(entity_type).keys())
