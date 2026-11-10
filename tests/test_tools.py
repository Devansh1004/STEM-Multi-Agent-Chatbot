import sympy as sp

from mcp_server.tools_math import solve_algebra, differentiate, integrate, find_limit, get_power

def test_solve_algebra():
    result = solve_algebra("x**2 - 5*x + 6 = 0")
    assert result == "[2, 3]"

def test_differentiate():
    result = differentiate("x**3 + 5*x**2")
    assert result == "3*x**2 + 10*x"

def test_integrate():
    result = integrate("x**2")
    assert result == "x**3/3"

def test_limit():
    result = find_limit("sin(x)/x", variable="x", point="0")
    assert result == "1"

def test_get_power():
    result = get_power("3", power=2)
    assert result == "9"
