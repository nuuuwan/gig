import os

import matplotlib.pyplot as plt
from utils import File, Log

from gig import Ent, EntType

log = Log("example-area")

MAP_CRS = "EPSG:3395"
PANEL_SIZE = 3


def draw_area_visual(ent_type, n_cols):
	ents = []
	for ent in Ent.list_from_type(ent_type):
		geo = ent.geo().to_crs(MAP_CRS)
		ents.append((ent, geo))

	ents.sort(key=lambda item: item[0].area, reverse=True)

	n_rows = (len(ents) + n_cols - 1) // n_cols
	fig, axes = plt.subplots(
		n_rows,
		n_cols,
		figsize=(n_cols * PANEL_SIZE, n_rows * PANEL_SIZE),
	)
	fig.patch.set_facecolor("#f7f4ec")

	max_span = max(
		max(
			geo.total_bounds[2] - geo.total_bounds[0],
			geo.total_bounds[3] - geo.total_bounds[1],
		)
		for _, geo in ents
	)
	half_span = max_span * 0.515
	colors = plt.cm.YlGn(
		[0.85 - rank * 0.5 / max(1, len(ents) - 1) for rank in range(len(ents))]
	)

	for rank, ((ent, geo), ax, color) in enumerate(
		zip(ents, axes.flat, colors), start=1
	):
		geo.plot(ax=ax, color=color, edgecolor="#18392b", linewidth=0.7)

		min_x, min_y, max_x, max_y = geo.total_bounds
		center_x = (min_x + max_x) / 2
		center_y = (min_y + max_y) / 2
		ax.set_xlim(center_x - half_span, center_x + half_span)
		ax.set_ylim(center_y - half_span, center_y + half_span)
		ax.set_aspect("equal")
		ax.axis("off")
		ax.set_title(
			f"{rank}. {ent.name}\n{ent.area:,.0f} sq. km",
			fontsize=10,
			fontweight="bold",
			color="#1d2b24",
			pad=5,
		)

	for ax in axes.flat[len(ents) :]:
		ax.axis("off")

	fig.suptitle(
		f"Sri Lanka {ent_type.name.title()}s by Area",
		fontsize=22,
		fontweight="bold",
		color="#14231c",
		y=0.975,
	)
	plt.subplots_adjust(top=0.87, bottom=0.025, left=0.03, right=0.97, hspace=0.36)

	image_path = os.path.join(
		os.path.dirname(__file__), f"{ent_type.name}s-by-area.png"
	)
	plt.savefig(image_path, dpi=300, facecolor=fig.get_facecolor())
	plt.close(fig)
	log.info(f"Wrote {File(image_path)}")


def main():
	draw_area_visual(EntType.DISTRICT, n_cols=5)
	draw_area_visual(EntType.PROVINCE, n_cols=3)


if __name__ == "__main__":
	main()
