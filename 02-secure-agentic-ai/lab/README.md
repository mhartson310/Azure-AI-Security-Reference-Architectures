# Agentic AI — Offline policy reference and tests

Run from this directory:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

All input identities and approvals are **synthetic**. This is a narrow standard-library reference to illustrate the authorization invariant: **even a successful agent tool selection cannot bypass independent policy and exact-action approval**.

**Not production-ready:** `Principal` must be built from cryptographically validated caller identity; agent-provided actor claims cannot be trusted. Approval proof must be issued, stored, integrity-protected and consumed **atomically** by a separate service; the sample accepts a dictionary to model checks only. This sample does not execute tools, validate OAuth tokens, call MCP servers, implement throttling, connect to Copilot Studio/Foundry or test prompt-injection effectiveness. Refer to the [full integration validation plan](../validation/README.md).
