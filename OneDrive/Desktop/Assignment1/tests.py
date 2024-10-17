import unittest
from ast_parser import parse_rule, combine_rules, evaluate_rule, Node
from database import save_rule, get_rule

class TestRuleEngine(unittest.TestCase):

    def test_parse_rule(self):
        rule_string = "age > 30 AND salary > 50000"
        ast = parse_rule(rule_string)
        self.assertEqual(ast.type, 'operator')  # Check the root node is an operator
        self.assertEqual(ast.value, 'AND')      # Check operator is 'AND'
        self.assertEqual(ast.left.value, 'age > 30')  # Ensure left node is correct
        self.assertEqual(ast.right.value, 'salary > 50000')  # Ensure right node is correct

    def test_evaluate_rule(self):
        rule_string = "age > 30 AND salary > 50000"
        ast = parse_rule(rule_string)
        user_data = {"age": 35, "salary": 60000}
        result = evaluate_rule(ast, user_data)
        self.assertTrue(result)  # Expecting True since the user matches the rule

    def test_save_rule(self):
        rule_string = "age > 30 AND salary > 50000"
        ast = parse_rule(rule_string)
        rule_id = save_rule(ast)  # Save the rule to the database
        self.assertIsNotNone(rule_id)  # Check that the rule was saved and has an ID

    def test_get_rule(self):
        rule_string = "age > 30 AND salary > 50000"
        ast = parse_rule(rule_string)
        rule_id = save_rule(ast)  # Save the rule to the database
        retrieved_ast = get_rule(rule_id)  # Retrieve the rule by its ID
        self.assertEqual(retrieved_ast.type, 'operator')
        self.assertEqual(retrieved_ast.value, 'AND')
        self.assertEqual(retrieved_ast.left.value, 'age > 30')  # Validate left operand
        self.assertEqual(retrieved_ast.right.value, 'salary > 50000')  # Validate right operand
        
    def test_combined_conditions(self):
        rule_string = "age > 30 OR salary > 50000"
        ast = parse_rule(rule_string)
        self.assertEqual(ast.type, 'operator')  # Check the root node is an operator
        self.assertEqual(ast.value, 'OR')       # Check operator is 'OR'
        self.assertEqual(ast.left.value, 'age > 30')  # Ensure left node is correct
        self.assertEqual(ast.right.value, 'salary > 50000')  # Ensure right node is correct

        user_data_1 = {"age": 25, "salary": 60000}
        user_data_2 = {"age": 35, "salary": 40000}
        user_data_3 = {"age": 25, "salary": 40000}

        result_1 = evaluate_rule(ast, user_data_1)  # Should be True (salary condition is met)
        result_2 = evaluate_rule(ast, user_data_2)  # Should be True (age condition is met)
        result_3 = evaluate_rule(ast, user_data_3)  # Should be False (no conditions met)

        self.assertTrue(result_1)
        self.assertTrue(result_2)
        self.assertFalse(result_3)

def test_nested_conditions(self):
    rule_string = "(age > 30 AND salary > 50000) OR (experience > 5)"
    ast = parse_rule(rule_string)
    self.assertEqual(ast.type, 'operator')  # Check the root node is an operator
    self.assertEqual(ast.value, 'OR')       # Check operator is 'OR'
    
    left_subtree = ast.left
    right_subtree = ast.right

    self.assertEqual(left_subtree.type, 'operator')  # Left subtree should be an operator (AND)
    self.assertEqual(left_subtree.value, 'AND')       # Check operator is 'AND'
    self.assertEqual(left_subtree.left.value, 'age > 30')  # Validate left operand of AND
    self.assertEqual(left_subtree.right.value, 'salary > 50000')  # Validate right operand of AND
    self.assertEqual(right_subtree.type, 'operand')  # Right subtree should be an operand
    self.assertEqual(right_subtree.value, 'experience > 5')  # Validate right operand of OR

    user_data_1 = {"age": 35, "salary": 60000, "experience": 2}  # Should return True
    user_data_2 = {"age": 25, "salary": 40000, "experience": 6}  # Should return True
    user_data_3 = {"age": 25, "salary": 40000, "experience": 2}  # Should return False

    result_1 = evaluate_rule(ast, user_data_1)  # True
    result_2 = evaluate_rule(ast, user_data_2)  # True
    result_3 = evaluate_rule(ast, user_data_3)  # False

    self.assertTrue(result_1)
    self.assertTrue(result_2)
    self.assertFalse(result_3)

if __name__ == '__main__':
    unittest.main()
