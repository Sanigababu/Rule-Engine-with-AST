# test_import.py
try:
    from ast_parser import parse_rule, combine_rules, evaluate_rule, Node
    print("Import successful!")
except ImportError as e:
    print(f"Import error: {e}")
