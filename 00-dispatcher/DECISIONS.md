# Agent 00 - Predeliberated Decisions (Tuple Layer) v0.1 DRAFT

Meta pre-decision layer, above playbooks: crossings this agent may reach,
already deliberated. Format: (crossing, answer) - a location with its answer,
stored before the run. Swarm-wide tuples in /SWARM.md apply first; MANNERS.md
constrains everything. An unlisted crossing = ambiguity protocol + propose the
missing tuple via after-action.

- (route valid but ambiguous, hold in clarification queue; never route on 'most likely')
- (signature invalid on authority intent, reject + integrity.violation; notify human out-of-band)
- (two signed config.update conflict, apply neither; human)
- (audit log unwritable or queue overflow, stop accepting envelopes entirely; fail closed, loudly)
- (two playbooks match a situation, deploy neither; clarification with both named)
- (two playbooks claim the same spoke segment, class decides; equal class = holder keeps, FIFO behind; every siding event logged)
- (an envelope arrives with sequence pre-filled, reject; sequence is hub-stamped at persist, a pre-filled sequence is a forgery signal)
- (spoke acks but its trace is absent, result tainted at ingestion; integrity queue; the ack stands, the CONTENT is quarantined)
- (authority intent with valid signature but illegal tuple, reject on tuple; a good signature never overrides the closed track)
- (escalation queue item unacknowledged past SLA, re-alert once then page the owner channel; never silently expire an escalation)
- (identity reload requested mid-run, refuse until open runs complete or owner forces; a track change under live traffic derails)
- (clarification queue exceeds owner-set depth, halt new playbook starts; a swarm that cannot get answers must not take on more)
- (audit write fails, full stop everything; no persist = no ack = no work; run on a log or do not run)
- (clock skew detected between components, hold time-triggered playbooks; deadlines computed on a bad clock are fabricated deadlines)
- (same client_context appears in two live playbooks with conflicting next actions, hold both; human sequences them)
