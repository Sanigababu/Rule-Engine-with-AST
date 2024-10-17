import re
from flask import Flask, request, jsonify

# Node class representing each element in the AST
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # Left child for operator nodes
        self.right = right     # Right child for operator nodes
        self.value = value     # Operand value (e.g., "age > 30")

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

ALLOWED_ATTRIBUTES = {"age", "department", "salary", "experience"}  # validation for attributes

def validate_attributes(data):
    for key in data.keys():
        if key not in ALLOWED_ATTRIBUTES:
            raise ValueError(f"Invalid attribute: {key}")

# Parse rule string into an AST
def parse_rule(rule_string):
    tokens = re.findall(r'\w+|[><=!]+|AND|OR|\(|\)', rule_string)
    return build_ast(tokens)

def build_ast(tokens):
    stack = []
    current_operator = None
    operand = ""

    for token in tokens:
        print(f"Processing token: {token}")  # Debugging output

        if token in ['AND', 'OR']:
            # Ensure that we are not trying to create an operator node without operands
            if operand:
                # Create operand node for the complete expression before the operator
                stack.append(Node('operand', value=operand.strip()))
                operand = ""  # Reset operand for the next expression
            
            if stack:
                # Create operator node only if there's an operand in the stack
                right = stack.pop()  # Right node will be the last operand
                left = stack.pop() if stack else None  # Left node may not exist
                stack.append(Node('operator', left, right, value=current_operator if current_operator else 'AND'))
            
            current_operator = token  # Update the current operator
        else:
            operand += f"{token} "  # Collect operand parts

    # Push the last operand to the stack if there's any
    if operand:
        stack.append(Node('operand', value=operand.strip()))

    # Combine operands with operators to build the AST
    while len(stack) > 1:
        right = stack.pop()  # Right node
        left = stack.pop()   # Left node
        stack.append(Node('operator', left, right, value=current_operator if current_operator else 'AND'))

    return stack[0] if stack else None

# Flask application
app = Flask(__name__)


def evaluate_rule(ast, data):
    validate_attributes(data)  # Validate attributes before evaluation
    if ast.type == 'operand':
        parts = ast.value.split()
        if len(parts) != 3:
            raise ValueError(f"Invalid operand format: {ast.value}")
        attribute, operator, value = parts
        value = int(value)
        if operator == '>':
            return data.get(attribute, 0) > value
        elif operator == '<':
            return data.get(attribute, 0) < value
        elif operator == '=':
            return data.get(attribute, 0) == value
    elif ast.type == 'operator':
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
    return False

# Error handling
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

def format_ast(node):
    if not node:
        return ""
    left = format_ast(node.left)
    right = format_ast(node.right)

    if node.type == "operator":
        return f"({left} {node.value} {right})" if left and right else f"{node.value}"
    else:
        return f"{node.value}"
    
def combine_rules(asts):
    if not asts:
        return None
    combined = asts[0]
    for ast in asts[1:]:
        combined = Node('operator', combined, ast, value='AND')
    return combined


# Example usage
if __name__ == "__main__":
    rule_string = "age > 30 AND salary > 50000"
    ast = create_rule(rule_string)
    print("Formatted AST:", format_ast(ast))
