---
name: P23-price-review-evidence
description: "Swarm deployment: assemble the market-and-activity evidence for a price conversation and hand it to the human - who decides. Agents 05, 10, 11, 14, 15. Distinct from P02 (executes a decided change) and P15 (pre-listing CMA); this is the 'is it time to talk price' evidence pack for a live listing."
---

# Playbook P23 - Price-Review Evidence Assembly

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-10 - owner sign-off)

## Trigger
A price-review signal on a live listing: days-on-market threshold crossed,
showing-to-offer ratio below a configured floor, or an owner command. This
playbook produces evidence; it never produces or implies a number. The price
opinion is the human's fiduciary decision, always - the same line P02 and P15
hold.

## Preconditions (all verified before Phase 1)
- The listing is live (05 status is active). A price-review on a listing that
  is not live is a different workflow; stop and name it.
- Showing and feedback history exists for the listing context in 14. Thin
  history is reported as thin, never silently padded.

## Deployment sequence

### Phase 1 - Gather (parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 05→10 | Push current listing data (status, DOM, position) to market data | `listing.data` (05→10) | 10 ack |
| 1b | 11→10 | Request comparable/absorption evidence for the listing's segment | `data.request` (11→10) | ack |
| 1c | 11→14 | Log the review as opened against the listing context | `interaction.log` (11→14) | ack + record ID |

### Phase 2 - Assemble (gated on 1a + 1b)
GATE: both the listing's own position (DOM, showings, feedback) and the
external market evidence are present. A one-sided pack (market with no activity,
or activity with no market) is incomplete; hold and name the missing half.
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 10→human | Deliver the comparable/absorption package to the human | `data.package` (10→human) | delivery on log |
| 2b | 14→human | Deliver the listing's activity summary (showings, feedback, DOM) | `report.package` (14→human) | delivery on log |
| 2c | 15→human | Deliver any financial context the human flagged (net-sheet inputs, concession history) | `report.package` (15→human) | delivery on log |

### Phase 3 - Hand off (gated on 2a-2c)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3a | - | Human reviews the assembled evidence and decides whether to adjust | - | human decision recorded |
| 3b | 11→14 | Log the human's decision (adjust / hold / re-review later) against context | `interaction.log` (11→14) | ack |

## HITL gates (hard stops, not judgment calls)
- The playbook states NO recommended price and NO "should reduce" language. Any
  drafted output that does → held before it reaches the human; the assembly is
  evidence, not advice.
- Any pricing question routed in from another party at any point →
  `escalation.legal_line`, never answered by the swarm.
- If the human decides to adjust → this playbook ends and P02 (price adjustment)
  begins on the human's signed change. P23 never crosses into execution.

## Completion criteria (all required)
A market package, an activity summary, and any requested financial context all
delivered to the human, each verified present on the log; the human's decision
recorded. No number produced by the swarm. Anything unverified = not complete.

## Abort paths
- 10 cannot produce comparables (thin market) → deliver what exists, name the
  gap as a gap; the human decides on partial evidence knowingly, never on a
  padded pack.
- Listing goes under contract mid-review → halt; the price conversation is moot;
  P03 takes the context.

## Notes for the Dispatcher
This is an assembly-and-present playbook: its entire output is evidence handed
to the human. It deliberately holds no path that could emit a price to any
party. Phase gates are checked against delivered artifacts, not assurances.
