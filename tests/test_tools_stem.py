import math

from mcp_server.tools_physics import calculate_force, kinematics_velocity
from mcp_server.tools_astronomy import orbital_period, escape_velocity
from mcp_server.tools_engineering import ohms_law, stress_calculation
from mcp_server.tools_chemistry import ideal_gas_law, ph_from_concentration
from mcp_server.tools_computer_science import base_convert, time_complexity_compare

def test_calculate_force():
    assert calculate_force(10, 5) == "50"

def test_kinematics_velocity():
    assert kinematics_velocity(5, 2, 4) == "13"

def test_orbital_period():
    result = float(orbital_period(1.5e11, 1.989e30))
    assert 3.0e7 < result < 3.3e7

def test_escape_velocity():
    result = float(escape_velocity(5.97e24, 6.371e6))
    assert 11000 < result < 11500

def test_ohms_law_voltage():
    assert ohms_law(current=2, resistance=10) == "20"

def test_ohms_law_current():
    assert ohms_law(voltage=12, resistance=4) == "3.0"

def test_stress_calculation():
    assert stress_calculation(500, 0.02) == "25000.0"

def test_ideal_gas_law_pressure():
    result = float(ideal_gas_law(volume=0.05, moles=2, temperature=300))
    assert 99000 < result < 100000

def test_ph_from_concentration():
    result = float(ph_from_concentration(1e-7))
    assert abs(result - 7.0) < 0.001

def test_base_convert_binary_to_decimal():
    assert base_convert("1010", 2, 10) == "10"

def test_base_convert_decimal_to_hex():
    assert base_convert("255", 10, 16) == "FF"

def test_time_complexity_compare():
    result = time_complexity_compare(100, "O(n)", "O(n^2)")
    assert "faster=O(n)" in result
