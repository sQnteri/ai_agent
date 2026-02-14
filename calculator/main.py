# calculator/main.py

import sys
from pkg.calculator import Calculator


def main():
    calculator = Calculator()
    print("Calculator App")
    print("Enter 'quit' to exit.")

    while True:
        expression = input("Enter a problem: ")
        if expression.lower() == 'quit':
            break
        elif not expression.strip():
            print("Error: Expression is empty or contains only whitespace.")
            continue

        try:
            result = calculator.evaluate(expression)
            if result is not None:
                print(result)
            else:
                print("Error: Expression is empty or contains only whitespace.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
