# Governed Azure AI/MLOps V2 — Negative-security runbook

**Status:** Planned Azure ML integration tests; offline policy tests are separate and limited.

## Prerequisites

Isolated sandbox workspace with **synthetic training dataset**; small or CPU-only test to limit cost, approved and disallowed workload identities, test registry/model versions, simple mock prediction endpoint or low-cost AML endpoint, protected production-like deployment identity, restricted CI/CD policy, audit collection and teardown/budget controls.

**Important:** Use only harmless test data and **never deploy a malicious/unknown model artifact for execution**. Verify integrity and quarantine without deserialization or execution.

| ID | Scenario and expected outcome |
|---|---|
| **ML-01** | Training user/compute identity without Storage data right attempts dataset read → denied, correlated evidence |
| **ML-02** | Untrusted dataset label/source/version enters pipeline → provenance or validation gate rejects before training |
| **ML-03** | Unexpected dependency or container digest substituted in release manifest → blocked, no deployment |
| **ML-04** | Model artifact content digest differs from release attestation → blocked and quarantined, no load/execution |
| **ML-05** | Model registered without required evaluation/approval → registry may contain version, **promotion** denied |
| **ML-06** | Model author attempts self-approval, expired approval, wrong target environment → denied |
| **ML-07** | Unauthorized client invokes managed online endpoint using wrong/no credentials → HTTP/auth failure; no scored output |
| **ML-08** | Release pipeline identity attempts deploy to unrelated endpoint or resource group → RBAC denies |
| **ML-09** | Disallowed network client connects to private workspace/endpoint; unauthorized egress from compute → blocked and DNS/routes confirmed |
| **ML-10** | Synthetic cost/runaway workload attempts exceed defined concurrency/time/quota thresholds → stopped by **configured** workload mechanism; budget alert alone not sufficient |

## Execution checklist

1. Capture deployment region, workspace, endpoint type, identities/RBAC, actual network isolation mode, data source, model/build digests, Azure ML and CLI/SDK versions. Save lab setup with fake IDs.
2. Run positive control first: allowed user can train on approved synthetic data; approved model/version can deploy.
3. Run ML-01/02 against permission and provenance; record Azure deny, not merely script return value.
4. For ML-03/04/05/06 verify policy gates and pipeline permissions with harmless substitute digest/manifest, *without loading malicious weights*.
5. Use managed online endpoint configured for intended auth mode to run ML-07; confirm client role denied.
6. Verify network inbound and outbound as **separate** tests for ML-09.
7. Capture Resource/Activity logs, pipeline run ID, model digest and deployment outcome; redact every identifier or data field that could expose a real organization.
8. Destroy or stop resources; check billing and record exceptions.

## Evidence promotion rules

Populate [evidence-template.json](evidence-template.json) privately for each test. Status values: `NOT_RUN`, `PASS`, `FAIL`, `BLOCKED`; only mark PASS when the **actual Azure/pipeline behavior** is observed. Repository source code and test plans do not prove production safety.

[Offline release-policy harness](../lab/README.md) covers narrow deterministic model manifest policy semantics, not service/RBAC/network enforcement.
