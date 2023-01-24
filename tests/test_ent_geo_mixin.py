import filecmp
import os
from unittest import TestCase

import matplotlib.pyplot as plt

from gig import Ent


class TestEntGeoMixin(TestCase):
    def test_geo(self):
        for id in ['LK-11']:
            ent = Ent.from_id(id)
            geo = ent.geo()
            geo.plot()
            png_file_name = f'gig.TestEntGeoMixin.{id}.png'
            test_png_file_path = os.path.join('/tmp', png_file_name)
            plt.savefig(test_png_file_path)

            control_png_file_path = os.path.join('tests/', png_file_name)
            self.assertTrue(
                filecmp.cmp(test_png_file_path, control_png_file_path)
            )
