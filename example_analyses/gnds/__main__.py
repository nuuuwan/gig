import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from utils import Log

from gig import Ent, EntType

log = Log(os.path.basename(os.path.dirname(__file__)))

ENT_TYPE = EntType.DSD
REASONABLE_FACTOR = 4


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

    median = np.median(values)
    p10 = stats.scoreatpercentile(values, 10)
    p90 = stats.scoreatpercentile(values, 90)
    max_reasonable = median * REASONABLE_FACTOR
    for [value, label, color] in [
        [p10, "10th Percentile", "green"],
        [median, "Median", "orange"],
        [max_reasonable, f"Median x {REASONABLE_FACTOR}", "gray"],
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

    median_population = np.median(populations)
    median_area = np.median(areas)
    max_reasonable_population = median_population * REASONABLE_FACTOR
    max_reasonable_area = median_area * REASONABLE_FACTOR

    # Plot and annotate each point with matching colors
    for ent in ents:
        population, area = ent.population, ent.area
        unreasonable_population = population > max_reasonable_population
        unreasonable_area = area > max_reasonable_area
        if unreasonable_population and unreasonable_area:
            color = "red"
        elif unreasonable_population:
            color = "orange"
        elif unreasonable_area:
            color = "blue"
        else:
            color = "gray"

        # Plot scatter point with same color as annotation
        plt.scatter(area, population, alpha=0.6, color=color, s=50)
        plt.annotate(
            ent.name,
            xy=(ent.area, ent.population),
            xytext=(5, 0),
            textcoords="offset points",
            fontsize=6,
            alpha=0.7,
            color=color,
        )

    plt.xlabel("Area (sq.km)")
    plt.ylabel("Population")
    plt.title("Population vs Area for GNDs")
    plt.grid(True, alpha=0.3)

    # Add legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(
            facecolor="red",
            alpha=0.6,
            label=f"Population > {REASONABLE_FACTOR} x Median & Area > {REASONABLE_FACTOR} x Median",
        ),
        Patch(
            facecolor="orange",
            alpha=0.6,
            label=f"Population > {REASONABLE_FACTOR} x Median",
        ),
        Patch(
            facecolor="blue",
            alpha=0.6,
            label=f"Area > {REASONABLE_FACTOR} x Median",
        ),
        Patch(facecolor="gray", alpha=0.6, label="Normal"),
    ]
    plt.legend(handles=legend_elements, loc="upper left")

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
        for ent in Ent.list_from_type(ENT_TYPE)
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
