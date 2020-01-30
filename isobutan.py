"""
a combination of the
 - ideal gas law and
 - a simple chemical reaction

But still, no warranty.
"""
# %% constants
AVOGARDRO = 6.02214076 * 10 ** 23  # 1/mol
BOLTZMANN = 1.380649 * 10 ** -23  # J/K or Nm/K or (kgm^2)/(Ks^2)
UNIVERSAL_GAS = AVOGARDRO * BOLTZMANN  # J/(molK) or (kgm^2)/(molKs^2)

# %% atomic masses in kg/mol or units/atom
CARBON_MOLAR = 12 / 1000
OXYGEN_MOLAR = 16 / 1000
HYDROGEN_MOLAR = 1 / 1000
NITROGEN_MOLAR = 14 / 1000
ISOBUTAN_MOLAR = 4 * CARBON_MOLAR + 10 * HYDROGEN_MOLAR

# %% environment
AIR_COMPOSITION_BY_VOLUME = {
    'nitrogen': 0.79,
    'oxygen': 0.21
}
# using standard temperature and pressure
TEMPERATURE = 273.15  # K
PRESSURE = 1.0 * 100000  # Pa or kg/(ms^2)

# %% reaction
# (4 * C + 10 * H) + 6.5 * O_2 --react--> 5 * H_2O + 4 * CO2 
# 1 mol of isobutan needs 6.5 mols of oxygen to burn completly
# or 1 mol of oxygen can completely burn (1 / 6.5) mols of isobutan
OXYGEN_TO_ISOBUTAN_RATIO = 6.5


def get_oxygen_volume_of_air(air):
    return air * AIR_COMPOSITION_BY_VOLUME['oxygen']


def get_air_volume_of_oxygen(oxygen):
    return oxygen / AIR_COMPOSITION_BY_VOLUME['oxygen']


def calc_volume_to_mol(volume):
    """
    pV = NRT solved for N: N = PV/(RT)
    expects `volume` to be cubic meters m^3
    """
    return (volume * PRESSURE) / (UNIVERSAL_GAS * TEMPERATURE)


def calc_mol_to_volume(mols):
    """
    pV = NRT solved for V: V = NRT/p
    returns in `V` in cubic meters m^3
    """
    return (mols * UNIVERSAL_GAS * TEMPERATURE) / PRESSURE


def oxygen_needed_for_isobutan(mols):
    return mols * OXYGEN_TO_ISOBUTAN_RATIO


def isobutan_needed_for_oxygen(mols):
    return mols / OXYGEN_TO_ISOBUTAN_RATIO


def air_volume_for_isobutan_mols(mols):
    """returns cubic meters m^3"""
    oxygen_mols = oxygen_needed_for_isobutan(mols)
    oxygen_volume = calc_mol_to_volume(oxygen_mols)
    air_volume = get_air_volume_of_oxygen(oxygen_volume)
    return air_volume


def isobutan_vol_to_air_vol(volume_isobutan):
    """returns cubic meters m^3"""
    mols_isobutan = calc_volume_to_mol(volume_isobutan)
    return air_volume_for_isobutan_mols(mols_isobutan)
     

def air_vol_to_isobutan_vol(volume_air):
    """returns cubic meters m^3"""
    volume_oxygen = get_oxygen_volume_of_air(volume_air)
    mols_oxygen = calc_volume_to_mol(volume_oxygen)
    mols_isobutan = isobutan_needed_for_oxygen(mols_oxygen)
    return calc_mol_to_volume(mols_isobutan)
    

def print_needed_air(isobutan_volume):
    """does not account for container volume"""
    print(
        f'{isobutan_vol_to_air_vol(isobutan_volume) * 1000:.3f} liters of air'
        f' are needed for a stoichiometric reaction of'
        f' {isobutan_volume * 1000:.3f} liters of isobutan'
    )


def print_needed_isobutan(air_volume):
    """does not account for container volume"""
    print(
        f'{air_vol_to_isobutan_vol(air_volume) * 1000:.3f} liters of isobutan'
        f' are needed for a stoichiometric reaction of' 
        f' {air_volume * 1000:.3f} liters of air'
    )


if __name__ == '__main__':
    ISOBUTAN_VOLUME = 0.1 / 1000  # m^3
    AIR_VOLUME = 3.095 / 1000  # m^3
    print_needed_air(ISOBUTAN_VOLUME)
    print_needed_isobutan(AIR_VOLUME)
