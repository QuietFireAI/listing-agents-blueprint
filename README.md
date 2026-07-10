# listing-agents - real-estate listing vertical for the DispatcherAgents runtime

An **identity side-load**: everything vertical-specific for a 21-agent
real-estate listing swarm, loadable into the content-neutral
[dispatcher-agents](https://github.com/QuietFireAI/dispatcher-agents) runtime.
The runtime never contains vertical text; this repo never contains transport
code. That split is the architecture.


## What this is for

A digital partner for a working realtor: part chatbot, part executor.
Morning brief assembled before the first coffee (calendar, overnight leads,
owner-configured market scrapes presented for review, prospect suggestions
reasoned from yesterday's books, the numbers). End-of-day books that close
the day and feed tomorrow's suggestions - including the missed-item sweep
that catches what a human assistant misses: the unanswered message, the
stale HOT lead, the doc past SLA, the listing with zero activity. One saved
listing or one caught deadline covers months of cost. Standardized client
engagement, lower labor cost, fewer inconsistencies - with hard review
gates: nothing client-facing moves without the human, and fiduciary
territory escalates immediately (the Legal Line). The full cycle:
DAILY_OPERATIONS.md; playbooks P16 (morning) and P17 (books); P18 seller
weekly report, P19 access custody, P20 vacant-property watch. Coverage map:
TASK_INVENTORY.md - every non-social task/decision domain, mapped to its
owning agent and playbook. Decision layer: 227 predeliberated tuples across
21 agents, rooted in the owner's pre-text rule - no suitable tuple = STOP,
human clarification; a missing tuple is a design omission, never agent
discretion.

## What's here

- **21 agent dirs (`00`-`20`)** - SKILL.md (open Agent Skills standard) +
  DECISIONS.md per agent. 00 is the dispatcher spec; 01-20 are spokes
  (lead capture, qualification, nurture, MLS management, showings,
  transaction coordination, compliance/fair-housing, CRM, etc.).
- **24 playbooks (`playbooks/P01-P24`)** - gated multi-agent sequences
  (P01 new-listing onboarding, P11 speed-to-lead, P14 incident containment,
  P16/P17 daily ops, P21 lead re-score, P22 buyer-feedback match refresh,
  P23 price-review evidence…).
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
