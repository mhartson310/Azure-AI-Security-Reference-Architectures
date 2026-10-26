# ADR-002 · Separate workspace, job, release, and endpoint identities

**Status:** Proposed · **Reviewed:** 2026-10-25

## Decision

Use separate identities and scopes for human development, workspace service calls, training compute/jobs, release pipeline and inference endpoint. Prefer a **managed Azure ML virtual network** where its isolation modes support the workload, and verify incoming/outgoing endpoint isolation separately from workspace network policy.

## Rejected alternatives

- Give all users and compute resources a shared broad Contributor identity.
- Assume a workspace private endpoint makes every model endpoint/storage connection private.
- Assume all training jobs use the interactive scientist's user identity.
- Reuse dev environment pipeline identities to promote to prod without explicit controls.

## Important caveats

- Managed network `allow_internet_outbound` is not restricted outbound mode.
- Azure ML service-side dependency access might require a Key Vault trusted-services bypass even when private endpoints are configured. Confirm the exact configuration and minimize its scope.
- Managed online endpoint authentication supports modes with different security and role requirements; prefer Entra for managed production endpoints where possible.
- Cross-workspace registry sharing can be useful, but doesn't eliminate artifact integrity and approval requirements.

## Tests

ML-01, ML-02, ML-07, ML-09, ML-10 in [validation](../validation/README.md).
