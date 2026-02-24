import pytest

from app.exceptions import ValidationError
from app.input_validators import parse_two_numbers, split_command


def test_split_command_strips_and_splits():
    assert split_command("  add  1   2  ") == ["add", "1", "2"]


def test_parse_two_numbers_success():
    a, b = parse_two_numbers("1.5", "2")
    assert a == 1.5
    assert b == 2.0


@pytest.mark.parametrize("a_str,b_str", [("a", "2"), ("1", "b"), ("x", "y")])
def test_parse_two_numbers_invalid_raises(a_str, b_str):
    with pytest.raises(ValidationError):
        parse_two_numbers(a_str, b_str)