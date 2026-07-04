#!/usr/bin/env python3
"""Generate playbooks P02-P15 for the TelsonBase Listing Agent swarm.
P01 is the hand-written approved exemplar and is NOT regenerated here."""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "playbooks")

def build(p):
    s = f'---\nname: {p["num"]}-{p["slug"]}\ndescription: "{p["desc"]}"\n---\n\n'
    s += f'# Playbook {p["num"]} - {p["name"]}\n\n'
    s += "**Swarm:** TelsonBase Listing Agent (Real Estate)\n**Type:** Deployment playbook (consumed by Agent 00 - Dispatcher)\n**Version:** 0.1 (DRAFT - not implemented)\n\n"
    s += "## Trigger\n" + p["trigger"] + "\n\n## Preconditions\n"
    for x in p["pre"]: s += f"- {x}\n"
    s += "Precondition unmet = playbook does not start; `clarification.request` to human.\n\n## Deployment sequence\n"
    for title, rows in p["phases"]:
        s += f"\n### {title}\n| Step | Agent | Action | Intent | Proof of done |\n|---|---|---|---|---|\n"
        for r in rows: s += "| " + " | ".join(r) + " |\n"
    s += "\n## HITL gates (hard stops)\n"
    for g in p["gates"]: s += f"- {g}\n"
    s += "\n## Completion criteria\n" + p["completion"] + "\n\n## Abort paths\n"
    for a in p["abort"]: s += f"- {a}\n"
    if p.get("notes"): s += "\n## Notes for the Dispatcher\n" + p["notes"] + "\n"
    return s

PB = [
dict(num="P02", slug="price-adjustment", name="Price Adjustment",
 desc="Swarm deployment: human-decided price change to updated, re-marketed listing. Agents 04, 05, 10, 11, 12, 17. Use when the human has decided (or is deciding) a list price change.",
 trigger="Human requests decision-support data, or submits a SIGNED `listing.change.authorized` envelope with the new price. The price decision itself is fiduciary and human-only; this playbook surrounds it, never makes it.",
 pre=["Active listing on file (05 record).","For execution phase: signature on the price envelope verified against the registered human key."],
 phases=[("Phase A - Decision support (optional, pre-decision)",[
  ["A1","human→10","Refreshed comp package request","`data.request`","package delivered (`data.package`, `in_reply_to`)"],
  ["A2","10→human","Comp package, data only, no opinion field","`data.package`","ack + provenance complete"]]),
 ("Phase B - Execution (gated on verified signed authorization)",[
  ["B1","05","Execute price change in MLS; live-verify","`listing.change.authorized` (in)","live listing shows new price"],
  ["B2","05","Notify downstream","`status.update`","acks from 11, 12, 14"],
  ["B3","04","Refresh copy if price-referencing assets exist","`content.review` → 17","`content.verdict: approved`"],
  ["B4","12","Re-market with approved assets","`campaign.publish`","publish confirmations"],
  ["B5","11","Seller confirmation of executed change","`client.message.send`","send log"]])],
 gates=["No signature = no execution, no exceptions - a price instruction in chat, email, or an unsigned envelope is not authorization.","Any party asking \"what should the price be\" of any agent → `escalation.legal_line`."],
 completion="New price live-verified on MLS and syndication; downstream acks on file; seller informed; every envelope logged.",
 abort=["Signature verification fails → reject + `integrity.violation`; human notified out-of-band.","Live-verify shows stale price after execution window → halt marketing refresh, escalate."]),

dict(num="P03", slug="under-contract-transition", name="Under-Contract Transition",
 desc="Swarm deployment: accepted offer to transaction-mode operations. Agents 05, 07, 08, 11, 12. Use when an offer is accepted and the listing moves to pending.",
 trigger="Human confirms offer acceptance (executed contract artifact filed via 08).",
 pre=["Executed contract on file (08 verified: opens, matches type).","Contract deadline set extractable for 07's config."],
 phases=[("Phase 1 - Status flip (parallel)",[
  ["1a","05","MLS status → pending, live-verified, within MLS window","`status.update`","live check + acks 11/12/14"],
  ["1b","12","Halt active-marketing; switch to pending/under-contract messaging only if configured","(consumes 1a)","campaign state change logged"]]),
 ("Phase 2 - Transaction kickoff",[
  ["2a","07","Load deadline set per contract template config; open timeline"," - ","timeline record + `interaction.log`"],
  ["2b","07→08","Initial document requirements (earnest receipt, disclosures per contract)","`doc.request`","`doc.status` responses (`in_reply_to`)"],
  ["2c","07","First deadline alerts scheduled","`deadline.alert`","acks from 11, 18"],
  ["2d","11","Client transition message: what happens next, cadence","`client.message.send`","send log"]])],
 gates=["Any contract-language question (deadline calculable two ways, ambiguous contingency) → `escalation.legal_line` - P03 hands ambiguity up, never interprets.","Earnest money handling questions → human (15's trust-accounting exclusion applies swarm-wide)."],
 completion="Pending status live-verified; timeline loaded with every deadline dated; initial doc requests acked; client informed.",
 abort=["Contract artifact fails verification (unreadable, unsigned pages) → halt kickoff, human immediately.","Deal falls through pre-kickoff → human directs status reversal; P05 wind-down does NOT auto-trigger."]),

dict(num="P04", slug="open-house-cycle", name="Open House Cycle",
 desc="Swarm deployment: scheduled open house from promotion through lead capture. Agents 01, 02, 04, 06, 11, 12, 14, 17. Use when human/config schedules an open house.",
 trigger="Open house scheduled (human decision or P01 step 3d).",
 pre=["Listing live (05 status active).","Open-house marketing assets exist or are producible (04)."],
 phases=[("Phase 1 - Promotion (compliance-gated)",[
  ["1a","04→17","Open-house materials review","`content.review`","`content.verdict: approved`"],
  ["1b","12","Promote per CCP-satisfied listing; special-ad-category rules","`campaign.publish`","publish confirmations"],
  ["1c","06","RSVP logistics open; confirmations to registrants","`client.message.request` → 11","RSVP log"]]),
 ("Phase 2 - Event + capture",[
  ["2a","06","Attendance/feedback logistics; access remains licensee-present per legal line","`interaction.log`","event log filed"],
  ["2b","01","Walk-in/registrant capture with consent recording","`lead.captured`","lead objects to 02"],
  ["2c","02","Score and tier new leads; hot → SLA path","`escalation.hot_lead` / `lead.nurture`","tier assignments logged"]])],
 gates=["No agent authorizes access - a licensee or authorized person is physically present, period.","Any pricing question from an attendee → capture the question verbatim, `escalation.legal_line`."],
 completion="Event executed with licensee present; every attendee contact captured with consent status; leads tiered; feedback logged to 14.",
 abort=["Licensee unavailable → event does not proceed; 06 cancels via 11, reschedule to human."]),

dict(num="P05", slug="expired-withdrawn-winddown", name="Expired/Withdrawn Wind-down",
 desc="Swarm deployment: immediate marketing halt and clean wind-down on expired or withdrawn listing. Agents 05, 11, 12, 14. Use when a listing expires or the seller withdraws.",
 trigger="Listing reaches expiration date (07/05 tracked) or seller withdrawal confirmed by human.",
 pre=["Status change authorization: expiration is automatic per listing agreement dates; withdrawal requires human confirmation on file."],
 phases=[("Phase 1 - Halt (immediate, parallel)",[
  ["1a","05","MLS status change, live-verified, within MLS window","`status.update`","live check + acks"],
  ["1b","12","ALL marketing halted on status consumption - ads paused, scheduled posts cancelled","(consumes 1a)","halt confirmations per platform"],
  ["1c","11","Seller communication per human-approved messaging","`client.message.send`","send log"]]),
 ("Phase 2 - Disposition (human decision)",[
  ["2a","14","Context annotated: outcome, reason if stated","`interaction.log`","record updated"],
  ["2b","human","Relist pursuit decision. If pursuing: seller re-enters via standard intake (01→02) - no agent auto-enrolls a former seller into sequences"," - ","human direction logged"]])],
 gates=["Marketing running after status change is a compliance incident, not a cleanup item - 1b failure escalates immediately.","Relist solicitation timing/approach is the human's call entirely."],
 completion="Status live-verified; zero active marketing verified per platform; seller informed; record annotated; human disposition logged.",
 abort=["Seller reverses withdrawal mid-winddown → halt playbook, human direction on state restore."]),

dict(num="P06", slug="new-buyer-onboarding", name="New Buyer Onboarding",
 desc="Swarm deployment: signed buyer agreement to active matched-search. Agents 10, 11, 13, 14. Use when a written buyer agreement is executed. Hard-stops without the agreement.",
 trigger="Signed written buyer agreement filed (08) and recorded (14).",
 pre=["BUYER AGREEMENT GATE: 13 verifies agreement on file via `record.request` before anything else - required before touring, in person or live-virtual (NAR settlement, effective Aug 17, 2024). Absent = full stop, human.","Buyer consent flags recorded (14)."],
 phases=[("Phase 1 - Profile",[
  ["1a","13","Criteria profile from client-stated criteria only, verbatim, `stated_by_party`","`record.request` (verify) + profile record","profile logged; fair-housing-sensitive phrasing → 17"],
  ["1b","13→10","Neighborhood packages for stated areas - sourced figures only, no characterizations","`data.request`","`data.package` (`in_reply_to`)"]]),
 ("Phase 2 - Activation",[
  ["2a","13","Enter listing feed matching (05 `listing.data` standing feed)"," - ","match engine active, logged"],
  ["2b","13","Welcome + first matches delivery","`client.message.request` → 11","send log"],
  ["2c","14","Cadence and consent enforcement live"," - ","record state"]])],
 gates=["No signed agreement = no showing requests ever leave 13 - the flag it sets is what 06 checks.","Any criterion correlating with a protected class → refuse criterion, `escalation.legal_line`, verbatim log.","\"Is this a good price?\" at any point → `escalation.legal_line`."],
 completion="Verified agreement on file; profile live with verbatim criteria; first matches delivered; consent enforced.",
 abort=["Agreement verification fails → stop, human; no partial onboarding."]),

dict(num="P07", slug="tour-day-coordination", name="Tour Day Coordination",
 desc="Swarm deployment: client showing interest to completed, feedback-logged tour. Agents 06, 11, 13, 14, 18. Use when a buyer wants to see one or more properties.",
 trigger="Buyer expresses interest in touring specific properties (via 13 matches or 11 inbound).",
 pre=["Buyer-agreement-on-file flag verified (13 sets it; 06 checks it).","Consent flags permit contact."],
 phases=[("Phase 1 - Sequencing",[
  ["1a","13→06","Showing requests, agreement flag set, per property","`showing.request`","acks"],
  ["1b","06","Seller-availability coordination; identity verification per config; occupied-property notice rules"," - ","confirmed slots"],
  ["1c","06→18","Calendar events, licensee availability confirmed","`calendar.event`","no-conflict confirmation"],
  ["1d","06","Confirmations to all parties","`client.message.request` → 11","send logs"]]),
 ("Phase 2 - Post-tour",[
  ["2a","06","Feedback requests; responses logged","`interaction.log`","feedback in 14"],
  ["2b","13","Profile updates from EXPLICIT client feedback only - never inferred from behavior alone"," - ","profile change log"]])],
 gates=["Access: licensee/authorized presence per 06's legal line - no lockbox codes, ever.","Feedback contradicting stated criteria → ask the client via 11, never silently rewrite the profile."],
 completion="All tours executed or explicitly cancelled; confirmations and feedback logged; profile updated only from explicit statements.",
 abort=["Identity verification fails for any access-bearing appointment → that showing is cancelled, human notified."]),

dict(num="P08", slug="offer-to-acceptance", name="Offer-to-Acceptance",
 desc="Swarm deployment: offer submission through human-negotiated resolution. Agents 07, 08, 11, 18. Thinnest playbook by design - negotiation is entirely human; agents track status and documents around it.",
 trigger="Offer submitted (buyer-side or received on a listing).",
 pre=["Transaction context established (14).","Offer artifact filed and verified (08)."],
 phases=[("Continuous - around the human negotiation",[
  ["1","07","Offer status tracking: submitted / countered / expired / response deadlines","`deadline.alert` → 11, 18","status log current"],
  ["2","07→08","Supporting docs: pre-approval / proof of funds current","`doc.request`","`doc.status` (`in_reply_to`)"],
  ["3","08","Chase missing support docs from parties","`client.message.request` → 11","chase log"],
  ["4","human","ALL negotiation: terms, counters, strategy, acceptance"," - ","human decisions logged as artifacts"],
  ["5","07","On acceptance → trigger P03"," - ","P03 preconditions met"]])],
 gates=["Every negotiation act is human-only - an agent relaying a counter is transport, an agent suggesting one is a violation.","Response-deadline expiry without human action → re-alert, never auto-respond."],
 completion="Offer resolved (accepted → P03, rejected/expired → logged); all status transitions and artifacts on file.",
 abort=["Multiple-offer situation → this playbook continues per offer; presentation order/strategy is human-only."],
 notes="Most steps here say 'the human does this.' That is the legal line working, not a thin spec."),

dict(num="P09", slug="contract-to-close", name="Contract-to-Close",
 desc="Swarm deployment: executed contract through closing day. Agents 07, 08, 09, 11, 18. The densest sequential playbook - deadline-driven, wire-fraud lines active throughout.",
 trigger="P03 completion (transaction kickoff done).",
 pre=["Timeline loaded with full deadline set (07).","Deadline arithmetic config bound to this contract template."],
 phases=[("Continuous - deadline engine",[
  ["1","07","Track every deadline: inspection, appraisal, financing contingency, title, HOA docs, repairs, closing","`deadline.alert` → 11, 18","alerts per config lead-time; 18 blocks protected"],
  ["2","07→08","Milestone documents requested as due","`doc.request`","`doc.status` (`in_reply_to`)"],
  ["3","07→09","Inspector/appraiser scheduling as milestones require","`vendor.request`","`vendor.schedule` confirmations"],
  ["4","09→08","Reports collected, verified present-and-opens","`deliverable.release`","filed by 08"],
  ["5","11","Milestone facts to client - facts, never characterizations","`client.message.send`","send logs"]]),
 ("Closing week",[
  ["6","07","Closing coordination: date, parties, document completeness check via 08","`deadline.alert`","completeness report"],
  ["7","human","Closing representation, signing, all legal acts"," - ","closed"],
  ["8","07","Emit closure → P10 triggers","`transaction.closed`","acks from 16, 14, 15"]])],
 gates=["WIRE FRAUD: no agent sends, confirms, or relays wire instructions - any wire topic in any channel → immediate `escalation.legal_line` flagged out-of-band. Active every step.","Missed or at-risk deadline → escalate with the clause verbatim; never interpret cure options.","Deadline satisfied only by artifact on file - verbal assurance is `stated_by_party`, not satisfaction."],
 completion="Every deadline satisfied-by-artifact or human-resolved; closing executed by human; `transaction.closed` acked by 16, 14, 15.",
 abort=["Contingency failure → human decision path; agents freeze the affected timeline branch, alerts continue on the rest.","Financing collapse → human; no agent communicates deal state to the other side."]),

dict(num="P10", slug="close-postclose-handoff", name="Close + Post-Close Handoff",
 desc="Swarm deployment: closing day to relationship-mode operations. Agents 12, 14, 15, 16. Use on `transaction.closed`.",
 trigger="`transaction.closed` from 07 (P09 step 8).",
 pre=["Closure acked by 16, 14, 15 (P09 completion)."],
 phases=[("Phase 1 - Transition (parallel)",[
  ["1a","16","Post-close program starts: 30/90/365 check-ins scheduled, consent-checked","`client.message.request` → 11 (as due)","schedule logged"],
  ["1b","15","Commission reconciliation opens; records queried from 14","`record.request` → `report.package` (`in_reply_to`)","pending-commission record"],
  ["1c","14","Context state → past-client; date triggers armed","`date.trigger` (ongoing → 16)","record state"],
  ["1d","12","\"Just sold\" marketing - compliance-approved assets, client-consent config respected","`content.review` → 17, then `campaign.publish`","verdict + publish log"]])],
 gates=["Commission figures come from recorded artifacts; a discrepancy with contract language → `escalation.legal_line` with clause verbatim (15's line).","Just-sold publication with identifiable client details requires the consent config to allow it."],
 completion="16's program scheduled; 15's reconciliation record open; 14 in past-client state; just-sold either published post-verdict or explicitly skipped per config.",
 abort=["Post-close dispute arises → 16 touches pause for that context per human direction; 14 annotates."]),

dict(num="P11", slug="speed-to-lead", name="Speed-to-Lead",
 desc="Swarm deployment: inbound contact to tiered, routed lead inside the SLA window. Agents 01, 02, 03, 11, 14, 20. The default always-on intake playbook.",
 trigger="Any inbound: call, form, text (01) or social lead signal (20).",
 pre=["None beyond swarm-up - this playbook is the front door and must not queue behind others."],
 phases=[("Continuous",[
  ["1","20→01","Social questions/lead signals routed to intake","`lead.signal`","ack"],
  ["2","01","Capture with consent recording; CRM dedupe first","`record.request` then `lead.captured`","lead object complete-or-unknown-flagged"],
  ["3","02","Score per human rubric version; tier assigned"," - ","tier + rubric version logged"],
  ["4a","02","HOT → human handoff with SLA re-alert","`escalation.hot_lead`","human acknowledgment inside window"],
  ["4b","02","WARM → nurture entry, consent-gated","`lead.nurture`","03 sequence started"],
  ["5","14","Everything logged; consent flags authoritative","`interaction.log`","records current"]])],
 gates=["Hot-lead SLA breach → re-alert path, never a substitute agent response beyond a holding message via 11.","No consent on file = no outbound sequence, regardless of tier."],
 completion="Per lead: captured with consent state, deduped, tiered with rubric version, routed, logged - inside configured SLA.",
 abort=["Dispatcher degradation → intake fails closed with the swarm; the watchdog covers the clock (core spec)."]),

dict(num="P12", slug="geographic-farm-campaign", name="Geographic Farm Campaign",
 desc="Swarm deployment: human-decided farm campaign in target zips. Agents 03, 10, 12, 17, 19. General marketing only - the Article 16 targeted-solicitation line is enforced structurally.",
 trigger="Human decides to run a farm campaign (zips, budget, duration as config).",
 pre=["Zip list and campaign brief human-approved.","19's discovery sources confirmed MLS-rule-compliant per config."],
 phases=[("Phase 1 - Intelligence",[
  ["1a","19","Zip monitoring active; opportunities to human queue with representation + DNC status fields","`prospect.opportunity`","records with legal-posture fields"],
  ["1b","03→10","Market trend data for update content","`data.request`","`data.package` (`in_reply_to`)"]]),
 ("Phase 2 - Campaign (general only)",[
  ["2a","12→17","Campaign creative review","`content.review`","`content.verdict: approved`"],
  ["2b","12","GENERAL geographic distribution - mailings/ads to the area, not to identified listed owners","`campaign.publish`","publish logs"],
  ["2c","03","Nurture sequences for responders, consent-gated","`lead.nurture` entries via 01→02 intake","sequence logs"]])],
 gates=["Article 16 line, structural: opportunity data (19's expired/FSBO/listed records) NEVER feeds campaign targeting - general marketing is permitted, targeted solicitation of identified exclusively-listed owners is not. Any crossover request → `escalation.legal_line`.","Outreach to any individual from 19's records is a per-target human decision outside this playbook."],
 completion="Campaign published post-verdict to general geography; responders entering standard intake; zero targeting derived from opportunity records - verifiable by audience-parameter logs.",
 abort=["Audience parameters found derived from opportunity data → halt campaign, `integrity.violation`, human review."]),

dict(num="P13", slug="referral-anniversary-cycle", name="Referral/Anniversary Cycle",
 desc="Swarm deployment: date-triggered relationship touches and referral solicitation from the supplied client list. Agents 02, 11, 14, 16. Always-on annuity playbook.",
 trigger="`date.trigger` from 14 (birthday, holiday, purchase/move-in anniversary) or 16's periodic referral cadence.",
 pre=["Contact on the human-supplied list - no list entry, no touch.","Consent/opt-out flags permit."],
 phases=[("Continuous",[
  ["1","14→16","Date triggers per supplied list","`date.trigger`","acks"],
  ["2","16","Greeting/check-in/referral touch composed per cadence; consent-checked","`client.message.request` → 11","send logs"],
  ["3","16","Referral responses and re-engagement signals captured","`lead.captured` → 02","lead objects tiered"],
  ["4","14","All touches logged; opt-outs propagate same-day","`interaction.log`","records current"]])],
 gates=["Adverse-life-event annotation on the contact → touch held, human decides (16's ambiguity rule).","Any incentive/gift for referrals → `escalation.legal_line` - state license law and RESPA territory.","Past client asking values/pricing → hand off with a 10 data package accompanying the HUMAN's answer, never replacing it."],
 completion="Per trigger: touch sent (or held with reason), logged; responses tiered into intake; zero touches against opt-out flags - verifiable from 14's records.",
 abort=["Complaint from a touched contact → P14 takes over for that context; cycle pauses there."]),

dict(num="P14", slug="complaint-response", name="Complaint Response",
 desc="Swarm deployment: detected complaint to human-resolved closure with outbound hold. Agents 11, 14, 17, 20. Entire response is human; agents detect, hold, and document.",
 trigger="20 classifies a complaint (social) or 11 receives one directly.",
 pre=["None - complaints preempt."],
 phases=[("Immediate",[
  ["1","20 or 11","Complaint verbatim + context to priority queue","`escalation.complaint`","human notification per urgency config"],
  ["2","11","Outbound HOLD for that client context - no scheduled touches fire"," - ","hold state logged"],
  ["3","20","Optional DRAFT response attached (labeled, unpublished), compliance-checked","`content.review` → 17","verdict attached to queue item"],
  ["4","human","Entire response: channel, content, resolution"," - ","resolution artifact"],
  ["5","14","Full thread logged; hold released only on human direction","`interaction.log`","context annotated"]])],
 gates=["No agent replies publicly or privately to the complaint - drafting is permitted, sending is human-only.","Complainant with an active transaction → highest urgency; no drafted response at all (20's line).","Never confirm the person's client status in any public channel, including while clarifying."],
 completion="Human resolution logged; hold released by direction; context annotated; if public, the human's response posted by the human.",
 abort=["Complaint reveals a potential legal claim → `escalation.legal_line` supersedes; counsel territory."]),

dict(num="P15", slug="cma-listing-appointment-prep", name="CMA / Listing-Appointment Prep",
 desc="Swarm deployment: listing appointment set to human-ready data package. Agents 10, 18 around a human-presented CMA. The opinion is the human's, always.",
 trigger="Listing appointment scheduled (human).",
 pre=["Subject property parameters supplied by human.","Appointment on calendar (18, human-directed)."],
 phases=[("Prep",[
  ["1","human→10","Comp package: recent sales, actives, expireds per parameters","`data.request`","`data.package` (`in_reply_to`), provenance per datum"],
  ["2","human→10","Neighborhood/market package for the presentation","`data.request`","`data.package`, sourced figures only"],
  ["3","10","Thin-comps honesty: if parameters return too few comps, report thinness - never silently widen"," - ","package notes field"],
  ["4","18","Prep time blocked; materials-ready reminder","`report.package` (briefing)","calendar state"],
  ["5","human","CMA judgment, price opinion, presentation - entirely human"," - "," - "]])],
 gates=["The packages contain no opinion field by schema - a request for \"the number you'd go with\" is the Legal Line, from anyone, including the human's assistant workflows.","Package data goes only to the human under MLS data license; seller-facing use is the human's presentation."],
 completion="Both packages delivered with full provenance and staleness within threshold; thinness reported if applicable; prep time blocked.",
 abort=["Data staleness beyond threshold at appointment time → regenerate; never present expired data as current."]),
]

def main():
    for p in PB:
        d = os.path.join(ROOT, f'{p["num"]}-{p["slug"]}')
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write(build(p))
    print(f"wrote {len(PB)} playbooks (P02-P15); P01 untouched")

if __name__ == "__main__":
    main()

DAILY = [
 {"num":"P16","slug":"morning-operations","name":"Morning Operations",
  "desc":"Swarm deployment: the realtor's morning brief. Calendar, overnight leads, market scrapes, prospect suggestions, and yesterday's books - assembled and presented for human review before the day starts. Agents 10, 14, 15, 18, 19.",
  "trigger":"Scheduled daily start (owner-configured time) or owner command.",
  "pre":["EOD books from previous day exist (P17 completion event on log); if absent, brief runs with the gap NAMED, never silently thinner."],
  "phases":[("Assemble (parallel, all to human review)",[
    ("1","18","Today's calendar, deadlines, time blocks","`report.package`","package on log"),
    ("2","14","Overnight interactions + open leads snapshot","`report.package`","package on log"),
    ("3","10","Owner-configured searches and scrapes: new listings, price changes, comps movement","`data.package`","package on log; every datum carries provenance"),
    ("4","19","Prospect suggestions ranked from yesterday's books + market deltas","`prospect.opportunity`","suggestions on log with reasoning trace"),
    ("5","15","Yesterday's numbers: pipeline value, aging, commission forecast","`report.package`","package on log")]),
   ("Present",[
    ("6","00","Single morning brief assembled from the five packages; NOTHING acted on - presented for human review","-","brief delivered; human review gate OPEN")])],
  "gates":["Every item in the brief is review-only. No client-facing action, no listing action, no send of any kind originates from this playbook.",
           "A scrape datum without provenance does not enter the brief (gate principle)."],
  "completion":"Human has the brief; review verdicts (act / park / discard) recorded via `config.update` or direct command. Completion event logged with brief size and gap flags.",
  "abort":["Any assembling agent unreachable: brief ships with that section marked ABSENT - a thin brief that says so beats a full-looking brief that lies."],
  "notes":"This playbook is why the product exists: the assistant that already read everything before the human's first coffee. One caught deadline or one surfaced expired-relist opportunity pays for the month."},
 {"num":"P17","slug":"end-of-day-books","name":"End-of-Day Books",
  "desc":"Swarm deployment: close the day's books. Every interaction, lead movement, financial delta, and missed-item candidate captured to a dated dataset that feeds tomorrow's P16 brief. Agents 14, 15, 18.",
  "trigger":"Scheduled daily close (owner-configured) or owner command.",
  "pre":["None beyond swarm-up; the books close even on a quiet day - an empty day recorded beats a missing day."],
  "phases":[("Close",[
    ("1","14","Day's interaction log, lead tier movements, oscillation flags","`report.package`","dated dataset on log"),
    ("2","15","Financial deltas: pipeline changes, aging receivables, commission movement","`report.package`","dated dataset on log"),
    ("3","18","Tomorrow's deadlines and unconfirmed appointments; anything unacknowledged today","`report.package`","dated dataset on log"),
    ("4","00","Missed-item sweep: unanswered client messages, stale HOT leads, docs pending past SLA, listings with zero activity - the things a human assistant misses at 6pm","-","missed-item list on log, each with evidence pointer")]),
   ("Book",[
    ("5","00","Dated EOD books object assembled; becomes P16's morning input","-","completion event with books hash")])],
  "gates":["Books are records, not actions - nothing client-facing originates here.",
           "A missed-item entry must carry its evidence pointer (envelope id or log ref); a hunch is not a books entry."],
  "completion":"Dated books object on log with hash; P16 precondition satisfied for tomorrow.",
  "abort":["Any closing agent unreachable: books close with the section marked ABSENT and flagged to the morning brief."],
  "notes":"The books are the memory. The suggestions in tomorrow's brief are only as honest as tonight's close - never rebuild from model memory, only from the log."}]
for p in DAILY:
    path = os.path.join(ROOT, f"{p['num']}-{p['slug']}")
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, "SKILL.md"), "w").write(build(p))
    print("emitted", p["num"])
