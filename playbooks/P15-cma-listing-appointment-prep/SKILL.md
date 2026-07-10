---
name: P15-cma-listing-appointment-prep
description: "Swarm deployment: listing appointment set to human-ready data package. Agents 10, 18 around a human-presented CMA. The opinion is the human's, always."
---

# Playbook P15 - CMA / Listing-Appointment Prep

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-10 - owner sign-off)

## Trigger
Listing appointment scheduled (human).

## Preconditions
- Subject property parameters supplied by human.
- Appointment on calendar (18, human-directed).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Prep
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | human→10 | Comp package: recent sales, actives, expireds per parameters | `data.request` | `data.package` (`in_reply_to`), provenance per datum |
| 2 | human→10 | Neighborhood/market package for the presentation | `data.request` | `data.package`, sourced figures only |
| 3 | 10 | Thin-comps honesty: if parameters return too few comps, report thinness - never silently widen |  -  | package notes field |
| 4 | 18 | Prep time blocked; materials-ready reminder | `report.package` (briefing) | calendar state |
| 5 | human | CMA judgment, price opinion, presentation - entirely human |  -  |  -  |

## HITL gates (hard stops)
- The packages contain no opinion field by schema - a request for "the number you'd go with" is the Legal Line, from anyone, including the human's assistant workflows.
- Package data goes only to the human under MLS data license; seller-facing use is the human's presentation.

## Completion criteria
Both packages delivered with full provenance and staleness within threshold; thinness reported if applicable; prep time blocked.

## Abort paths
- Data staleness beyond threshold at appointment time → regenerate; never present expired data as current.
