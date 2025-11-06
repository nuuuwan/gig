import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from utils import Log

from gig import Ent, EntType

log = Log(os.path.basename(os.path.dirname(__file__)))


def draw_histogram(title, values, unit):
    plt.figure(figsize=(12, 6))
    plt.hist(
        values,
        bins=50,
        color="steelblue",
        alpha=0.7,
        edgecolor="black",
        linewidth=0.5,
    )

    median_pop = np.median(values)
    p10 = stats.scoreatpercentile(values, 10)
    p90 = stats.scoreatpercentile(values, 90)
    for [value, label, color] in [
        [p10, "10th Percentile", "green"],
        [median_pop, "Median", "orange"],
        [p90, "90th Percentile", "red"],
    ]:
        plt.axvline(
            value,
            color=color,
            linestyle="--",
            linewidth=2,
            label=f"{label} - {value:,.0f} {unit}",
        )

    plt.xlabel(f"{title} ({unit})")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of GND {title}")
    plt.legend()
    plt.grid(True, axis="y")

    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.tight_layout()

    image_path = os.path.join(os.path.dirname(__file__), f"{title}.png")
    plt.savefig(image_path, dpi=300)
    log.info(f"Wrote {image_path}")


def draw_xy_plot(ents):
    populations = [ent.population for ent in ents]
    areas = [ent.area for ent in ents]

    plt.figure(figsize=(12, 8))
    plt.scatter(areas, populations, alpha=0.6, color="steelblue", s=50)

    plt.xlabel("Area (sq.km)")
    plt.ylabel("Population")
    plt.title("Population vs Area for GNDs")
    plt.grid(True, alpha=0.3)

    # Remove box/spines
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.tight_layout()

    image_path = os.path.join(
        os.path.dirname(__file__), "population_vs_area.png"
    )
    plt.savefig(image_path, dpi=300)
    log.info(f"Wrote {image_path}")


def main():

    ents = [
        ent
        for ent in Ent.list_from_type(EntType.DSD)
        if ent.population and ent.area
    ]
    n_ents = len(ents)
    log.debug(f"{n_ents=}")
    populations = [ent.population for ent in ents]
    areas = [ent.area for ent in ents]

    draw_histogram("Population", populations, "persons")
    draw_histogram("Area", areas, "sq.km")
    draw_xy_plot(ents)


if __name__ == "__main__":
    main()
