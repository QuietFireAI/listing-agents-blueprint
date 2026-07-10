---
name: P24-prospecting-outreach
description: "Swarm deployment: agent 19 surfaces prospecting opportunities (FSBO, expired, farm signals) under a HITL-per-case probation gate. Agents 10, 13, 14, 19 (probation, legal today); adds 11, 17 at graduation (requires ratified tuples). Every case pauses for human validation until the agent has logged reps and its working limits are known."
---

# Playbook P24 - Prospecting Outreach

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-10 - owner sign-off; probation state active, graduation still gated on owner-ratified tuples)

## Two states, one playbook
This playbook has a **probation state (active now, legal on the current
35-route track)** and a **graduation state (inert until owner-ratified
tuples exist)**. It STARTS in probation and stays there until (a) the reps
criterion below is met on the audit log AND (b) the owner has ratified the
graduation tuples. Absent either, the autonomous-outreach phase never runs;
the playbook stops at human hand-off. This is deliberate: cold prospecting
carries the sharpest compliance lines in the swarm (Article 16 targeted
solicitation, DNC, FSBO/expired contact rules), so the agent earns autonomy
by logged reps, it is not granted it.

## Trigger
A prospecting signal for agent 19: a date-driven scrape cadence over the
configured farm/FSBO/expired sources, or an owner command. Sources are config;
this playbook never widens them on its own.

## Preconditions (all verified before any case is surfaced)
- The prospecting source is on the owner-configured allowlist. A source not on
  the list is not scraped; `clarification.request` to human.
- Suppression state is available (DNC / prior-opt-out / do-not-contact records
  in 14). Absent = the case cannot be cleared for any contact; hold.

---

## PROBATION STATE (active now - every step below is legal on the current track)

### Phase P1 - Surface, with evidence (per prospect)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| P1a | 19→10 | Pull supporting data for the prospect (comps, status, days-on-market) | `data.request` (19→10) | ack |
| P1b | 10→19 | Return the data package | `data.package` (10→19) | package on log |
| P1c | 19→14 | Log the surfaced prospect + evidence against a prospect context | `interaction.log` (19→14) | ack + record ID |

### Phase P2 - HITL validation, CASE BY CASE (hard gate, no exceptions in probation)
GATE: **every** surfaced prospect pauses here. The agent does not batch, does
not auto-advance, does not infer approval from silence.
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| P2a | 19→human | Surface the single prospect for human validation with its evidence | `prospect.opportunity` (19→human) | human verdict recorded |
| P2b | - | Human validates this case: approve-for-outreach / reject / needs-more | - | decision logged in 14 |

The human's decision is the rep. Each validated (or rejected) case is one data
point on the agent's working limits: which sources convert, which the human
kills, where the compliance lines actually fall in practice.

### Phase P3 - Route the validated case (no autonomous outreach in probation)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| P3a | 19→13 | If the validated prospect is a buyer-side match, hand to buyer-match | `prospect.opportunity` (19→13) | 13 ack |
| P3b | - | If listing-side, the human runs the touch (or authorizes it) - probation issues no message from the swarm | - | human action logged |

## Reps criterion (measured from the audit log, never self-reported)
Graduation is a COUNT on the log, not a feeling:
- **N = 10 validated cases** with a human verdict and NO compliance flag raised
  on the touch. **N is PROVISIONAL AND ARBITRARY** - no spec number, no
  empirical basis yet - exactly like the hub's loop threshold and MANNERS
  N=10. The after-action data from these first runs sets the real N; until
  then 10 is a placeholder the owner adjusts.
- Reps reset to zero on any compliance flag (a flagged touch means the working
  limits are not yet understood; the agent goes back to earning the count).

---

## GRADUATION STATE (INERT until owner ratifies the tuples below)
When the reps criterion is met AND the owner has ratified the graduation
tuples, the human gate moves from **every case** to **exceptions only**: the
agent may draft and send compliance-reviewed outreach autonomously, with the
human reviewing flags and samples rather than every case. It never reaches
zero HITL.

Graduation steps (**each requires a tuple that is NOT on the current track -
see the ratification proposal; until ratified these steps cannot run**):
| Step | Agent | Action | Intent | Requires ratified tuple |
|---|---|---|---|---|
| G1 | 19→17 | Drafted outreach copy to compliance | `content.review` | **19 as sender of `content.review`** |
| G2 | 17→19 | Verdict back to prospecting | `content.verdict` | **19 as receiver of `content.verdict`** |
| G3 | 19→11 | Approved copy to the client-message path | `client.message.request` | **19 as sender of `client.message.request`** |
| G4 | 11→external | Send | `client.message.send` | (already legal) |

## HITL gates (hard stops, not judgment calls)
- Probation: **every** case is a HITL stop (Phase P2). This is the whole point.
- Any prospect on a suppression/DNC/opt-out list → not surfaced for outreach at
  all; recorded and dropped. No human override of a suppression record.
- Any Article-16 targeted-solicitation concern (contacting a prospect whose
  listing is with another broker) → `escalation.legal_line`, never an
  automated touch, in probation OR graduation.
- Graduation is a two-key action: reps-on-log AND owner ratification. One
  without the other keeps the agent in probation.

## Completion criteria (per run)
Every surfaced prospect either human-validated (approved/rejected) with the
decision logged, or dropped on a suppression record. No prospect left in an
unknown state. In probation, zero autonomous outreach occurred. Anything
unverified = run not complete = reported as not complete.

## Abort paths
- 10 cannot supply evidence → the prospect is surfaced as "evidence-thin" or not
  surfaced at all per config; it is never sent to the human dressed as verified.
- Suppression state unavailable → no case clears; the whole run holds and names
  the gap.
- A compliance flag on any touch → reps reset to zero (see criterion); the agent
  returns to full per-case probation regardless of prior count.

## Notes for the Dispatcher
Probation is the default and the safe state. The graduation phase is written
here so the design is visible and reviewable, but it is inert code until the
owner ratifies the three prospecting tuples. The agent's autonomy is a function
of logged reps, checked against the audit log, never asserted.
