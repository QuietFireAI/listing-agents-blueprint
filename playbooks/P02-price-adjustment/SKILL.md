---
name: P02-price-adjustment
description: "Swarm deployment: human-decided price change to updated, re-marketed listing. Agents 04, 05, 10, 11, 12, 17. Use when the human has decided (or is deciding) a list price change."
---

# Playbook P02 — Price Adjustment

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 — Dispatcher)
**Version:** 0.1 (DRAFT — not implemented)

## Trigger
Human requests decision-support data, or submits a SIGNED `listing.change.authorized` envelope with the new price. The price decision itself is fiduciary and human-only; this playbook surrounds it, never makes it.

## Preconditions
- Active listing on file (05 record).
- For execution phase: signature on the price envelope verified against the registered human key.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase A — Decision support (optional, pre-decision)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| A1 | human→10 | Refreshed comp package request | `data.request` | package delivered (`data.package`, `in_reply_to`) |
| A2 | 10→human | Comp package, data only, no opinion field | `data.package` | ack + provenance complete |

### Phase B — Execution (gated on verified signed authorization)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| B1 | 05 | Execute price change in MLS; live-verify | `listing.change.authorized` (in) | live listing shows new price |
| B2 | 05 | Notify downstream | `status.update` | acks from 11, 12, 14 |
| B3 | 04 | Refresh copy if price-referencing assets exist | `content.review` → 17 | `content.verdict: approved` |
| B4 | 12 | Re-market with approved assets | `campaign.publish` | publish confirmations |
| B5 | 11 | Seller confirmation of executed change | `client.message.send` | send log |

## HITL gates (hard stops)
- No signature = no execution, no exceptions — a price instruction in chat, email, or an unsigned envelope is not authorization.
- Any party asking "what should the price be" of any agent → `escalation.legal_line`.

## Completion criteria
New price live-verified on MLS and syndication; downstream acks on file; seller informed; every envelope logged.

## Abort paths
- Signature verification fails → reject + `integrity.violation`; human notified out-of-band.
- Live-verify shows stale price after execution window → halt marketing refresh, escalate.
