def ohms_law(voltage: float = None, current: float = None, resistance: float = None) -> str:
    """Solve Ohm's law V = I*R for the missing value given exactly two of voltage, current, and resistance."""
    try:
        if voltage is None:
            return str(current * resistance)
        if current is None:
            return str(voltage / resistance)
        if resistance is None:
            return str(voltage / current)
        return "Error: provide exactly two known values"
    except Exception as e:
        return f"Error solving Ohm's law: {e}"

def stress_calculation(force: float, area: float) -> str:
    """Calculate mechanical stress in pascals using stress = force / area."""
    try:
        return str(force / area)
    except Exception as e:
        return f"Error calculating stress: {e}"
