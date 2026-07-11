---
name: P13-referral-anniversary-cycle
description: "Swarm deployment: date-triggered relationship touches and referral solicitation from the supplied client list. Agents 02, 11, 14, 16. Always-on annuity playbook."
---

# Playbook P13 - Referral/Anniversary Cycle

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (ratified 2026-07-11 - owner sign-off; not runtime-hardened)

## Trigger
`date.trigger` from 14 (birthday, holiday, purchase/move-in anniversary) or 16's periodic referral cadence.

## Preconditions
- Contact on the human-supplied list - no list entry, no touch.
- Consent/opt-out flags permit.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Continuous
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1 | 14→16 | Date triggers per supplied list | `date.trigger` | acks |
| 2 | 16 | Greeting/check-in/referral touch composed per cadence; consent-checked | `client.message.request` → 11 | send logs |
| 3 | 16 | Referral responses and re-engagement signals captured | `lead.captured` → 02 | lead objects tiered |
| 4 | 14 | All touches logged; opt-outs propagate same-day | `interaction.log` | records current |

## HITL gates (hard stops)
- Adverse-life-event annotation on the contact → touch held, human decides (16's ambiguity rule).
- Any incentive/gift for referrals → `escalation.legal_line` - state license law and RESPA territory.
- Past client asking values/pricing → hand off with a 10 data package accompanying the HUMAN's answer, never replacing it.

## Completion criteria
Per trigger: touch sent (or held with reason), logged; responses tiered into intake; zero touches against opt-out flags - verifiable from 14's records.

## Abort paths
- Complaint from a touched contact → P14 takes over for that context; cycle pauses there.
