def calculate_force(mass: float, acceleration: float) -> str:
    """Calculate force in newtons using Newton's second law F = m*a."""
    try:
        return str(mass * acceleration)
    except Exception as e:
        return f"Error calculating force: {e}"

def kinematics_velocity(initial_velocity: float, acceleration: float, time: float) -> str:
    """Calculate final velocity using v = u + a*t."""
    try:
        return str(initial_velocity + acceleration * time)
    except Exception as e:
        return f"Error calculating velocity: {e}"
