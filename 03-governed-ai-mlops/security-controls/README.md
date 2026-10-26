# Governed AI/MLOps V2 — Azure service-specific control map

**Scope:** Azure Machine Learning v2; Microsoft Foundry only where explicitly called out. Architecture recommendation ≠ enabled security feature.

| Service | Enforceable capability/design recommendation | Evidence required | Nuance |
|---|---|---|---|
| **Entra ID + Azure RBAC** | Separate developer, workspace, data, compute, registry and prod deployment roles | Effective assignments and failed unauthorized calls | Workspace Contributor is not a substitute for segregation of duties |
| **Azure ML workspace** | Resource isolation by environment, workspace permissions, identities, network settings | Resource configuration & unauthorized operation | Dev/test/prod can use separate workspaces/subscriptions |
| **Azure Storage (Blob/ADLS)** | Dataset ACL/RBAC, encryption and controlled ingestion | Job storage access denied where not entitled | Classification/labels don't universally enforce training dataset access |
| **Azure ML training compute** | Job/compute managed identity with scoped access, trusted code/environment and network | Secret/data denial and dependency image record | Identity can differ by job, compute and datastore auth path |
| **Azure Container Registry** | ACR image provenance, scanning policy, reader rights; disallow unrelated images | Immutable image digest, role denial | Container image tags can move; pin digest where appropriate |
| **Azure ML registries/models** | Versioned artifact IDs, approved publishers and source history | Artifact digest + linked training job, promotion approval | **Registry is not inherently a signed approval gate** |
| **CI/CD (GitHub/Azure DevOps)** | Protected branches, restricted prod environment, approval and digest-bound deploy | Release approver, pipeline version, denied unapproved release | Build and promotion permissions must be separated |
| **Online endpoints** | Entra token scoring for supported managed endpoints; endpoint RBAC; secure ingress/egress | Unauthorized invocation denied, routes verified | Entra `aad_token` auth not identical across endpoint types |
| **AML managed VNet** | Correct isolation mode, approved outbound/private endpoints and DNS | Actual effective routes/denial probes | Training/workspace/endpoint network controls differ |
| **Key Vault** | Secure workspace secrets with supported authentication; scoped access | Secret denial; required trusted-service exception reviewed | Private endpoint alone may not satisfy AML service-side requirements |
| **Microsoft Purview** | Discover/classify supported sources and keep sensitivity lineage | Classification and permission behavior at each source | Purview labels do not automatically prevent a compute identity from reading data |
| **Azure Monitor / Sentinel** | Audit resource changes, ML deployment lifecycle, unusual secret/data reads, security alerts | Correlated sanitized test logs | Studio UI visibility is not an immutable end-to-end audit trail |
| **Microsoft Foundry** | Separate model / project / agent identity, inference permissions, network and evaluation plan | Explicit Foundry configuration evidence | Foundry and AML endpoint IAM/network rules must be validated independently |

## Configuration review checklist

- Dev and prod workspace identities are separated, with bounded subscriptions/resource groups.
- Only an approved **compute identity** reads sensitive training data; human Studio visibility does not imply Storage RBAC.
- Build provenance ties **git commit + dependency image digest + dataset version + training job + model digest**.
- Model promotion uses a distinct deploy principal and independently authorized reviewers; re-check decision at deployment time.
- Validate endpoint `auth_mode`, network, DNS and calling principal for the **specific** endpoint type.
- Avoid `allow_internet_outbound` if an outbound-restricted threat model requires more.
- Time-box workloads, scale idle compute down, and use billing visibility to avoid validation labs unexpectedly accruing costs.
- Never save real datasets, access tokens, PII, model secrets or unredacted traces to the public repo.

### Official documentation

[Azure ML managed identities](https://learn.microsoft.com/azure/machine-learning/how-to-use-managed-identities) · [managed network](https://learn.microsoft.com/azure/machine-learning/how-to-managed-network) · [secure online endpoints](https://learn.microsoft.com/azure/machine-learning/concept-secure-online-endpoint?view=azureml-api-2) · [endpoint authentication](https://learn.microsoft.com/azure/machine-learning/how-to-authenticate-online-endpoint?view=azureml-api-2) · [MLOps registries](https://learn.microsoft.com/azure/machine-learning/concept-machine-learning-registries-mlops?view=azureml-api-2).
