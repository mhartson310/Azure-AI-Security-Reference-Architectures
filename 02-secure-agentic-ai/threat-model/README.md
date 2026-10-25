# Agent threat model · Draft

| Risk | Control |
|---|---|
| Tool privilege escalation | Tool/API authorization independent of agent |
| Indirect prompt injection from email or documents | Untrusted-content boundary; parameter validation |
| Bypassing high-impact approval | Centralized action gateway; server-side approval state |
| Data exfiltration through connectors | Connector restrictions, scoped egress and applicable DLP |
| Session leakage | Session/user/tenant isolation and cache scoping |
| Runaway cost or repeated operations | Execution ceilings, quotas where supported, monitoring |
