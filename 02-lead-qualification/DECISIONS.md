# Agent 02 - Predeliberated Decisions (Tuple Layer) v0.1 DRAFT

Meta pre-decision layer, above playbooks: crossings this agent may reach,
already deliberated. Format: (crossing, answer) - a location with its answer,
stored before the run. Swarm-wide tuples in /SWARM.md apply first; MANNERS.md
constrains everything. An unlisted crossing = ambiguity protocol + propose the
missing tuple via after-action.

- (score lands on a tier boundary, assign the lower tier + flag for human)
- (rubric version missing or unreadable, halt scoring; clarification - never score from memory of the rubric)
- (lead demands a human, hot path regardless of score)
- (stated urgency conflicts with financing signals, weight verifiable financing over stated urgency; log the conflict)
- (a lead's tier oscillates a third time, human review; oscillation is a signal, not noise)
- (supplied rubric conflicts with a predeliberated tuple, the tuple wins; apply the tuple, record the conflict verbatim in the tier record, flag for human review; never silently pick either side - a surfaced conflict is a spec finding, a silent pick is drift)
- (financing letter present but expired, treat as no financing verification; stated_by_party at best)
- (lead is an agent shopping for a client, flag agent-to-agent; different track, human decides engagement)
- (rubric update arrives unsigned, keep scoring on the last signed version; alert human; never adopt unsigned config)
- (lead's stated budget conflicts with pre-approval doc, doc wins for scoring; conflict logged verbatim)
- (re-score request on a context with an open escalation, hold; the human's read outranks the rubric mid-escalation)
- (all rubric inputs unknown, tier is UNKNOWN not COLD; unknown is not a low score, it is absent data)
