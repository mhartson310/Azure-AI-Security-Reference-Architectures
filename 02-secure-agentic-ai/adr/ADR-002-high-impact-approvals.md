# ADR-002 · Independent approval for high-impact agent actions

**Status:** Proposed · **Reviewed:** 2026-10-25

High-impact actions (data export, privileged write, credential changes, financial/HR/production changes) require independently verified human approval, not free-form text from an agent stating "approved."

## Decision
Use a business-owned approval service and a server-side approval artifact bound to the **actor, tenant, action, resource, normalized parameters, expiry and unique request ID**. Validate the approver's role and that the approver is independent where segregation-of-duties requires it. Consume approvals once; audit both approval and execution.

## Important details
- Replacing a destination, record ID, amount or action invalidates approval.
- Expired, reused, revoked or wrong-approver approvals are rejected.
- Agent cannot grant its own approval; don't let it choose the approval authority.
- Tool owner rechecks authorization **after** approval and at execution time.
- Asynchronous automation/event triggers require the **same controls** and a sensible actor/delegation model.
- Idempotency, rate limits and rollback plans are needed for repeated tool calls.

## Tradeoff
Approval slows completion and requires business ownership. Use risk tiers: read-only low-impact actions may execute without human review, but still require authorization and audit.

## Proof
[AG-04, AG-06, AG-07](../validation/README.md) and post-execution audit linkage.
