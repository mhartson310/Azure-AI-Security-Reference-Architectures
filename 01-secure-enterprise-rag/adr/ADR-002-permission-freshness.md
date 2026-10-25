# ADR-002 · Permission revocation and stale-index handling

**Status:** Proposed · **Date:** 2026-10-25.

## Problem

Retrieval indexes, search caches, conversation history and ACL metadata can outlive source permission changes. SharePoint/Search-native permission ingestion and other provider sync methods may have different update semantics or preview limitations.

## Decision

- Define a **revocation SLO/SLA** (to be selected by data owners; no universal number is assumed).
- At request time consult an **authoritative, independently maintained** ACL/read-permission source (or validated native permission mechanism satisfying the SLO). Reject missing, inactive, wrong-tenant, or indeterminate records.
- Bind cache keys and conversation state to tenant, user, authorization state/version, and document permission freshness where needed.
- Trigger index updates on ACL change/deletion and verify that revoked content is no longer eligible for retrieval/citation.
- **Fail closed** if the permission authority is unavailable, behind the defined freshness limit, or lacks document provenance.
- Do not treat re-reading ACL metadata from the same index as an independent check.

## Options rejected

- **Keep stale content until next indexing job:** unacceptable for sensitive permission revocations.
- **Trust Search filtering alone:** not enough for an app-managed ACL mirror without lifecycle controls.
- **Ignore cache revocation:** a stale answer can leak without another Search call.

## Proof

Disable an existing user permission, invalidate/recheck dependent caches, query immediately and through the target SLA, and record permissions refresh times, returned citation IDs, app decision and observed result. Results pending deployed-lab validation.
