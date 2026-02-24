# History Calculator

A modular, production-style command-line calculator application built in Python using advanced object-oriented design patterns, persistent history storage with pandas, environment-based configuration, and 100% unit test coverage enforced through continuous integration.

---

## Overview

This project implements a modular command-line calculator using clean architecture principles and multiple design patterns.

It supports:

- A fully interactive REPL (Read–Eval–Print Loop)  
- Arithmetic operations (add, subtract, multiply, divide, power, root)  
- Persistent calculation history stored as CSV using pandas  
- Undo and redo functionality via state snapshots  
- Environment-based configuration using dotenv  
- Observer-driven optional auto-save behavior  
- Strategy-based execution abstraction  
- Factory pattern for calculation creation  
- 100% unit test coverage enforced in continuous integration  

The project emphasizes separation of concerns, maintainability, extensibility, and professional development practices.

---

## REPL Interface

The application runs as a continuous command-line session allowing users to:

- Perform calculations  
- View calculation history  
- Clear history  
- Undo and redo actions  
- Save and load history from CSV  
- Request help  
- Exit cleanly  

---

## Supported Commands

### Arithmetic

- `add a b` — Adds two numbers  
- `sub a b` — Subtracts two numbers  
- `mul a b` — Multiplies two numbers  
- `div a b` — Divides two numbers  
- `pow a b` — Raises a to the power of b  
- `root a b` — Computes the b-th root of a  

### History and State Management

- `history` — Displays calculation history  
- `clear` — Clears history  
- `undo` — Reverts the last change  
- `redo` — Reapplies the last undone change  
- `save` — Saves history to CSV  
- `load` — Loads history from CSV  
- `help` — Displays instructions  
- `exit` — Exits the program  

---

## Architecture and Design Patterns

This project implements several advanced object-oriented design patterns.

### Facade Pattern

The `Calculator` class acts as the central interface for executing operations, managing history, and coordinating internal components.

### Factory Pattern

`CalculationFactory` dynamically instantiates operation objects based on user input, eliminating conditional logic inside the REPL.

### Strategy Pattern

Execution behavior is abstracted through interchangeable strategies. The default strategy executes calculations directly, but custom strategies can alter execution behavior without modifying the core system.

### Observer Pattern

Observers subscribe to calculator state changes. An `AutoSaveObserver` can automatically persist history when calculations are added, undone, redone, cleared, or loaded.

### Memento Pattern

Undo and redo functionality is implemented using history snapshots stored in caretaker stacks.

---

## Configuration

The application uses environment variables via `python-dotenv`.

Create a `.env` file using the provided `.env.example` template.

### Environment Variables

- `CALC_HISTORY_PATH` — Path to CSV file for history persistence  
- `CALC_AUTO_LOAD` — Automatically load history on startup  
- `CALC_AUTO_SAVE` — Automatically save history after state changes  

Example:
CALC_HISTORY_PATH = history.csv
CALC_AUTO_LOAD = true
CALC_AUTO_SAVE = false

Configuration errors are handled gracefully at application startup.

---

## Persistent History

The `CalculationHistory` class:

- Stores history using a pandas DataFrame  
- Supports CSV save and load operations  
- Validates required columns  
- Enforces numeric type conversion  
- Supports snapshot and restore operations  

History persistence is file-based and configurable via environment variables.

---

## Error Handling Strategy

This application demonstrates multiple error handling paradigms.

### LBYL (Look Before You Leap)

Used for checking file existence before loading history.

### EAFP (Easier to Ask Forgiveness than Permission)

Used for user input parsing and numeric conversion.

Custom exception classes ensure consistent validation and configuration error reporting.

All invalid input cases are handled gracefully with clear, user-friendly error messages.

---

## Testing

This project uses pytest with:

- Unit tests for all modules  
- Parameterized tests  
- Positive and negative case testing  
- Strategy and observer behavior verification  
- Persistence and file-handling tests  
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
pow 2 3
Result: 8.0
undo
Undo successful.
history
add 2 3 = 5.0