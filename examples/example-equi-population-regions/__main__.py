
from gig import EntType, Ent
import matplotlib.pyplot as plt 
from utils import JSONFile

LATLNG_TOWN_HALL_COLOMBO = [6.91585, 79.86379]
LATLNG_KANDALAMA = [7.8782630952368145, 80.70185841196397]


def distance(latlng1, latlng2):
    return (latlng1[0] - latlng2[0])**2 + (latlng1[1] - latlng2[1])**2

ALGORITHM_IDX = {
    'lat': lambda ent: ent.d['center_lat'],
    'lng': lambda ent: ent.d['center_lng'],
    'town_hall': lambda ent: distance([ent.d['center_lat'], ent.d['center_lng']], LATLNG_TOWN_HALL_COLOMBO),
    'kandalama': lambda ent: distance([ent.d['center_lat'], ent.d['center_lng']], LATLNG_KANDALAMA),
}

PARENT_REGION_ID = 'LK'
CHILD_REGION_TYPE = EntType.DSD

COLORS = ['red', 'yellow', 'orange', 'green', 'cyan', 'blue', 'purple']


ents = [ent for ent in Ent.list_from_type(CHILD_REGION_TYPE) if PARENT_REGION_ID in ent.id ]
ethnicity_data = JSONFile('examples/example-equi-population-regions/ethnicity.json').read()
idx = {d['region_id']: d['total_value'] for d in ethnicity_data}

total_population = sum([idx[ent.id] for ent in ents])
print(f'{total_population=}')


for algo_key, algo in ALGORITHM_IDX.items():
    sorted_ents = sorted(ents, key=algo)


    

    N_COLORS =7
    pop_segment_size = total_population / N_COLORS

    ax = plt.gca()

    cum_pop = 0
    for ent in sorted_ents:
        population = idx[ent.id]
        pop_group = int(cum_pop / pop_segment_size)
        cum_pop += population
        
        color = COLORS[pop_group]

        geo = ent.geo()
        geo.plot(ax=ax, color=color)

    ax.set_axis_off()
    ax.set_title(f'Sri Lanka - Each color includes ~ {pop_segment_size:,.0f} people')

    image_path = f'examples/example-equi-population-regions/{PARENT_REGION_ID}.{CHILD_REGION_TYPE.name}.{algo_key}.png'
    plt.savefig(
        image_path,
        dpi=300
    )
    plt.close()
    print(f'Wrote {image_path}')

    