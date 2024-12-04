import os
from functools import cache, cached_property

from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from utils import Log

from gig import Ent, EntType

log = Log("ex-3-01")


class PopulationDensityBandMap:

    def __init__(self, parent_ent_id, ent_type):
        self.parent_ent_id = parent_ent_id
        self.ent_type = ent_type

    @cached_property
    def ent_list(self):
        return sorted(
            [
                ent
                for ent in Ent.list_from_type(self.ent_type)
                if self.parent_ent_id in ent.id
            ],
            key=lambda ent: ent.population_density,
        )

    @property
    def parent_ent(self):
        return Ent.from_id(self.parent_ent_id)

    @cached_property
    def total_population(self):
        return sum(ent.population for ent in self.ent_list)

    @cached_property
    def total_area(self):
        return sum(ent.area for ent in self.ent_list)

    @cache
    def get_color(
        self,
        p_population,
    ):
        for config_item in self.get_legend_config():
            min_p_population, max_p_population = config_item["bounds"]
            if min_p_population < p_population <= max_p_population:
                return config_item["color"]
        return "#fff"

    def add_legend(self, plt):
        handles = []
        for config_item in self.get_legend_config():
            min_p_population, max_p_population = config_item["bounds"]
            p_area = self.get_p_area_for_population(
                min_p_population, max_p_population
            )
            p_population_span = max_p_population - min_p_population
            handle = mpatches.Patch(
                color=config_item["color"],
                label=f"{p_population_span:.0%} Pop. ({p_area:.0%} Area)",
            )
            handles.append(handle)
        plt.legend(handles=handles)

    def get_p_area_for_population(self, min_p_population, max_p_population):

        cum_population = 0

        filtered_ent_list = []
        for ent in self.ent_list:

            cum_population += ent.population
            p_population = cum_population / self.total_population
            if min_p_population <= p_population <= max_p_population:
                filtered_ent_list.append(ent)

        return sum(ent.area for ent in filtered_ent_list) / self.total_area

    def get_p_population_for_area(self, min_p_area, max_p_area):

        cum_area = 0

        filtered_ent_list = []
        for ent in self.ent_list:
            cum_area += ent.area
            p_area = cum_area / self.total_area
            if min_p_area <= p_area <= max_p_area:
                filtered_ent_list.append(ent)

        return (
            sum(ent.population for ent in filtered_ent_list)
            / self.total_population
        )

    def render_parent_region_boundaries(self, ax):
        ent_list = Ent.list_from_type(EntType.DISTRICT)
        for ent in ent_list:
            ent.geo_safe().plot(
                ax=ax,
                color="#fff0",
                edgecolor="#fff",
                linewidth=0.1,
            )

    def render_ents(self, ax):

        cum_area = 0
        cum_population = 0
        for ent in self.ent_list:
            cum_area += ent.area
            cum_population += ent.population

            p_population = cum_population / self.total_population
            print(
                f"({p_population:.1%}) {ent.id} {ent.name}".ljust(80), end="\r"
            )

            ent.geo_safe().plot(ax=ax, color=self.get_color(p_population))

    @cached_property
    def image_path(self):
        dir_images = os.path.join(
            os.path.dirname(__file__), "images", self.ent_type.name
        )
        os.makedirs(dir_images, exist_ok=True)

        return os.path.join(
            dir_images,
            ".".join(
                [
                    self.parent_ent_id,
                    self.parent_ent.name,
                    "png",
                ]
            ),
        )

    def hide_grid(self, ax):
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    def draw(self):
        plt.close()

        ax = plt.gca()
        self.render_ents(ax)
        # self.render_parent_region_boundaries(ax)
        self.hide_grid(ax)
        self.add_legend(plt)

        plt.gcf().set_size_inches(8, 9)
        plt.title(self.parent_ent.name)
        plt.savefig(self.image_path, dpi=300)
        plt.close()

        log.info(f"Saved {self.image_path}")
        # os.startfile(self.image_path)

    @cache
    def get_legend_config(self):

        p1 = 0.01
        p2 = 0.5

        return [
            dict(
                color="#08f",
                bounds=(0, p1),
            ),
            dict(
                color="#8f0",
                bounds=(p1, p2),
            ),
            dict(
                color="#f00",
                bounds=(p2, 1),
            ),
        ]


if __name__ == "__main__":
    district_ent_list = Ent.list_from_type(EntType.DISTRICT)

    for district_ent in district_ent_list:
        PopulationDensityBandMap(district_ent.id, EntType.GND).draw()
