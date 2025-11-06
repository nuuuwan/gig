import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from utils import Log

from gig import Ent, EntType

log = Log(os.path.basename(os.path.dirname(__file__)))

REASONABLE_FACTOR = 4


def draw_histogram(ent_type, title, values, unit):
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
    for [value, label, color] in sorted(
        [
            [p10, "10th Percentile", "green"],
            [median, "Median", "orange"],
            [p90, "90th Percentile", "red"],
            [max_reasonable, f"Median x {REASONABLE_FACTOR}", "gray"],
        ],
        key=lambda x: x[0],
    ):
        plt.axvline(
            value,
            color=color,
            linestyle="--",
            linewidth=2,
            label=f"{value:,.0f} {unit} - {label}",
        )

    plt.xlabel(f"{title.title()} ({unit})")
    plt.ylabel("Frequency")
    plt.xscale("log")
    plt.title(f"Histogram of {ent_type.name.upper()} {title.title()}")
    plt.legend()
    plt.grid(True, axis="y")

    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.tight_layout()

    image_path = os.path.join(
        os.path.dirname(__file__), f"{ent_type.name}-{title}.png"
    )
    plt.savefig(image_path, dpi=300)
    log.info(f"Wrote {image_path}")


def draw_xy_plot(ent_type, ents):
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
            color = "orange"
        elif unreasonable_population:
            color = "red"
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
    plt.ylabel("Population (persons)")
    plt.title(f"Population vs Area for {ent_type.name.upper()}")
    plt.grid(True, alpha=0.3)

    plt.axhline(
        y=max_reasonable_population,
        color="red",
        linestyle=":",
        linewidth=2,
        alpha=0.5,
        label=f"{max_reasonable_population:,.0f} persons"
        + f" - Median Population x {REASONABLE_FACTOR}",
    )
    plt.axvline(
        x=max_reasonable_area,
        color="blue",
        linestyle=":",
        linewidth=2,
        alpha=0.5,
        label=f"{max_reasonable_area:,.0f} sq.km"
        + f" - Median Area x {REASONABLE_FACTOR}",
    )

    plt.legend()

    # Remove box/spines
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.tight_layout()

    image_path = os.path.join(
        os.path.dirname(__file__), f"{ent_type.name}-population-vs-area.png"
    )
    plt.savefig(image_path, dpi=300)
    log.info(f"Wrote {image_path}")


def analyze(ent_type):

    ents = [
        ent
        for ent in Ent.list_from_type(ent_type)
        if ent.population and ent.area
    ]
    n_ents = len(ents)
    log.debug(f"{n_ents=}")
    populations = [ent.population for ent in ents]
    areas = [ent.area for ent in ents]

    draw_histogram(ent_type, "population", populations, "persons")
    draw_histogram(ent_type, "area", areas, "sq.km")
    draw_xy_plot(ent_type, ents)


if __name__ == "__main__":
    for ent_type in [EntType.DSD, EntType.GND]:
        analyze(ent_type)
