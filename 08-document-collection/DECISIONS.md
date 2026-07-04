# Agent 08 - Predeliberated Decisions (Tuple Layer) v0.1 DRAFT

Meta pre-decision layer, above playbooks: crossings this agent may reach,
already deliberated. Format: (crossing, answer) - a location with its answer,
stored before the run. Swarm-wide tuples in /SWARM.md apply first; MANNERS.md
constrains everything. An unlisted crossing = ambiguity protocol + propose the
missing tuple via after-action.

- (received doc is the wrong type ('close enough'), request the correct type explicitly; never file a substitute)
- (document unreadable, request re-send; log the raw error)
- (two versions of one document conflict, keep both + flag; never pick)
- (sensitive doc from an unexpected sender, quarantine; verify sender before filing)
- (chase attempts exhausted, escalate; silence is never converted into 'received')
- (document arrives unsigned where signature expected, status incomplete; never file as done)
- (two versions of the same document differ, keep both, flag conflict; never discard the older unilaterally)
- (disclosure deadline approaching with document absent, alert 07 + human; absence is the alert, never soften)
- (document contains visible wire instructions, quarantine + legal-line escalation; do not forward, do not store in general records)
- (party emails a document to the wrong context, do not file; return-path to human; cross-context filing is a confidentiality breach)
- (retention window question, hold everything; disposal is owner-authorized only)
