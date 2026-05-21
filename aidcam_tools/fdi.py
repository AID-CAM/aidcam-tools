"""FDI tooth-numbering helpers.

FDI numbers are two digits: the first is the quadrant (1=UR, 2=UL, 3=LL, 4=LR),
the second is the tooth position within the quadrant (1=central incisor through
8=third molar). So 16 = upper right first molar, 31 = lower left central incisor,
etc.
"""

from __future__ import annotations

_VALID_QUADRANTS = {1, 2, 3, 4}
_VALID_POSITIONS = {1, 2, 3, 4, 5, 6, 7, 8}


def _split(fdi: int) -> tuple[int, int]:
    """Return (quadrant, position) for a valid FDI number, else raise ValueError."""
    if not isinstance(fdi, int):
        raise TypeError(f"FDI number must be int, got {type(fdi).__name__}")
    q, p = divmod(fdi, 10)
    if q not in _VALID_QUADRANTS or p not in _VALID_POSITIONS:
        raise ValueError(f"{fdi} is not a valid permanent-dentition FDI number")
    return q, p


def quadrant(fdi: int) -> int:
    """Return the FDI quadrant (1=UR, 2=UL, 3=LL, 4=LR)."""
    return _split(fdi)[0]


def position(fdi: int) -> int:
    """Return the position within the quadrant (1=central incisor … 8=third molar)."""
    return _split(fdi)[1]


def is_anterior(fdi: int) -> bool:
    """Anterior teeth are central + lateral incisors + canines (positions 1–3)."""
    return position(fdi) in {1, 2, 3}


def is_premolar(fdi: int) -> bool:
    """Premolars sit in positions 4 and 5."""
    return position(fdi) in {4, 5}


def is_molar(fdi: int) -> bool:
    """Molars sit in positions 6, 7, 8."""
    return position(fdi) in {6, 7, 8}


def is_upper(fdi: int) -> bool:
    """Upper arch contains quadrants 1 and 2."""
    return quadrant(fdi) in {1, 2}


def is_lower(fdi: int) -> bool:
    """Lower arch contains quadrants 3 and 4."""
    return quadrant(fdi) in {3, 4}


def opposite(fdi: int) -> int:
    """Vertical opposite (same position, opposite arch).

    Examples:
        opposite(11) == 41   # upper right central → lower right central
        opposite(26) == 36   # upper left first molar → lower left first molar
    """
    q, p = _split(fdi)
    return ((q + 2 - 1) % 4 + 1) * 10 + p if False else (5 - q) * 10 + p if q in {1, 4} else (q == 2 and 30 or 20) + p


def _vertical_opposite(q: int, p: int) -> int:
    """Helper. Quadrant 1 ↔ 4, quadrant 2 ↔ 3."""
    opposites = {1: 4, 2: 3, 3: 2, 4: 1}
    return opposites[q] * 10 + p


def contralateral(fdi: int) -> int:
    """Horizontal mirror (same arch, opposite side).

    Examples:
        contralateral(11) == 21   # upper right central → upper left central
        contralateral(36) == 46   # lower left first molar → lower right first molar
    """
    q, p = _split(fdi)
    pairs = {1: 2, 2: 1, 3: 4, 4: 3}
    return pairs[q] * 10 + p


# Replace the messy opposite() implementation above with the helper.
def opposite(fdi: int) -> int:  # noqa: F811
    """Vertical opposite (same position, opposite arch).

    Examples:
        opposite(11) == 41   # upper right central → lower right central
        opposite(26) == 36   # upper left first molar → lower left first molar
    """
    q, p = _split(fdi)
    return _vertical_opposite(q, p)
