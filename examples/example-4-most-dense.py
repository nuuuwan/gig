import os

from matplotlib import pyplot as plt
from utils import Log

from gig import Ent, EntType

log = Log('ex-4')

ENT_TYPE = EntType.DSD
COLORS = ["#c008", "#0cf8"]
N_COLORS = len(COLORS)


def get_ent_id_to_group(ents):
    ent_id_to_group = {}
    total_pop = sum(ent.population for ent in ents)
    print(ents[0])
    sorted_ents = sorted(ents, key=lambda ent: ent.population, reverse=True)
    cum_pop = 0
    for ent in sorted_ents:
        group = int(cum_pop * N_COLORS / total_pop)
        ent_id_to_group[ent.id] = group
        cum_pop += ent.population

    return ent_id_to_group


def main():
    ents = Ent.list_from_type(ENT_TYPE)

    ax = plt.gca()
    ent_id_to_group = get_ent_id_to_group(ents)

    n_ents = len(ents)
    for i_ent, ent in enumerate(ents):
        group = ent_id_to_group[ent.id]
        color = COLORS[group]
        try:
            geo = ent.geo()
            geo.plot(ax=ax, color=color)
            if (i_ent + 1) % 10 == 0:
                log.debug(f'{i_ent + 1}/{n_ents} Drew {ent.id}')
        except BaseException:
            log.error(f'Failed to draw {ent.id}')
    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])

    image_path = __file__ + '.png'

    plt.savefig(image_path, dpi=600)
    plt.close()
    log.info(f'Saved {image_path}')
    os.startfile(image_path)


if __name__ == '__main__':
    main()
