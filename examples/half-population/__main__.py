from functools import cache

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from gig import Ent, EntType, GIGTable

LAT_LNG_COLOMBO = [6.927079, 79.861243]
LAT_LNG_KANDY = [7.290572, 80.633728]
LAT_LNG_GALLE = [6.053519, 80.220978]
LAT_LNG_JAFFNA = [9.668450, 80.007420]
LAT_LNG_BATTICALOA = [7.7102, 81.6924]


def distance2(ent, latlng2):
    lat1, lng1 = ent.d["center_lat"], ent.d["center_lng"]
    lat2, lng2 = latlng2
    return (lat1 - lat2) ** 2 + (lng1 - lng2) ** 2


SORTER_IDX = dict(
    lat=lambda ent: ent.d["center_lat"],
    lng=lambda ent: ent.d["center_lng"],
    colombo=lambda ent: distance2(ent, LAT_LNG_COLOMBO),
    kandy=lambda ent: distance2(ent, LAT_LNG_KANDY),
    galle=lambda ent: distance2(ent, LAT_LNG_GALLE),
    jaffna=lambda ent: distance2(ent, LAT_LNG_JAFFNA),
    batticaloa=lambda ent: distance2(ent, LAT_LNG_BATTICALOA),
)
COLOR_IDX = ["red", "green"]

GIG_TABLE_ETHNICITY = GIGTable("population-ethnicity", "regions", "2012")
FIG_SIZE = (6, 6)


def get_id_to_population(ents):
    id_to_population = {}
    for ent in ents:
        try:
            population = ent.gig(GIG_TABLE_ETHNICITY).total
        except Exception as e:
            population = 0
        id_to_population[ent.id] = population
    return id_to_population


def draw(
    ent_type=EntType.PROVINCE,
    sorter_id="lat",
):
    ents = Ent.list_from_type(ent_type)
    ent = ents[0]
    sorter = SORTER_IDX[sorter_id]
    ents.sort(key=sorter)

    id_to_population = get_id_to_population(ents)
    total_population = sum(id_to_population.values())
    cum_population = 0
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    fig.subplots_adjust(right=0.65)
    i_to_population = {}
    i_to_area = {}
    total_area = sum([ent.area_sqkm for ent in ents])
    for ent in ents:
        area = ent.area_sqkm
        population = id_to_population[ent.id]
        color_i = int(2 * cum_population / total_population)
        color = COLOR_IDX[color_i]
        cum_population += population
        geo = ent.geo()
        geo.plot(ax=ax, color=color)

        i_to_population[color_i] = i_to_population.get(color_i, 0) + population

        i_to_area[color_i] = i_to_area.get(color_i, 0) + area

    ax.set_axis_off()
    ax.legend(
        handles=[
            mpatches.Patch(
                color=COLOR_IDX[color_i],
                label=(
                    f"{population / total_population:.0%} pop. "
                    f"{i_to_area[color_i] / total_area:.0%} area"
                ),
            )
            for color_i, population in i_to_population.items()
        ],
        loc="upper left",
        bbox_to_anchor=(0.5, 1),
    )

    image_path = f"examples/half-population/{sorter_id}-{ent_type.name}.png"
    fig.savefig(image_path, dpi=300)
    print(f"Wrote {image_path}")


if __name__ == "__main__":
    for ent_type in [EntType.DSD]:
        for sorter_id in SORTER_IDX.keys():
            draw(ent_type, sorter_id)
