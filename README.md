# Rule Engine with Abstract Syntax Tree (AST)

## Project Overview
This project implements a **Rule Engine** that parses rules using an Abstract Syntax Tree (AST) and evaluates them against user-provided data. It allows users to define complex conditions using a simple rule-based syntax (e.g., "age > 30 AND salary > 50000"). These rules are then converted into an AST, which makes it easier to evaluate and combine complex expressions efficiently.

## Features
- Parse rule strings into an AST for efficient evaluation.
- Support for logical operators such as `AND` and `OR`.
- Evaluate rules based on user data input.
- Save and retrieve rules from a database using SQLAlchemy.
- Combine multiple rules for more complex conditions.

## Installation Instructions

### Prerequisites
- **Python 3.10.0** is required.
- **pip** for installing Python packages.
- Optional: **Docker** for containerization.

### Step-by-Step Installation

### 1. Clone the repository:
   ```bash
   git clone https://github.com/USERNAME/Rule-Engine-with-AST.git
   cd Rule-Engine-with-AST
```

### 2. Set up a virtual environment (recommended):

It is recommended to use a virtual environment to isolate project dependencies.
### On Windows:
 ```bash
 python -m venv venv
 venv\Scripts\activate

```
### On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3.Install the required dependencies: 

Install the project dependencies listed in the requirements.txt file.

```bash
pip install -r requirements.txt
```

#### Dependencies
- Python 3.x: The primary language for this project.
- SQLAlchemy: For managing the database and storing rules.
- Requests: For making API requests (if needed).
- Python-dotenv: For managing environment variables.
- Unittest: For running unit tests.


### 4.Run the application locally: 
Once the dependencies are installed, run the application:

```bash
python main.py
```
## Usage Instructions
### 1.Define a Rule:
Use the following Python code to define a rule:
```python
rule_string = "age > 30 AND salary > 50000"
ast = parse_rule(rule_string)
```
### 2. Evaluate the Rule:
Evaluate the rule against user data:

```python
user_data = {"age": 35, "salary": 60000}
result = evaluate_rule(ast, user_data)
print(result)  # Expected output: True
```
### 3. Save and Retrieve Rules:
Save rules to the database:

```python
rule_id = save_rule(ast)
```
Retrieve a saved rule:

```python
retrieved_ast = get_rule(rule_id)
```
### 4. Combine Multiple Rules:
Combine multiple ASTs for complex conditions:
```python
combined_ast = combine_rules(asts)
```
### 5. Modify an Existing Rule:
You can modify an existing rule by changing the AST:

```python
modified_rule = modify_rule(rule_id, new_rule_string)
```

## Design Choices
### 1. Abstract Syntax Tree (AST) for Rule Parsing
AST provides a scalable way to parse and evaluate rules, handling complex logical operations such as AND, OR. It enables easy future extensions for more advanced operations.

### 2. SQLAlchemy for Database Operations
SQLAlchemy provides flexibility in interacting with databases such as SQLite, PostgreSQL, etc. It allows easy persistence and retrieval of rules from the database.
### 3. Error Handling
Implemented error handling for invalid rule strings or data formats. If a rule string is malformed or if required attributes are missing, the application raises an appropriate error.



## Testing
### Running Unit Tests
Unit tests are provided to ensure the system behaves as expected. Run the tests using:

```bash
python -m unittest discover
```
### Example Test Cases
Test Rule Parsing:
```python
def test_parse_rule():
    rule_string = "age > 30 AND salary > 50000"
    ast = parse_rule(rule_string)
    assert ast.type == 'operator'
```
Test Rule Evaluation:
```python
def test_evaluate_rule():
    rule_string = "age > 30 AND salary > 50000"
    ast = parse_rule(rule_string)
    user_data = {"age": 35, "salary": 60000}
    result = evaluate_rule(ast, user_data)
    assert result == True
```
## Bonus Features
- Rule Modification: Users can modify existing rules by changing operators, operand values, or adding/removing sub-expressions.
- Attribute Validation: Attributes used in rules are validated against a predefined catalog, ensuring that only valid attributes are used.
- Error Handling: Graceful error handling for malformed rule strings or missing operators and operands.



## License

This project is licensed under the MIT License. See the LICENSE file for details.


 
