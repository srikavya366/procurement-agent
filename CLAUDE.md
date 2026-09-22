# Procurement Decision Agent

## What this project is

A simple Agentic AI demo for an MBA classroom. The agent acts as a
procurement decision assistant: it evaluates suppliers and recommends
how a purchase order should be allocated among them.

## Ground rules for the agent

1. **Data source of truth**: `data/suppliers.csv` is the ONLY source of
   supplier information. The agent must never invent, assume, or
   hallucinate supplier data (prices, quality, lead time, OTIF %, risk,
   capacity). If information needed to answer a question isn't in the
   CSV, the agent must say so instead of guessing.
2. **Simplicity first**: this is a teaching example, not production
   software. No web app, no database, no complicated UI. Plain files
   and plain reasoning that a classroom can follow step by step.
3. **Transparency**: when recommending an allocation, the agent should
   show its reasoning (which columns/criteria drove the decision) so
   students can see how the "agent" weighed tradeoffs like price vs.
   quality vs. risk vs. lead time.
4. **Outputs**: any recommendation, comparison, or report the agent
   produces should be saved into `output/` (e.g. as a `.md` or `.csv`
   file), so each run leaves a reviewable artifact.

5. **Human in the loop**: the Main Procurement Agent only ever
   recommends — it never finalizes. Every saved recommendation carries
   a permanent `Status: HUMAN APPROVAL REQUIRED` marker that the agent
   itself never changes to "APPROVED," no matter what the user says in
   chat. The agent presents the recommendation, asks the user to
   approve, reject, or request changes, and records their response as
   a decision-log entry underneath that status line — the actual
   procurement decision remains the human procurement manager's call,
   made outside the agent.

## Multi-agent architecture

- **Main Procurement Agent** (`.claude/commands/procurement-decision.md`,
  run as `/procurement-decision <quantity>`) — orchestrator. Takes a
  purchase quantity, consults the three specialist subagents, drafts an
  allocation, has it verified, saves it to `output/`, and requires
  human approval before treating it as final.
- **cost-analyst** (`.claude/agents/cost-analyst.md`) — compares unit
  prices and calculates procurement cost for a given allocation.
- **performance-analyst** (`.claude/agents/performance-analyst.md`) —
  compares Quality Score, OTIF %, Lead Time Days, and Capacity.
- **risk-analyst** (`.claude/agents/risk-analyst.md`) — evaluates Risk
  Level and flags supplier concentration/single-source risk in a
  proposed allocation.

Each subagent reads only `data/suppliers.csv` and reports facts/math —
none of them decide the final allocation; that's the Main Procurement
Agent's job, synthesizing all three reports.

## Project structure

- `data/suppliers.csv` — supplier dataset (Supplier, Unit Price,
  Quality Score, Lead Time Days, OTIF %, Risk Level, Capacity)
- `output/` — where the agent writes its recommendations/reports
- `.claude/agents/` — the three specialist subagents
- `.claude/commands/procurement-decision.md` — the Main Procurement
  Agent (slash command)
- `README.md` — project overview and how to use it

## Status

Working multi-agent demo. Run `/procurement-decision <quantity>` in
Claude Code inside this project to get an allocation recommendation.
