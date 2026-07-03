---
name: P05-expired-withdrawn-winddown
description: "Swarm deployment: immediate marketing halt and clean wind-down on expired or withdrawn listing. Agents 05, 11, 12, 14. Use when a listing expires or the seller withdraws."
---

# Playbook P05 — Expired/Withdrawn Wind-down

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 — Dispatcher)
**Version:** 0.1 (DRAFT — not implemented)

## Trigger
Listing reaches expiration date (07/05 tracked) or seller withdrawal confirmed by human.

## Preconditions
- Status change authorization: expiration is automatic per listing agreement dates; withdrawal requires human confirmation on file.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 — Halt (immediate, parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 05 | MLS status change, live-verified, within MLS window | `status.update` | live check + acks |
| 1b | 12 | ALL marketing halted on status consumption — ads paused, scheduled posts cancelled | (consumes 1a) | halt confirmations per platform |
| 1c | 11 | Seller communication per human-approved messaging | `client.message.send` | send log |

### Phase 2 — Disposition (human decision)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 14 | Context annotated: outcome, reason if stated | `interaction.log` | record updated |
| 2b | human | Relist pursuit decision. If pursuing: seller re-enters via standard intake (01→02) — no agent auto-enrolls a former seller into sequences | — | human direction logged |

## HITL gates (hard stops)
- Marketing running after status change is a compliance incident, not a cleanup item — 1b failure escalates immediately.
- Relist solicitation timing/approach is the human's call entirely.

## Completion criteria
Status live-verified; zero active marketing verified per platform; seller informed; record annotated; human disposition logged.

## Abort paths
- Seller reverses withdrawal mid-winddown → halt playbook, human direction on state restore.
