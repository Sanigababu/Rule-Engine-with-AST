import re

# Node class representing each element in the AST
class Node:
    def __init__(self, node_type, left=None, right=None, value=None, is_function=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # Left child for operator nodes
        self.right = right     # Right child for operator nodes
        self.value = value     # Operand value (e.g., "age > 30")
        self.is_function = is_function  # New attribute to check if it's a function

# Parse rule string into an AST
def parse_rule(rule_string):
    tokens = re.findall(r'\w+|[><=!]+|AND|OR|\(|\)', rule_string)
    print(f"Tokens: {tokens}")  # Print tokens for debugging

    def build_ast(tokens):
        stack = []
        current_operator = None
        operand = ""

        for token in tokens:
            print(f"Processing token: {token}")  # Print current token
            if token in ['AND', 'OR']:
                if operand:
                    # Create operand node for the complete expression before the operator
                    stack.append(Node('operand', value=operand.strip()))
                    operand = ""  # Reset operand for the next expression
                current_operator = token
            else:
                if current_operator:
                    # Complete the previous operand with the current token
                    operand += f"{token} "  # Append current token to operand
                else:
                    # We are directly dealing with an operand
                    operand += f"{token} "

        # Push the last operand to the stack if there's any
        if operand:
            stack.append(Node('operand', value=operand.strip()))

        # Now, combine operands with operators to build the AST
        while len(stack) > 1:
            right = stack.pop()
            left = stack.pop()
            stack.append(Node('operator', left, right, value=current_operator if current_operator else 'AND'))

        return stack[0] if stack else None

    return build_ast(tokens)

ALLOWED_ATTRIBUTES = {"age", "department", "salary", "experience"} #validation for attributes

def validate_attributes(data):
    for key in data.keys():
        if key not in ALLOWED_ATTRIBUTES:
            raise ValueError(f"Invalid attribute: {key}")

def evaluate_rule(ast, data):
    if ast.type == 'operand':
        parts = ast.value.split()
        if len(parts) != 3:
            raise ValueError(f"Invalid operand format: {ast.value}")
        attribute, operator, value = parts
        value = int(value)
        print(f"Evaluating: {attribute} {operator} {value}")  # Print evaluation details
        if operator == '>':
            return data.get(attribute, 0) > value
        elif operator == '<':
            return data.get(attribute, 0) < value
        elif operator == '=':
            return data.get(attribute, 0) == value
    elif ast.type == 'operator':
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        print(f"Operator: {ast.value}, Left: {left_result}, Right: {right_result}")  # Print results of evaluation
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
    return False

# Combine multiple ASTs
def combine_rules(asts):
    if not asts:
        return None
    combined = asts[0]
    for ast in asts[1:]:
        combined = Node('operator', combined, ast, value='AND')
    return combined

#Error handling
def create_rule(rule_string):
    if not rule_string:
        raise ValueError("Rule string cannot be empty.")
    
    # Basic validation for operators
    valid_operators = ['>', '<', '=', 'AND', 'OR']
    tokens = re.findall(r'\w+|[><=!]+|AND|OR|\(|\)', rule_string)
    
    for token in tokens:
        if token not in valid_operators and not token.isidentifier():
            raise ValueError(f"Invalid token in rule: {token}")

    return parse_rule(rule_string)

