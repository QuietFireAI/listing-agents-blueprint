# TelsonBase Listing Agent — Swarm Roster v0.1 (DRAFT)

21 agents, hub-and-spoke via 00. Changes from the original 18-agent breakdown:

| # | Agent | Origin |
|---|---|---|
| 00 | Dispatcher | ADDED — hub, escalation queues, audit log, fail-closed |
| 01 | Lead Capture | original |
| 02 | Lead Qualification | original |
| 03 | Lead Nurture | original |
| 04 | Listing Description | original (boundary with 12 defined) |
| 05 | MLS & Listing Management | original |
| 06 | Showing Scheduler | original |
| 07 | Transaction Coordinator | EXTENDED — scope now starts at offer submission |
| 08 | Document Collection | original (boundary with 07 defined) |
| 09 | Vendor Coordination | original |
| 10 | Market Data | MERGED — former CMA Data + Neighborhood & Market Research |
| 11 | Client Communication | original |
| 12 | Marketing Campaign | original (distributes 04's assets, never rewrites) |
| 13 | Buyer Search & Match | ADDED — buyer-side gap; anti-steering rules |
| 14 | CRM & Pipeline | original (now emits date triggers; 16 executes greetings) |
| 15 | Financial Tracking | original |
| 16 | After-Close & Referral | MERGED — former After-Close Nurture + requested Referral Agent (~60% overlap eliminated; all requested referral/greeting functions present) |
| 17 | Compliance & Fair Housing | original (mandatory pre-publish hop for 03/04/12/13/20) |
| 18 | Calendar & Task Management | original |
| 19 | Prospecting | ADDED per request — zip-code monitoring; value-add: expired/FSBO flagging; zero autonomous outreach |
| 20 | Social Media Monitoring | ADDED per request — monitor/classify/route; zero autonomous public replies |

Swarm-standard blocks (byte-identical across 01–20): topology, message envelope,
handoff rules, confidentiality, ambiguity protocol, anti-fabrication, failure &
logging. Generated from generate_skills.py — edit the generator, not the files,
until the protocol stabilizes.
