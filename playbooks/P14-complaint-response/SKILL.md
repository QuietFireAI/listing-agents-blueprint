---
name: P14-complaint-response
description: "Swarm deployment: detected complaint to human-resolved closure with outbound hold. Agents 11, 14, 17, 20. Entire response is human; agents detect, hold, and document."
---

# Playbook P14 - Complaint Response

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-10 - owner sign-off)

## Trigger
20 classifies a complaint (social) or 11 receives one directly.

## Preconditions
- None - complaints preempt.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Immediate
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 20 or 11 | Complaint verbatim + context to priority queue | `escalation.complaint` | human notification per urgency config |
| 2 | 11 | Outbound HOLD for that client context - no scheduled touches fire |  -  | hold state logged |
| 3 | 20 | Optional DRAFT response attached (labeled, unpublished), compliance-checked | `content.review` → 17 | verdict attached to queue item |
| 4 | human | Entire response: channel, content, resolution |  -  | resolution artifact |
| 5 | 14 | Full thread logged; hold released only on human direction | `interaction.log` | context annotated |

## HITL gates (hard stops)
- No agent replies publicly or privately to the complaint - drafting is permitted, sending is human-only.
- Complainant with an active transaction → highest urgency; no drafted response at all (20's line).
- Never confirm the person's client status in any public channel, including while clarifying.

## Completion criteria
Human resolution logged; hold released by direction; context annotated; if public, the human's response posted by the human.

## Abort paths
- Complaint reveals a potential legal claim → `escalation.legal_line` supersedes; counsel territory.
