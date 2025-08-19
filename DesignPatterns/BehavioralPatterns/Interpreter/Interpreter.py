from abc import ABC, abstractmethod
from typing import Dict, List

# Abstract Expression
class Expression(ABC):
    """Abstract base class for all expressions"""
    @abstractmethod
    def interpret(self, context: 'Context') -> int:
        """Interpret the expression and return result"""
        pass

# Terminal Expressions
class NumberExpression(Expression):
    """Expression that represents a number"""
    def __init__(self, number: int):
        self.number = number
    
    def interpret(self, context: 'Context') -> int:
        return self.number

class VariableExpression(Expression):
    """Expression that represents a variable"""
    def __init__(self, name: str):
        self.name = name
    
    def interpret(self, context: 'Context') -> int:
        return context.get_variable(self.name)

# Non-Terminal Expressions
class AddExpression(Expression):
    """Expression that represents addition"""
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: 'Context') -> int:
        return self.left.interpret(context) + self.right.interpret(context)

class SubtractExpression(Expression):
    """Expression that represents subtraction"""
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: 'Context') -> int:
        return self.left.interpret(context) - self.right.interpret(context)

class MultiplyExpression(Expression):
    """Expression that represents multiplication"""
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: 'Context') -> int:
        return self.left.interpret(context) * self.right.interpret(context)

class DivideExpression(Expression):
    """Expression that represents division"""
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: 'Context') -> int:
        right_val = self.right.interpret(context)
        if right_val == 0:
            raise ValueError("Division by zero")
        return self.left.interpret(context) // right_val

# Context Class
class Context:
    """Holds variable values and provides interpretation context"""
    def __init__(self):
        self._variables: Dict[str, int] = {}
    
    def set_variable(self, name: str, value: int) -> None:
        """Set a variable value"""
        self._variables[name] = value
    
    def get_variable(self, name: str) -> int:
        """Get a variable value"""
        if name not in self._variables:
            raise ValueError(f"Variable '{name}' not defined")
        return self._variables[name]

# Parser Class
class ExpressionParser:
    """Parses a string expression into an expression tree"""
    def __init__(self):
        self._tokens: List[str] = []
        self._current = 0
    
    def parse(self, expression: str) -> Expression:
        """Parse a string expression into an expression tree"""
        self._tokens = self._tokenize(expression)
        self._current = 0
        return self._expression()
    
    def _tokenize(self, expression: str) -> List[str]:
        """Convert expression string to tokens"""
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i] == ' ':
                i += 1
                continue
            elif expression[i] in '()+-*/':
                tokens.append(expression[i])
                i += 1
            elif expression[i].isdigit():
                num = ''
                while i < len(expression) and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                tokens.append(num)
            elif expression[i].isalpha():
                var = ''
                while i < len(expression) and expression[i].isalpha():
                    var += expression[i]
                    i += 1
                tokens.append(var)
            else:
                raise ValueError(f"Invalid character: {expression[i]}")
        return tokens
    
    def _expression(self) -> Expression:
        """Parse an expression (addition and subtraction)"""
        expr = self._term()
        
        while self._match('+') or self._match('-'):
            operator = self._previous()
            right = self._term()
            if operator == '+':
                expr = AddExpression(expr, right)
            else:
                expr = SubtractExpression(expr, right)
        
        return expr
    
    def _term(self) -> Expression:
        """Parse a term (multiplication and division)"""
        expr = self._factor()
        
        while self._match('*') or self._match('/'):
            operator = self._previous()
            right = self._factor()
            if operator == '*':
                expr = MultiplyExpression(expr, right)
            else:
                expr = DivideExpression(expr, right)
        
        return expr
    
    def _factor(self) -> Expression:
        """Parse a factor (number, variable, or parenthesized expression)"""
        if self._match('('):
            expr = self._expression()
            self._consume(')', "Expected ')' after expression")
            return expr
        elif self._match_number():
            return NumberExpression(int(self._previous()))
        elif self._match_variable():
            return VariableExpression(self._previous())
        else:
            raise ValueError("Expected expression")
    
    def _match(self, expected: str) -> bool:
        """Check if current token matches expected"""
        if self._is_at_end():
            return False
        if self._tokens[self._current] == expected:
            self._current += 1
            return True
        return False
    
    def _match_number(self) -> bool:
        """Check if current token is a number"""
        if self._is_at_end():
            return False
        if self._tokens[self._current].isdigit():
            self._current += 1
            return True
        return False
    
    def _match_variable(self) -> bool:
        """Check if current token is a variable"""
        if self._is_at_end():
            return False
        if self._tokens[self._current].isalpha():
            self._current += 1
            return True
        return False
    
    def _consume(self, expected: str, message: str) -> None:
        """Consume a token or raise error"""
        if self._check(expected):
            self._current += 1
            return
        raise ValueError(message)
    
    def _check(self, expected: str) -> bool:
        """Check if current token is expected"""
        if self._is_at_end():
            return False
        return self._tokens[self._current] == expected
    
    def _previous(self) -> str:
        """Get previous token"""
        return self._tokens[self._current - 1]
    
    def _is_at_end(self) -> bool:
        """Check if we've reached the end of tokens"""
        return self._current >= len(self._tokens)

# Client
def main():
    # Create context and set variables
    context = Context()
    context.set_variable('x', 10)
    context.set_variable('y', 5)
    context.set_variable('z', 2)
    
    # Create parser
    parser = ExpressionParser()
    
    # Test expressions
    expressions = [
        "5 + 3",                    # Simple addition
        "10 - x",                   # Variable subtraction
        "x * y",                    # Variable multiplication
        "y / z",                    # Variable division
        "(x + y) * z",              # Parenthesized expression
        "x + y * z",                # Operator precedence
        "(x + y) * (z + 1)",        # Complex expression
        "100 / (x - y)",            # Division with subtraction
        "x + y + z",                # Multiple additions
        "x * y / z"                 # Multiplication and division
    ]
    
    print("=== Expression Evaluation ===")
    for expr_str in expressions:
        try:
            # Parse the expression
            expression = parser.parse(expr_str)
            
            # Interpret the expression
            result = expression.interpret(context)
            
            print(f"'{expr_str}' = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr_str}': {e}")
    
    # Test error cases
    print("\n=== Error Cases ===")
    error_expressions = [
        "5 +",                      # Incomplete expression
        "x *",                      # Incomplete expression
        "10 / 0",                   # Division by zero
        "(x + y",                   # Unclosed parenthesis
        "x + unknown",              # Undefined variable
        "5 + * 3"                   # Invalid syntax
    ]
    
    for expr_str in error_expressions:
        try:
            expression = parser.parse(expr_str)
            result = expression.interpret(context)
            print(f"'{expr_str}' = {result}")
        except Exception as e:
            print(f"Error evaluating '{expr_str}': {e}")

if __name__ == "__main__":
    main()