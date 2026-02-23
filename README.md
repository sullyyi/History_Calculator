# History Calculator

A modular, professional-grade command-line calculator application built in Python with full unit testing, 100% test coverage, and continuous integration using GitHub Actions.

---

## Overview

This project implements a modular command-line calculator using clean architecture principles.

It supports:

- A fully interactive REPL (Read–Eval–Print Loop)
- Arithmetic operations (add, subtract, multiply, divide)
- Input validation and robust error handling
- Calculation history tracking
- Factory pattern for calculation creation
- 100% unit test coverage enforced in continuous integration
- Automated testing via GitHub Actions

The project emphasizes clean architecture, maintainability, DRY principles, and professional development practices.

---

## REPL Interface

The application runs as a continuous command-line session allowing users to:

- Perform calculations  
- View calculation history  
- Request help  
- Exit cleanly  

---

## Supported Commands

- `add a b` — Adds two numbers  
- `sub a b` — Subtracts two numbers  
- `mul a b` — Multiplies two numbers  
- `div a b` — Divides two numbers  
- `history` — Displays session history  
- `help` — Displays instructions  
- `exit` — Exits the program  

---

## Error Handling Strategy

This application demonstrates both error handling paradigms:

### LBYL (Look Before You Leap)

Used in division to explicitly check for division by zero.

### EAFP (Easier to Ask Forgiveness than Permission)

Used when converting user input to floats via `try/except`.

All invalid input cases are handled gracefully with clear, user-friendly error messages.

---

## Calculation History

The `CalculationHistory` class:

- Stores session calculations  
- Supports retrieval and formatted output  
- Maintains clean separation of concerns  

---

## Testing

This project uses pytest with:

- Unit tests for all modules  
- Parameterized tests  
- Positive and negative case testing  
- REPL logic testing via dependency injection  
- 100% test coverage enforcement  

### Run Tests Locally

From the `calculator-app` directory:
pytest --cov=app tests/ --cov-report=term-missing --cov-fail-under=100


If coverage falls below 100%, the test run will fail.

---

## Continuous Integration

GitHub Actions automatically performs the following on every push to `main`:

- Installs dependencies  
- Runs all tests  
- Measures coverage  
- Fails if coverage is less than 100%  

The workflow configuration file is located at:
.github/workflows/python-app.yml


---

## Setup Instructions

### Clone the Repository
git clone <repository-url>
cd History_Calculator/calculator-app


### Create Virtual Environment

Mac/Linux:
python -m venv .venv
source .venv/bin/activate


Windows:
python -m venv .venv
..venv\Scripts\activate


### Install Dependencies
pip install -r requirements.txt


---

## Running the Calculator

From inside the `calculator-app` directory:
python -c "from app.calculator.cli import run_repl; run_repl()"

### Example Usage

add 2 3
Result: 5.0
div 1 0
Error: Cannot divide by zero.
history
add 2 3 = 5.0

