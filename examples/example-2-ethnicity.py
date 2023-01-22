if __name__ == '__main__':
    from gig import Ent, GIGTable

    gig_table = GIGTable('population-ethnicity', 'regions', '2012')
    ent_colombo = Ent.load_for_id('LK-11')
    print(ent_colombo)
    print(ent_colombo.gig(gig_table))
