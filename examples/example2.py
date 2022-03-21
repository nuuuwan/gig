if __name__ == '__main__':
    from gig import ext_data

    census_index = ext_data._get_table_index(
        'census', 'ethnicity_of_population')
    print(census_index['LK-1'])

    election_index = ext_data._get_table_index(
        'elections', 'parliamentary_election_2020')
    print(election_index['EC-01A'])
