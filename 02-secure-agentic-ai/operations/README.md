# Agentic AI V2 — Operations and SOC evidence

**Application gateway event:** timestamp, trace ID, platform, agent ID alias, principal/tenant alias, tool ID, tool version/hash, normalized operation, target alias, authorization decision and rule ID, approval fingerprint ID, connector identity alias, destination classification, safe outcome and duration.

**Monitor:** repeated unauthorized tools, high-impact action without matching approval, tool inventory/config change, new MCP destinations, connector privilege grants, unusually high tool volume, out-of-policy destination, policy change, missing correlation between tool action and gateway decision.

**Do not assume** Foundry traces or Copilot Studio platform logs contain granular business authorization evidence. Emit gateway/API logs and correlate through Application Insights/Azure Monitor and optionally Sentinel, with redacted arguments.

**Runbook:** stop affected connector or agent, block destination or role, preserve sanitized traces, revoke leaked credentials, inspect decisions and affected records, invalidate approvals, correct policy, re-run negative tests.

Evidence samples contain synthetic data only. Define local retention, investigation owner, severity, runbooks, business approval escalation and residual risk.
