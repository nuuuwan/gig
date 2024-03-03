import math
import os
import random
from dataclasses import dataclass

from utils import LatLng, Log, _

from gig import Ent, EntType

log = Log('example-7')
random.seed(2)
WIDTH, HEIGHT = 600, 1000
PADDING = 50

RADIUS_LATLNG = 0.024


@dataclass
class Shape:
    id: str
    name: str
    centroid: LatLng
    i_shape: int


def get_random_color() -> str:
    return f'#{random.randint(0, 0xFFFFFF):06x}'


def get_color(label) -> str:
    i = int(label[-2:])
    i3 = i % 3
    h = int(300 * i / 25)
    s = 100
    l = 25 * (i3 + 1)
    a = 0.5
    return f'hsla({h},{s}%,{l}%,{a})'


def render_polygon(label, cx, cy, r, n, color):
    points = []
    theta = math.pi / 2
    for i in range(n):
        x = cx + r * math.cos(2 * math.pi * i / n + theta)
        y = cy + r * math.sin(2 * math.pi * i / n + theta)
        points.append(f'{x},{y}')
    points.append(points[0])
    points = ' '.join(points)

    return _(
        'g',
        [
            # _(
            #     'polygon',
            #     None,
            #     dict(
            #         points=points, fill=color, stroke="black", stroke_width=2
            #     ),
            # ),
            _(
                'circle',
                None,
                dict(
                    cx=cx,
                    cy=cy,
                    r=r,
                    fill=color,
                    stroke="black",
                    stroke_width=1,
                ),
            ),
            # _(
            #     'text',
            #     label,
            #     dict(
            #         x=cx,
            #         y=cy + font_size / 2,
            #         fill="black",
            #         font_size=font_size,
            #         font_family="sans-serif",
            #         text_anchor="middle",
            #     ),
            # ),
        ],
    )


def render_shape(ent, t):
    lat, lng = ent.centroid
    cx, cy = t(LatLng(lat, lng))
    cx1, cy1 = t(LatLng(lat + RADIUS_LATLNG, lng + RADIUS_LATLNG))
    r = ((cx1 - cx) ** 2 + (cy1 - cy) ** 2) ** 0.5
    color = get_color(ent.id[:5])
    label = ''.join([c[:2] for c in ent.name.split(' ')])
    n = 6
    return render_polygon(label, cx, cy, r, n, color)


def move_shapes(
    ents: list[Ent],
    N_EPOCHS: int = 1_000,
    MIN_D: float = RADIUS_LATLNG * 3,
    ALPHA: float = 0.1,
) -> dict[str, LatLng]:
    n = len(ents)

    for epoch in range(N_EPOCHS):
        print(f'', end='\r')
        n_overlaps = 0
        for i1 in range(0, n - 1):
            lat1, lng1 = ents[i1].centroid
            for i2 in range(i1 + 1, n):
                lat2, lng2 = ents[i2].centroid
                dlat = lat2 - lat1
                dlng = lng2 - lng1
                d = (dlat**2 + dlng**2) ** 0.5
                if d < MIN_D:
                    if dlat == 0 and dlng == 0:
                        dlat = random.random() * ALPHA
                        dlng = random.random() * ALPHA

                    n_overlaps += 1
                    ents[i1].centroid = (
                        ents[i1].centroid[0] - dlat * ALPHA,
                        ents[i1].centroid[1] - dlng * ALPHA,
                    )
                    ents[i2].centroid = (
                        ents[i2].centroid[0] + dlat * ALPHA,
                        ents[i2].centroid[1] + dlng * ALPHA,
                    )
        p_overlaps = n_overlaps / (n * (n - 1) / 2)
        print(f'{epoch=:,}, {n_overlaps=:,}, {p_overlaps=:.3%}', end='\r')

        if n_overlaps == 0:
            log.info(f'✅ Converged at {epoch=}')
            break

    log.info(f'🏁 Finished at {epoch=}')


def render(ents: list[Ent]):
    shapes = []
    min_pop = max(20_000, min(ent.population for ent in ents))
    log.debug(f'{min_pop=:,}')
    for ent in ents:
        shapes_per_ent = int(round(ent.population / min_pop, 0))
        for i_shape in range(shapes_per_ent):
            shape = Shape(
                id=ent.id,
                name=ent.name,
                centroid=ent.centroid,
                i_shape=i_shape,
            )
            shapes.append(shape)
    n_shapes = len(shapes)
    log.debug(f'{n_shapes=}')

    move_shapes(shapes)
    latlng_list = [LatLng(*shape.centroid) for shape in shapes]
    t = LatLng.get_func_t(latlng_list, WIDTH, HEIGHT, PADDING)
    rendered_shapes = [render_shape(shape, t) for shape in shapes]

    svg = _('svg', rendered_shapes, dict(width=WIDTH, height=HEIGHT))
    path = __file__[:-3] + '.svg'
    svg.store(path)
    log.info(f'Wrote {path}')
    os.startfile(path)


def main():
    ents = Ent.list_from_type(EntType.PD)
    # ents = [ent for ent in ents if ent.id[:5] in ['EC-01', 'EC-02', 'EC-03']]
    log.debug(f'n={len(ents)}')
    render(ents)


if __name__ == "__main__":
    main()
