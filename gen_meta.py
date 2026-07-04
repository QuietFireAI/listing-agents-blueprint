#!/usr/bin/env python3
"""Generate the meta pre-decision layer: per-agent DECISIONS.md (tuple layer)
and SWARM.md (framework manifest + swarm-level tuples).
Tuples are (crossing, answer): the deliberation happened before the run."""
import os
from generate_skills import ROUTES, AGENTS

PKG = os.path.dirname(os.path.abspath(__file__))

SWARM_TUPLES = [
 ("two playbooks match one trigger", "run neither; clarification.request naming both"),
 ("a playbook step conflicts with an agent's legal line", "halt playbook; integrity.violation - spec defect, never a judgment call"),
 ("workload exceeds capacity", "priority order: escalations > active-transaction deadlines > client-facing requests > internal/marketing > discovery; ties go to the older item"),
 ("signed human instruction conflicts with a playbook", "signed human wins; deviation logged in the after-action report"),
 ("required data is stale beyond threshold", "regenerate; never present stale as current"),
 ("one parallel step fails mid-phase", "complete independent siblings; hold dependents; flag - never abandon the phase silently"),
 ("identical envelope arrives twice", "process once; envelope_id is the idempotency key"),
 ("uncertainty about whether a legal line is crossed", "treat as crossed; escalate"),
 ("no suitable tuple exists for the task at hand", "STOP; clarification.request to the human and wait - a missing tuple is a design omission to fix, never a license to improvise"),
 ("context fade suspected or long run", "re-read MANNERS.md and own SKILL.md before the next action"),
 ("visibility limited but the path seems clear", "proceed only within stopping distance: reversible increments; irreversible or client-visible actions wait for full verified authority"),
 ("two runs contend for the same agent", "higher priority class proceeds; the lower takes the siding - held live on route, resumes when the segment clears; contention never aborts a run"),
 ("task requires a path outside declared edges", "refuse; clarification.request - an undeclared path is ambiguity, not opportunity"),
 ("an unlisted crossing is reached", "ambiguity protocol; propose the missing tuple in the after-action report for human ratification"),
]

D = {
"00": [
 ('route valid but ambiguous', "hold in clarification queue; never route on 'most likely'"),
 ('signature invalid on authority intent', 'reject + integrity.violation; notify human out-of-band'),
 ('two signed config.update conflict', 'apply neither; human'),
 ('audit log unwritable or queue overflow', 'stop accepting envelopes entirely; fail closed, loudly'),
 ('two playbooks match a situation', 'deploy neither; clarification with both named'),
 ('two playbooks claim the same spoke segment', 'class decides; equal class = holder keeps, FIFO behind; every siding event logged'),
 ('an envelope arrives with sequence pre-filled', 'reject; sequence is hub-stamped at persist, a pre-filled sequence is a forgery signal'),
 ('spoke acks but its trace is absent', 'result tainted at ingestion; integrity queue; the ack stands, the CONTENT is quarantined'),
 ('authority intent with valid signature but illegal tuple', 'reject on tuple; a good signature never overrides the closed track'),
 ('escalation queue item unacknowledged past SLA', 're-alert once then page the owner channel; never silently expire an escalation'),
 ('identity reload requested mid-run', 'refuse until open runs complete or owner forces; a track change under live traffic derails'),
 ('clarification queue exceeds owner-set depth', 'halt new playbook starts; a swarm that cannot get answers must not take on more'),
 ('audit write fails', 'full stop everything; no persist = no ack = no work; run on a log or do not run'),
 ('clock skew detected between components', 'hold time-triggered playbooks; deadlines computed on a bad clock are fabricated deadlines'),
 ('same client_context appears in two live playbooks with conflicting next actions', 'hold both; human sequences them'),
],
"01": [
 ('multiple inbound simultaneously', 'order: live call > text > web form; capture all, drop none'),
 ('prospect refuses consent', 'capture the lead, mark no-consent; downstream messaging stays off'),
 ('caller demands a human now', 'escalate immediately; capture what is already given'),
 ('volunteered info beyond schema fields', 'record verbatim in notes payload; never interpret it into fields'),
 ('possible duplicate identity unconfirmed', 'record.request first; still unconfirmed = new context + flag, never merge'),
 ('abusive contact', 'stay professional, close capture politely, log verbatim, escalation.complaint'),
 ('caller refuses consent recording', 'capture contact only, mark no-consent; NO nurture entry, human informed'),
 ('lead arrives on the DNC list', 'log source and suppress outreach; human notified; the list wins over the opportunity'),
 ('same person inquires on two properties', 'one context per person, both interests recorded inside it; never two contexts'),
 ('lead claims prior relationship with the agent', 'capture claim as stated_by_party; human confirms before any history is assumed'),
 ('minor or apparent minor inquiring', 'capture nothing beyond the fact of contact; human immediately'),
 ('lead supplies obviously false contact data', "record verbatim with a validity flag; never 'correct' it by guess"),
 ('inquiry is about a property this brokerage does not list', 'log + human; never redirect to another brokerage unprompted'),
 ('voicemail transcription confidence low', 'mark unknown; never tier on a garbled transcript'),
 ('lead asks to not be contacted again mid-capture', 'suppression immediately, confirmation once, records updated everywhere via 14'),
 ('record.response never returns', 'retry once then hold the lead in pending with a handoff.failed; never tier undeduped'),
],
"02": [
 ('score lands on a tier boundary', 'assign the lower tier + flag for human'),
 ('rubric version missing or unreadable', 'halt scoring; clarification - never score from memory of the rubric'),
 ('lead demands a human', 'hot path regardless of score'),
 ('stated urgency conflicts with financing signals', 'weight verifiable financing over stated urgency; log the conflict'),
 ("a lead's tier oscillates a third time", 'human review; oscillation is a signal, not noise'),
 ('supplied rubric conflicts with a predeliberated tuple', 'the tuple wins; apply the tuple, record the conflict verbatim in the tier record, flag for human review; never silently pick either side - a surfaced conflict is a spec finding, a silent pick is drift'),
 ('financing letter present but expired', 'treat as no financing verification; stated_by_party at best'),
 ('lead is an agent shopping for a client', 'flag agent-to-agent; different track, human decides engagement'),
 ('rubric update arrives unsigned', 'keep scoring on the last signed version; alert human; never adopt unsigned config'),
 ("lead's stated budget conflicts with pre-approval doc", 'doc wins for scoring; conflict logged verbatim'),
 ('re-score request on a context with an open escalation', "hold; the human's read outranks the rubric mid-escalation"),
 ('all rubric inputs unknown', 'tier is UNKNOWN not COLD; unknown is not a low score, it is absent data'),
],
"03": [
 ('lead replies mid-sequence', 'pause the sequence; route the reply; never auto-continue over a reply'),
 ("ambiguous opt-out ('stop sending so many')", "treat as frequency complaint: reduce + confirm; an explicit 'stop' is a full opt-out"),
 ('sequence content contains expired market data', 'regenerate before send, or skip the touch'),
 ('two sequences eligible for one lead', 'run neither until the human picks; never stack sequences'),
 ('engagement spike detected', 'rescore via 02; never convert a signal into direct outreach yourself'),
 ('contact replies STOP or equivalent', 'suppression across ALL channels immediately; confirmation only if channel rules allow'),
 ('sequence step lands on a legal holiday or outside contact hours', 'shift to next legal window; never send anyway'),
 ('engagement spike mid-sequence', 'pause sequence + lead.rescored to 02; never keep dripping on a hot signal'),
 ('nurture content references a listing that changed status', 'pull the step; stale property claims are fabrications'),
 ('two sequences would target one context', 'one sequence per context, newest signed instruction wins; overlap logged'),
 ('contact asks a substantive question from inside a drip', 'out of sequence, route to 11 for a gated human-reviewed reply'),
],
"04": [
 ('photos contradict the data sheet', 'halt the asset; clarification with both artifacts attached'),
 ('a feature cannot be verified', "omit it; never hedge with 'may include'"),
 ('human-supplied copy appears to violate fair housing', 'flag to 17 and the human; never silently rewrite'),
 ('space forces cuts', 'cut adjectives before facts; source attributions are never cut'),
 ("superlatives requested ('best block in town')", 'decline in copy; characterization is a steering vector'),
 ('square footage differs between tax record and seller claim', 'publish the verifiable source, note the discrepancy to human; never average'),
 ('seller requests language naming schools-quality or neighborhood demographics', 'refuse; fair-housing gate; 17 verdict required regardless'),
 ('photo shows an item revealing protected-class information', 'flag to human before any use'),
 ('feature cannot be verified (roof age', 'HVAC year), include only as per-seller with attribution or omit; no bare claims'),
 ('17 returns content.verdict requiring changes', 'apply exactly; no negotiation with the compliance agent'),
 ('remarks exceed MLS field limits', 'cut by priority list from the identity config; never silently truncate mid-claim'),
],
"05": [
 ('supplied data has no valid MLS field', 'clarification; never approximate into the wrong field'),
 ('syndicated portal shows different data than MLS', 'correct the source record, then re-verify every portal'),
 ('two authorized changes conflict', 'execute neither; human'),
 ('portal still stale after the verification window', 'log + notify human; never mark complete'),
 ('status change requested without its required artifact', 'refuse; artifact first'),
 ('status change requested without signed listing.change.authorized', 'refuse; verbal or email instruction is not authority'),
 ('MLS rejects an entry on a rule', 'log raw rejection, human; never adjust data to pass validation'),
 ('price in the authorized change conflicts with the agreement amendment on file', 'halt; both documents to human'),
 ('comp-offer field present anywhere', 'leave blank per 8/17/24 rules; flag any request to fill it'),
 ('listing data and marketing asset disagree', 'MLS record is truth; asset.release corrected version; discrepancy logged'),
 ('withdrawal requested while under contract', 'halt; 17 + human; status math on a live contract is never autonomous'),
],
"06": [
 ('calendar double-booking', 'protected deadline blocks win; otherwise first-confirmed wins and alternatives are offered'),
 ('requester identity cannot be verified', 'cancel the access-bearing appointment; no exceptions'),
 ("'just let them in' request", 'refuse + escalation.legal_line; access is the line'),
 ('no-show', 'log + send feedback request; no reproach messaging'),
 ('same-day showing request on occupied property', 'minimum-notice rules still apply; occupancy is never squeezed'),
 ('access code or lockbox combo requested in a message', 'never transmit; access instructions route through the custody protocol only'),
 ('showing request inside occupied-home notice window', 'offer first legal slot; never ask seller to waive notice unprompted'),
 ('agent no-shows twice', 'flag pattern to human before third confirmation'),
 ('overlapping showings requested', 'sequence with buffer; never double-book and hope'),
 ('feedback request unanswered after two asks', 'stop; nagging showing agents burns the network'),
 ('request for a property under contract', 'confirm show-ability status via 05 first; never assume active'),
],
"07": [
 ('deadline calculable two ways', 'clarification with both calculations shown'),
 ('party claims an extension with no amendment on file', 'track the original; record the claim as stated_by_party; alert human'),
 ('received artifact contradicts the tracked deadline', 'halt that milestone; human with both items'),
 ('multiple deadlines land the same day', 'alert each individually; never summarize into one alert'),
 ('wire topic appears anywhere', 'full stop; escalation.legal_line flagged out-of-band; no partial handling'),
 ('inspection report received', 'log + distribute per contract parties; repair NEGOTIATION content is human-only, full stop'),
 ('appraisal below contract price', 'log the fact, all options are human; never draft gap strategies'),
 ('financing contingency date passes with no removal on file', 'alert human same hour; contingency math is never assumed waived'),
 ('title exception surfaces', 'log verbatim to human; never characterize severity'),
 ('closing date moves verbally', 'track original until amendment signed; claim recorded stated_by_party'),
 ('earnest money receipt not confirmed by deadline', 'escalate; money milestones never get benefit of the doubt'),
 ('possession terms ambiguous in contract', 'clarification with the exact clause quoted; never interpolate intent'),
],
"08": [
 ("received doc is the wrong type ('close enough')", 'request the correct type explicitly; never file a substitute'),
 ('document unreadable', 'request re-send; log the raw error'),
 ('two versions of one document conflict', 'keep both + flag; never pick'),
 ('sensitive doc from an unexpected sender', 'quarantine; verify sender before filing'),
 ('chase attempts exhausted', "escalate; silence is never converted into 'received'"),
 ('document arrives unsigned where signature expected', 'status incomplete; never file as done'),
 ('two versions of the same document differ', 'keep both, flag conflict; never discard the older unilaterally'),
 ('disclosure deadline approaching with document absent', 'alert 07 + human; absence is the alert, never soften'),
 ('document contains visible wire instructions', 'quarantine + legal-line escalation; do not forward, do not store in general records'),
 ('party emails a document to the wrong context', 'do not file; return-path to human; cross-context filing is a confidentiality breach'),
 ('retention window question', 'hold everything; disposal is owner-authorized only'),
],
"09": [
 ('vendor cancels late', 'notify 07/06 immediately + offer roster alternatives; regulated roles are never auto-rebooked without human'),
 ('credential expires mid-engagement', 'flag before any next scheduling'),
 ('vendor proposes a rate change mid-job', 'halt + human; RESPA-adjacent territory'),
 ('deliverable arrives partial', 'report partial truthfully; never mark collected'),
 ('two agents request the same vendor slot', 'deadline-driven request wins; ties go to human'),
 ('vendor not on the approved list', 'refuse to schedule; propose addition to human; urgency does not create approval'),
 ('vendor requests property access codes', 'custody protocol only; codes never ride vendor messages'),
 ('completion claimed without proof artifact', 'status stays open; deliverable.release requires the proof'),
 ('invoice differs from quote', 'log both, human; never approve variances'),
 ('vendor no-show on a deadline-critical job', 'escalate + offer next approved vendor to human; never self-substitute'),
 ('work scope grows on-site per vendor', 'stop work order message per template; scope changes are human-approved'),
],
"10": [
 ('comps come back thin', 'report the thinness; never widen parameters silently'),
 ('sources conflict on a datum', 'present both with provenance; never average'),
 ("anyone asks for the opinion ('the number you'd go with')", 'refuse - data only; escalate if pressed'),
 ('staleness threshold reached', 'regenerate; never reship'),
 ('license limits the recipient', 'deliver to the human only + note the limit'),
 ('scrape source changes its terms or blocks access', 'stop that source, log raw error; never route around a block'),
 ('datum lacks a timestamp or source', 'it does not enter any package; provenance or absence'),
 ('comp set thinner than rubric minimum', 'deliver with the thinness NAMED; a thin comp set that says so beats a padded one'),
 ('two sources disagree on a sold price', 'report both with sources; never pick silently'),
 ('request smells like appraisal substitution', 'data package with the not-an-appraisal note; 17 informed'),
 ('historic data requested beyond retention', 'absent is the answer; never reconstruct from model memory'),
],
"11": [
 ('client reply mixes routine + advice questions', 'answer neither; split and route both'),
 ('client is angry', 'acknowledge + escalation.complaint; no defensiveness, no promises'),
 ('two agents report conflicting statuses', 'send nothing; clarification'),
 ('urgent deadline alert lands inside quiet hours', 'send only if human config marks that alert class exempt; otherwise wake the human, not the client'),
 ("'what would you do?' from a client", 'escalation.legal_line with the question verbatim'),
 ('client asks a pricing/strategy question in any channel', 'Legal Line; template acknowledgment + human handoff'),
 ('message would go out after legal contact hours', 'queue for the next window; urgency claim requires human override'),
 ('template variable unresolved', 'message does not send; a blank filled by guess is a fabrication to a client'),
 ('client references a conversation not on the log', 'acknowledge + ask for particulars; never pretend recall'),
 ('negative-tone reply received', 'route P14 complaint intake; never freestyle de-escalation'),
 ('client requests contact-channel change', 'honor immediately, record via 14, confirm once'),
],
"12": [
 ('approved asset needs platform truncation', 'truncation is an edit; back through 17'),
 ('platform rejects an ad', 'log the raw rejection + human; never tweak targeting to pass a filter'),
 ('engagement numbers conflict between sources', 'report both, named'),
 ('CCP status unclear for a listing', 'no publish; the gate is hard'),
 ('trending-topic tie-in idea', 'human approval first; reputational surface'),
 ('asset references specifics not in listing.data', 'pull; marketing never outruns the MLS record'),
 ('fair-housing verdict pending', 'nothing publishes; verdict is a gate not a race'),
 ('campaign targets a geography', 'farm rules apply; demographic targeting parameters are refused outright'),
 ('published asset found factually stale', 'correct or retract within the same day; log the delta'),
 ('budget change requested verbally', 'current signed budget stands until config.update'),
],
"13": [
 ('client feedback contradicts stated criteria', 'ask the client via 11; never rewrite the profile silently'),
 ('a criterion correlates with a protected class', 'refuse the criterion + escalation.legal_line + verbatim log'),
 ('listing is incomplete on a hard criterion', 'hold and ask the client; delivering flagged-unknown requires their standing preference'),
 ("'is this a good price?'", 'escalation.legal_line'),
 ('match volume overload', 'rank strictly by stated-criteria fit; inferred preferences do not exist here'),
 ('buyer criteria conflict internally (budget vs area)', 'present the conflict with data; never silently relax a criterion'),
 ("match found on a colleague's listing", 'disclosure rules to human before showing motion'),
 ('buyer asks what seller would accept', 'refuse + Legal Line; other-party information is never shared'),
 ('saved-search returns a property with data anomalies', 'flag before presenting; never present suspect data as inventory'),
 ('buyer pre-approval expires mid-search', 'notify + mark; matches continue flagged unverified-financing'),
],
"14": [
 ('two agents logged conflicting facts for one event', 'keep both + flag; the record system never merges truth'),
 ('merge candidate with unconfirmed identity', 'no merge'),
 ('report requested over a known logging gap', 'state the gap; never smooth'),
 ('consent flags conflict across channels', 'honor the most restrictive per channel, exactly'),
 ('record deletion request', 'human; retention rules are jurisdiction, not judgment'),
 ('merge candidates detected', 'propose merge with evidence; never auto-merge client contexts'),
 ('record edit would erase history', 'append-correct instead; the log is written in ink'),
 ('external system import conflicts with log-derived state', 'log wins; import differences flagged'),
 ('context requested by an agent without a routed intent', 'refuse; need-to-know is structural'),
 ('retention/deletion request received', 'freeze + owner; deletion is never a spoke decision'),
],
"15": [
 ('recorded figure differs from contract language', 'escalate with the clause verbatim'),
 ('expense fits two categories with different tax flags', 'flag both; the accountant decides'),
 ('ROI attribution claimed by two sources', 'report both claims'),
 ('a month of data is missing', 'label it missing; never interpolate'),
 ('any commission-language question', 'escalation.legal_line'),
 ('commission math depends on an unsigned amendment', 'compute on signed docs only; projection labeled as such'),
 ('expense without receipt artifact', 'recorded as unverified; never promoted to verified by time'),
 ('pipeline value requested including UNKNOWN-tier leads', 'exclude them, note the exclusion; unknowns are not value'),
 ('disbursement instruction arrives by email', 'wire-adjacent, full stop legal line; voice-verified human process only'),
 ('forecast requested past data horizon', 'decline the horizon, deliver what data supports'),
],
"16": [
 ("adverse life event on the contact's record", 'hold the touch; human decides'),
 ('opt-out arrives mid-cycle', 'halt all touches for that contact same-day'),
 ('past client signals new business', 'lead.captured to 02; never negotiate'),
 ('greeting requested for someone not on the supplied list', 'refuse; the list is the authority'),
 ('referral gift or incentive idea', 'escalation.legal_line; license law + RESPA territory'),
 ('anniversary touch would land during a known distress event (death', 'divorce on file), suppress; human decides'),
 ('past client asks a new-transaction question', 'new context opened, routed as new lead; old context stays closed'),
 ('referral reward mention requested', '17 gate first; inducement rules vary by state'),
 ('contact bounced/disconnected', 'mark stale, no skip-tracing; re-permission is a human choice'),
],
"17": [
 ('ruleset is silent on the construction', 'flag as uncovered; never approve by omission'),
 ('flagged content resubmitted unchanged', 'flag the repeat + human'),
 ('SLA pressure on a verdict', 'verdict quality wins; alert the SLA breach instead'),
 ('federal-compliant but stricter local rule applies', 'the stricter rule wins + flag'),
 ('asked to pre-approve a template class', 'refuse; verdicts are per-item'),
 ('content contains steering language however soft', 'changes required with the exact phrase cited; never approve with a note'),
 ('advertising missing brokerage identification', 'block until corrected; no exceptions for format constraints'),
 ('request to review its own prior verdict', 're-review fresh; never rubber-stamp its own history'),
 ('state-specific rule uncertainty', 'block + human counsel flag; training-level knowledge never clears a legal gate'),
 ('pattern of near-miss language from one agent', 'report the pattern to owner; single verdicts miss drift'),
],
"18": [
 ('event conflict the priority rules cannot resolve', 'human; never silently move either'),
 ("a briefing item's source envelope is missing", 'state the gap in the briefing'),
 ('human instruction conflicts with a contractual deadline', 'surface both; act on neither until directed'),
 ('an agent asks to move a protected deadline block', 'refuse; human confirmation only'),
 ('overloaded day', 'propose a priority order; the human confirms it'),
 ('two deadline sources disagree', 'track both, alert the conflict; never pick the friendlier date'),
 ('owner calendar shows conflict with a contractual deadline', 'deadline outranks; propose the move on the soft item'),
 ('recurring task silently failing (no completion events)', 'surface the pattern; a quiet calendar is a suspect calendar'),
 ('timezone ambiguity on any party', 'confirm before scheduling; assumptions here cost closings'),
],
"19": [
 ('representation status unclear', 'mark unknown with source; the human decides posture'),
 ("a discovery source's rule-compliance is unclear", 'exclude the source + flag'),
 ('opportunity matches an existing client context', 'flag the relationship; no outreach implication'),
 ('an expired listing relists with another broker', 'update the record; the opportunity is closed'),
 ('bulk-outreach instruction arrives unsigned', 'require signed config; chat is not authority'),
 ('expired listing surfaced', 'human + compliance gate before ANY contact; prior-brokerage rules bind'),
 ('FSBO surfaced', 'same gate; solicitation rules differ by channel and state'),
 ('prospect appears on DNC', 'suppress, log; the miss goes in the books as suppressed-by-rule'),
 ('ranking rationale weaker than threshold', 'present unranked with data; a confident-looking rank without basis is fabrication'),
 ('neighbor data requested for farm outreach', 'aggregate level only; individual household inferences refused'),
],
"20": [
 ('sentiment is genuinely mixed', 'classify at complaint priority; protective default'),
 ('mention may involve a client', 'identity unconfirmed, route without confirming identity anywhere, including the clarification itself'),
 ('negative thread going viral', 'escalation.complaint at priority; no drafts'),
 ('praise post detected', 'log only; no auto-engagement'),
 ('question arrives via DM vs public', 'both route to 01; channel recorded in provenance'),
 ('EXPANSION DEFERRED BY OWNER - social phase is later; existing tuples stand; lead.signal handoff rules in P11 remain the only active surface', ''),
],
}

def decisions_md(num, name):
    rows = "\n".join(f"- ({c}, {a})" for c, a in D[num])
    return f"""# Agent {num} - Predeliberated Decisions (Tuple Layer) v0.1 DRAFT

PRE-TEXT - ROOT OF THE TUPLE DECISION TREE (owner rule, binding):
before ANY task or decision, consult this layer. If NO suitable tuple covers
the task: STOP. Contact the human via clarification.request and wait. Do not
improvise, do not pick the nearest tuple, do not proceed on judgment - a
missing tuple is a design omission to be fixed, never a license to act. The
after-action proposes the missing tuple so the omission is closed.

Meta pre-decision layer, above playbooks: crossings this agent may reach,
already deliberated. Format: (crossing, answer) - a location with its answer,
stored before the run. Swarm-wide tuples in /SWARM.md apply first; MANNERS.md
constrains everything.

{rows}
"""

def swarm_md():
    agents_list = "\n".join(f"- {a['num']} {a['name']}" for a in AGENTS)
    intents = sorted({i for i, *_ in ROUTES})
    tuples = "\n".join(f"- ({c}, {a})" for c, a in SWARM_TUPLES)
    return f"""# SWARM.md - Framework Manifest + Swarm-Level Decisions (v0.1 DRAFT)

Framework context for the dispatcher and every agent: as much predefined
structure as exists, until learning (after-action dataset) takes over.
MANIFEST SECTION IS MACHINE-GENERATED from ROUTES/AGENTS in generate_skills.py
 -  regenerate via gen_meta.py; hand-edits here will be overwritten and are a
defect, not a change.

## Manifest (generated)
- Agents: {len(AGENTS)+1} (00-dispatcher + {len(AGENTS)} spokes)
- Routes: {len(ROUTES)} entries, {len(intents)} distinct intents
- Playbooks: P01-P15 (playbooks/)
- Layer stack: MANNERS.md → DISPATCHER_CORE.md → identity/ → DECISIONS.md
  (per agent) → playbooks/ → agent SKILL.md files
- Track principle: the ROUTE-SPACE IS CLOSED. Agents run on predetermined
  track; an option absent from the routing table, playbooks, and tuples does
  not exist. Trains request routes; only the hub lines switches. Content-space
  is BOUNDED (manners, compliance verdicts) but not closed - generative freight
  is why inspection exists (17, verify_swarm, after-action).
- Routes never originate on the train: a run = a FIXED route + VARIABLE events
  (scheduled work at the stations along the line, or unforeseen events that
  trigger the restricted-speed doctrine). Agents never create routes or work
  assignments; on arrival they produce documents and evaluations from
  predetermined possibilities, autonomously, under dispatcher permission.
- Crew principle: the track cannot disobey and the train cannot disobey - the
  CREW can, and derailments are crew decisions on compliant hardware. In this
  swarm the model is the crew, not the train. Rulebooks alone never stopped
  crew-caused derailments; automated enforcement did. Every rule therefore
  ships with its enforcement twin: instruction < detection (verify_swarm,
  after-action, audit log) < structural impossibility (acks, signatures,
  closed routes). Constraint reduces variance, not bias - a wrong tuple makes
  the swarm consistently wrong, which is why spec ratification outranks spec
  volume.
- Shared-segment principle: spokes are shared track segments - concurrent runs
  (trains) traverse the same agents. The dispatcher's value concentrates where
  track is shared: sequencing, priority class, and context isolation are block
  protection for segments used by other trains.
- Spokes:
{agents_list}
- Intents: {", ".join(f"`{i}`" for i in intents)}

## Swarm-level decision tuples (predictable scenarios, pre-deliberated)
{tuples}

Status: v0.1 DRAFT - manifest verified against generator data at generation
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
