# calculator/pkg/calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.strip() == "":
            return None  # Or raise a specific error like ValueError("Expression cannot be empty or whitespace only")
        tokens = expression.strip().split()
        result = self._evaluate_infix(tokens)
        # If the result is a whole number, convert it to an integer
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        
        # Handle division by zero
        if operator == '/' and b == 0:
            raise ValueError("division by zero")
            
        values.append(self.operators[operator](a, b))
