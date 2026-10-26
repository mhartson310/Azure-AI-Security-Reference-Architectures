# ADR-001 · Immutable model promotion with independent approval

**Status:** Proposed · **Reviewed:** 2026-10-25

## Decision

Only a deployment pipeline with restricted production rights may promote an exact model artifact (content digest/immutable identity). Release policy requires trusted source commit, dataset provenance, pinned dependency/container image, completed model quality/safety/security evaluation, explicit release-eligible classification, and independent reviewer authorization bound to the artifact and target environment.

A model name, version label or placement in a registry does **not** by itself imply approval.

## Alternatives

- **Manual console deployment:** rejected as default for production; difficult to enforce provenance and segregation of duties.
- **Auto-deploy every new model registry version:** rejected; registration does not prove safety.
- **Trust a mutable model tag/image tag:** rejected; can change what is deployed without approval.
- **Digest-bound release attestation + separate pipeline identity:** selected design; operational overhead and CI/CD work are acceptable for protected production.

## Consequences

Maintaining model artifact hashes, build/SBOM provenance, release evidence, rollback manifests, registry access reviews, and a rejection path is required. The final endpoint should report exactly which artifact digest it serves.

## Tests

ML-03, ML-04, ML-05, ML-06 and ML-08 in [validation](../validation/README.md). The offline gate is a reference control **not equivalent** to a deployed release pipeline.
