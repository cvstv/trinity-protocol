# Trinity Protocol

An autonomous multi-agent coordination framework where the repository is the only shared state.

## What This Is

Trinity Protocol is a filesystem-based state machine for coordinating AI agents that
cannot talk to each other. Agents read state from markdown files, act, and write new
state. No central orchestrator, no shared memory, no API calls between agents — just
files, git, and rules.

Three roles. One repo. Zero direct communication.

## How It Works

```
ORCHESTRATOR — plans, dispatches, resolves, chairs councils
ARCHITECT    — reviews, gates merges, owns architectural law
BUILDER      — writes code, runs tests, commits per task
```

The `AGENT-GUIDE.md` contains a **dispatch table** — a set of numbered rules that
determine what happens next based on the current state of the protocol files. A head
agent evaluates rules top-to-bottom. First match fires.

```
INDEX.md shows sprint approved  →  dispatch BUILDER  →  execute sprint on sprint-N branch
INDEX.md shows diff-blocked     →  dispatch BUILDER  →  targeted fix
Blocks >= 3 on one sprint       →  dispatch ORCHESTRATOR  →  council session
ESCALATIONS.md has OPEN entry   →  PAUSE  →  wait for human
Architect approves diff         →  merge sprint-N → main  →  delete branch
```

## The Protocol Files

| File | Purpose |
|------|---------|
| `ACTIVITY.md` | Append-only event log. Every action by every role. |
| `DECISIONS.md` | Architectural law. Technology choices, security invariants, rejected approaches. |
| `INDEX.md` | Sprint coordination table. Status, role, date, block count per sprint. |
| `BLOCKERS.md` | Dead letter queue. Work that hit a stop condition. |
| `ESCALATIONS.md` | Human valve. Pauses the autonomous loop for human decisions. |
| `AGENT-GUIDE.md` | The rule engine. Dispatch table + invariants + bootstrap sequence. |
| `docs/council/` | Council deliberation records. Structured async meetings between roles. |

## How It Runs

The system is **autonomous**. A head agent reads the rule engine, dispatches sub-agents
to the three roles, and the loop runs itself. The human kicks it off and the framework
handles the rest.

The human is only pulled in when the system hits something it can't resolve on its own:
- A sprint blocked 5+ times → mandatory escalation via `ESCALATIONS.md`
- A `[MAJOR]` council decision → requires human approval before execution
- Any role that's genuinely uncertain → writes to `ESCALATIONS.md` and pauses

This isn't a separate "human mode" — it's a safety valve built into the autonomous loop.

## Key Features

- **Autonomous dispatch loop** — head agent reads state, matches rules, dispatches
  sub-agents. No human routing needed for routine work.
- **Human escalation valve** — `ESCALATIONS.md` pauses the loop when decisions exceed
  agent authority. The system asks instead of guessing.
- **Council sessions** — structured 3-round deliberation when the sprint loop can't
  resolve a problem. Auto-triggered at 3+ blocks on one sprint.
- **Epistemic protocol** — agents must verify project state before acting. If uncertain,
  stop and read. Never guess. Never proceed on partial context.
- **Protected main branch** — all work happens on sprint branches. The only path to
  main is through the Architect's merge gate.
- **Block counter** — INDEX.md tracks how many times each sprint has been blocked.
  Thresholds trigger councils (3+) and human escalation (5+).
- **Model-agnostic** — roles are not tied to specific AI models. Assign whatever
  agents you have to whichever roles fit.
- **Git-native** — all state is version-controlled, auditable, and reproducible.

## Getting Started

### Option A: Skill-based setup (recommended)

If using Claude Code (or any agent platform that supports skills):

1. Copy `SKILL.md` to your agent's skill directory (e.g., `~/.claude/skills/trinity-protocol/SKILL.md`)
2. Open a new project directory and run `git init`
3. Invoke the skill (e.g., `/trinity-protocol` in Claude Code)
4. The Architect role runs a conversational foundation session and produces all populated files
5. Hand the repo to your head agent with: "Read `docs/AGENT-GUIDE.md` and begin at R-011"

### Option B: Manual Setup

1. Copy the `templates/` directory contents into your project root
2. Copy `AGENT-GUIDE.md` into `docs/AGENT-GUIDE.md`
3. Populate `DECISIONS.md` with your project's architecture decisions
4. Create milestone plans in `docs/plans/`
5. Assign roles to your available agents in `DECISIONS.md`
6. Hand to your head agent: "Read `docs/AGENT-GUIDE.md`, run bootstrap, begin at R-011"

## Design Principles

- **The repo is the nervous system.** If it's not in a file, it didn't happen.
- **Append-only history.** ACTIVITY.md is event-sourced. Never edit, only append.
- **Invariants are law.** DECISIONS.md constraints override agent judgment.
- **Main is protected.** No role commits directly. Sprint branches only.
- **When uncertain, stop and read.** A wrong action costs more than the tokens spent reading.
- **Escalate, don't guess.** If a decision exceeds authority, write ESCALATIONS.md and pause.

## Project Structure

```
trinity-protocol/
  README.md                              ← you are here
  AGENT-GUIDE.md                         ← canonical rule engine
  SKILL.md                               ← initialization skill (works with Claude Code and compatible platforms)
  FRAMEWORK-DECISIONS.md                 ← meta-decisions about the framework itself
  templates/
    ACTIVITY.md                          ← event log template
    BLOCKERS.md                          ← dead letter queue template
    DECISIONS.md                         ← architecture decisions template
    ESCALATIONS.md                       ← human valve template
    INDEX.md                             ← sprint coordination template
    docs/
      council/
        COUNCIL-TEMPLATE.md              ← council meeting template
        MEETING-LOG.md                   ← council session index template
      sprints/                           ← sprint files go here
      plans/                             ← milestone plan files go here
```

## Origin

Trinity Protocol was developed during the build of a threat intelligence terminal UI
coordinated across three separate AI agents in different IDEs and CLIs.
The framework emerged from the practical need to coordinate agents that couldn't talk
to each other, using only the filesystem as a communication channel.

The core insight: if the repo files are precise enough, they become a complete
communication protocol. Markdown is the medium. Git is the transport.
