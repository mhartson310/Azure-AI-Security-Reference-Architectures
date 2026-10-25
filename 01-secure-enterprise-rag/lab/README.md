# Secure RAG V2 — Offline authorization harness

This zero-dependency Python reference demonstrates **server-built tenant/user/group Search filters** and an **independent authoritative ACL check** before Search candidate contents enter model prompts or citation lists.

## Run

From the `lab/` directory, execute:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

**Local validation state:** the reference-equivalent harness was executed with synthetic inputs on 2026-10-25; all test scenarios passed. Re-run the committed version after checkout. No live Azure resource, Entra token, Azure AI Search SDK or LLM is exercised in these tests.

## Security contract — read before reuse

- The caller **MUST** validate actual Entra tokens (signature, audience, issuer, lifetime, appropriate tenant and group membership), not parse identity details from client JSON.
- The `Principal` constructor only checks **GUID syntax**; it cannot authenticate a human or verify memberships.
- `allowed_users`, `allowed_groups`, and `tenant_id` are **example filterable index fields**, not built-in permissions or an Azure search index schema.
- A separately authoritative `trusted_acl_lookup` (source API/permissions store) **MUST** enforce current, trusted permissions, avoid ACL spoofing, and fail closed if permissions are stale or unavailable.
- The sample uses canonical GUIDs as one safe filter encoding. Any real-world non-GUID names/ids need independent validation and correct escaping and group claim overage handling.
- Sample `authorized_hits` is intentionally small: no network retries, concurrent changes, nested document/chunk metadata, per-user caching, permission revocation SLA, eventual-consistency guarantees, token validation or rate limiting.
- The delimiter around untrusted source data is **not** a defense against model prompt injection. Model red-teaming must assess behavior separately.
- Apply citation/history/export/cache authorization consistently. Do not trust response-generated document IDs.

## Execution claims

The code is a **reference implementation**, not a production-ready RAG service. The [full Azure negative-security test plan](../validation/README.md) lists the required integration evidence.
