"""Deterministic reference for server-side RAG filtering and independent ACL checks.

Not a production API or Search SDK client. The caller MUST construct Principal
from server-validated identity and directory permissions, not client JSON.
"""
from dataclasses import dataclass
from typing import Callable, Iterable, Mapping, Sequence
from uuid import UUID
import re


class AuthorizationError(ValueError):
    """Invalid or missing trusted identity information."""


def guid(value: str) -> str:
    if not isinstance(value, str):
        raise AuthorizationError("Entra object/tenant ID must be a string")
    try:
        return str(UUID(value))
    except (ValueError, AttributeError) as exc:
        raise AuthorizationError("Invalid Entra GUID") from exc


def guid_collection(values: Sequence[str]) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not hasattr(values, "__len__") or len(values) > 128:
        raise AuthorizationError("Group list invalid or over limit")
    return tuple(sorted({guid(value) for value in values}))


@dataclass(frozen=True)
class Principal:
    tenant_id: str
    user_id: str
    group_ids: tuple[str, ...] = ()

    def __post_init__(self):
        object.__setattr__(self, "tenant_id", guid(self.tenant_id))
        object.__setattr__(self, "user_id", guid(self.user_id))
        object.__setattr__(self, "group_ids", guid_collection(self.group_ids))


@dataclass(frozen=True)
class ACL:
    """Permissions obtained from an INDEPENDENT authoritative source."""
    tenant_id: str
    users: tuple[str, ...] = ()
    groups: tuple[str, ...] = ()
    active: bool = True

    def __post_init__(self):
        object.__setattr__(self, "tenant_id", guid(self.tenant_id))
        object.__setattr__(self, "users", guid_collection(self.users))
        object.__setattr__(self, "groups", guid_collection(self.groups))


def build_search_filter(principal: Principal) -> str:
    """Azure AI Search OData for illustrative filterable index fields.

    tenant_id is Edm.String; allowed_users and allowed_groups are
    Collection(Edm.String). Canonical GUIDs prevent filter injection.
    Only an app with independently validated identity may call this.
    """
    user = f"allowed_users/any(u:search.in(u, '{principal.user_id}', '|'))"
    groups = ""
    if principal.group_ids:
        joined = "|".join(principal.group_ids)
        groups = f" or allowed_groups/any(g:search.in(g, '{joined}', '|'))"
    return f"tenant_id eq '{principal.tenant_id}' and ({user}{groups})"


_DOC_ID = re.compile(r"^[a-zA-Z0-9._:-]{1,128}$")


def authorized_hits(
    principal: Principal,
    search_hits: Iterable[Mapping[str, str]],
    trusted_acl_lookup: Callable[[str], ACL | None],
) -> list[dict[str, str]]:
    """Reject Search candidates unless authoritative ACL independently permits.

    A production lookup must fail closed for stale/unknown permissions
    and enforce a documented revocation freshness requirement.
    """
    allowed = []
    for hit in search_hits:
        doc_id = hit.get("doc_id")
        if not isinstance(doc_id, str) or not _DOC_ID.fullmatch(doc_id):
            continue
        acl = trusted_acl_lookup(doc_id)
        if acl is None or not acl.active or acl.tenant_id != principal.tenant_id:
            continue
        if principal.user_id not in acl.users and not set(principal.group_ids).intersection(acl.groups):
            continue
        if not isinstance(hit.get("content"), str):
            continue
        allowed.append({"doc_id": doc_id, "content": hit["content"]})
    return allowed


def context_from_authorized_hits(hits: Iterable[Mapping[str, str]]) -> str:
    """Delimit authorized source TEXT as untrusted; this is NOT an injection defense."""
    return "\n\n".join(
        f"[BEGIN UNTRUSTED SOURCE {hit['doc_id']}]\n{hit['content']}\n[END UNTRUSTED SOURCE]"
        for hit in hits
    )
