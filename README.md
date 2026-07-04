# listing-agents - real-estate listing vertical for the DispatcherAgents runtime

An **identity side-load**: everything vertical-specific for a 21-agent
real-estate listing swarm, loadable into the content-neutral
[dispatcher-agents](https://github.com/QuietFireAI/dispatcher-agents) runtime.
The runtime never contains vertical text; this repo never contains transport
code. That split is the architecture.

## What's here

- **21 agent dirs (`00`-`20`)** - SKILL.md (open Agent Skills standard) +
  DECISIONS.md per agent. 00 is the dispatcher spec; 01-20 are spokes
  (lead capture, qualification, nurture, MLS management, showings,
  transaction coordination, compliance/fair-housing, CRM, etc.).
- **15 playbooks (`playbooks/P01-P15`)** - gated multi-agent sequences
  (P01 new-listing onboarding, P11 speed-to-lead, P14 incident containment…).
- **`identity/routes.json`** - the closed track: 35 ratified
  (sender → intent → receiver) tuples. The runtime enforces these at send
  time; an unlisted tuple does not move.
- **`identity/priority.json`** - JIT priority classes per playbook
  (ratified 07/2026, adjustable), consumed by the runtime's siding scheduler.
- **`MANNERS.md`** - 14 conduct constants + the re-injection anti-fade
  mechanism (constant triggers; N=10 backstop PROVISIONAL pending
  after-action data). Its hash is registered at boot attestation.
- **`DISPATCHER_CORE.md`** - doctrine the runtime implements; status section
  states exactly what is and isn't runtime-tested.
- **`SWARM.md`, `ROSTER.md`, `AFTER_ACTION.md`, `INSTALL.md`,
  `verify_swarm.py`, generators** - manifest, report schema, build-time
  tuple verification (the runtime enforces the same tuples live).

## Compliance encoded (training-level, not legal advice)

NAR settlement buyer-agreement requirements, Clear Cooperation MLS filing,
compensation-offer prohibition, Article 16, wire-fraud hard lines,
TCPA/CAN-SPAM consent gating, RESPA referral lines. **Reviewed by no
licensed attorney. Verify against current local rules before use.**

## Use

```
git clone https://github.com/QuietFireAI/dispatcher-agents
git clone https://github.com/QuietFireAI/listing-agents
cd dispatcher-agents && pip install -e .
IDENTITY_DIR=../listing-agents python3 demo/run_p11_demo.py
```

First of several verticals. Status: v0.17; owner density review of P02-P15
pending. MIT - [QuietFireAI](https://github.com/QuietFireAI).

## License

Proprietary - commercial licenses available from QuietFireAI. See LICENSE.
