---
name: P19-property-access-custody
description: "Swarm deployment: keys, codes, and lockboxes as custody items. Issue, audit, rotate, revoke - with access secrets never transmitted in messages. Agents 06, 09, 14, 18."
---

# Playbook P19 - Property Access Custody

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off; not runtime-hardened)

## Trigger
New listing access setup (from P01), custody audit cadence, or a custody event (lost key, code exposure, vendor access need).

## Preconditions
- Custody register exists for the property (created at P01 step or first event).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Custody operations
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 06 | Access grants recorded per showing/vendor need; instructions route parties to the custody protocol - the SECRET ITSELF never rides a message | `interaction.log` | grant recorded, no secret in any payload |
| 2 | 09 | Vendor access windows scheduled; entry/exit confirmations required | `vendor.request` / `calendar.event` | confirmations on log |
| 3 | 14 | Custody register current: who holds what, since when | `record.request`/`record.response` | register reconciles |

### Audit
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 4 | 18 | Cadence audit: outstanding grants past window flagged | `deadline.alert` | alerts on log |
| 5 | 00 | Exposure event = escalation; rotation task to human same day | `escalation.*` | human acknowledgment |

## HITL gates (hard stops)
- An access code, combo, or key location NEVER appears in a message payload, log free-text, or report - references only (custody register id).
- A grant without an expiry is refused - open-ended access does not exist.
- Exposure suspicion = rotate first, investigate second; the cost asymmetry decides.

## Completion criteria
Register reconciled: every outstanding grant inside its window, every expiry scheduled.

## Abort paths
- Register cannot reconcile (unknown holder): escalation, showings on that property hold until human clears access state.

## Notes for the Dispatcher
One unaccounted key is a liability event, not an inconvenience. This playbook exists because access custody is where informal practice hurts agents worst.
