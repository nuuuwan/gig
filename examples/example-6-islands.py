import os

import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon, Polygon
from utils import Log

from gig import Ent, EntType

MAX_AREA = 0.1**1 * 0.5
MIN_AREA = 0.1**4
AREA_FACTOR = 1_000 * 130.0 / 11.0
DIR_IMAGE = os.path.join('examples', 'example-6')
os.makedirs(DIR_IMAGE, exist_ok=True)

log = Log('example-6')


def main():
    ents = Ent.list_from_type(EntType.DISTRICT)
    i_island = 0
    large_polygons = []
    for ent in ents:
        print(ent.id, ent.name)
        gdf = ent.geo()
        gdf['geometry'] = gdf.geometry.buffer(0)
        if isinstance(gdf.geometry.unary_union, MultiPolygon):
            multipolygon = MultiPolygon(gdf.geometry.unary_union)
            polygons = list(multipolygon.geoms)
        else:
            polygon = Polygon(gdf.geometry.unary_union)
            polygons = [polygon]
        log.debug(f'{ent.name} has {len(polygons)} polygons')
        large_polygons_in_region = [
            polygon
            for polygon in polygons
            if MIN_AREA < polygon.area < MAX_AREA
        ]
        large_polygons.extend(large_polygons_in_region)
        log.debug(
            f'{ent.name} has {len(large_polygons_in_region)} large_polygons_in_region'
        )

    sorted_polygons = sorted(
        large_polygons, key=lambda polygon: polygon.area, reverse=True
    )[1:]

    for i_polygon, polygon in enumerate(sorted_polygons):
        id = chr(i_polygon + ord('A'))
        lng, lat = polygon.centroid.coords[0]

        x, y = polygon.exterior.xy
        file_path = os.path.join(DIR_IMAGE, f'{id}.png')
        plt.plot(x, y)
        area_km2 = round(polygon.area * AREA_FACTOR)

        title = f'{id} ({lat:.2f}°N,{lng:.2f}°E,  {area_km2:.1f}km²)'
        plt.title(title)
        plt.savefig(file_path)
        plt.close()
        log.debug(f'Wrote {file_path}')
        i_island += 1

        gmaps_url = (
            f'https://www.google.com/maps/search/?api=1&query={lat},{lng}'
        )
        # webbrowser.open(gmaps_url)


if __name__ == "__main__":
    main()
