from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

from ast_parser import Node

# Initialize the base class for models
Base = declarative_base()

# Define the Rule model
class Rule(Base):
    __tablename__ = 'rules'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_json = Column(JSON)  # Store the AST as JSON
    description = Column(String)  # Optional: description or metadata about the rule

# Setup SQLite or any other database
DATABASE_URL = 'sqlite:///rules.db'  # SQLite database file
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create the rules table if it doesn't exist
Base.metadata.create_all(engine)

# Function to save a rule (AST) to the database
def save_rule(ast):
    """
    Save the given AST (as JSON) to the database.
    """
    rule = Rule(rule_json=json.dumps(ast_to_dict(ast)))  # Convert AST to JSON before saving
    session.add(rule)
    session.commit()
    return rule.id  # Return the rule's ID after saving

# Function to convert AST to a dictionary (for JSON storage)
def ast_to_dict(ast):
    if not ast:
        return None
    return {
        'type': ast.type,
        'value': ast.value,
        'left': ast_to_dict(ast.left),
        'right': ast_to_dict(ast.right)
    }

# Function to retrieve a rule (AST) from the database by ID
def get_rule(rule_id):
    """
    Fetch the AST from the database using the rule ID.
    """
    rule = session.query(Rule).filter_by(id=rule_id).first()
    if rule:
        return dict_to_ast(json.loads(rule.rule_json))  # Convert the JSON back into an AST
    return None

# Function to convert a dictionary (JSON) back into an AST
def dict_to_ast(data):
    if not data:
        return None
    return Node(
        node_type=data['type'],
        left=dict_to_ast(data['left']),
        right=dict_to_ast(data['right']),
        value=data['value']
    )
