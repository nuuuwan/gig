from gig import Ent, EntType
import matplotlib.pyplot as plt

ED_TO_SEATS = {
            "EC-01": 18,
        "EC-02": 19,
        "EC-03": 11,
        "EC-04": 12,
        "EC-05": 5,
        "EC-06": 8,
        "EC-07": 9,
        "EC-08": 7,
        "EC-09": 7,
        "EC-10": 6,
        "EC-11": 6,
        "EC-12": 5,
        "EC-13": 7,
        "EC-14": 4,
        "EC-15": 15,
        "EC-16": 8,
        "EC-17": 9,
        "EC-18": 5,
        "EC-19": 9,
        "EC-20": 6,
        "EC-21": 11,
        "EC-22": 9,
}

ents = Ent.list_from_type(EntType.ED)
ax=plt.gca()
for ent in ents:
    ent.geo().plot(ax=ax)

plt.savefig('examples/example-seats/seats.png')
plt.close()