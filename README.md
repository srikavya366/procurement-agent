# Procurement Decision Agent

A simple Agentic AI demo built for an MBA classroom setting.

## What it does

Helps a procurement manager evaluate suppliers and decide how to
allocate a purchase order among them, based on real tradeoffs:
price, quality, lead time, delivery reliability (OTIF %), risk, and
capacity.

## Project structure

```
procurement-agent/
├── CLAUDE.md                     # ground rules for the agent
├── README.md                     # this file
├── data/
│   └── suppliers.csv             # supplier dataset (the only source of supplier info)
├── output/                       # agent-generated recommendations/reports land here
└── .claude/
    ├── agents/
    │   ├── cost-analyst.md       # compares unit prices, calculates order cost
    │   ├── performance-analyst.md# compares quality, OTIF %, lead time, capacity
    │   └── risk-analyst.md       # evaluates risk level & concentration risk
    └── commands/
        └── procurement-decision.md  # the Main Procurement Agent (orchestrator)
```

## How it works (multi-agent)

The **Main Procurement Agent** is a slash command that orchestrates
three specialist subagents, each reading only `data/suppliers.csv`:

1. **Cost Analyst** — compares unit prices and calculates procurement
   cost for a proposed allocation, checking supplier capacity.
2. **Performance Analyst** — compares Quality Score, OTIF %, Lead Time
   Days, and Capacity to identify strong/weak suppliers.
3. **Risk Analyst** — evaluates Risk Level and flags supplier
   concentration or single-source risk in a proposed allocation.

The Main Procurement Agent combines all three reports, proposes a
draft order allocation, has it verified by the Cost and Risk Analysts,
saves the recommendation to `output/`, and then **asks the human user
to approve, reject, or request changes** — it never finalizes a
decision on its own.

## Usage

In Claude Code, from inside this project folder, run:

```
/procurement-decision 10000
```

(replace `10000` with your desired total purchase quantity). The
agent will consult the three subagents, propose how to split that
quantity across the 5 suppliers, show the total cost and reasoning,
save the recommendation as a markdown file in `output/`, and wait for
your approval before marking it final.

## Data

`data/suppliers.csv` contains 5 sample suppliers with these columns:

| Column | Meaning |
|---|---|
| Supplier | Supplier name |
| Unit Price | Price per unit ($) |
| Quality Score | Quality rating, 0–10 |
| Lead Time Days | Days to deliver an order |
| OTIF % | On-Time-In-Full delivery rate |
| Risk Level | Low / Medium / High |
| Capacity | Max units the supplier can supply |

The agent is only allowed to use this file for supplier facts — it
must never make up supplier data.

## Status

Working multi-agent demo: run `/procurement-decision <quantity>` to
get a full allocation recommendation with human approval built in.
