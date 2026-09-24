from gig import Ent, EntType
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse



data_list = [
    dict(
        name='Colombo District',
        ent_ids=['LK-11'],
        color='red',
    ),
    dict(
        name='Colombo Municipal Council',
        ent_ids=['LK-1103', 'LK-1127'],
        color='blue',

    ),
    dict(
        name='Colombo DSD',
        ent_ids=['LK-1103'],
        color='green',
    )
]

fig, ax = plt.subplots(figsize=(10, 6.5))
ax.set_axis_off()
geo_by_ent_id = {}

for data in data_list:
    for ent_id in data['ent_ids']:
        ent = Ent.from_id(ent_id)
        geo = ent.geo()
        geo_by_ent_id[ent_id] = geo
        geo.plot(ax=ax, color=data['color'])

padding_by_color = {
    'red': 1.8,
    'blue': 1.8,
    'green': 1.5,
}
oval_extents = []
arrow_targets = {}

for data in data_list:
    bounds = [geo_by_ent_id[ent_id].total_bounds for ent_id in data['ent_ids']]
    min_x = min(bound[0] for bound in bounds)
    min_y = min(bound[1] for bound in bounds)
    max_x = max(bound[2] for bound in bounds)
    max_y = max(bound[3] for bound in bounds)
    padding = padding_by_color[data['color']]
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = (max_x - min_x) * padding
    height = (max_y - min_y) * padding
    ax.add_patch(Ellipse(
        (center_x, center_y),
        width=width,
        height=height,
        fill=False,
        edgecolor=data['color'],
        linewidth=2,
        zorder=10,
    ))
    arrow_targets[data['color']] = {
        'red': (center_x + width / 2, center_y),
        'blue': (center_x, center_y - height / 2),
        'green': (center_x, center_y + height / 2),
    }[data['color']]
    oval_extents.append((
        center_x - width / 2,
        center_y - height / 2,
        center_x + width / 2,
        center_y + height / 2,
    ))

min_x = min(extent[0] for extent in oval_extents)
min_y = min(extent[1] for extent in oval_extents)
max_x = max(extent[2] for extent in oval_extents)
max_y = max(extent[3] for extent in oval_extents)
margin_x = (max_x - min_x) * 0.03
margin_y = (max_y - min_y) * 0.03
ax.set_xlim(min_x - margin_x, max_x + margin_x)
ax.set_ylim(min_y - margin_y, max_y + margin_y)

label_positions = {
    'red': (0.68, 0.78),
    'blue': (0.48, 0.12),
    'green': (0.03, 0.90),
}
for data in data_list:
    ax.annotate(
        data['name'],
        xy=arrow_targets[data['color']],
        xycoords='data',
        xytext=label_positions[data['color']],
        textcoords='axes fraction',
        color=data['color'],
        fontfamily='Gill Sans',
        fontsize=10,
        bbox={
            'facecolor': 'white',
            'edgecolor': 'none',
            'pad': 1.5,
        },
        arrowprops={
            'arrowstyle': '->',
            'color': data['color'],
            'connectionstyle': 'arc3,rad=0.12',
            'linewidth': 1.5,
        },
    )

fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
plt.savefig(
    'examples/example-colombo/colombo.png',
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.02,
)
plt.close()
    