---
name: P01-new-listing-onboarding
description: "Swarm deployment playbook: signed listing agreement to live, marketed listing. Deploys agents 04, 05, 06, 09, 11, 12, 13, 14, 17, 18 in three gated phases. Use when a new listing agreement is executed and the human authorizes go-to-market."
---

# Playbook P01 - New Listing Onboarding

**Swarm:** TelsonBase Listing Agent (Real Estate)
**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)
**Version:** 0.1 (DRAFT - not implemented)

## Trigger
Signed listing agreement executed and human submits the authorized listing
package (property data + list price) as a SIGNED `listing.change.authorized`
envelope. Price is the human's fiduciary decision made before this playbook
starts; no step below produces or modifies it.

## Preconditions (all verified before Phase 1)
- Signed listing agreement artifact on file (08/14 record confirmed).
- Signature on the listing package verified against the registered human key.
- Seller `client_context_id` established with consent flags recorded (14).
Precondition unmet = playbook does not start; `clarification.request` to human.

## Deployment sequence

### Phase 1 - Setup (parallel)
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 1a | 14 | Establish/confirm client context, log agreement | `interaction.log` | ack + record ID |
| 1b | 09 | Order photography / staging / cleaning per config | `vendor.request` | vendor confirmations |
| 1c | 18 | Calendar blocks: shoot, prep, go-live target | `calendar.event` | ack |
| 1d | 11 | Seller onboarding message + comms cadence (consent-checked) | `client.message.request` → `client.message.send` | send log |

### Phase 2 - Production (gated on 1b deliverables)
GATE: photos delivered, verified present-and-opens by 09.
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 2a | 09→05 | Photo deliverables to MLS agent | `deliverable.release` | 05 receipt ack |
| 2b | 05→04 | Property data package to description agent | `listing.data` | ack |
| 2c | 04 | Draft MLS description, captions, flyer, tour script | - | drafts complete |
| 2d | 04→17 | All assets to compliance | `content.review` | verdict returned |
| 2e | 17→04 | Verdict | `content.verdict` | `approved`, or flag→HITL |
| 2f | 04→05, 04→12 | Release approved assets | `asset.release` | acks |

### Phase 3 - Go-live (gated on 2f + MLS entry)
GATE: 05 completes MLS entry and verifies the LIVE listing (live-check, not
push log), then emits `status.update` (active) to 11, 12, 14.
| Step | Agent | Action | Intent | Proof of done |
|---|---|---|---|---|
| 3a | 05 | Syndication to portals, live-verified | - | live listing checks |
| 3b | 12 | Launch campaign - CLEAR COOPERATION GATE satisfied by 3a's `status.update`; housing special-ad-category rules | `campaign.publish` | publish confirmations |
| 3c | 05→13 | Listing into buyer-match feeds | `listing.data` | ack |
| 3d | 06 | Open house scheduling if configured | `calendar.event` | confirmations |
| 3e | 11 | "Your listing is live" + links to seller | `client.message.request` | send log |

## HITL gates (hard stops, not judgment calls)
- Any `content.verdict: flagged` (2e) → marketing path halts until licensed review.
- Any pricing question from any party at any step → `escalation.legal_line`.
- Photos reveal property-data conflicts (04's ambiguity rule) → human.
- Exempt-status marketing (office exclusive / delayed marketing) → requires the
  signed seller disclosure on file BEFORE any 12 activity; otherwise 3b waits
  for 3a. No exceptions; local MLS rules are config.

## Completion criteria (all required)
MLS live-verified; syndication live-verified; campaign published post-verdict;
seller informed; every step's envelope acked and logged. Anything unverified =
playbook not complete = reported as not complete.

## Abort paths
- Seller withdraws pre-live → halt all phases, 12 publishes nothing, 05 per
  human direction, 11 confirms to seller, context annotated in 14.
- Compliance flag unresolved > SLA → marketing stays halted; MLS entry proceeds
  only on explicit human direction (listing without marketing is human's call).
- Vendor failure (1b) → 09 flags, human decides reshoot/replace; Phase 2 waits.

## Notes for the Dispatcher
Steps within a phase run parallel unless a Proof-of-done of one is another's
input. Phase gates are checked against artifacts, not assurances. This playbook
never routes around a spoke's own legal line - it sequences them.
