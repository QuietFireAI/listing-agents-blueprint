---
name: P10-close-postclose-handoff
description: "Swarm deployment: closing day to relationship-mode operations. Agents 12, 14, 15, 16. Use on `transaction.closed`."
---

# Playbook P10 - Close + Post-Close Handoff

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
`transaction.closed` from 07 (P09 step 8).

## Preconditions
- Closure acked by 16, 14, 15 (P09 completion).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Transition (parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 16 | Post-close program starts: 30/90/365 check-ins scheduled, consent-checked | `client.message.request` → 11 (as due) | schedule logged |
| 1b | 15 | Commission reconciliation opens; records queried from 14 | `record.request` → `report.package` (`in_reply_to`) | pending-commission record |
| 1c | 14 | Context state → past-client; date triggers armed | `date.trigger` (ongoing → 16) | record state |
| 1d | 12 | "Just sold" marketing - compliance-approved assets, client-consent config respected | `content.review` → 17, then `campaign.publish` | verdict + publish log |

## HITL gates (hard stops)
- Commission figures come from recorded artifacts; a discrepancy with contract language → `escalation.legal_line` with clause verbatim (15's line).
- Just-sold publication with identifiable client details requires the consent config to allow it.

## Completion criteria
16's program scheduled; 15's reconciliation record open; 14 in past-client state; just-sold either published post-verdict or explicitly skipped per config.

## Abort paths
- Post-close dispute arises → 16 touches pause for that context per human direction; 14 annotates.
