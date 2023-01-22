if __name__ == '__main__':
    from gig import Ent, EntType

    province_list = Ent.load_list_for_type(EntType.PROVINCE)
    print(province_list[0])

    district_idx = Ent.load_idx_for_type(EntType.DISTRICT)
    print(district_idx['LK-11'])

    print(Ent.load_for_id('LK-1103'))
