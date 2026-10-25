# Security control matrix

| Control | Where enforced | Proof needed |
|---|---|---|
| User authentication | Entra ID, app session validation | Invalid tokens denied |
| Document authorization | Application and retrieval service | Cross-user and revocation tests |
| Agent tool authorization | Connector/API tool gateway | Unauthorized action denied |
| Least privilege | Managed identity / RBAC | Negative permissions tests |
| Network isolation | Supported service firewall/private endpoint design | Public path blocked where required |
| Sensitive data governance | Applicable Purview sources, labels, policies | Observed policy behavior in supported integration |
| Prompt/tool injection defenses | Retrieval and agent execution boundaries | Malicious source cannot cause forbidden action |
| Model integrity | Provenance, registry and deployment approvals | Unapproved artifacts cannot deploy |
| Threat detection | Azure Monitor, audit logs, Sentinel integrations | Sanitized end-to-end trace |
| Cost allocation and limits | Cost Management, policy, quotas, automation | Usage attribution and alert test |

Controls above are **design objectives**, not claims of default capability. Verify product-specific scope.
