# Secure RAG V2 — Observability, detections, and response

**Design guidance:** not an enabled Sentinel analytics rule or proven detection. Azure service diagnostics are useful but **Azure AI Search does not inherently log the original end-user identity for each document query**. The application must emit authorization decisions and correlation IDs itself.

## Recommended security events (app-owned)

| Field | Meaning | Privacy guidance |
|---|---|---|
| `timestamp_utc`, `request_id` | Cross-service transaction and time | Random UUID correlation ID |
| `principal_alias`, `tenant_alias` | Pseudonymous end-user and tenant | Avoid actual UPN, emails and raw object ID if unnecessary |
| `search_operation_id` | Correlation with Search activity | No search key or bearer token |
| `auth_mode` | App-managed filter or verified native ACL mode | Explicit mode in every request |
| `authorized_document_count` | Number of results permitted after ACL check | Log count instead of sensitive titles/content |
| `denied_document_count`, `decision_reason` | Enforcement outcome | Standardized enums; no raw prompt |
| `acl_revision`, `acl_age_seconds` | Revocation freshness | Verify authority and acceptable TTL |
| `model_request_id`, `citation_ids_hash` | Correlate inference and safe citation allowlist | Prefer hashed IDs |
| `policy_version` | Reproducible controls | Commit/policy tag |

**Example detections:**

1. 10+ access-denied RAG queries from one pseudonymous principal in 10 minutes (threshold is illustrative; tune locally).
2. A denied tenant-scoped query followed by a high-volume document retrieval event.
3. Unexpected Search Index Data Contributor grants to the app runtime identity.
4. Surge in ingestion ACL updates or new source owners preceding a retrieval anomaly.
5. Citation ID not among approved document IDs (must be blocked, not only alerted).

## KQL — Search operation diagnostics (service-side)

Enable [Azure AI Search diagnostic logging](https://learn.microsoft.com/azure/search/search-monitor-enable-logging) and confirm the selected resource log table before use. This query uses the documented **AzureDiagnostics** table; some environments may use resource-specific tables instead.

```kusto
AzureDiagnostics
| where TimeGenerated > ago(24h)
| where ResourceProvider == "MICROSOFT.SEARCH"
| summarize Operations=count() by bin(TimeGenerated, 1h), OperationName
| order by TimeGenerated desc
```

**Limitation:** The above summarizes service operations, **not human-user authorization**. To detect actual per-user RAG failures, ingest the custom app events above into a **dedicated, verified schema** (for example via Application Insights/OpenTelemetry) and build separate queries against actual field names. Do not invent a turnkey production Sentinel rule from an unprovisioned custom table.

## Evidence collection and response

- Trigger synthetic denial and correlate app event ↔ Search diagnostic ↔ model request via `request_id`.
- Restrict and review diagnostics retention; sensitive prompt/response logging should be opt-in and protected, if ever used.
- On confirmed unauthorized retrieval: block the affected path, repair ACL and index permissions, invalidate answer caches, rotate credentials if exposed, audit document access, notify incident owner.
- Document alert tuning, data owner, escalation, evidence location, residual risk, and false positives.

**Status:** monitoring policy proposal; no pipeline deployment or Sentinel alert execution evidence included.
