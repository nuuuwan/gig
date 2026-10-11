import math
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


def distance1(ent, latlng2):
    lat1, lng1 = ent.d["center_lat"], ent.d["center_lng"]
    lat2, lng2 = latlng2
    return abs(lat1 - lat2) + abs(lng1 - lng2)


SORTER_IDX = dict(
    colombo=lambda ent: distance2(ent, LAT_LNG_COLOMBO),
    colombo1=lambda ent: distance1(ent, LAT_LNG_COLOMBO),
    kandy=lambda ent: distance2(ent, LAT_LNG_KANDY),
    galle=lambda ent: distance2(ent, LAT_LNG_GALLE),
    jaffna=lambda ent: distance2(ent, LAT_LNG_JAFFNA),
    batticaloa=lambda ent: distance2(ent, LAT_LNG_BATTICALOA),
    lat=lambda ent: ent.d["center_lat"],
    lng=lambda ent: ent.d["center_lng"],
)
BACKGROUND_COLOR = "#80d0ed"

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


def get_best_ent_sorter(ents, n_groups):
    total_population = sum(get_id_to_population(ents).values())
    min_area = None
    min_area_ent = None
    for ent in ents:
        latlng = [ent.d["center_lat"], ent.d["center_lng"]]
        sorted_ents = sorted(ents, key=lambda e: distance2(e, latlng))

        cum_area = 0
        cum_population = 0

        for ent1 in sorted_ents:
            cum_area += ent1.area_sqkm
            cum_population += get_id_to_population([ent1])[ent1.id]
            if cum_population >= total_population / n_groups:
                break

        if not min_area_ent or cum_area < min_area:
            min_area = cum_area
            min_area_ent = ent

    return lambda ent: distance2(
        ent, [min_area_ent.d["center_lat"], min_area_ent.d["center_lng"]]
    )


def draw(
    n_groups: int,
    parent_id: str,
    ent_type: EntType,
    sorter_id: str,
):
    colors = plt.get_cmap("RdYlGn_r").resampled(n_groups)
    ents = Ent.list_from_type(ent_type)
    ents = [ent for ent in ents if parent_id in ent.id or parent_id == "LK"]

    id_to_population = get_id_to_population(ents)
    if sorter_id == "densest":
        id_to_density = [
            (ent.id, id_to_population[ent.id] / ent.area_sqkm) for ent in ents
        ]
        densest_ent = max(id_to_density, key=lambda x: x[1])[0]
        latlng_densest = [
            Ent.from_id(densest_ent).d["center_lat"],
            Ent.from_id(densest_ent).d["center_lng"],
        ]
        sorter = lambda ent: distance2(ent, latlng_densest)
    elif sorter_id == "best":
        sorter = get_best_ent_sorter(ents, n_groups)

    else:
        sorter = SORTER_IDX[sorter_id]
    ents.sort(key=sorter)
    parent_ent = Ent.from_id(parent_id)

    total_population = sum(id_to_population.values())
    cum_population = 0
    fig, ax = plt.subplots(
        figsize=FIG_SIZE,
        facecolor=BACKGROUND_COLOR,
    )
    ax.set_facecolor(BACKGROUND_COLOR)
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.94)
    i_to_population = {}
    i_to_area = {}
    total_area = sum([ent.area_sqkm for ent in ents])
    for ent in ents:
        area = ent.area_sqkm
        population = id_to_population[ent.id]
        color_i = (
            math.ceil(n_groups * cum_population / total_population) - 1
            if cum_population > 0
            else 0
        )
        color = colors(color_i)
        cum_population += population
        geo = ent.geo()
        geo.plot(ax=ax, color=color)

        i_to_population[color_i] = i_to_population.get(color_i, 0) + population

        i_to_area[color_i] = i_to_area.get(color_i, 0) + area

    ax.margins(0.01)
    ax.set_axis_off()
    name = parent_ent.name + " " + EntType.from_id(parent_id).name.upper()
    ax.set_title(f"{name} in {n_groups} equal Parts")
    ax.legend(
        handles=[
            mpatches.Patch(
                color=colors(color_i),
                label=(
                    f"{population / total_population:.0%} pop. "
                    f"{i_to_area[color_i] / total_area:.0%} area"
                ),
            )
            for color_i, population in i_to_population.items()
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.01),
        ncol=min(2, len(i_to_population)),
        borderaxespad=0,
    )

    image_path = (
        "examples/half-population/"
        + f"n{n_groups}-{parent_id}.by-{ent_type.name}.{sorter_id}.png"
    )
    fig.savefig(
        image_path,
        dpi=300,
        facecolor=BACKGROUND_COLOR,
        bbox_inches="tight",
        pad_inches=0.03,
    )
    print(f"Wrote {image_path}")


if __name__ == "__main__":
    for n_groups in range(2, 6 + 1):
        for parent_id in ["LK"]:
            for ent_type in [EntType.GND]:
                for sorter_id in ["best"]:
                    draw(
                        n_groups,
                        parent_id,
                        ent_type,
                        sorter_id,
                    )
