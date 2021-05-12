"""Various utils related to entity types."""


class ENTITY_TYPE:
    """Enum class ENTITY_TYPE."""

    COUNTRY = 'country'
    PROVINCE = 'province'
    DISTRICT = 'district'
    DSD = 'dsd'
    GND = 'gnd'
    ED = 'ed'
    PD = 'pd'
    PS = 'ps'
    UNKNOWN = 'unknown'

    @staticmethod
    def list():
        """List all entity types."""
        return [
            ENTITY_TYPE.PROVINCE,
            ENTITY_TYPE.DISTRICT,
            ENTITY_TYPE.DSD,
            ENTITY_TYPE.GND,
            ENTITY_TYPE.ED,
            ENTITY_TYPE.PD,
            ENTITY_TYPE.PS,
        ]


NEARBY_ENTITY_TYPES = [ENTITY_TYPE.PS]


def get_entity_type(entity_id):
    """Get entity type from entity id.

    Args:
        entity_id (str): entity id
    Returns:
        entity type (str)


    .. code-block:: python

        >> from gig.ent_types import get_entity_type
        >> get_entity_type('LK-11')  # Colombo District
        'district'

    """
    n = len(entity_id)
    if entity_id[:2] == 'LK':
        if n == 2:
            return ENTITY_TYPE.COUNTRY
        if n == 4:
            return ENTITY_TYPE.PROVINCE
        if n == 5:
            return ENTITY_TYPE.DISTRICT
        if n == 7:
            return ENTITY_TYPE.DSD
        if n == 10:
            return ENTITY_TYPE.GND

    if entity_id[:2] == 'EC':
        if n == 5:
            return ENTITY_TYPE.ED
        if n == 6:
            return ENTITY_TYPE.PD

    if entity_id[:2] == 'PS':
        return ENTITY_TYPE.PS

    return ENTITY_TYPE.UNKNOWN
