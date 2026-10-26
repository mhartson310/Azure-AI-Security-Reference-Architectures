# Secure Agentic AI V2 — Architecture and trust boundaries

## Threat-driven objective

An agent receives a trusted user's request alongside lower-trust data (emails, documents, web pages, other tools, MCP server responses), then selects powerful tools. **The enforcement decision happens outside the LLM/agent prompt**, on every operation and target.

## Boundaries

| Boundary | Crossing | Owner | Required test |
|---|---|---|---|
| **AG-TB1** | Browser/channel → authenticated agent | Entra/agent publisher | Reject unauthenticated and invalid session paths |
| **AG-TB2** | User authorization → agent identity/delegation | App/identity | Acting on behalf of Alice cannot become workload owner's unrestricted rights |
| **AG-TB3** | Untrusted messages/data/tool outputs → agent context | Agent/runtime | Injected instructions cannot authorize actions |
| **AG-TB4** | Agent-selected tool name/parameters → policy gateway | API owner | Allowlist tool, target, operation and parameter schema |
| **AG-TB5** | Policy decision → human approval | Workflow owner | Approval independent, scoped, fresh, one-time |
| **AG-TB6** | Approved call → downstream connector/API | Service owner | Least privilege and server-side API authorization |
| **AG-TB7** | Tool/MCP definition or endpoint → runtime | Platform/integration owner | Tool metadata/integrity and destination allowlists |
| **AG-TB8** | Conversation/action traces → retention/SOC | SecOps/privacy | Complete causal audit without excess sensitive details |

## Sequence with independent decision

```mermaid
sequenceDiagram
  autonumber
  actor U as Employee
  participant A as Copilot / Foundry agent
  participant G as Policy gateway (custom)
  participant P as Human approval (independent)
  participant API as Restricted business API
  participant S as Audit evidence
  U->>A: Ask to change a synthetic record
  Note over A: Email/tool text is untrusted; the model may propose only
  A->>G: Proposed tool, actor context, target and parameters
  G->>G: Validate user identity, allowed operation, resource and tenant
  alt Denied or unknown
    G-->>A: DENY
    G->>S: Audit denial / reason / trace
  else High-impact action
    G->>P: Request approval bound to exact action fingerprint
    P-->>G: Verified approval bound to fingerprint and expiry
    G->>G: Check fresh single-use approval
    G->>API: Execute with minimum required identity
    API-->>G: Outcome
    G->>S: Audit actor, approval, action, outcome
  else Low-impact allowed
    G->>API: Execute least-privilege read/action
    API-->>G: Outcome
    G->>S: Audit actor, action, outcome
  end
```

## Identity modes are design choices

- **Delegated / on-behalf-of user:** preferred where downstream user-level authorization and connector behavior support it; verify OAuth claims/scopes/audience.
- **Agent or app workload identity:** possible in Foundry and connectors, but can be broader than user permissions. A tool gateway must constrain *acting_user × tenant × target × operation* even when identity is otherwise authorized at the Azure API layer.
- **Shared maker/connection credentials:** high risk if the connection can act broadly; inventory effective permission and confirm invocation context; never infer end-user trimming.

## Platform flows must not be conflated

- **Copilot Studio:** Power Platform environment governance, data policies and connector/action settings; publish/channel and authentication restrictions apply according to configured rules. Test these in the correct environment.
- **Foundry Agent Service:** Agent identity and tools, network isolation, traces, model deployment scopes; tool and external knowledge traffic paths differ by agent type. Verify required egress and private endpoints **per tool**, not only per agent.
- **Human approval:** platform support varies by workflow. This reference designs an independent authorization gateway + approval store whose enforcement is *not* entrusted to model text.

## Sensitive data and tool outputs

Outputs from a tool can be both **sensitive** and **instructionally untrusted**. Apply data classification and relevant Purview integration where supported, minimize the returned fields, prevent tool responses from rewriting system instructions, redact secrets in audit, and limit outbound destinations. Content filtering is a secondary control rather than the authorization boundary.

## Residual risks

User consent phishing, stale group memberships, external MCP servers, secret-bearing tool results, indirect injection, replay, automation loops, connector overpermission, errors in API authorization, and privacy leakage in traces.

[Controls](../security-controls/README.md) · [ADRs](../adr/ADR-001-tool-authorization.md) · [Validation](../validation/README.md).
