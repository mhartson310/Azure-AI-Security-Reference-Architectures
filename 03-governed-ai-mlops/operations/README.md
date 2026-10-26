# Azure ML V2 — Operational evidence, alerts, and response

## Traceability requirements

For each deployment link **dataset version/hash → training job ID → source commit → dependency/container image digest → model digest → release policy version → independent approver → pipeline identity → endpoint served model version**.

Store this chain in protected CI/CD evidence, with the public repo containing only sanitized artifacts.

## Monitoring ideas

| Signal | Response owner |
|---|---|
| Unapproved changes to AML workspace/job roles, Storage data access or Key Vault grants | IAM/SecOps |
| New model or image version without linked training/evaluation evidence | MLOps platform |
| Deployment request with missing or invalid approval | Release engineering |
| Deployed artifact hash differs from approved one | Release engineering / incident commander |
| Inference endpoint unexpectedly made public or scoring auth weakened | Cloud platform/SecOps |
| Training data drift, degraded risk/safety metrics, suspicious outputs | Data science + governance |
| Compute job spend abnormal / forgotten online endpoint | FinOps / platform owner |

## Incident workflow

Freeze deployment pipeline, deny affected model asset, quarantine suspect source (no unsafe deserialization), revoke compromised roles, isolate endpoint where required, rollback to approved known-good digest, preserve logs and provenance, re-run tests before restoration.

**Limitations:** Azure ML and Foundry generate different diagnostics. Confirm exact diagnostic categories and schemas for chosen SKU/region before writing Sentinel analytics or claiming end-to-end logging. Avoid logging raw training examples, protected features, weights, keys and inference payloads.
