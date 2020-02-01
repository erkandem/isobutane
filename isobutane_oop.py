"""
a combination of the
 - ideal gas law and
 - a simple chemical reaction

object oriented approach
Most important advantage:
 - code instead of comments
 - more comments are now part of doc-strings
"""


class Constants:
    pass


class PhysicalConstants(Constants):
    AVOGARDRO = 6.02214076 * 10 ** 23  # 1/mol
    BOLTZMANN = 1.380649 * 10 ** -23  # J/K or Nm/K or (kgm^2)/(Ks^2)
    UNIVERSAL_GAS = AVOGARDRO * BOLTZMANN  # J/(molK) or (kgm^2)/(molKs^2)


class AtomicMasses(Constants):
    """
    atomic masses in kg/mol
    """
    CARBON_MOLAR = 12 / 1000
    OXYGEN_MOLAR = 16 / 1000
    HYDROGEN_MOLAR = 1 / 1000
    NITROGEN_MOLAR = 14 / 1000
    ISOBUTANE_MOLAR = 4 * CARBON_MOLAR + 10 * HYDROGEN_MOLAR


def get_default_two_element_atmosphere() -> {}:
    return {
            'nitrogen': 0.79,
            'oxygen': 0.21
        }


class Environment:
    """
    default assumptions
        standard temperature
        standard pressure
        simplified earth atmosphere composition
    """

    def __init__(
            self,
            temperature: float = 273.15,  # K
            pressure: float = 1.0 * 100000,  # Pa or kg/(ms^2)
            air_composition_by_volume: {str: float} = None
    ):
        self.TEMPERATURE = temperature
        self.PRESSURE = pressure
        if not air_composition_by_volume:
            air_composition_by_volume = get_default_two_element_atmosphere()
        self.AIR_COMPOSITION_BY_VOLUME = air_composition_by_volume
        self.ensure_sums_up_to_one()

    def get_oxygen_volume_of_air(self, air: float):
        return air * self.AIR_COMPOSITION_BY_VOLUME['oxygen']

    def get_air_volume_of_oxygen(self, oxygen: float):
        return oxygen / self.AIR_COMPOSITION_BY_VOLUME['oxygen']

    def ensure_sums_up_to_one(self):
        grand_total = 1.0
        expected = 0.0
        for share in self.AIR_COMPOSITION_BY_VOLUME.values():
            grand_total = grand_total - share
        if grand_total - expected > 1e-10:
            raise ValueError(f"Percentages of atmosphere don't add up to 1 ({grand_total})")


class GasModel:
    """abstract class"""
    env: Environment

    def calc_mol_to_volume(self, mols: float) -> float:
        pass

    def calc_volume_to_mol(self, mols: float) -> float:
        pass


class IdealGasLaw(GasModel):
    """
    based on the equation `pV = NRT` with:
      - `p` absolute pressure
      - `V` volume
      - `N` quantity of (gas) molecules
      - `R` universal gas constant
      - `T` temperature in Kelvin

    methods could be extended as needed

    Args:
         env (Environment): contains ambient properties used in this model

    """
    env: Environment

    def __init__(self, env: Environment):
        super().__init__()
        self.env = env

    def calc_volume_to_mol(
            self,
            volume: float
    ) -> float:
        """
        pV = NRT solved for N: N = PV/(RT)
        expects `volume` to be cubic meters m^3
        """
        return (
            (volume * self.env.PRESSURE)
            / (PhysicalConstants().UNIVERSAL_GAS * self.env.TEMPERATURE)
        )

    def calc_mol_to_volume(
            self,
            mols: float
    ) -> float:
        """
        pV = NRT solved for V: V = NRT/p
        returns in `V` in cubic meters m^3
        """
        return (
            (mols * PhysicalConstants().UNIVERSAL_GAS * self.env.TEMPERATURE)
            / self.env.PRESSURE
        )


class Reaction:
    pass


class IsobutaneOxygenReaction(Reaction):
    """
    (4 * C + 10 * H) + 6.5 * O_2 --react--> 5 * H_2O + 4 * CO2
    1 mol of isobutane needs 6.5 mols of oxygen to burn completely
    or 1 mol of oxygen can completely burn (1 / 6.5) mols of isobutane
    """
    OXYGEN_TO_ISOBUTANE_RATIO = 6.5

    def __init__(self, gas_model: GasModel):
        self.gas_model = gas_model

    def oxygen_needed_for_isobutane(self, mols: float) -> float:
        return mols * self.OXYGEN_TO_ISOBUTANE_RATIO

    def isobutane_needed_for_oxygen(self, mols: float) -> float:
        return mols / self.OXYGEN_TO_ISOBUTANE_RATIO

    def air_volume_for_isobutane_mols(self, mols: float) -> float:
        """returns cubic meters m^3"""

        oxygen_mols = self.oxygen_needed_for_isobutane(mols)
        oxygen_volume = self.gas_model.calc_mol_to_volume(oxygen_mols)
        air_volume = self.gas_model.env.get_air_volume_of_oxygen(oxygen_volume)
        return air_volume

    def isobutane_vol_to_air_vol(
            self,
            volume_isobutane: float
    ) -> float:
        """returns cubic meters m^3"""
        mols_isobutane = self.gas_model.calc_volume_to_mol(volume_isobutane)
        return self.air_volume_for_isobutane_mols(mols_isobutane)

    def air_vol_to_isobutane_vol(self, volume_air: float) -> float:
        """returns cubic meters m^3"""
        volume_oxygen = self.gas_model.env.get_oxygen_volume_of_air(volume_air)
        mols_oxygen = self.gas_model.calc_volume_to_mol(volume_oxygen)
        mols_isobutane = self.isobutane_needed_for_oxygen(mols_oxygen)
        return self.gas_model.calc_mol_to_volume(mols_isobutane)


def default_reaction_factory():
    env = Environment()
    gas_model = IdealGasLaw(env)
    return IsobutaneOxygenReaction(gas_model)


def print_needed_air(isobutane_volume):
    """does not account for container volume"""
    reaction = default_reaction_factory()
    print(
        f'{reaction.isobutane_vol_to_air_vol(isobutane_volume) * 1000:.3f} liters of air'
        f' are needed for a stoichiometric reaction of'
        f' {isobutane_volume * 1000:.3f} liters of isobutane'
    )


def print_needed_isobutane(air_volume):
    """does not account for container volume"""
    reaction = default_reaction_factory()
    print(
        f'{reaction.air_vol_to_isobutane_vol(air_volume) * 1000:.3f} liters of isobutane'
        f' are needed for a stoichiometric reaction of'
        f' {air_volume * 1000:.3f} liters of air'
    )


def main():
    """extend to accept arguments"""
    ISOBUTANE_VOLUME = 0.1 / 1000  # m^3
    AIR_VOLUME = 3.095 / 1000  # m^3
    print_needed_air(ISOBUTANE_VOLUME)
    print_needed_isobutane(AIR_VOLUME)


if __name__ == '__main__':
    main()
