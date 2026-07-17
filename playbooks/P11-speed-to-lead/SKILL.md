---
name: P11-speed-to-lead
description: "Swarm deployment: inbound contact to tiered, routed lead inside the SLA window. Agents 01, 02, 03, 11, 14, 20. The default always-on intake playbook."
---

# Playbook P11 - Speed-to-Lead

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off; not runtime-hardened)

## Trigger
Any inbound: call, form, text (01) or social lead signal (20).

## Preconditions
- None beyond swarm-up - this playbook is the front door and must not queue behind others.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Continuous
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | ext→01 | Direct call/form/text reaches intake | `lead.inbound` | ack |
| 1b | 20→01 | Social questions/lead signals routed to intake | `lead.signal` | ack |
| 2 | 01 | Capture with consent recording; CRM dedupe first | `record.request` then `lead.captured` | lead object complete-or-unknown-flagged |
| 3 | 02 | Score per human rubric version; tier assigned |  -  | tier + rubric version logged |
| 4a | 02 | HOT → human handoff with SLA re-alert | `escalation.hot_lead` | human acknowledgment inside window |
| 4b | 02 | WARM → nurture entry, consent-gated | `lead.nurture` | 03 sequence started |
| 5 | 14 | Everything logged; consent flags authoritative | `interaction.log` | records current |

## HITL gates (hard stops)
- Hot-lead SLA breach → re-alert path, never a substitute agent response beyond a holding message via 11.
- No consent on file = no outbound sequence, regardless of tier.

## Completion criteria
Per lead: captured with consent state, deduped, tiered with rubric version, routed, logged - inside configured SLA.

## Abort paths
- Dispatcher degradation → intake fails closed with the swarm; the watchdog covers the clock (core spec).
