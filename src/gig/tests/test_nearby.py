"""Test gig_data."""
import unittest

from gig import nearby


class TestNearby(unittest.TestCase):
    """Test."""

    def test_get_nearby_entities(self):
        """Test."""
        lat, lng = 6.9073, 79.8638  # Cinnamon Gardens Police Station
        distance_info_list = nearby.get_nearby_entities([lat, lng])
        closest_entity_info = distance_info_list[0]
        self.assertEqual(
            closest_entity_info['entity']['name'],
            'Cinnamon Garden',
        )
