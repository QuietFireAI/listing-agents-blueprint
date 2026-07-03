# Agent 00 — Predeliberated Decisions (Tuple Layer) v0.1 DRAFT

Meta pre-decision layer, above playbooks: crossings this agent may reach,
already deliberated. Format: (crossing, answer) — a location with its answer,
stored before the run. Swarm-wide tuples in /SWARM.md apply first; MANNERS.md
constrains everything. An unlisted crossing = ambiguity protocol + propose the
missing tuple via after-action.

- (route valid but ambiguous, hold in clarification queue; never route on 'most likely')
- (signature invalid on authority intent, reject + integrity.violation; notify human out-of-band)
- (two signed config.update conflict, apply neither; human)
- (audit log unwritable or queue overflow, stop accepting envelopes entirely; fail closed, loudly)
- (two playbooks match a situation, deploy neither; clarification with both named)
