if __name__ == '__main__':
    from gig import ext_data

    census_index = ext_data._get_table_index(
        'population-ethnicity.regions.2012'
    )
    print(census_index['LK-1'])
