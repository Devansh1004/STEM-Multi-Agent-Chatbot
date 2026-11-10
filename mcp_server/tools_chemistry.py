import math

def ideal_gas_law(pressure: float = None, volume: float = None, moles: float = None, temperature: float = None) -> str:
    """Solve the ideal gas law P*V = n*R*T for the missing value given exactly three known values."""
    try:
        R = 8.314
        if pressure is None:
            return str(moles * R * temperature / volume)
        if volume is None:
            return str(moles * R * temperature / pressure)
        if moles is None:
            return str(pressure * volume / (R * temperature))
        if temperature is None:
            return str(pressure * volume / (moles * R))
        return "Error: provide exactly three known values"
    except Exception as e:
        return f"Error solving ideal gas law: {e}"

def ph_from_concentration(hydrogen_ion_concentration: float) -> str:
    """Calculate pH from hydrogen ion concentration in moles per liter."""
    try:
        return str(-math.log10(hydrogen_ion_concentration))
    except Exception as e:
        return f"Error calculating pH: {e}"
