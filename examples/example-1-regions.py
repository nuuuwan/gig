if __name__ == '__main__':
    from gig import Ent, EntType

    province_list = Ent.list_from_type(EntType.PROVINCE)
    print(province_list[0])

    district_idx = Ent.idx_from_type(EntType.DISTRICT)
    print(district_idx['LK-11'])

    print(Ent.from_id('LK-1103'))
