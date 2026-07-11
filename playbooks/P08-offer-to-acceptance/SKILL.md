---
name: P08-offer-to-acceptance
description: "Swarm deployment: offer submission through human-negotiated resolution. Agents 07, 08, 11, 18. Thinnest playbook by design - negotiation is entirely human; agents track status and documents around it."
---

# Playbook P08 - Offer-to-Acceptance

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off; not runtime-hardened)

## Trigger
Offer submitted (buyer-side or received on a listing).

## Preconditions
- Transaction context established (14).
- Offer artifact filed and verified (08).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Continuous - around the human negotiation
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 07 | Offer status tracking: submitted / countered / expired / response deadlines | `deadline.alert` → 11, 18 | status log current |
| 2 | 07→08 | Supporting docs: pre-approval / proof of funds current | `doc.request` | `doc.status` (`in_reply_to`) |
| 3 | 08 | Chase missing support docs from parties | `client.message.request` → 11 | chase log |
| 4 | human | ALL negotiation: terms, counters, strategy, acceptance |  -  | human decisions logged as artifacts |
| 5 | 07 | On acceptance → trigger P03 |  -  | P03 preconditions met |

## HITL gates (hard stops)
- Every negotiation act is human-only - an agent relaying a counter is transport, an agent suggesting one is a violation.
- Response-deadline expiry without human action → re-alert, never auto-respond.

## Completion criteria
Offer resolved (accepted → P03, rejected/expired → logged); all status transitions and artifacts on file.

## Abort paths
- Multiple-offer situation → this playbook continues per offer; presentation order/strategy is human-only.

## Notes for the Dispatcher
Most steps here say 'the human does this.' That is the legal line working, not a thin spec.
