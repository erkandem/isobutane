import unittest
from isobutane import *


class TestMethods(unittest.TestCase):

    def test_get_oxygen_volume_of_air(self):
        self.assertAlmostEqual(
            get_oxygen_volume_of_air(100),
            21
        )

    def test_get_air_volume_of_oxygen(self):
        self.assertAlmostEqual(
            get_air_volume_of_oxygen(0.21),
            1.0
        )

    def test_calc_volume_to_mol(self):
        self.assertAlmostEqual(
            calc_volume_to_mol(0.02271095464),
            1
        )

    def test_calc_mol_to_volume(self):
        self.assertAlmostEqual(
            calc_mol_to_volume(1),
            0.02271095464
        )

    def test_oxygen_needed_for_isobutan(self):
        self.assertAlmostEqual(
            oxygen_needed_for_isobutane(1),
            6.5
        )

    def test_isobutane_needed_for_oxygen(self):
        self.assertAlmostEqual(
            isobutane_needed_for_oxygen(6.5),
            1
        )

    def test_isobutan_vol_to_air_vol(self):
        self.assertAlmostEqual(
            isobutane_vol_to_air_vol(.1),
            3.095238095
        )

    def test_air_vol_to_isobutan_vol(self):
        self.assertAlmostEqual(
            air_vol_to_isobutane_vol(3.095238095),
            .1
        )

    def test_air_volume_for_isobutan_mols(self):
        self.assertAlmostEqual(
            air_volume_for_isobutane_mols(1.422559853501),
            1.0
        )


if __name__ == '__main__':
    unittest.main()
