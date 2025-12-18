import os

import matplotlib.pyplot as plt

from gig import Ent, EntType


def main(ent_type=None):
    ent_type = ent_type or EntType.GND
    ents = Ent.list_from_type(ent_type)

    _, ax = plt.subplots(figsize=(6, 10))
    plt.gcf().patch.set_facecolor("#002288")
    ax.grid(False)
    ax.axis("off")
    n_ents = len(ents)

    for i in range(n_ents):
        ent_i = ents[i]
        xi, yi = [float(x) for x in (ent_i.center_lon, ent_i.center_lat)]
        for j in range(i + 1, n_ents):
            ent_j = ents[j]
            xj, yj = [float(x) for x in (ent_j.center_lon, ent_j.center_lat)]
            distance = ((xi - xj) ** 2 + (yi - yj) ** 2) ** 0.5
            line_width = min(1, 0.02 / distance)
            if line_width < 0.01:
                continue
            ax.plot(
                [xi, xj],
                [yi, yj],
                color="white",
                alpha=0.3,
                linewidth=line_width,
            )

    image_path = os.path.join("examples", "example-4-line-map.png")
    plt.savefig(image_path, dpi=300)
    plt.close()


if __name__ == "__main__":
    main()
