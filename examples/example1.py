if __name__ == '__main__':
    from gig import ents
    from gig.ent_types import ENTITY_TYPE

    provinces = ents.get_entities(ENTITY_TYPE.PROVINCE)
    print(provinces[0])

    district_index = ents.get_entity_index(ENTITY_TYPE.DISTRICT)
    print(district_index['LK-11'])

    print(ents.get_entity('LK-1103'))
