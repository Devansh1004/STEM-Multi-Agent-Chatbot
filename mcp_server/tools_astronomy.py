import math

def orbital_period(semi_major_axis_m: float, central_mass_kg: float) -> str:
    """Calculate orbital period in seconds using Kepler's third law given semi-major axis and central mass."""
    try:
        G = 6.674e-11
        period = 2 * math.pi * math.sqrt((semi_major_axis_m ** 3) / (G * central_mass_kg))
        return str(period)
    except Exception as e:
        return f"Error calculating orbital period: {e}"

def escape_velocity(mass_kg: float, radius_m: float) -> str:
    """Calculate escape velocity in meters per second for a celestial body given mass and radius."""
    try:
        G = 6.674e-11
        velocity = math.sqrt(2 * G * mass_kg / radius_m)
        return str(velocity)
    except Exception as e:
        return f"Error calculating escape velocity: {e}"
