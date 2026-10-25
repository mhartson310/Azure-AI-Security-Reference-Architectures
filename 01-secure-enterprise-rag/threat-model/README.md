# Secure RAG threat model · Draft

| Threat | Failure mode | Mitigation |
|---|---|---|
| Cross-user data exposure | Search results exceed requester ACL | Filter and independently verify permissions |
| Indirect prompt injection | Retrieved content supplies malicious instructions | Treat retrieved content as untrusted data; restrict tools |
| RAG poisoning | Attacker modifies source or metadata | Ingestion ownership, integrity and provenance |
| Sensitive output leakage | Prompts, logs or output expose restricted text | Data minimization and applicable output controls |
| Stale ACLs | Revoked content remains accessible | Refresh rules and permission revocation tests |

MITRE ATLAS IDs will be added only after verifying exact mappings.
