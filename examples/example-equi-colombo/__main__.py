import colorsys
import math
import os

import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
from utils import File, JSONFile, Log

from gig import Ent, EntType

log = Log("example-equi-colombo")


def draw_area_visual(target_ent_id, ent_type, sorter_name):

    ethnicity_data = JSONFile(
        "examples/example-equi-population-regions/ethnicity.json"
    ).read()
    id_to_pop = {d["region_id"]: d["total_value"] for d in ethnicity_data}

    ax = plt.gca()

    # draw Colombo
    ents = Ent.list_from_type(ent_type)
    ent_target = Ent.from_id(target_ent_id)

    def sorter_distance(ent):
        lat, lng = ent.d["center_lat"], ent.d["center_lng"]
        lat0, lng0 = ent_target.d["center_lat"], ent_target.d["center_lng"]
        return (lat - lat0) ** 2 + (lng - lng0) ** 2

    def sorter_distance3(ent):
        lat, lng = ent.d["center_lat"], ent.d["center_lng"]
        lat0, lng0 = ent_target.d["center_lat"], ent_target.d["center_lng"]
        return (lat - lat0) ** 3 + (lng - lng0) ** 3

    def sorter_lat(ent):
        return ent.d["center_lat"]

    def sorter_lng(ent):
        return ent.d["center_lng"]

    sorter = {
        "distance": sorter_distance,
        "distance3": sorter_distance3,
        "lat": sorter_lat,
        "lng": sorter_lng,
    }[sorter_name]

    ents.sort(key=lambda ent: sorter(ent))
    total_pop = sum(id_to_pop[ent.id] for ent in ents)
    cum_pop = 0
    target_ent_pop = id_to_pop[target_ent_id]
    N_REGIONS = math.ceil(total_pop / target_ent_pop)
    color_group_to_population = {}
    for ent in ents:
        pop = id_to_pop[ent.id]
        if target_ent_id in ent.id:
            h = 0
        else:
            cum_pop += pop
            i_h = (int(N_REGIONS * cum_pop / total_pop) + 1) * 1.0 / N_REGIONS
            h = i_h * 0.8

        rgb = colorsys.hsv_to_rgb(h, 1, 0.75)
        color_group_to_population[h] = (
            color_group_to_population.get(h, 0) + pop
        )
        geo = ent.geo()
        geo.plot(ax=ax, color=rgb, edgecolor="white", linewidth=0.1)

    handles = [
        mpatches.Patch(
            color=colorsys.hsv_to_rgb(h, 1, 0.75),
            label=f"{population / 1_000_000:.0f}M",
        )
        for h, population in color_group_to_population.items()
    ]
    ax.legend(
        handles=handles,
        title="Population",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0,
    )
    ax.set_axis_off()
    image_path = f"examples/example-equi-colombo/image-{target_ent_id}-{ent_type.name}-{sorter_name}.png"
    plt.savefig(image_path, dpi=300, bbox_inches="tight")
    log.info(f"Wrote {File(image_path)}")


def main():
    for sorter_name in ["distance", "distance3", "lat", "lng"]:
        for target_ent_id in ["LK-1"]:
            for ent_type in [
                # EntType.DSD,
                # EntType.DISTRICT,
                EntType.PROVINCE,
            ]:
                draw_area_visual(
                    target_ent_id=target_ent_id,
                    ent_type=ent_type,
                    sorter_name=sorter_name,
                )


if __name__ == "__main__":
    main()
