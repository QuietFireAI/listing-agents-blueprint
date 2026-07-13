---
name: listing-agents
description: >
  Run a governed real-estate listing assistant swarm: 21 agents on a closed
  35-route track under the dispatcher-agents runtime. Use this skill whenever
  a real-estate workflow needs auditable multi-agent execution - lead capture
  and qualification, listing prep and MLS management, showings, transaction
  coordination, vendor work, client communication, compliance-gated marketing.
  Trigger on: loading the listing identity, routing listing traffic, running
  playbooks P01-P24, or any request for a governed real-estate assistant.
  Money and contract changes move only on signed human authority; fair-housing
  and wire-fraud lines are hard stops, never suggestions.
---

# listing-agents - the identity (dispatcher-agents wearing real estate)

This repo is a SIDE-LOAD, not a runtime: `identity/routes.json` (the closed
track), `identity/priority.json` (JIT classes, ratified), 21 agent folders
each carrying its own SKILL.md role spec, playbooks P01-P24, MANNERS.md
conduct constants (hash-registered at boot), and the deployment kit
(INTEGRATIONS.md, DEPLOY.md, config/).

## Load it

```bash
git clone https://github.com/QuietFireAI/dispatcher-agents
git clone https://github.com/QuietFireAI/listing-agents
cd dispatcher-agents && pip install -e ".[pillars,crypto,dev]"
```

```python
from dispatcher.loader import load_identity
from dispatcher.core import Routes, AuditLog
from dispatcher.hub import Hub

ident = load_identity("../listing-agents")   # 21 agents, 35 routes, warnings []
hub = Hub(Routes(ident.routes_path), AuditLog("audit.jsonl"))
```

Arming the authority tier (signature verifier + signer registry from a
RATIFIED `config/authority_signers.json`) is documented in the runtime's
SKILL.md; the shipped config is an unratified template and the runtime
refuses to arm from it - that refusal is the feature.

## Per-agent skills (Claude, OpenClaw/Codex, Gemini, Copilot, Hermes)

Each numbered folder (00-dispatcher ... 20-social-media-monitoring) is an
Agent Skills-standard SKILL.md. INSTALL.md carries per-platform install
paths and the Hermes governance note (make role specs read-only; agents must
not rewrite their own roles). Role specs give an agent its lane; the swarm
semantics (routing, envelopes, holds, audit) exist only under the runtime.

## Rules for the agent running this skill

- The tuple layer decides before you do: no suitable (from, intent, to)
  tuple = STOP and hold in clarification. Never invent a route.
- Money, commission, contract, and listing-change actions execute only on
  signed human authority - `listing.change.authorized` is the signed lane.
- Fair housing (17's lane), wire-fraud freezes, TCPA/CAN-SPAM consent gates,
  and NAR-settlement rules are hard stops. When in doubt, route to human.
- Every "done" claim must cite verify_swarm output, the runtime suite, or
  the audit log - never memory.

Status: v0.17, ratified 2026-07-10/11 (owner sign-off). PROPRIETARY - see
LICENSE. No licensed legal review; compliance content is training-level.
