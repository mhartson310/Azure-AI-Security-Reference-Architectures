# ADR-001 · Authorization before model context

**Status:** Proposed

**Context:** Documents in a RAG corpus have distinct user/group/tenant access controls.

**Decision:** authenticate the requesting principal; authorize the requested data scope; enforce trusted ACLs or application-managed filters at retrieval; verify permitted results before prompt construction. Apply revocation handling and fail-closed behavior.

**Rejected alternative:** instructing the LLM not to reveal unauthorized data; language prompts cannot enforce access boundaries.

**Tradeoffs:** shared indexes reduce operational overhead but require careful tenant filtering, reliable permission synchronization and cache isolation; per-tenant indexes increase isolation but cost more to operate.

**Evidence:** cross-user denial, tenant isolation, ACL revocation, malicious-document injection and redacted audit traces.
