---
name: P07-tour-day-coordination
description: "Swarm deployment: client showing interest to completed, feedback-logged tour. Agents 06, 11, 13, 14, 18. Use when a buyer wants to see one or more properties."
---

# Playbook P07 - Tour Day Coordination

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Buyer expresses interest in touring specific properties (via 13 matches or 11 inbound).

## Preconditions
- Buyer-agreement-on-file flag verified (13 sets it; 06 checks it).
- Consent flags permit contact.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Sequencing
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 13→06 | Showing requests, agreement flag set, per property | `showing.request` | acks |
| 1b | 06 | Seller-availability coordination; identity verification per config; occupied-property notice rules |  -  | confirmed slots |
| 1c | 06→18 | Calendar events, licensee availability confirmed | `calendar.event` | no-conflict confirmation |
| 1d | 06 | Confirmations to all parties | `client.message.request` → 11 | send logs |

### Phase 2 - Post-tour
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 06 | Feedback requests; responses logged | `interaction.log` | feedback in 14 |
| 2b | 13 | Profile updates from EXPLICIT client feedback only - never inferred from behavior alone |  -  | profile change log |

## HITL gates (hard stops)
- Access: licensee/authorized presence per 06's legal line - no lockbox codes, ever.
- Feedback contradicting stated criteria → ask the client via 11, never silently rewrite the profile.

## Completion criteria
All tours executed or explicitly cancelled; confirmations and feedback logged; profile updated only from explicit statements.

## Abort paths
- Identity verification fails for any access-bearing appointment → that showing is cancelled, human notified.
