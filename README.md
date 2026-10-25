# Azure AI Security Reference Architectures

**The Cloud Security Architect** — Secure Azure AI architecture, Zero Trust, governance, validation, and FinOps.

> **Maturity: Reference designs (not yet lab validated).** Confirm product features, licensing, network support, preview status and regional availability before deployment.

Four complementary enterprise AI solution patterns:

| Architecture | Design objective | Technical materials |
|---|---|---|
| [01 · Secure Enterprise RAG](01-secure-enterprise-rag/README.md) | Enforce document authorization **before** retrieved context enters the model | [ADR](01-secure-enterprise-rag/adr/ADR-001-retrieval-authorization.md) · [Threats](01-secure-enterprise-rag/threat-model/README.md) · [Validation](01-secure-enterprise-rag/validation/README.md) |
| [02 · Secure Agentic AI](02-secure-agentic-ai/README.md) | Independently authorize agent tool actions, approvals and connector access | [Threats](02-secure-agentic-ai/threat-model/README.md) · [Validation](02-secure-agentic-ai/validation/README.md) |
| [03 · Governed AI/MLOps](03-governed-ai-mlops/README.md) | Protect training data, model artifacts, pipelines and inference endpoints | [Threats](03-governed-ai-mlops/threat-model/README.md) · [Validation](03-governed-ai-mlops/validation/README.md) |
| [04 · Azure AI FinOps](04-ai-finops-cost-optimization/README.md) | Attribute AI spending, control resource usage and prove savings against baselines | [Budget controls](04-ai-finops-cost-optimization/budgets-and-policy/README.md) · [Cost models](04-ai-finops-cost-optimization/cost-models/README.md) |

## Architecture gallery

[![Secure RAG](assets/01-rag.svg)](01-secure-enterprise-rag/README.md)

[![Agentic AI](assets/02-agent.svg)](02-secure-agentic-ai/README.md)

[![Governed MLOps](assets/03-mlops.svg)](03-governed-ai-mlops/README.md)

[![AI FinOps](assets/04-finops.svg)](04-ai-finops-cost-optimization/README.md)

## Architecture quality bar

Every architecture should expose **the actors, data flows, trust boundaries, enforcement points, threat scenarios, negative-security tests, and expected evidence**. Diagrams are conceptual until linked lab evidence establishes behavior.

- [Security control matrix](docs/security-control-matrix.md)
- [Publishing and validation checklist](docs/publishing-checklist.md)
- [Visual style guide](docs/visual-style-guide.md)

### Important design distinctions

**Microsoft Purview classification and governance do not automatically enforce document-level retrieval authorization in arbitrary RAG apps.** Entra ID authentication, application authorization, service-level permissions and network controls each perform different jobs. **Azure Cost Management budgets provide alerting; they do not universally stop spending at a hard cap.**

**Publisher:** The Cloud Security Architect · [GitHub](https://github.com/mhartson310)

Independent reference designs, not official Microsoft documentation. Microsoft and other product marks belong to their respective owners. MIT license applies per repository license.
