"""Tests for the FDI tooth-numbering helpers."""

import pytest

from aidcam_tools.fdi import (
    is_anterior,
    is_premolar,
    is_molar,
    is_upper,
    is_lower,
    quadrant,
    position,
    opposite,
    contralateral,
)


@pytest.mark.parametrize("fdi,expected", [(11, True), (12, True), (13, True), (14, False), (16, False)])
def test_is_anterior(fdi, expected):
    assert is_anterior(fdi) is expected


@pytest.mark.parametrize("fdi,expected", [(14, True), (15, True), (13, False), (16, False)])
def test_is_premolar(fdi, expected):
    assert is_premolar(fdi) is expected


@pytest.mark.parametrize("fdi,expected", [(16, True), (17, True), (18, True), (15, False), (11, False)])
def test_is_molar(fdi, expected):
    assert is_molar(fdi) is expected


@pytest.mark.parametrize("fdi,expected", [(11, True), (28, True), (35, False), (47, False)])
def test_is_upper(fdi, expected):
    assert is_upper(fdi) is expected


@pytest.mark.parametrize("fdi,expected", [(35, True), (47, True), (11, False), (28, False)])
def test_is_lower(fdi, expected):
    assert is_lower(fdi) is expected


def test_quadrant_and_position():
    assert quadrant(16) == 1
    assert position(16) == 6
    assert quadrant(47) == 4
    assert position(47) == 7


@pytest.mark.parametrize("fdi,expected", [(11, 41), (16, 46), (26, 36), (35, 25)])
def test_opposite(fdi, expected):
    assert opposite(fdi) == expected


@pytest.mark.parametrize("fdi,expected", [(11, 21), (16, 26), (36, 46), (47, 37)])
def test_contralateral(fdi, expected):
    assert contralateral(fdi) == expected


@pytest.mark.parametrize("fdi", [0, 10, 19, 50, 99])
def test_invalid_fdi_raises(fdi):
    with pytest.raises(ValueError):
        quadrant(fdi)
