---
name: P12-geographic-farm-campaign
description: "Swarm deployment: human-decided farm campaign in target zips. Agents 03, 10, 12, 17, 19. General marketing only - the Article 16 targeted-solicitation line is enforced structurally."
---

# Playbook P12 - Geographic Farm Campaign

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Human decides to run a farm campaign (zips, budget, duration as config).

## Preconditions
- Zip list and campaign brief human-approved.
- 19's discovery sources confirmed MLS-rule-compliant per config.
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Intelligence
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 19 | Zip monitoring active; opportunities to human queue with representation + DNC status fields | `prospect.opportunity` | records with legal-posture fields |
| 1b | 03→10 | Market trend data for update content | `data.request` | `data.package` (`in_reply_to`) |

### Phase 2 - Campaign (general only)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 12→17 | Campaign creative review | `content.review` | `content.verdict: approved` |
| 2b | 12 | GENERAL geographic distribution - mailings/ads to the area, not to identified listed owners | `campaign.publish` | publish logs |
| 2c | 03 | Nurture sequences for responders, consent-gated | `lead.nurture` entries via 01→02 intake | sequence logs |

## HITL gates (hard stops)
- Article 16 line, structural: opportunity data (19's expired/FSBO/listed records) NEVER feeds campaign targeting - general marketing is permitted, targeted solicitation of identified exclusively-listed owners is not. Any crossover request → `escalation.legal_line`.
- Outreach to any individual from 19's records is a per-target human decision outside this playbook.

## Completion criteria
Campaign published post-verdict to general geography; responders entering standard intake; zero targeting derived from opportunity records - verifiable by audience-parameter logs.

## Abort paths
- Audience parameters found derived from opportunity data → halt campaign, `integrity.violation`, human review.
