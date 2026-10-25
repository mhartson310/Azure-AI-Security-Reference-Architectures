# ADR-001 · Authorize every tool request outside the agent

**Status:** Proposed · **Reviewed:** 2026-10-25

## Decision
Treat agent output as an **untrusted proposal**. Every tool request must be checked at a dedicated business API/policy gateway against a trusted authenticated actor, tenant, registered tool, exact operation, target resource, allowed parameter schema and current permission state. Use a minimum-privilege tool identity and log the decision.

## Rejected options

- **Rely on system prompt:** an injected document or tool output can override behavioral instructions.
- **Rely on model safety/content filter:** safety policy is not business authorization.
- **Rely on connector/workload identity alone:** a privileged connection can act for users without those privileges.
- **Rely solely on Power Platform DLP:** connector classification is not per-record business ACL.
- **Trust agent-supplied actor or tenant:** identity spoofing risk.

## Consequences
Custom authorization gateway ownership, per-tool policy catalog, careful identity propagation, latency, dependency reliability, approval integration, and tests on **all** execution routes (including retries/event triggers). Fail closed when context cannot be verified.

## Proof
[AG-01–AG-05](../validation/README.md), including synthetic unauthorized operation, cross-tenant, malicious tool parameters, and alternate-connector routes.
