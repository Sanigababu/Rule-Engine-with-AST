
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

1. **Clone the repository**:
   ```bash
   git clone https://github.com/USERNAME/Rule-Engine-with-AST.git
   cd Rule-Engine-with-AST
