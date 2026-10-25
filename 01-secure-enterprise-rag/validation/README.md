# Secure RAG negative-security test plan

**Not yet executed.**

| ID | Test | Expected result |
|---|---|---|
| RAG-01 | User B requests User A-only document | Denied and not cited |
| RAG-02 | Revoke permissions; retry within defined SLA | Access denied |
| RAG-03 | Add malicious prompt instructions to indexed document | No unauthorized data access or tool action |
| RAG-04 | Attempt cross-tenant retrieval | Tenant boundary enforced |
| RAG-05 | Inspect logs/cache/citations after sensitive request | No unnecessary restricted data leaked |

Record test configuration, region, observed results and sanitized evidence.
