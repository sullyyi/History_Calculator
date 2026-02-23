# Calculator CLI

A modular command-line calculator with a testable REPL, calculation history, and CI-enforced 100% coverage.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
# .\.venv\Scripts\activate  # windows

pip install -r requirements.txt

Run
From the project root:
python -c "from app.calculator.cli import run_repl; run_repl()"

Commands
add <a> <b>
sub <a> <b>
mul <a> <b>
div <a> <b>
history
help
exit

Test + Coverage
pytest --cov=app --cov-report=term-missing --cov-fail-under=100