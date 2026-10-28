"""Grader rules: never stamp OPEN, no verdict override (harness gap check side finding, 2026-10-28)."""
import inspect
import math

import pytest

from residue_lab.grader import certify, verdict_from_leftover
from residue_lab.protocols import run_v0
from residue_lab.types import Verdict


@pytest.mark.parametrize("leftover", [0.0, 1e-13, -1e-13, 1e-9, 1.0, -1.0, 1e6, math.inf, -math.inf, math.nan])
@pytest.mark.parametrize("l2_on", [(), ("li_torr_lab_bg",)])
@pytest.mark.parametrize("child_failed", [False, True])
def test_grader_never_returns_open(leftover, l2_on, child_failed):
    assert verdict_from_leftover(leftover, 1e-12, l2_on, child_failed=child_failed) is not Verdict.OPEN


def test_above_floor_without_l2_is_residue():
    assert verdict_from_leftover(1.0, 1e-12, ()) is Verdict.RESIDUE


def test_nan_leftover_is_residue():
    assert verdict_from_leftover(math.nan, 1e-12, ()) is Verdict.RESIDUE


def test_certify_has_no_forced_verdict():
    assert "forced_verdict" not in inspect.signature(certify).parameters
    with pytest.raises(TypeError):
        certify("x", 0.0, 1e-9, forced_verdict=Verdict.OPEN)


def test_run_v0_contains_no_open():
    assert all(c.verdict is not Verdict.OPEN for c in run_v0())
