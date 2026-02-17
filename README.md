History Calculator
A modular, professional-grade command-line calculator application built in Python with full unit testing, 100% test coverage, and continuous integration using GitHub Actions.
Overview:
This project implements a modular command-line calculator using clean architecture principles. It supports:
A fully interactive REPL (Read–Eval–Print Loop)
Arithmetic operations (add, subtract, multiply, divide)
Input validation and robust error handling
Calculation history tracking
Factory pattern for calculation creation
100% unit test coverage enforced in CI
Automated testing via GitHub Actions
The project emphasizes clean architecture, maintainability, DRY principles, and professional development practices.

Project Structure
History_Calculator/
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── calculator-app/
│   ├── app/
│   │   ├── calculator/
│   │   │   └── cli.py
│   │   │
│   │   ├── calculation/
│   │   │   ├── models.py
│   │   │   ├── factory.py
│   │   │   └── history.py
│   │   │
│   │   └── operation/
│   │       ├── base.py
│   │       └── arithmetic.py
│   │
│   ├── tests/
│   │   ├── test_operations.py
│   │   ├── test_calculations.py
│   │   └── test_cli.py
│   │
│   ├── requirements.txt
│   └── README.md

REPL Interface
The application runs as a continuous command-line session allowing users to:
Perform calculations
View calculation history
Request help
Exit cleanly

Operations:
add      a b	    Adds two numbers
sub      a b	    Subtracts
mul      a b	    Multiplies
div      a b	    Divides
history	            Displays session history
help	            Displays instructions
exit	            Exits the program

Error Handling Strategy
This application demonstrates both:
~LBYL (Look Before You Leap)
Used in division to explicitly check for division by zero.
~EAFP (Easier to Ask Forgiveness than Permission)
Used when converting user input to floats via try/except.
All invalid input cases are handled gracefully with user-friendly error messages.

A CalculationHistory class:
Stores session calculations
Supports retrieval and formatted output
Maintains clean separation of concerns

Testing:
This project uses pytest with:
Unit tests for all modules
Parameterized tests
Positive and negative case testing
REPL logic testing via dependency injection
100% test coverage enforcement

Run tests locally:
From the calculator-app directory:
pytest --cov=app tests/ --cov-report=term-missing --cov-fail-under=100

Continuous Integration (GitHub Actions):
Every push to main automatically:
Installs dependencies
Runs all tests
Measures coverage
Fails if coverage < 100%

Setup Instructions
- Clone the repository
git clone <repo-url>
cd History_Calculator/calculator-app
- Create virtual environment
Mac/Linux:
python -m venv .venv
source .venv/bin/activate
Windows:
python -m venv .venv
.\.venv\Scripts\activate
- Install dependencies
pip install -r requirements.txt
- Running the Calculator
From inside calculator-app:
python -c "from app.calculator.cli import run_repl; run_repl()"