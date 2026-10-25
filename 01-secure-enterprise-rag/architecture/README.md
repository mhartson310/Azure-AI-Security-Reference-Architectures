# Secure RAG V2 — Architecture, data flow and trust boundaries

**Reference deployment (not implemented).** The [visual](../../assets/01-rag-trust-boundaries.svg) is a control-oriented logical architecture, **not** a deployment topology or a guarantee that every Azure service provides identical networking features.

## Security assumptions

1. Users are interactive employees/approved partners authenticated through a configured Microsoft Entra tenant.
2. Documents have **per-document/tenant permissions**; retrieval must enforce them.
3. Search indexes can be stale or misconfigured; the app does not accept their ACL fields as authoritative without independent confirmation.
4. Model prompts and retrieved documents are untrusted relative to authorization/identity.
5. App/API uses its own limited workload identity for Search and model calls. No direct browser access to Search admin keys or model credentials.
6. The architecture chooses **application-managed Search security filters** as its reproducible GA-pattern baseline; preview native features are alternatives, not presumed active.
7. This walkthrough is a **reference design** and must be adapted to actual source systems, supported APIs and service versions.

## Trust boundary catalog

| ID | Boundary | Crossing | Required enforcement | Failure case |
|---|---|---|---|---|
| **TB-1** | Untrusted browser → ingress | User request, session token | TLS, ingress/WAF rules as appropriate; session/CORS/CSRF controls; restrict request size | Stolen/invalid token, untrusted claims |
| **TB-2** | Ingress → application authorization | Authenticated principal → allowed tenant/groups/resources | Validate issuer, audience, signature, expiry; obtain trusted membership and entitlements; reject missing context | Forged `group_ids` posted in request body |
| **TB-3** | Source systems → ingestion/search | Data chunks, citations, ACL metadata | Trusted ingestion identity, source integrity, stable IDs, protected write permissions, permission update strategy | Forged index ACL, poisoned source, stale permissions |
| **TB-4** | App authorization → Search query | Tenant and principal scoped query | AND tenant filter and allowed principal filter; no client-controlled filter override; Search reader RBAC | Search returns other user's snippets |
| **TB-5** | Search results → application/model context | Retrieved snippets and metadata | Independently re-check ACL, permission freshness, source provenance; minimize snippets and citations | Unauthorized text enters model context |
| **TB-6** | Application → Foundry model | System instructions + authorized untrusted context | Restrict model endpoint identity; enforce no-agent/no-tool paths unless explicitly authorized; content boundaries; output checks | Retrieved document impersonates system instruction |
| **TB-7** | App/Search/model → operational telemetry | Denial events, usage, traces | Sanitized structured events, correlation IDs, minimal retention and controlled access | Secrets appear in logs; missing attribution |

*TB numbering is logical, not a claim of separate subnets. Internal service-to-service edges can cross network boundaries depending on deployment.*

## Request and ingestion flows (distinct identities)

```mermaid
sequenceDiagram
    autonumber
    actor U as Employee
    participant IdP as Microsoft Entra ID
    participant App as RAG App/API
    participant Auth as Authoritative ACL store
    participant Search as Azure AI Search
    participant Model as Foundry model
    U->>IdP: Sign in
    IdP-->>U: Signed access/session context
    U->>App: Query + validated session/token
    App->>App: Validate token issuer/audience/expiry; determine trusted tenant, user, groups
    App->>Search: Query with server-built tenant + principal filter (app MI/Search Reader)
    Search-->>App: Candidate documents/snippets
    loop Every candidate
        App->>Auth: Read current document permission + tenant
        Auth-->>App: ACL, active state, freshness decision
        App->>App: Reject missing, stale, wrong-tenant or unauthorized hits
    end
    App->>Model: User query + permitted snippets (untrusted data)
    Model-->>App: Generated answer
    App->>App: Check output/citation IDs against authorized hits
    App-->>U: Answer + permitted citations
```

**Separate ingestion flow:** approved content source → ingestion identity/service → document extraction and splitting → carry forward immutable source/tenant/document IDs and ACL metadata → index update. The ingestion identity should not be reused by inference; Search Index Data Contributor (writes) and Search Index Data Reader (queries) should be separately granted. Source deletion or ACL change must trigger synchronization or an authoritative check on requests, according to the organization's revocation SLA.

## Retrieval decisions that matter

- Use **stable Entra object IDs**, not display names or free-form emails, for user/group matching when your permission model is Entra-backed.
- Treat **service RBAC** and **document ACL** as independent gates. A Search Index Data Reader can query the index under its workload identity, but this doesn't certify what end-user content is permitted.
- Example schema for [security filter pattern](https://learn.microsoft.com/azure/search/search-security-trimming-for-azure-search): `tenant_id` (`Edm.String`, filterable), `allowed_users`/`allowed_groups` (`Collection(Edm.String)`, filterable). See the [runnable filter builder](../lab/authorization_reference.py). A production index additionally requires key, content/chunk fields, and suitable vector/hybrid configuration.
- Apply tenant scoping in **every** query path, including semantic/vector/hybrid, citations, follow-on retrievals, export, history and cache paths.
- Use a separately trusted ACL source for the post-retrieval check. A second read of the same tampered index metadata is **not** independent verification.
- Decide how to handle revoked access, group membership changes, source deletions, cache invalidation, ACL lookups being unavailable, and index update lag. **Fail closed** when authorization is unknown.
- Split source text and model instructions; keep retrieval tools disabled unless separately authorized. Input delimiters reduce ambiguity but **do not stop prompt injection by themselves**.
- Do not accept model-generated citation IDs that are not in the currently authorized document set.

## Network and infrastructure considerations

An example production topology places the app in a private-connected workload network, uses supported Private Link connections for Search, storage, Key Vault and Foundry model endpoints, and controls egress by policy. Validate DNS, public-network-access restrictions, dependency limitations and per-product SKUs. A private endpoint on one service **does not** make the entire RAG system private. Refer to Microsoft's [Foundry networking guidance](https://learn.microsoft.com/azure/ai-foundry/how-to/configure-private-link?view=foundry).

## Verification checkpoints

1. Negative query with mismatched user/group: **no restricted snippets or citations**.
2. Tenant mismatch even with coincident group: **no results**.
3. Permission revocation: **denial within explicitly defined revocation SLA** and no stale cached answer.
4. Backend returns unauthorized candidate despite query filter: **app post-filter rejects it**.
5. Indirect prompt injection inside authorized source: **model must not perform prohibited action or leak restricted data** (requires deployed model/agent eval).
6. Search and model identities must not load or administer data outside their required roles.
7. Cross-service events should be correlated via app-issued trace IDs and contain **no secret content by default**.
