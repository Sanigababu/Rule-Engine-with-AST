from flask import Flask, request, jsonify
from ast_parser import parse_rule, combine_rules, evaluate_rule
from database import save_rule, get_rule
import json

# Initialize the Flask app
app = Flask(__name__)

# Route to create a rule and generate its AST
@app.route('/create_rule', methods=['POST'])
def create_rule():
    try:
        rule_string = request.json.get('rule')  # Rule in string format from the request body
        ast = parse_rule(rule_string)          # Parse the rule string to AST
        rule_id = save_rule(ast)               # Save the rule to the database (optional)
        return jsonify({"ast": ast, "rule_id": rule_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to combine multiple rules into a single AST
@app.route('/combine_rules', methods=['POST'])
def combine_multiple_rules():
    try:
        rules = request.json.get('rules')     # List of rules from the request body
        asts = [parse_rule(rule) for rule in rules]  # Parse each rule to AST
        combined_ast = combine_rules(asts)    # Combine all the ASTs into one
        return jsonify({"combined_ast": combined_ast}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to evaluate a rule against user data
@app.route('/evaluate_rule', methods=['POST'])
def evaluate():
    try:
        rule_id = request.json.get('rule_id')  # Rule ID to fetch the AST from the database
        user_data = request.json.get('data')   # User data to evaluate the rule
        ast = get_rule(rule_id)                # Fetch the rule AST from the database
        result = evaluate_rule(ast, user_data) # Evaluate the rule against user data
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
