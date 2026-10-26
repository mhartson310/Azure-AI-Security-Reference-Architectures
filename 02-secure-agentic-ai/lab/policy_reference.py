"""Illustrative server-side authorization policy for agent tool requests.

NOT an authentication system, Copilot Studio integration, or Foundry runtime.
The trusted user and approvals MUST originate from independently validated services.
"""
from dataclasses import dataclass
import hashlib
import json

ALLOWED = {
    "analyst": frozenset({"get_case"}),
    "editor": frozenset({"get_case", "update_case"}),
    "approver": frozenset({"get_case", "update_case", "export_case"}),
}
HIGH_IMPACT = frozenset({"update_case", "export_case"})
DESTINATIONS = frozenset({"internal://approved-archive"})

@dataclass(frozen=True)
class Principal:
    user_id: str
    tenant_id: str
    role: str

@dataclass(frozen=True)
class Action:
    name: str
    tenant_id: str
    target: str
    destination: str = ""

def fingerprint(user: Principal, action: Action) -> str:
    payload = [user.user_id, user.tenant_id, action.name,
               action.tenant_id, action.target, action.destination]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()

def authorize(user: Principal, action: Action, approval: dict | None = None,
              now: int = 1000) -> bool:
    """Fail closed: role/tenant/action/destination/approval must be valid.

    Approval is synthetic in this example. Production must verify authenticity,
    approver authority, expiry and atomic one-time consumption independently.
    """
    if not user.user_id or not user.tenant_id or not action.target:
        return False
    if action.tenant_id != user.tenant_id:
        return False
    if action.name not in ALLOWED.get(user.role, frozenset()):
        return False
    if action.destination and action.destination not in DESTINATIONS:
        return False
    if action.name in HIGH_IMPACT:
        return bool(approval and approval.get("fingerprint") == fingerprint(user, action)
                    and approval.get("expires_at", 0) > now
                    and approval.get("approved_by") != user.user_id
                    and approval.get("approved_by")
                    and not approval.get("used"))
    return True
