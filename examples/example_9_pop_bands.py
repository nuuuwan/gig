import os
from matplotlib import pyplot as plt
from utils import Log, Parallel
from gig import Ent, EntType
import colorsys

log = Log('examples')

# COLORS = ['#E40303', '#FF8C00', '#FFED00', '#008026', '#004CFF']
COLORS = ['red', 'orange', 'yellow', 'green', 'blue']
N_COLORS = len(COLORS)

ENT_TYPE = EntType.GND
PARENT_ENT_ID_LIST = ["LK-1"]

# CENTER = [9.663203555637029, 80.01332119260337] # LK-4
CENTER = [6.961312108947133, 79.85694398099878] # LK-11, LK-1
N_BANDS = 5

def get_progress(p):
    N_BARS = 10
    n = int(p * N_BARS)
    bars = "🟩" * n + "⬛" * (N_BARS - n)
    return f'[{bars} {p:.1%}]'

def get_distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


def get_color(i_band):
    return COLORS[i_band % N_COLORS]

def is_in_parent(id):
    for parent_ent_id in PARENT_ENT_ID_LIST:
        if parent_ent_id in id:
            return True
    return False

def get_ents_list():
    ents = [ent for ent in Ent.list_from_type(ENT_TYPE) if is_in_parent(ent.id)]
    
    ents.sort(
        key=lambda ent: get_distance(ent.centroid, CENTER)
    )
    
    n = len(ents)
    log.debug(f'{n=}')
    return ents

def get_ent_info_list(ent_list):
    total_pop = sum([ent.population for ent in ent_list])
    cum_pop = 0
    ent_info_list = []
    for ent in ent_list:
        p_pop = cum_pop / total_pop
        i_band = int(p_pop * N_BANDS)
        color = get_color(i_band)
        ent_info = {
            'ent': ent,
            'i_band': i_band,
            'color': color,
        }
        ent_info_list.append(ent_info)
        cum_pop += ent.population
    return ent_info_list

def get_geo_idx(ent_list):
    n = len(ent_list)
    def get_worker(i, ent):
        def worker(i=i,ent=ent):
            p = i / n
            print(f'{get_progress(p)} {ent.id} {ent.name}'.ljust(80), end='\r')
            try:
                geo = ent.geo()
            except Exception as e:
                log.error(f'[{ent.id}] {e}')
                geo = None
            return ent.id, geo
        return worker
    
    workers = [get_worker(i, ent) for i, ent in enumerate(ent_list, start=1)]
    
    tuple_list = Parallel.run(workers, max_threads=32)
    geo_idx = dict(tuple_list)
    return geo_idx

def draw():
    ax = plt.gca()

    ent_list = get_ents_list()
    ent_info_list = get_ent_info_list(ent_list)  
    geo_idx = get_geo_idx(ent_list)
    n = len(ent_info_list)
    log.debug('Drawing...')
    for i, ent_info in enumerate(ent_info_list, start=1):
        p = i / n
        ent = ent_info['ent']
        print(f'{get_progress(p)} Drawing {ent.id} {ent.name}'.ljust(80), end='\r')
        
        color = ent_info['color']        
        geo = geo_idx[ent.id]
        if geo is not None:
            geo.plot(ax=ax, color=color, alpha=1)


    
    for ent in Ent.list_from_type(EntType.DISTRICT):
        if is_in_parent(ent.id):
            geo = ent.geo()
            geo.plot(ax=ax, color="white", edgecolor='black', linewidth=1, alpha=0.333)


    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.title(f"Each Band of {ENT_TYPE.name.upper()}s has (roughly) the same population.")

    parent_id_str = '-'.join(PARENT_ENT_ID_LIST)
    image_path = __file__ + f'.{ENT_TYPE.name}.{parent_id_str}.png'
    plt.savefig(image_path, dpi=600)
    plt.close()
    log.info(f'Saved {image_path}')
    os.startfile(image_path)

def main():
    
    draw()


if __name__ == '__main__':
    main()