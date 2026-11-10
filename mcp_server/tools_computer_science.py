import math

def base_convert(number: str, from_base: int, to_base: int) -> str:
    """Convert a number between numeral bases such as binary, decimal, and hexadecimal."""
    try:
        decimal_value = int(number, from_base)
        if to_base == 10:
            return str(decimal_value)
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if decimal_value == 0:
            return "0"
        result = ""
        n = decimal_value
        while n > 0:
            result = digits[n % to_base] + result
            n //= to_base
        return result
    except Exception as e:
        return f"Error converting base: {e}"

def time_complexity_compare(n: int, complexity_a: str, complexity_b: str) -> str:
    """Compare the growth of two algorithmic time complexities at a given input size n."""
    try:
        def evaluate(c):
            c = c.lower().replace(" ", "")
            if c == "o(1)":
                return 1
            if c == "o(logn)":
                return math.log2(n) if n > 0 else 0
            if c == "o(n)":
                return n
            if c == "o(nlogn)":
                return n * math.log2(n) if n > 0 else 0
            if c == "o(n^2)":
                return n ** 2
            if c == "o(2^n)":
                return 2 ** n
            raise ValueError("unsupported complexity")
        a = evaluate(complexity_a)
        b = evaluate(complexity_b)
        faster = complexity_a if a < b else complexity_b
        return f"{complexity_a}={a}, {complexity_b}={b}, faster={faster}"
    except Exception as e:
        return f"Error comparing complexities: {e}"
