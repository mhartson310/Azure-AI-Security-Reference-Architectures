# 03 · Governed Azure AI & MLOps

**Status: Conceptual reference design.**

```mermaid
flowchart LR
D[Approved data] --> P[Prepare & classify]
P --> T[Azure Machine Learning training]
T --> E[Evaluate quality, safety and security]
E --> R[Governed model registry]
R --> G[Deployment approval gate]
G --> S[Protected inference endpoint]
S --> M[Monitor drift, access and spend]
```

Treat datasets, training pipelines, model weights, registries, build dependencies, evaluation artifacts, and inference endpoints as **separately protected resources**. Apply scoped identity, data governance, provenance checks, approved deployment paths, network boundaries and telemetry.

[Threat model](threat-model/README.md) · [Validation](validation/README.md)
