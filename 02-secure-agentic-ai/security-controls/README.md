# Agentic AI V2 — Azure and Power Platform control matrix

**Review:** 2026-10-25. This matrix distinguishes product capabilities from **separately implemented** architecture components. Some details vary by agent type, channel, identity mode, licensing and environment.

| Layer | Copilot Studio | Microsoft Foundry Agent Service | Required independent proof |
|---|---|---|---|
| Authentication | Microsoft Entra authentication options; data policy can block unauthenticated agent publishing | Entra-based caller/agent identity; identity and RBAC on runtime | Anonymous/invalid identity denied at ingress and action API |
| Maker/author privileges | Power Platform environment security roles and governance | Foundry project/resource RBAC and agent management permissions | Maker cannot grant unreviewed production tool access |
| Tool/connectors | Data policies can block Power Platform connectors, HTTP endpoints, event triggers, publishing channels | Toolbox/agents/tools, own endpoint authorization, network routing and RBAC | Unauthorized tool and destination denied by actual API |
| Data exfiltration | Data policy connector grouping and blocks; Purview compliance for supported interactions | Custom destination filters, private network controls where supported | Neither channel nor HTTP/MCP tool exports synthetic protected marker |
| Agent identity | Verify connection mode and user impersonation for each tool | Per-agent identity and OBO where configured | Tool resource permissions bound to acting user and service principal |
| Networking | Depends on channel, connector and environment routing | Agent networking differs for prompt vs hosted agents; external built-in tools may bypass expected routes | DNS/egress inspection of **each** relevant tool |
| Secrets | Connection credentials/Key Vault where suitable | Managed identities/Key Vault and scoped credentials | No secrets in prompt, chat, agent config or telemetry |
| High-impact approvals | Configure workflow/API owner approval (not prompt-based) | Configure independent gateway/workflow approval | Replayed/wrong-parameter approval rejected |
| Monitoring | Platform logs / Purview audit where supported; custom API decisions | Foundry traces, Azure Monitor / Application Insights; custom decision events | End-to-end action/denial replay without raw sensitive payload |
| Sensitive-data governance | Purview supports multiple Copilot Studio interaction protections depending on settings, channel and billing | Purview governance varies with data source/integration | Verify actual coverage, never assume all connectors are governed |

### Copilot Studio policy validation checklist

1. Require Entra authentication for internal agents through supported settings and block 'Chat without Microsoft Entra ID authentication' using a data policy if appropriate.
2. Separate Business / Non-business / Blocked connector categories as intended; test actual blocking and avoid accidental business interruption.
3. Restrict HTTP requests/endpoints, unwanted tools/connectors, event triggers and publish channels.
4. Verify maker restrictions in **Power Platform admin center** and user-visible enforcement in Copilot Studio. Data policies can surface publishing errors / restrictions.
5. Verify Purview protections for Copilot Studio interactions **under the organization's channel, license, and configuration**. Non-Microsoft channels can have additional pay-as-you-go billing dependencies.

### Foundry Agent Service checklist

1. Inventory agent, caller, tool and OBO identities and explicit scopes; avoid broad service principals.
2. Verify role assignments for agent creation, invocation, tool administration, resource data and model inference.
3. For host/runtime networking, test the documented **agent type's path** through Tools Service/data proxy and external tool routes. Built-in knowledge tools do not necessarily traverse the assumed customer firewall.
4. Constrain tool invocation and destinations at the downstream API, even with private VNet access.
5. Separate agent/model traces from sensitive business action audit, and test end-to-end correlation.

### Native vs custom diagram legend

**Native configuration:** Power Platform data policies, Entra, RBAC, service-level networking, supported Foundry tracing.  
**Reference custom components:** actor-aware policy gateway, single-use business approval, dynamic resource authorization, tamper-evident business action audit.

### Source links

- [Copilot Studio data policies](https://learn.microsoft.com/microsoft-copilot-studio/admin-data-loss-prevention)
- [Copilot Studio project security guidance](https://learn.microsoft.com/microsoft-copilot-studio/guidance/sec-gov-phase3)
- [Purview controls for Copilot Studio](https://learn.microsoft.com/purview/ai-copilot-studio)
- [Foundry Agent Service overview](https://learn.microsoft.com/azure/ai-foundry/agents/overview)
- [Foundry networking deep dive](https://learn.microsoft.com/azure/foundry/agents/concepts/agents-networking-deep-dive)
- [Foundry chat baseline reference](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat)
