---
name: P16-morning-operations
description: "Swarm deployment: the realtor's morning brief. Calendar, overnight leads, market scrapes, prospect suggestions, and yesterday's books - assembled and presented for human review before the day starts. Agents 10, 14, 15, 18, 19."
---

# Playbook P16 - Morning Operations

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Scheduled daily start (owner-configured time) or owner command.

## Preconditions
- EOD books from previous day exist (P17 completion event on log); if absent, brief runs with the gap NAMED, never silently thinner.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Assemble (parallel, all to human review)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 18 | Today's calendar, deadlines, time blocks | `report.package` | package on log |
| 2 | 14 | Overnight interactions + open leads snapshot | `report.package` | package on log |
| 3 | 10 | Owner-configured searches and scrapes: new listings, price changes, comps movement | `data.package` | package on log; every datum carries provenance |
| 4 | 19 | Prospect suggestions ranked from yesterday's books + market deltas | `prospect.opportunity` | suggestions on log with reasoning trace |
| 5 | 15 | Yesterday's numbers: pipeline value, aging, commission forecast | `report.package` | package on log |

### Present
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 6 | 00 | Single morning brief assembled from the five packages; NOTHING acted on - presented for human review | - | brief delivered; human review gate OPEN |

## HITL gates (hard stops)
- Every item in the brief is review-only. No client-facing action, no listing action, no send of any kind originates from this playbook.
- A scrape datum without provenance does not enter the brief (gate principle).

## Completion criteria
Human has the brief; review verdicts (act / park / discard) recorded via `config.update` or direct command. Completion event logged with brief size and gap flags.

## Abort paths
- Any assembling agent unreachable: brief ships with that section marked ABSENT - a thin brief that says so beats a full-looking brief that lies.

## Notes for the Dispatcher
This playbook is why the product exists: the assistant that already read everything before the human's first coffee. One caught deadline or one surfaced expired-relist opportunity pays for the month.
