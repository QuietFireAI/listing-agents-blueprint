---
name: P18-seller-weekly-report
description: "Swarm deployment: the standing seller update. Showings, feedback, market movement, next steps - assembled, compliance-gated, human-approved, sent on cadence. Agents 05, 06, 10, 11, 14, 17."
---

# Playbook P18 - Seller Weekly Report

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off; not runtime-hardened)

## Trigger
Weekly per active listing (owner-configured day) or owner command.

## Preconditions
- Listing active in MLS (05 status current).
- Seller update template exists in identity config; free-composition to clients is not a fallback.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Assemble
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 06 | Week's showings + feedback received | `interaction.log` refs | items on log |
| 2 | 10 | Market movement for the property's segment, provenance on every datum | `data.package` | package on log |
| 3 | 05 | Status and activity summary for the listing | `status.update` | update on log |

### Gate and send
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 17 | Fair-housing/advertising screen on assembled draft | `content.review` | `content.verdict` clean |
| 5 | 11 | Human review of draft; on approval, send via template | `client.message.send` | send log + human approval on file |

## HITL gates (hard stops)
- No send without human approval - the weekly report is client-facing.
- No market claim without provenance; thin data weeks say so rather than pad.
- Pricing commentary or strategy suggestions are Legal Line - the report STATES data, the human interprets it.

## Completion criteria
Send logged with approval reference; next cadence scheduled via 18.

## Abort paths
- Verdict requires changes past send-day: report ships next day corrected, delay logged; never ship unverdicted.
- Seller has requested pause: cadence suspended, resumption is owner action.

## Notes for the Dispatcher
Consistency is the product here: the seller who hears every week, in the same shape, with sourced data, stays a client. This playbook is the standardization claim made real.
