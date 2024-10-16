"""Draww BandVisual"""

import os
from functools import cached_property

from matplotlib import pyplot as plt
from utils import Log, Parallel

from gig import Ent, EntType

CENTER_COLOMBO = [6.961312108947133, 79.85694398099878]

log = Log("examples")


class Int:
    @staticmethod
    def humanize(n):
        """Humanize Integer"""
        if n > 10_000_000:
            return f"{n/1_000_000:.0f}M"
        if n > 1_000_000:
            return f"{n/1_000_000:.1f}M"
        if n > 100_000:
            return f"{n/100_000:.0f}K"
        return f"{n}"


class Progress:
    """Console Progress Bar"""

    N_BARS = 10

    @staticmethod
    def get(p):
        """Render Progress Bar"""
        n = int(p * Progress.N_BARS)
        bars = "🟩" * n + "⬛" * (Progress.N_BARS - n)
        return f"[{bars} {p:.1%}]"


class Color:
    """Color Utils"""

    COLORS = ["red", "orange", "yellow", "green", "blue"]
    N_COLORS = len(COLORS)

    @staticmethod
    def get(i_band):
        """Get color for band"""
        return Color.COLORS[i_band % Color.N_COLORS]


class BandVisual:
    """Implements Band Visual"""

    def __init__(self, parent_ent_id_list, ent_type, center):
        self.parent_ent_id_list = parent_ent_id_list
        self.ent_type = ent_type
        self.center = center

    def get_image_path(self, n_bands):
        """Get Image Path to save visual"""
        return os.path.join(
            "examples",
            "example_9_band_visual",
            ".".join(
                [
                    "-".join(self.parent_ent_id_list),
                    self.ent_type.name.lower(),
                    f"{n_bands:02d}",
                    "png",
                ]
            ),
        )

    def get_distance(self, p):
        """Get Distance from Center"""
        return ((p[0] - self.center[0]) ** 2 + (p[1] - self.center[1]) ** 2) ** 0.5

    def is_in_parent(self, ent_id):
        """Check if id is inside parent region"""
        for parent_ent_id in self.parent_ent_id_list:
            if parent_ent_id in ent_id:
                return True
        return False

    @cached_property
    def ents_list(self):
        """Get Ent List"""
        ent_list = [
            ent
            for ent in Ent.list_from_type(self.ent_type)
            if self.is_in_parent(ent.id)
        ]
        ent_list.sort(key=lambda ent: self.get_distance(ent.centroid))
        return ent_list

    @cached_property
    def total_pop(self):
        """Total Population"""
        return sum([ent.population for ent in self.ents_list])

    @cached_property
    def ent_info_list(self):
        """Ent Info List"""
        ent_list = self.ents_list
        total_pop = sum([ent.population for ent in ent_list])
        cum_pop = 0
        ent_info_list = []
        for ent in ent_list:
            p_pop = cum_pop / total_pop
            ent_info = {
                "ent": ent,
                "p_pop": p_pop,
            }
            ent_info_list.append(ent_info)
            cum_pop += ent.population
        return ent_info_list

    @cached_property
    def geo_idx(self):
        """Get Geo Index"""
        ent_list = self.ents_list
        n = len(ent_list)

        def get_worker(i, ent):

            def worker(i=i, ent=ent):
                p = i / n
                print(f"{Progress.get(p)} {ent.id} {ent.name}".ljust(40), end="\r")
                try:
                    geo = ent.geo()
                except Exception as e:
                    log.error(f"[{ent.id}] {e}")
                    geo = None
                return ent.id, geo

            return worker

        workers = [get_worker(i, ent) for i, ent in enumerate(ent_list, start=1)]

        tuple_list = Parallel.run(workers, max_threads=32)
        geo_idx = dict(tuple_list)
        return geo_idx

    @staticmethod
    def draw_core(ax, n_bands, ent_info_list, geo_idx):
        """Draw core visual"""
        log.debug("Drawing...")
        n = len(ent_info_list)

        for i, ent_info in enumerate(ent_info_list, start=1):
            p = i / n
            ent = ent_info["ent"]
            print(f"{Progress.get(p)} Drawing {ent.id} {ent.name}".ljust(40), end="\r")

            p_pop = ent_info["p_pop"]
            i_band = int(p_pop * n_bands)
            color = Color.get(i_band)
            geo = geo_idx[ent.id]
            if geo is not None:
                geo.plot(ax=ax, color=color, alpha=1)

    @staticmethod
    def draw_boundaries(ax, is_in_parent):
        """Draw boundaries"""
        for ent in Ent.list_from_type(EntType.DISTRICT):
            if is_in_parent(ent.id):
                geo = ent.geo()
                geo.plot(
                    ax=ax, color="white", edgecolor="black", linewidth=1, alpha=0.333
                )
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])

        # Remove outer border (spines)
        for spine in ax.spines.values():
            spine.set_visible(False)

    def draw(self, n_bands):
        """Draw"""
        ax = plt.gca()
        BandVisual.draw_core(ax, n_bands, self.ent_info_list, self.geo_idx)
        BandVisual.draw_boundaries(ax, self.is_in_parent)

        band_pop = Int.humanize(23_100_000 / n_bands)

        plt.title(f"[{n_bands:02d}] ~{band_pop} people/band")
        image_path = self.get_image_path(n_bands)
        plt.savefig(image_path, dpi=1200)
        plt.close()
        log.info(f"Wrote {image_path}")


if __name__ == "__main__":
    bv = BandVisual(
        parent_ent_id_list=["LK"],
        ent_type=EntType.GND,
        center=CENTER_COLOMBO,
    )
    for n_bands in range(1, 22 + 1):
        bv.draw(n_bands)
