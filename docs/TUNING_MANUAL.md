# TUNING_MANUAL - listing-agents-blueprint (STUB)

This blueprint carries the ratified SPEC (SKILL.mds, DECISIONS tuples,
routes, generators); the operational tunables live with the working
build. **Authoritative manual:** listing-agents `docs/TUNING_MANUAL.md`
(TOP OF LIST first - every placeholder and ratified threshold).

Binding rules this repo enforces on itself:
- Config edits go to BOTH repos in the same change (both-repos rule,
  found and fixed 2026-07-17/18) - a config that drifts between
  blueprint and build is the named defect class.
- Docs generated here (JOB_DESCRIPTIONS, PLAYBOOKS) regenerate from
  these sources only; hand-edits in the working repo are drift.
Nothing in this repo is separately tunable beyond that.
