---
name: P09-contract-to-close
description: "Swarm deployment: executed contract through closing day. Agents 07, 08, 09, 11, 18. The densest sequential playbook — deadline-driven, wire-fraud lines active throughout."
---

# Playbook P09 — Contract-to-Close

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 — Dispatcher)
**Version:** 0.1 (DRAFT — not implemented)

## Trigger
P03 completion (transaction kickoff done).

## Preconditions
- Timeline loaded with full deadline set (07).
- Deadline arithmetic config bound to this contract template.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Continuous — deadline engine
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 07 | Track every deadline: inspection, appraisal, financing contingency, title, HOA docs, repairs, closing | `deadline.alert` → 11, 18 | alerts per config lead-time; 18 blocks protected |
| 2 | 07→08 | Milestone documents requested as due | `doc.request` | `doc.status` (`in_reply_to`) |
| 3 | 07→09 | Inspector/appraiser scheduling as milestones require | `vendor.request` | `vendor.schedule` confirmations |
| 4 | 09→08 | Reports collected, verified present-and-opens | `deliverable.release` | filed by 08 |
| 5 | 11 | Milestone facts to client — facts, never characterizations | `client.message.send` | send logs |

### Closing week
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 6 | 07 | Closing coordination: date, parties, document completeness check via 08 | `deadline.alert` | completeness report |
| 7 | human | Closing representation, signing, all legal acts | — | closed |
| 8 | 07 | Emit closure → P10 triggers | `transaction.closed` | acks from 16, 14, 15 |

## HITL gates (hard stops)
- WIRE FRAUD: no agent sends, confirms, or relays wire instructions — any wire topic in any channel → immediate `escalation.legal_line` flagged out-of-band. Active every step.
- Missed or at-risk deadline → escalate with the clause verbatim; never interpret cure options.
- Deadline satisfied only by artifact on file — verbal assurance is `stated_by_party`, not satisfaction.

## Completion criteria
Every deadline satisfied-by-artifact or human-resolved; closing executed by human; `transaction.closed` acked by 16, 14, 15.

## Abort paths
- Contingency failure → human decision path; agents freeze the affected timeline branch, alerts continue on the rest.
- Financing collapse → human; no agent communicates deal state to the other side.
