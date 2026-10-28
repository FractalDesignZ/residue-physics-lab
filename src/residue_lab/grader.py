from __future__ import annotations
from residue_lab.types import Certificate, TermTag, Verdict

def leftover_weight_frac(sim, l1):
    return sim.weight_drop_frac - l1.weight_drop_frac

def verdict_from_leftover(leftover, floor, l2_on, child_failed=False):
    """Computed verdict. Never returns Verdict.OPEN: the grader does not stamp OPEN (MaxOp rule).
    A leftover above the floor is RESIDUE whether or not an L2 term is on; a non-finite leftover is RESIDUE."""
    if child_failed:
        return Verdict.RESIDUE
    if not (abs(leftover) <= floor):  # also catches NaN
        return Verdict.RESIDUE
    return Verdict.OPEN_NULL

def certify(protocol, leftover, floor, l2_on=(), unpaid=(), child_failed=False, notes=None):
    """Certificate with the computed verdict only; there is no caller override (forced_verdict was removed)."""
    v = verdict_from_leftover(leftover, floor, l2_on, child_failed=child_failed)
    if v is Verdict.OPEN:  # defensive: unreachable by construction
        raise ValueError("grader must never emit Verdict.OPEN")
    tag = TermTag.SPECULATIVE if l2_on else TermTag.KNOWN
    return Certificate(protocol, v, leftover, floor, l2_on, unpaid, tag, notes or {})
