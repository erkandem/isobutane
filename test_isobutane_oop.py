from isobutane_oop import *
import unittest


class TestEnvironment(unittest.TestCase):
    def test_init(self):
        env = Environment()

    def test_setting_custom_temperature(self):
        env = Environment(temperature=0)
        self.assertEqual(
            env.TEMPERATURE,
            0
        )

    def test_setting_custom_pressure(self):
        env = Environment(pressure=0)
        assert env.PRESSURE == 0

    def test_get_oxygen_volume_of_air(self):
        air = 100
        expected = 21
        env = Environment()
        self.assertEqual(
            env.get_oxygen_volume_of_air(air),
            expected
        )

    def test_get_air_volume_of_oxygen(self):
        air = 0.21
        expected = 1
        env = Environment()
        assert env.get_air_volume_of_oxygen(air) == expected

    def test_ensure_sums_up_to_one(self):
        env = Environment()

    def test_ensure_sums_up_to_one_fails(self):
        env = Environment()
        env.AIR_COMPOSITION_BY_VOLUME['nitrogen'] = .50
        self.assertRaises(
            ValueError,
            env.ensure_sums_up_to_one
        )


class TestIdealGasLaw(unittest.TestCase):

    def test_init(self):
        model = IdealGasLaw(Environment())

    def test_init_fails(self):
        self.assertRaises(
            TypeError,
            IdealGasLaw
        )

    def test_calc_mol_to_volume(self):
        model = IdealGasLaw(Environment())
        self.assertAlmostEqual(
            model.calc_mol_to_volume(1),
            0.02271095464
        )

    def test_calc_volume_to_mol(self):
        model = IdealGasLaw(Environment())
        self.assertAlmostEqual(
            model.calc_volume_to_mol(0.02271095464),
            1
        )


class TestIsobutaneOxygenReaction(unittest.TestCase):
    def test_init(self):
        reaction = IsobutaneOxygenReaction(IdealGasLaw(Environment()))

    def test_init_fails(self):
        self.assertRaises(
            TypeError,
            IsobutaneOxygenReaction
        )

    def test_isobutane_vol_to_air_vol(self):
        reaction = IsobutaneOxygenReaction(IdealGasLaw(Environment()))
        self.assertAlmostEqual(
            reaction.isobutane_vol_to_air_vol(.1),
            3.095238095
        )

    def test_isobutane_needed_for_oxygen(self):
        reaction = IsobutaneOxygenReaction(IdealGasLaw(Environment()))
        self.assertAlmostEqual(
            reaction.isobutane_needed_for_oxygen(6.5),
            1
        )

    def test_oxygen_needed_for_isobutane(self):
        reaction = IsobutaneOxygenReaction(IdealGasLaw(Environment()))
        self.assertAlmostEqual(
            reaction.oxygen_needed_for_isobutane(1),
            6.5
        )

    def test_air_volume_for_isobutane_mols(self):
        reaction = IsobutaneOxygenReaction(IdealGasLaw(Environment()))
        self.assertAlmostEqual(
            reaction.air_vol_to_isobutane_vol(3.095238095),
            .1
        )


class TestGasModel(unittest.TestCase):
    def test_init(self):
        model = GasModel()

    def test_calc_mol_to_volume(self):
        model = GasModel()
        model.calc_mol_to_volume(1.0)

    def test_calc_volume_to_mol(self):
        model = GasModel()
        model.calc_volume_to_mol(1.0)


class TestReactionFactory(unittest.TestCase):
    def test_default_reaction_factory(self):
        reaction = default_reaction_factory()


class TestPrintMethods(unittest.TestCase):
    def test_print_needed_air(self):
        print_needed_air(0.1)

    def test_print_needed_isobutane(self):
        print_needed_isobutane(0.1)

    def test_main(self):
        main()


class TestAtmosphere(unittest.TestCase):

    def test_get_default_two_element_atmosphere(self):
        atm = get_default_two_element_atmosphere()
        assert isinstance(atm, dict)


if __name__ == '__main__':
    unittest.main()
