
from gig import EntType, Ent
import matplotlib.pyplot as plt 
from utils import JSONFile

LATLNG_TOWN_HALL_COLOMBO = [6.91585, 79.86379]
LATLNG_KANDALAMA = [7.8782630952368145, 80.70185841196397]

LATLNG_KANDY = [7.2914, 80.6367]
LATLNG_GALLE = [6.0321, 80.2168]
LATLNG_BATTICALOA = [7.7101, 81.6920]
LATLNG_JAFFNA = [9.6615, 80.0255]

def distance(latlng1, latlng2):
    return (latlng1[0] - latlng2[0])**2 + (latlng1[1] - latlng2[1])**2

def get_distance_lambda(latlng):
    def inner(ent):
        return distance([ent.d['center_lat'], ent.d['center_lng']], latlng)
    return inner

ALGORITHM_IDX = {
'town_hall':  get_distance_lambda(LATLNG_TOWN_HALL_COLOMBO),
    'lat': lambda ent: ent.d['center_lat'],
    'lng': lambda ent: ent.d['center_lng'],
    'kandalama':  get_distance_lambda(LATLNG_KANDALAMA),
    # 
    'kandy': get_distance_lambda(LATLNG_KANDY),
    'batticaloa': get_distance_lambda(LATLNG_BATTICALOA),
    'jaffna': get_distance_lambda(LATLNG_JAFFNA),
    'galle': get_distance_lambda(LATLNG_GALLE),
}

PARENT_REGION_ID = 'LK'
CHILD_REGION_TYPE = EntType.GND

N_COLORS = 7
COLORS = [
     '#EB2939',
     '#FD731B',
'#E2C225',
    '#198D3D',
    '#17A1C9',
    '#4D80BD',
    '#8669CE',
    
   
    
]
    

ents = [ent for ent in Ent.list_from_type(CHILD_REGION_TYPE) if PARENT_REGION_ID in ent.id ]
ethnicity_data = JSONFile('examples/example-equi-population-regions/ethnicity.json').read()
idx = {d['region_id']: d['total_value'] for d in ethnicity_data}

total_population = sum([idx.get(ent.id,0) for ent in ents])
print(f'{total_population=}')


for algo_key, algo in ALGORITHM_IDX.items():
    sorted_ents = sorted(ents, key=algo)
    pop_segment_size = total_population / N_COLORS

    ax = plt.gca()

    cum_pop = 0
    for ent in sorted_ents:
        population = idx.get(ent.id, 0)
        pop_group = int(cum_pop / pop_segment_size)
        cum_pop += population
        
        color = COLORS[pop_group]

        geo = ent.geo()
        geo.plot(ax=ax, color=color)

    ax.set_axis_off()
    pop_segment_size_m = pop_segment_size / 1_000_000
    ax.set_title(f'Sri Lanka - Each color includes ~ {pop_segment_size_m:,.0f}M people')

    image_path = f'examples/example-equi-population-regions/{PARENT_REGION_ID}.{CHILD_REGION_TYPE.name}.{algo_key}.png'
    plt.savefig(
        image_path,
        dpi=300
    )
    plt.close()
    print(f'Wrote {image_path}')

    