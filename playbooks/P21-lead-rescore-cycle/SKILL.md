---
name: P21-lead-rescore-cycle
description: "Swarm deployment: standing re-score of nurtured leads so a warming lead is promoted back into the SLA path before it goes cold. Agents 02, 03, 10, 14, 17. The long-tail companion to P11 - P11 catches the lead, P21 keeps re-reading it."
---

# Playbook P21 - Lead Re-Score Cycle

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Date-driven cadence over the nurture pool (owner-configured interval) or an
owner command. P11 routes a WARM/COLD lead into nurture (`lead.nurture`, 02→03);
P21 is what periodically re-reads that lead instead of letting it sit.

## Preconditions (all verified before the cycle runs)
- The lead already carries a recorded consent state in 14 (P11 established it).
  No consent record = the lead is not touched; `clarification.request` to human.
- A prior tier/score exists on the lead's context. Absent = this is an intake
  case, not a re-score; hand back to P11, do not fabricate a starting tier.

## Deployment sequence

### Phase 1 - Refresh the evidence (parallel, per lead)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 03 | Pull current market/context signals for the lead's area or interest | `data.request` (03→10) | ack |
| 1b | 10 | Return the refreshed data package | `data.package` (10→03) | package on log |
| 1c | 03 | Log the re-score attempt against the lead context | `interaction.log` (03→14) | ack + record ID |

### Phase 2 - Re-score and route (gated on 1b)
GATE: fresh data present. A re-score run against stale data is not a re-score;
if 10 returns no new data, the cycle records "no change" and stops for that lead.
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 03 | Apply the tiering rubric to the refreshed signals | - | new tier computed |
| 2b | 03→02 | Submit the re-score for promotion/demotion decision | `lead.rescored` (03→02) | 02 ack |
| 2c | 02 | Promote to HOT → hand into the SLA path (P11 hot-lead handling); WARM/COLD stays in nurture | - | routing decision logged |

### Phase 3 - Any outbound copy is compliance-gated (only if a touch is authorized)
GATE: this playbook does not itself message the lead - see the tuple note below.
Where a re-score authorizes an outbound *touch*, the drafted copy is reviewed
before it can leave.
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3a | 03→17 | Any drafted re-engagement copy to compliance | `content.review` (03→17) | verdict returned |
| 3b | 17→03 | Verdict | `content.verdict` (17→03) | `approved`, or flag→HITL |

## HITL gates (hard stops, not judgment calls)
- A re-score that crosses into HOT with a legal/complaint signal on the context
  → `escalation.legal_line`, not an automated promotion.
- Any `content.verdict` flag on re-engagement copy → outbound holds until
  licensed review; the re-score itself still stands.
- A consent state that changed to withdrawn since P11 → no touch, no promotion;
  annotate 14 and stop for that lead.

## Completion criteria (all required)
Every lead in the cycle either re-scored with a logged tier decision, or
explicitly recorded as "no change / no data." No lead is left in an unknown
state. Anything unverified = cycle not complete = reported as not complete.

## Abort paths
- 10 unavailable (no data package) → cycle records the gap by name and defers;
  it never re-scores on memory of old data.
- Complaint detected on a lead context → P14 takes over for that context; the
  re-score pauses there.

## Tuple note for the Dispatcher (stated plainly, not worked around)
Agent 03 has NO legal client-messaging tuple on the current 35-route track:
it can re-score (`lead.rescored`), pull data (`data.request`), get copy
reviewed (`content.review`), and log (`interaction.log`) - but it cannot emit
a client message. So P21 is a re-score-and-route loop, not a drip-sender. The
actual client touch is issued by an agent that holds a legal client-message
tuple (11 via a legal requester), after promotion. Closing that gap - a
sanctioned nurture-send path - is a routes change requiring owner ratification,
not something this playbook invents.
