---
name: P03-under-contract-transition
description: "Swarm deployment: accepted offer to transaction-mode operations. Agents 05, 07, 08, 11, 12. Use when an offer is accepted and the listing moves to pending."
---

# Playbook P03 - Under-Contract Transition

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off; not runtime-hardened)

## Trigger
Human confirms offer acceptance (executed contract artifact filed via 08).

## Preconditions
- Executed contract on file (08 verified: opens, matches type).
- Contract deadline set extractable for 07's config.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Status flip (parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 05 | MLS status → pending, live-verified, within MLS window | `status.update` | live check + acks 11/12/14 |
| 1b | 12 | Halt active-marketing; switch to pending/under-contract messaging only if configured | (consumes 1a) | campaign state change logged |

### Phase 2 - Transaction kickoff
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 07 | Load deadline set per contract template config; open timeline |  -  | timeline record + `interaction.log` |
| 2b | 07→08 | Initial document requirements (earnest receipt, disclosures per contract) | `doc.request` | `doc.status` responses (`in_reply_to`) |
| 2c | 07 | First deadline alerts scheduled | `deadline.alert` | acks from 11, 18 |
| 2d | 11 | Client transition message: what happens next, cadence | `client.message.send` | send log |

## HITL gates (hard stops)
- Any contract-language question (deadline calculable two ways, ambiguous contingency) → `escalation.legal_line` - P03 hands ambiguity up, never interprets.
- Earnest money handling questions → human (15's trust-accounting exclusion applies swarm-wide).

## Completion criteria
Pending status live-verified; timeline loaded with every deadline dated; initial doc requests acked; client informed.

## Abort paths
- Contract artifact fails verification (unreadable, unsigned pages) → halt kickoff, human immediately.
- Deal falls through pre-kickoff → human directs status reversal; P05 wind-down does NOT auto-trigger.
