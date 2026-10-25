# MLOps threat model · Draft

| Risk | Control |
|---|---|
| Unauthorized training data access | Scoped identities and data roles |
| Data poisoning | Provenance, ingestion checks and quality reviews |
| Malicious or substituted model artifacts | Integrity checks and protected model registry |
| Pipeline supply-chain compromise | Trusted dependencies, protected branch and release gates |
| Inference endpoint exposure | Authentication, network isolation where supported, rate control |
| Sensitive telemetry | Minimized logs, access and retention policies |
