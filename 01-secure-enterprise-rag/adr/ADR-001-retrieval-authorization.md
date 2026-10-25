# ADR-001 · Enforce data authorization before model context

**Status:** Proposed · **Date:** 2026-10-25 · **Security objective:** confidentiality and cross-tenant isolation.

## Context

Users can ask an enterprise assistant questions that cause the vector/hybrid search index to return content with different source permissions. An application identity allowed to query an index is not the authorization identity of the human request originator.

## Decision

1. Validate the human user through Microsoft Entra ID and determine tenant/user/group entitlements in **trusted server-side code**, never from client-supplied identity strings.
2. Apply a **tenant AND permitted principal** filter at query time using app-managed Search security trimming.
3. Independently check retrieved documents against a trusted, suitably fresh permission store before snippets enter prompts, responses, citations or caches.
4. Fail closed on missing/expired permission state and revalidate revocation according to a documented SLA.
5. Treat model-generated citations as untrusted: only emit permitted source IDs.

## Alternatives

| Option | Decision / tradeoff |
|---|---|
| Prompt instructs LLM not to disclose unauthorized sources | **Rejected:** prompt instruction cannot enforce access |
| Client-supplied Search filter | **Rejected:** attacker can omit or widen it |
| Dedicated indexes by tenant | **Consider** for stronger isolation; operational cost higher and document/user ACLs still needed |
| Server-built app-managed filters + independent ACL check | **Selected** for reference: available across API versions but adds implementation burden |
| Native Search ACL/RBAC/Purview query permissions | **Evaluate** where supported; several documented integrations remain preview as of this review |

## Consequences / residual risk

- Permissions must be synchronized or queried directly; stale Search metadata cannot be accepted blindly.
- Cache, semantic answers, conversation histories, document exports, citation links and follow-up tools need the **same authorization rules**.
- A search filter that's correct today may miss new group memberships or source revocations tomorrow.
- Runtime MI with Search Index Data Reader is not per-human ACL enforcement.
- RBAC, private networking, classification and logging all matter but don't replace authorization.

## Proof required

[RAG-01 through RAG-05](../validation/README.md), verified principal binding, source-ACL provenance, and privacy-preserving audit traces. No production proof is present yet.

Microsoft docs: [security filters](https://learn.microsoft.com/azure/search/search-security-trimming-for-azure-search), [Search document access control](https://learn.microsoft.com/azure/search/search-document-level-access-overview).
