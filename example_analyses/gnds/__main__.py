import numpy as np
from scipy import stats

from gig import Ent, EntType


def main():

    ents = Ent.list_from_type(EntType.GND)

    ents.sort(key=lambda x: x.population)
    populations = [ent.population for ent in ents]

    ent_ids = [ent.id for ent in ents]
    ent_ids.sort()
    Ent.get_ent_id_to_geo(ent_ids)
    areas = [ent.area for ent in ents]

    print(populations[:10])
    print(areas[:10])


if __name__ == "__main__":
    main()
