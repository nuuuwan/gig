import os
import re
from matplotlib.font_manager import FontProperties
from matplotlib import pyplot as plt
from utils import Log

from gig import Ent, EntType, GIGTable

log = Log('example-5')

ENT_TYPE = EntType.DSD
MIN_LAT = 5.923389
MAX_LAT = 9.835556
MID_LAT = (MIN_LAT + MAX_LAT) / 2
log.debug(f'{MID_LAT=}')


FONT_PATH = "C:\\Users\\ASUS\\AppData\\Local\\Microsoft\\Windows\\Fonts\\p22.ttf"
FONT = FontProperties(fname=FONT_PATH)
plt.rcParams['font.family'] = FONT.get_name()


class COLOR:
    NORTH = '#eee'
    SOUTH = '#c00'


def find_population_midlat():
    ents = Ent.list_from_type(ENT_TYPE)
    lats_and_pop = [(ent.centroid[0], ent.population) for ent in ents]
    total_pop = sum([pop for __, pop in lats_and_pop])
    sorted_lats_and_pop = sorted(lats_and_pop, key=lambda x: x[0])
    running_pop = 0
    for lat, pop in sorted_lats_and_pop:
        running_pop += pop
        if running_pop > total_pop / 2:
            return lat


def build_map_nocache(label, func_is_south, image_path):
    ents = Ent.list_from_type(ENT_TYPE)
    n_ents = len(ents)

    plt.title(label)
    ax = plt.gca()

    for i_ent, ent in enumerate(ents):
        is_south = func_is_south(ent)
        if i_ent % 100 == 0:
            log.debug(
                f'{label} {i_ent}/{n_ents}'
                + f' ({ent.id}) {ent.name}\t -> {is_south}'
            )
        color = COLOR.SOUTH if is_south else COLOR.NORTH
        try:
            geo = ent.geo()
            geo.plot(ax=ax, color=color)
        except BaseException:
            log.error(f'Failed to draw {ent.id}')
    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])

    plt.savefig(image_path, dpi=600)
    plt.close()
    log.info(f'Saved {image_path}')
    os.startfile(image_path)


def build_map(label, func_is_south):
    id = re.sub(r'\W+', '-', label)
    image_path = f'{__file__}.{id}.png'

    if os.path.exists(image_path):
        log.info(f'Already exists {image_path}')
        return

    build_map_nocache(label, func_is_south, image_path)


def main():
    # lat_lng
    build_map('Latitude', lambda ent: ent.centroid[0] < MID_LAT)

    # population
    population_midlat = find_population_midlat()
    log.debug(f'{population_midlat=}')
    build_map(
        'Population Midpoint',
        lambda ent: ent.centroid[0] < population_midlat,
    )

    # name
    build_map('Province (1889 to Present)', lambda ent: 'LK-3' in ent.id)
    build_map(
        'Province (1886 to 1889)',
        lambda ent: 'LK-3' in ent.id or 'LK-91' in ent.id,
    )
    build_map(
        'Province (1833 to 1886)',
        lambda ent: 'LK-3' in ent.id
        or 'LK-91' in ent.id
        or (
            ('LK-23' in ent.id or 'LK-8' in ent.id)
            and (ent.centroid[0] < 6.75)
        ),
    )

    # Ruhuna
    y1, x1 = [8.627065368127024, 81.22475803344648]
    y2, x2 = [7.3439535978450055, 80.98185630310215]
    y3, x3 = [7.277279644820882, 80.5903026319759]
    y4, x4 = [6.633164495000538, 80.50560572439693]
    y5, x5 = [6.427988464153805, 79.99438086963133]

    m12 = (y2 - y1) / (x2 - x1)
    c12 = y1 - m12 * x1

    m23 = (y3 - y2) / (x3 - x2)
    c23 = y2 - m23 * x2

    m34 = (y4 - y3) / (x4 - x3)
    c34 = y3 - m34 * x3

    m45 = (y5 - y4) / (x5 - x4)
    c45 = y4 - m45 * x4

    build_map(
        'Ancient Ruhuna',
        lambda ent: all(
            [
                any(
                    [
                        ent.centroid[0] < m12 * ent.centroid[1] + c12,
                        all(
                            [
                                ent.centroid[0] < m23 * ent.centroid[1] + c23,
                                ent.centroid[0] < m34 * ent.centroid[1] + c34,
                            ]
                        ),
                        ent.centroid[0] < m45 * ent.centroid[1] + c45,
                    ]
                ),
            ]
        ),
    )

    # Ethnicity & Religion
    gig_table_eth = GIGTable('population-ethnicity', 'regions', '2012')

    def p_sinhalese(ent):
        row = ent.gig(gig_table_eth)
        return row.sinhalese / row.total

    build_map(
        'Ethnicity (Majority Sinhala)',
        lambda ent: p_sinhalese(ent) > 0.5,
    )


    build_map(
        'Ethnicity (>80% Sinhala)',
        lambda ent: p_sinhalese(ent) > 0.8,
    )


    gig_table_rel = GIGTable('population-religion', 'regions', '2012')

    def p_buddhist(ent):
        row = ent.gig(gig_table_rel)
        return row.buddhist / row.total

    build_map(
        'Religion (Majority Buddhist)',
        lambda ent: p_buddhist(ent) > 0.5,
    )

    build_map(
        'Religion (>80% Buddhist)',
        lambda ent: p_buddhist(ent) > 0.8,
    )

    # Elections
    global ENT_TYPE 
    ENT_TYPE = EntType.PD
    gig_table_prespoll_2019 = GIGTable(
        'government-elections-presidential', 'regions-ec', '2019'
    )

    def p_slpp(ent):
        row = ent.gig(gig_table_prespoll_2019)
        return row.SLPP / row.valid

    build_map(
        '2019 Presidential Election (Majority SLPP)',
        lambda ent: p_slpp(ent) > 0.5,
    )

    gig_table_prespoll_2015 = GIGTable(
        'government-elections-presidential', 'regions-ec', '2015'
    )

    def p_upfa(ent):
        row = ent.gig(gig_table_prespoll_2015)
        return row.UPFA / row.valid

    build_map(
        '2015 Presidential Election (Majority UPFA)',
        lambda ent: p_upfa(ent) > 0.5,
    )


if __name__ == '__main__':
    main()
