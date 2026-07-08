---
name: P22-buyer-feedback-match-refresh
description: "Swarm deployment: turn post-tour feedback into a refreshed buyer match set and the next round of showings. Agents 06, 10, 11, 13, 14. The iterative loop that P07 (single tour day) feeds into."
---

# Playbook P22 - Buyer Feedback & Match Refresh

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
A completed tour with logged feedback (P07 completion), or an owner command to
re-run a buyer's match. P07 coordinates one tour day; P22 is what closes the
loop - feedback in, a sharper match set and next showings out.

## Preconditions (all verified before Phase 1)
- An active written buyer agreement on file (P06 established it). Absent =
  hard stop, same line as P06; `clarification.request` to human. No match work
  proceeds for an unrepresented buyer.
- Tour feedback exists for this buyer context (06 logged it). Absent = there is
  nothing to refine on; hand back to P07, do not invent preferences.

## Deployment sequence

### Phase 1 - Capture the signal (parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 06→11 | Route the buyer's own words/feedback back toward the client thread | `client.message.request` (06→11) | send log |
| 1b | 06→14 | Log structured feedback against the buyer context | `interaction.log` (06→14) | ack + record ID |
| 1c | 13→14 | Pull the buyer's current criteria record | `record.request` (13→14) | ack |
| 1d | 14→13 | Return the criteria record | `record.response` (14→13) | record on log |

### Phase 2 - Refresh the match (gated on 1b + 1d)
GATE: both the new feedback and the stored criteria are present. Re-matching on
one without the other is a partial match; hold and name the missing side.
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 13→10 | Request fresh inventory/comps against the adjusted criteria | `data.request` (13→10) | ack |
| 2b | 10→13 | Return the data package | `data.package` (10→13) | package on log |
| 2c | 13 | Recompute the match set from feedback-adjusted criteria | - | new match set |
| 2d | 13→14 | Log the refreshed match set and criteria delta | `interaction.log` (13→14) | ack |

### Phase 3 - Present and schedule (gated on 2c)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3a | 13→17 | Any buyer-facing match commentary to compliance (fair-housing steering line) | `content.review` (13→17) | verdict returned |
| 3b | 17→13 | Verdict | `content.verdict` (17→13) | `approved`, or flag→HITL |
| 3c | 13→11 | Approved match set toward the buyer | `client.message.request` (13→11) | send log |
| 3d | 11 | Deliver to the buyer | `client.message.send` (11→external) | send confirmation |
| 3e | 13→06 | Request showings for the buyer-selected subset | `showing.request` (13→06) | 06 ack |

## HITL gates (hard stops, not judgment calls)
- Any `content.verdict` flag - especially a fair-housing / steering concern on
  match commentary (17's line) → outbound holds until licensed review.
- Feedback that reads as a discriminatory preference → 17 line first; the swarm
  never encodes it into criteria. Straight to human.
- Buyer signals intent to write an offer → this loop ends; P08 takes over.

## Completion criteria (all required)
Feedback logged; criteria delta recorded; refreshed match set produced and
compliance-cleared; buyer informed; next showings requested or explicitly
declined. Every envelope acked and logged. Anything unverified = not complete.

## Abort paths
- 10 returns no new inventory → present "no new matches this cycle" plainly;
  do not pad the set with stale or off-criteria listings.
- Buyer agreement lapses mid-loop → halt; represented-buyer precondition fails;
  human directs renewal before any further match work.

## Notes for the Dispatcher
Steps within a phase run parallel unless one's Proof-of-done is another's input
(2a needs 1d's criteria; 3c needs 3b's verdict). The match is recomputed from
recorded feedback, never from the swarm's memory of the tour.
