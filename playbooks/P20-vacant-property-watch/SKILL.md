---
name: P20-vacant-property-watch
description: "Swarm deployment: standing watch on vacant listings. Condition checks scheduled, utility status tracked, activity anomalies surfaced. Agents 05, 09, 10, 14, 18."
---

# Playbook P20 - Vacant Property Watch

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off; not runtime-hardened)

## Trigger
Listing marked vacant (from P01 data or status change) until occupied/closed.

## Preconditions
- Vacancy recorded on the listing record; owner-configured check cadence exists.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Standing watch
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 18 | Condition-check cadence scheduled (owner/vendor walkthroughs) | `calendar.event` | events scheduled |
| 2 | 09 | Walkthrough vendor scheduling + completion proof per visit | `vendor.request` | `deliverable.release` with proof |
| 3 | 14 | Utility/service status tracked on the record; lapses flagged | `record.request` | record current |
| 4 | 10 | Showing-activity anomaly check: zero-activity streak or unusual access pattern to morning brief | `data.package` | anomalies in P16 brief |

### Event response
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 5 | 00 | Condition event (damage, break-in sign, utility failure) = same-day escalation to human with the raw report | `escalation.*` | human acknowledgment |

## HITL gates (hard stops)
- Condition reports carry the vendor's raw artifact - never a paraphrase.
- No repair authorization originates here; scope and spend are human decisions (P09 vendor rules apply).

## Completion criteria
Continuous until vacancy ends; each cadence cycle completes with proof artifacts on log.

## Abort paths
- Two consecutive missed walkthroughs: escalation - an unwatched vacant is the risk this playbook exists to prevent.

## Notes for the Dispatcher
Vacant listings fail quietly. The watch converts quiet failure into logged events with proof.
