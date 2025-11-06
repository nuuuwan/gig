import numpy as np
from scipy import stats

from gig import Ent, EntType


def main():

    ents = Ent.list_from_type(EntType.GND)

    ents.sort(key=lambda x: x.population)
    populations = [ent.population for ent in ents]

    areas = [ent.area for ent in ents]

    print(populations[:10])
    print(areas[:10])


if __name__ == "__main__":
    main()
