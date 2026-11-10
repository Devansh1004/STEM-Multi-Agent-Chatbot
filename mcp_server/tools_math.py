import sympy as sp

def solve_algebra(expression: str) -> str:
    """Solve an algebraic equation or expression."""
    try:
        x = sp.symbols("x")

        if "=" in expression:
            lhs, rhs = expression.split("=")
            equation = sp.Eq(
                sp.sympify(lhs.strip()),
                sp.sympify(rhs.strip()),
            )
        else:
            equation = sp.sympify(expression)

        solutions = sp.solve(equation, x)
        return str(solutions)

    except Exception as e:
        return f"Error solving expression: {e}"
    
def differentiate(expression: str, variable: str = "x") -> str:
    """Differentiate a mathematical expression with respect to a variable."""
    try:
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        derivative = sp.diff(expr, var)
        return str(derivative)
    
    except Exception as e:
        return f"Error differentiating expression: {str(e)}"

def integrate(expression: str, variable: str = "x") -> str:
    """Integrate a mathematical expression with respect to a variable."""
    try:
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        integral = sp.integrate(expr, var)
        return str(integral)
    
    except Exception as e:
        return f"Error integrating expression: {str(e)}"

def find_limit(expression: str, variable: str = "x", point: str = "0") -> str:
    """Find the limit of a mathematical expression as the variable approaches a point."""
    try:
        var = sp.symbols(variable)
        expr = sp.sympify(expression)
        lim = sp.limit(expr, var, sp.sympify(point))
        return str(lim)
    
    except Exception as e:
        return f"Error finding limit: {str(e)}"
    
def get_power(expression : str, power : int = 2) -> str:
    "Raise an integer number or expression to a power."
    try:
        expr = sp.sympify(expression)
        power_expr = sp.Pow(expr, power)
        return str(power_expr)
    
    except Exception as e:
        return f"Error raising expression to a power: {str(e)}"
