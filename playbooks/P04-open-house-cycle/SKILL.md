---
name: P04-open-house-cycle
description: "Swarm deployment: scheduled open house from promotion through lead capture. Agents 01, 02, 04, 06, 11, 12, 14, 17. Use when human/config schedules an open house."
---

# Playbook P04 — Open House Cycle

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 — Dispatcher)
**Version:** 0.1 (DRAFT — not implemented)

## Trigger
Open house scheduled (human decision or P01 step 3d).

## Preconditions
- Listing live (05 status active).
- Open-house marketing assets exist or are producible (04).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 — Promotion (compliance-gated)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 04→17 | Open-house materials review | `content.review` | `content.verdict: approved` |
| 1b | 12 | Promote per CCP-satisfied listing; special-ad-category rules | `campaign.publish` | publish confirmations |
| 1c | 06 | RSVP logistics open; confirmations to registrants | `client.message.request` → 11 | RSVP log |

### Phase 2 — Event + capture
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 06 | Attendance/feedback logistics; access remains licensee-present per legal line | `interaction.log` | event log filed |
| 2b | 01 | Walk-in/registrant capture with consent recording | `lead.captured` | lead objects to 02 |
| 2c | 02 | Score and tier new leads; hot → SLA path | `escalation.hot_lead` / `lead.nurture` | tier assignments logged |

## HITL gates (hard stops)
- No agent authorizes access — a licensee or authorized person is physically present, period.
- Any pricing question from an attendee → capture the question verbatim, `escalation.legal_line`.

## Completion criteria
Event executed with licensee present; every attendee contact captured with consent status; leads tiered; feedback logged to 14.

## Abort paths
- Licensee unavailable → event does not proceed; 06 cancels via 11, reschedule to human.
