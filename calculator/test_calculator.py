from pkg.calculator import Calculator

def test_calculator():
    calculator = Calculator()

    # Test basic arithmetic
    assert calculator.evaluate("1 + 2") == 3.0
    assert calculator.evaluate("5 - 2") == 3.0
    assert calculator.evaluate("2 * 3") == 6.0
    assert calculator.evaluate("6 / 2") == 3.0

    # Test operator precedence
    assert calculator.evaluate("1 + 2 * 3") == 7.0  # Should be 1 + (2 * 3)
    assert calculator.evaluate("6 / 2 + 1") == 4.0  # Should be (6 / 2) + 1
    assert calculator.evaluate("1 + 2 - 3") == 0.0 # Should be (1 + 2) - 3

    # Test division by zero
    try:
        calculator.evaluate("1 / 0")
        assert False, "Expected ValueError for division by zero"
    except ValueError as e:
        assert str(e) == "division by zero"

    # Test invalid expression
    try:
        calculator.evaluate("1 +")
        assert False, "Expected ValueError for invalid expression"
    except ValueError as e:
        assert str(e) == "not enough operands for operator +"

    # Test empty expression
    assert calculator.evaluate("") is None
    assert calculator.evaluate("   ") is None

    print("All test cases passed!")

test_calculator()
