# 01 · Secure Enterprise RAG on Azure

**Status: Conceptual reference design — not yet lab validated.**

```mermaid
flowchart LR
U[User] --> ID[Microsoft Entra ID]
ID --> APP[Application / API]
APP --> AUTH[Enforce user and document scope]
DATA[Enterprise documents + permissions] --> ING[Ingest with ACL metadata]
ING --> SEARCH[Azure AI Search]
AUTH --> SEARCH
SEARCH --> VERIFY[Check authorized retrieval]
VERIFY --> PROMPT[Build grounded prompt]
PROMPT --> MODEL[Azure AI Foundry model endpoint]
MODEL --> APP
```

**Design decision:** do not let the model decide whether documents are authorized. Validate user context and apply query-time permission trimming, followed by appropriate result verification, **before** inserting retrieved data into a model prompt.

**Controls:** Entra ID, app authorization, scoped workload identities, supported private networking, Key Vault, Purview data classification where integrated, injection-resistant content boundaries, Azure Monitor and audit evidence.

**Caution:** Purview does not automatically enforce arbitrary RAG access control; verify native Azure AI Search ACL capabilities and preview status for your exact design.

[ADR](adr/ADR-001-retrieval-authorization.md) · [Threat model](threat-model/README.md) · [Validation](validation/README.md)
