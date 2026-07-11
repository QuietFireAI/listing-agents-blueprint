---
name: P17-end-of-day-books
description: "Swarm deployment: close the day's books. Every interaction, lead movement, financial delta, and missed-item candidate captured to a dated dataset that feeds tomorrow's P16 brief. Agents 14, 15, 18."
---

# Playbook P17 - End-of-Day Books

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off; not runtime-hardened)

## Trigger
Scheduled daily close (owner-configured) or owner command.

## Preconditions
- None beyond swarm-up; the books close even on a quiet day - an empty day recorded beats a missing day.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Close
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 14 | Day's interaction log, lead tier movements, oscillation flags | `report.package` | dated dataset on log |
| 2 | 15 | Financial deltas: pipeline changes, aging receivables, commission movement | `report.package` | dated dataset on log |
| 3 | 18 | Tomorrow's deadlines and unconfirmed appointments; anything unacknowledged today | `report.package` | dated dataset on log |
| 4 | 00 | Missed-item sweep: unanswered client messages, stale HOT leads, docs pending past SLA, listings with zero activity - the things a human assistant misses at 6pm | - | missed-item list on log, each with evidence pointer |

### Book
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 5 | 00 | Dated EOD books object assembled; becomes P16's morning input | - | completion event with books hash |

## HITL gates (hard stops)
- Books are records, not actions - nothing client-facing originates here.
- A missed-item entry must carry its evidence pointer (envelope id or log ref); a hunch is not a books entry.

## Completion criteria
Dated books object on log with hash; P16 precondition satisfied for tomorrow.

## Abort paths
- Any closing agent unreachable: books close with the section marked ABSENT and flagged to the morning brief.

## Notes for the Dispatcher
The books are the memory. The suggestions in tomorrow's brief are only as honest as tonight's close - never rebuild from model memory, only from the log.
