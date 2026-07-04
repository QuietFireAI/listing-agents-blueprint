---
name: P06-new-buyer-onboarding
description: "Swarm deployment: signed buyer agreement to active matched-search. Agents 10, 11, 13, 14. Use when a written buyer agreement is executed. Hard-stops without the agreement."
---

# Playbook P06 - New Buyer Onboarding

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Signed written buyer agreement filed (08) and recorded (14).

## Preconditions
- BUYER AGREEMENT GATE: 13 verifies agreement on file via `record.request` before anything else - required before touring, in person or live-virtual (NAR settlement, effective Aug 17, 2024). Absent = full stop, human.
- Buyer consent flags recorded (14).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Profile
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 13 | Criteria profile from client-stated criteria only, verbatim, `stated_by_party` | `record.request` (verify) + profile record | profile logged; fair-housing-sensitive phrasing → 17 |
| 1b | 13→10 | Neighborhood packages for stated areas - sourced figures only, no characterizations | `data.request` | `data.package` (`in_reply_to`) |

### Phase 2 - Activation
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 13 | Enter listing feed matching (05 `listing.data` standing feed) |  -  | match engine active, logged |
| 2b | 13 | Welcome + first matches delivery | `client.message.request` → 11 | send log |
| 2c | 14 | Cadence and consent enforcement live |  -  | record state |

## HITL gates (hard stops)
- No signed agreement = no showing requests ever leave 13 - the flag it sets is what 06 checks.
- Any criterion correlating with a protected class → refuse criterion, `escalation.legal_line`, verbatim log.
- "Is this a good price?" at any point → `escalation.legal_line`.

## Completion criteria
Verified agreement on file; profile live with verbatim criteria; first matches delivered; consent enforced.

## Abort paths
- Agreement verification fails → stop, human; no partial onboarding.
