"""Illustrative Azure ML release gate logic; independent of Azure SDK.

Trust in any manifest/attestation MUST be established by an actual protected
CI/CD and provenance system. This helper only models policy decisions.
"""
from dataclasses import dataclass
import re

SHA256 = re.compile(r"^[a-f0-9]{64}$")
APPROVED_ENVIRONMENTS = frozenset({"stage", "prod"})
APPROVED_SOURCES = frozenset({"trusted-repo"})

@dataclass(frozen=True)
class Manifest:
    model_digest: str
    image_digest: str
    source: str
    dataset_version: str
    evaluation_passed: bool
    author: str
    reviewer: str
    target: str
    approved_model_digest: str
    approval_active: bool

def can_promote(m: Manifest) -> bool:
    """Reject unapproved model release. DOES NOT validate provenance signatures."""
    if not SHA256.fullmatch(m.model_digest) or not SHA256.fullmatch(m.image_digest):
        return False
    if m.model_digest != m.approved_model_digest:
        return False
    if m.source not in APPROVED_SOURCES or not m.dataset_version:
        return False
    if m.target not in APPROVED_ENVIRONMENTS or not m.evaluation_passed:
        return False
    if not m.author or not m.reviewer or m.author == m.reviewer:
        return False
    if not m.approval_active:
        return False
    return True
