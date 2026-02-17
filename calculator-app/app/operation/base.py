from __future__ import annotations

from abc import ABC, abstractmethod


class Operation(ABC):
    """Abstract base for a binary arithmetic operation."""

    name: str

    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        """Compute the result of applying the operation to a and b."""
        raise NotImplementedError
