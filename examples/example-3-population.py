import os

from matplotlib import pyplot as plt
from utils import Log

from gig import Ent, EntType

GROUP_LARGER = "GROUP_LARGER"
GROUP_SMALLER = "GROUP_SMALLER"
COLOR_IDX = {GROUP_LARGER: "#f008", GROUP_SMALLER: "#08f8"}

log = Log("ex-3")

ENT_TYPE = EntType.DSD
N_CUTS = 100


def get_bbox(ents):
    min_lat, min_lng = 1000, 1000
    max_lat, max_lng = -1000, -1000
    for ent in ents:
        lat, lng = ent.centroid
        min_lat = min(min_lat, lat)
        min_lng = min(min_lng, lng)
        max_lat = max(max_lat, lat)
        max_lng = max(max_lng, lng)
    lat_span = max_lat - min_lat
    lng_span = max_lng - min_lng

    bbox = min_lat, min_lng, lat_span, lng_span
    return bbox


def get_ent_id_to_group(k, ents):
    min_lat, min_lng, lat_span, lng_span = get_bbox(ents)
    ent_id_to_group = {}
    for ent in ents:
        lat, lng = ent.centroid
        plat = (lat - min_lat) / lat_span
        plng = (lng - min_lng) / lng_span
        p = plat * k + plng * (1 - k)
        group = GROUP_SMALLER if p > 0.5 else GROUP_LARGER
        ent_id_to_group[ent.id] = group
    return ent_id_to_group


def get_group_to_pop_sum(ents, ent_id_to_group):
    group_to_pop_sum = {}
    for ent in ents:
        group = ent_id_to_group[ent.id]
        if group not in group_to_pop_sum:
            group_to_pop_sum[group] = 0
        group_to_pop_sum[group] += ent.population
    return group_to_pop_sum


def get_best_k(ents):
    best_k = None
    max_group_larger_pop = None
    for i in range(0, N_CUTS + 1):
        k = i * 1.0 / N_CUTS
        ent_id_to_group = get_ent_id_to_group(k, ents)
        group_to_pop_sum = get_group_to_pop_sum(ents, ent_id_to_group)

        group_larger_pop = group_to_pop_sum[GROUP_LARGER]
        if max_group_larger_pop is None or group_larger_pop > max_group_larger_pop:
            max_group_larger_pop = group_larger_pop
            best_k = k
    log.info(f"{best_k=}")
    return best_k


def main():
    ents = Ent.list_from_type(ENT_TYPE)

    ax = plt.gca()
    best_k = get_best_k(ents)
    ent_id_to_group = get_ent_id_to_group(best_k, ents)

    n_ents = len(ents)
    for i_ent, ent in enumerate(ents):
        group = ent_id_to_group[ent.id]
        color = COLOR_IDX[group]

        geo = ent.geo()
        geo.plot(ax=ax, color=color)
        if i_ent % 10 == 0:
            log.debug(f"{i_ent + 1}/{n_ents} Drew {ent.id}")

    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])

    image_path = __file__ + ".png"

    plt.savefig(image_path, dpi=600)
    plt.close()
    log.info(f"Saved {image_path}")
    os.startfile(image_path)

    group_to_pop_sum = get_group_to_pop_sum(ents, ent_id_to_group)
    total_population = sum(group_to_pop_sum.values())
    for group, pop_sum in group_to_pop_sum.items():
        log.info(f"{COLOR_IDX[group]} {pop_sum / total_population:.0%}")


if __name__ == "__main__":
    main()
