#!/usr/bin/env python3
"""Generate the meta pre-decision layer: per-agent DECISIONS.md (tuple layer)
and SWARM.md (framework manifest + swarm-level tuples).
Tuples are (crossing, answer): the deliberation happened before the run."""
import os
from generate_skills import ROUTES, AGENTS

PKG = "/home/claude/listing-agent/package"

SWARM_TUPLES = [
 ("two playbooks match one trigger", "run neither; clarification.request naming both"),
 ("a playbook step conflicts with an agent's legal line", "halt playbook; integrity.violation — spec defect, never a judgment call"),
 ("workload exceeds capacity", "priority order: escalations > active-transaction deadlines > client-facing requests > internal/marketing > discovery; ties go to the older item"),
 ("signed human instruction conflicts with a playbook", "signed human wins; deviation logged in the after-action report"),
 ("required data is stale beyond threshold", "regenerate; never present stale as current"),
 ("one parallel step fails mid-phase", "complete independent siblings; hold dependents; flag — never abandon the phase silently"),
 ("identical envelope arrives twice", "process once; envelope_id is the idempotency key"),
 ("uncertainty about whether a legal line is crossed", "treat as crossed; escalate"),
 ("context fade suspected or long run", "re-read MANNERS.md and own SKILL.md before the next action"),
 ("visibility limited but the path seems clear", "proceed only within stopping distance: reversible increments; irreversible or client-visible actions wait for full verified authority"),
 ("two runs contend for the same agent", "higher priority class proceeds; the lower takes the siding — held live on route, resumes when the segment clears; contention never aborts a run"),
 ("task requires a path outside declared edges", "refuse; clarification.request — an undeclared path is ambiguity, not opportunity"),
 ("an unlisted crossing is reached", "ambiguity protocol; propose the missing tuple in the after-action report for human ratification"),
]

D = {
"00": [("route valid but ambiguous", "hold in clarification queue; never route on 'most likely'"),
 ("signature invalid on authority intent", "reject + integrity.violation; notify human out-of-band"),
 ("two signed config.update conflict", "apply neither; human"),
 ("audit log unwritable or queue overflow", "stop accepting envelopes entirely; fail closed, loudly"),
 ("two playbooks match a situation", "deploy neither; clarification with both named")],
"01": [("multiple inbound simultaneously", "order: live call > text > web form; capture all, drop none"),
 ("prospect refuses consent", "capture the lead, mark no-consent; downstream messaging stays off"),
 ("caller demands a human now", "escalate immediately; capture what is already given"),
 ("volunteered info beyond schema fields", "record verbatim in notes payload; never interpret it into fields"),
 ("possible duplicate identity unconfirmed", "record.request first; still unconfirmed = new context + flag, never merge"),
 ("abusive contact", "stay professional, close capture politely, log verbatim, escalation.complaint")],
"02": [("score lands on a tier boundary", "assign the lower tier + flag for human"),
 ("rubric version missing or unreadable", "halt scoring; clarification — never score from memory of the rubric"),
 ("lead demands a human", "hot path regardless of score"),
 ("stated urgency conflicts with financing signals", "weight verifiable financing over stated urgency; log the conflict"),
 ("a lead's tier oscillates a third time", "human review; oscillation is a signal, not noise")],
"03": [("lead replies mid-sequence", "pause the sequence; route the reply; never auto-continue over a reply"),
 ("ambiguous opt-out ('stop sending so many')", "treat as frequency complaint: reduce + confirm; an explicit 'stop' is a full opt-out"),
 ("sequence content contains expired market data", "regenerate before send, or skip the touch"),
 ("two sequences eligible for one lead", "run neither until the human picks; never stack sequences"),
 ("engagement spike detected", "rescore via 02; never convert a signal into direct outreach yourself")],
"04": [("photos contradict the data sheet", "halt the asset; clarification with both artifacts attached"),
 ("a feature cannot be verified", "omit it; never hedge with 'may include'"),
 ("human-supplied copy appears to violate fair housing", "flag to 17 and the human; never silently rewrite"),
 ("space forces cuts", "cut adjectives before facts; source attributions are never cut"),
 ("superlatives requested ('best block in town')", "decline in copy; characterization is a steering vector")],
"05": [("supplied data has no valid MLS field", "clarification; never approximate into the wrong field"),
 ("syndicated portal shows different data than MLS", "correct the source record, then re-verify every portal"),
 ("two authorized changes conflict", "execute neither; human"),
 ("portal still stale after the verification window", "log + notify human; never mark complete"),
 ("status change requested without its required artifact", "refuse; artifact first")],
"06": [("calendar double-booking", "protected deadline blocks win; otherwise first-confirmed wins and alternatives are offered"),
 ("requester identity cannot be verified", "cancel the access-bearing appointment; no exceptions"),
 ("'just let them in' request", "refuse + escalation.legal_line; access is the line"),
 ("no-show", "log + send feedback request; no reproach messaging"),
 ("same-day showing request on occupied property", "minimum-notice rules still apply; occupancy is never squeezed")],
"07": [("deadline calculable two ways", "clarification with both calculations shown"),
 ("party claims an extension with no amendment on file", "track the original; record the claim as stated_by_party; alert human"),
 ("received artifact contradicts the tracked deadline", "halt that milestone; human with both items"),
 ("multiple deadlines land the same day", "alert each individually; never summarize into one alert"),
 ("wire topic appears anywhere", "full stop; escalation.legal_line flagged out-of-band; no partial handling")],
"08": [("received doc is the wrong type ('close enough')", "request the correct type explicitly; never file a substitute"),
 ("document unreadable", "request re-send; log the raw error"),
 ("two versions of one document conflict", "keep both + flag; never pick"),
 ("sensitive doc from an unexpected sender", "quarantine; verify sender before filing"),
 ("chase attempts exhausted", "escalate; silence is never converted into 'received'")],
"09": [("vendor cancels late", "notify 07/06 immediately + offer roster alternatives; regulated roles are never auto-rebooked without human"),
 ("credential expires mid-engagement", "flag before any next scheduling"),
 ("vendor proposes a rate change mid-job", "halt + human; RESPA-adjacent territory"),
 ("deliverable arrives partial", "report partial truthfully; never mark collected"),
 ("two agents request the same vendor slot", "deadline-driven request wins; ties go to human")],
"10": [("comps come back thin", "report the thinness; never widen parameters silently"),
 ("sources conflict on a datum", "present both with provenance; never average"),
 ("anyone asks for the opinion ('the number you'd go with')", "refuse — data only; escalate if pressed"),
 ("staleness threshold reached", "regenerate; never reship"),
 ("license limits the recipient", "deliver to the human only + note the limit")],
"11": [("client reply mixes routine + advice questions", "answer neither; split and route both"),
 ("client is angry", "acknowledge + escalation.complaint; no defensiveness, no promises"),
 ("two agents report conflicting statuses", "send nothing; clarification"),
 ("urgent deadline alert lands inside quiet hours", "send only if human config marks that alert class exempt; otherwise wake the human, not the client"),
 ("'what would you do?' from a client", "escalation.legal_line with the question verbatim")],
"12": [("approved asset needs platform truncation", "truncation is an edit; back through 17"),
 ("platform rejects an ad", "log the raw rejection + human; never tweak targeting to pass a filter"),
 ("engagement numbers conflict between sources", "report both, named"),
 ("CCP status unclear for a listing", "no publish; the gate is hard"),
 ("trending-topic tie-in idea", "human approval first; reputational surface")],
"13": [("client feedback contradicts stated criteria", "ask the client via 11; never rewrite the profile silently"),
 ("a criterion correlates with a protected class", "refuse the criterion + escalation.legal_line + verbatim log"),
 ("listing is incomplete on a hard criterion", "hold and ask the client; delivering flagged-unknown requires their standing preference"),
 ("'is this a good price?'", "escalation.legal_line"),
 ("match volume overload", "rank strictly by stated-criteria fit; inferred preferences do not exist here")],
"14": [("two agents logged conflicting facts for one event", "keep both + flag; the record system never merges truth"),
 ("merge candidate with unconfirmed identity", "no merge"),
 ("report requested over a known logging gap", "state the gap; never smooth"),
 ("consent flags conflict across channels", "honor the most restrictive per channel, exactly"),
 ("record deletion request", "human; retention rules are jurisdiction, not judgment")],
"15": [("recorded figure differs from contract language", "escalate with the clause verbatim"),
 ("expense fits two categories with different tax flags", "flag both; the accountant decides"),
 ("ROI attribution claimed by two sources", "report both claims"),
 ("a month of data is missing", "label it missing; never interpolate"),
 ("any commission-language question", "escalation.legal_line")],
"16": [("adverse life event on the contact's record", "hold the touch; human decides"),
 ("opt-out arrives mid-cycle", "halt all touches for that contact same-day"),
 ("past client signals new business", "lead.captured to 02; never negotiate"),
 ("greeting requested for someone not on the supplied list", "refuse; the list is the authority"),
 ("referral gift or incentive idea", "escalation.legal_line; license law + RESPA territory")],
"17": [("ruleset is silent on the construction", "flag as uncovered; never approve by omission"),
 ("flagged content resubmitted unchanged", "flag the repeat + human"),
 ("SLA pressure on a verdict", "verdict quality wins; alert the SLA breach instead"),
 ("federal-compliant but stricter local rule applies", "the stricter rule wins + flag"),
 ("asked to pre-approve a template class", "refuse; verdicts are per-item")],
"18": [("event conflict the priority rules cannot resolve", "human; never silently move either"),
 ("a briefing item's source envelope is missing", "state the gap in the briefing"),
 ("human instruction conflicts with a contractual deadline", "surface both; act on neither until directed"),
 ("an agent asks to move a protected deadline block", "refuse; human confirmation only"),
 ("overloaded day", "propose a priority order; the human confirms it")],
"19": [("representation status unclear", "mark unknown with source; the human decides posture"),
 ("a discovery source's rule-compliance is unclear", "exclude the source + flag"),
 ("opportunity matches an existing client context", "flag the relationship; no outreach implication"),
 ("an expired listing relists with another broker", "update the record; the opportunity is closed"),
 ("bulk-outreach instruction arrives unsigned", "require signed config; chat is not authority")],
"20": [("sentiment is genuinely mixed", "classify at complaint priority; protective default"),
 ("mention may involve a client, identity unconfirmed", "route without confirming identity anywhere, including the clarification itself"),
 ("negative thread going viral", "escalation.complaint at priority; no drafts"),
 ("praise post detected", "log only; no auto-engagement"),
 ("question arrives via DM vs public", "both route to 01; channel recorded in provenance")],
}

def decisions_md(num, name):
    rows = "\n".join(f"- ({c}, {a})" for c, a in D[num])
    return f"""# Agent {num} — Predeliberated Decisions (Tuple Layer) v0.1 DRAFT

Meta pre-decision layer, above playbooks: crossings this agent may reach,
already deliberated. Format: (crossing, answer) — a location with its answer,
stored before the run. Swarm-wide tuples in /SWARM.md apply first; MANNERS.md
constrains everything. An unlisted crossing = ambiguity protocol + propose the
missing tuple via after-action.

{rows}
"""

def swarm_md():
    agents_list = "\n".join(f"- {a['num']} {a['name']}" for a in AGENTS)
    intents = sorted({i for i, *_ in ROUTES})
    tuples = "\n".join(f"- ({c}, {a})" for c, a in SWARM_TUPLES)
    return f"""# SWARM.md — Framework Manifest + Swarm-Level Decisions (v0.1 DRAFT)

Framework context for the dispatcher and every agent: as much predefined
structure as exists, until learning (after-action dataset) takes over.
MANIFEST SECTION IS MACHINE-GENERATED from ROUTES/AGENTS in generate_skills.py
— regenerate via gen_meta.py; hand-edits here will be overwritten and are a
defect, not a change.

## Manifest (generated)
- Agents: {len(AGENTS)+1} (00-dispatcher + {len(AGENTS)} spokes)
- Routes: {len(ROUTES)} entries, {len(intents)} distinct intents
- Playbooks: P01–P15 (playbooks/)
- Layer stack: MANNERS.md → DISPATCHER_CORE.md → identity/ → DECISIONS.md
  (per agent) → playbooks/ → agent SKILL.md files
- Track principle: the ROUTE-SPACE IS CLOSED. Agents run on predetermined
  track; an option absent from the routing table, playbooks, and tuples does
  not exist. Trains request routes; only the hub lines switches. Content-space
  is BOUNDED (manners, compliance verdicts) but not closed — generative freight
  is why inspection exists (17, verify_swarm, after-action).
- Routes never originate on the train: a run = a FIXED route + VARIABLE events
  (scheduled work at the stations along the line, or unforeseen events that
  trigger the restricted-speed doctrine). Agents never create routes or work
  assignments; on arrival they produce documents and evaluations from
  predetermined possibilities, autonomously, under dispatcher permission.
- Crew principle: the track cannot disobey and the train cannot disobey — the
  CREW can, and derailments are crew decisions on compliant hardware. In this
  swarm the model is the crew, not the train. Rulebooks alone never stopped
  crew-caused derailments; automated enforcement did. Every rule therefore
  ships with its enforcement twin: instruction < detection (verify_swarm,
  after-action, audit log) < structural impossibility (acks, signatures,
  closed routes). Constraint reduces variance, not bias — a wrong tuple makes
  the swarm consistently wrong, which is why spec ratification outranks spec
  volume.
- Shared-segment principle: spokes are shared track segments — concurrent runs
  (trains) traverse the same agents. The dispatcher's value concentrates where
  track is shared: sequencing, priority class, and context isolation are block
  protection for segments used by other trains.
- Spokes:
{agents_list}
- Intents: {", ".join(f"`{i}`" for i in intents)}

## Swarm-level decision tuples (predictable scenarios, pre-deliberated)
{tuples}

Status: v0.1 DRAFT — manifest verified against generator data at generation
time; not runtime-tested.
"""

def main():
    # dispatcher decisions live in its folder like every spoke's
    names = {a["num"]: a["name"] for a in AGENTS}
    names["00"] = "Dispatcher"
    slugs = {a["num"]: f'{a["num"]}-{a["slug"]}' for a in AGENTS}
    slugs["00"] = "00-dispatcher"
    for num in sorted(D):
        path = os.path.join(PKG, slugs[num], "DECISIONS.md")
        open(path, "w").write(decisions_md(num, names[num]))
    open(os.path.join(PKG, "SWARM.md"), "w").write(swarm_md())
    print(f"wrote {len(D)} DECISIONS.md + SWARM.md")

if __name__ == "__main__":
    main()
