import importlib.util
from pathlib import Path


def test_flat_calculation_module_is_executed():
    # Load app/calculation.py explicitly (avoid package name collision with app/calculation/)
    root = Path(__file__).resolve().parents[1]
    mod_path = root / "app" / "calculation.py"

    spec = importlib.util.spec_from_file_location("app_flat_calculation", mod_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "Calculation")