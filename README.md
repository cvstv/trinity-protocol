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

## Installation

### Prerequisites

- Git installed and configured
- At least one AI agent with filesystem/repo access (e.g., Claude Code, Cursor,
  Windsurf, Gemini in an IDE, Codex CLI, or any agent that can read/write files)
- For the full trinity: three agents that can each access the same git repo

### Install the Skill (Claude Code)

The fastest way to get started is installing the initialization skill in Claude Code:

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/trinity-protocol.git

# Install the skill
mkdir -p ~/.claude/skills/trinity-protocol
cp trinity-protocol/SKILL.md ~/.claude/skills/trinity-protocol/SKILL.md
```

Restart Claude Code. The `/trinity-protocol` slash command will now appear.

Alternatively, you can just tell Claude Code in conversation:

> "Read the SKILL.md file at [path to your clone]/trinity-protocol/SKILL.md
> and install it as a skill at ~/.claude/skills/trinity-protocol/SKILL.md"

### Install Without Claude Code

If you're not using Claude Code, you don't need the skill file. The skill is just
a conversational helper — everything it produces can be set up manually.

## Getting Started

### Option A: Skill-based setup (recommended)

After installing the skill:

1. Create a new directory for your project and `cd` into it
2. Run `git init`
3. Run `/trinity-protocol` in Claude Code
4. Claude asks you questions about your project (what it is, tech stack, security
   constraints, milestones) and produces fully populated coordination files
5. When it's done, it will tell you:
   ```
   Foundation complete.
   Next step: Hand to Orchestrator → R-011 (Approve Project Foundation)
   ```
6. Open your head agent (whatever you're using as the Orchestrator) and give it:
   ```
   Read docs/AGENT-GUIDE.md in this repo. Run the Session Bootstrap sequence.
   Then execute rule R-011 (Approve Project Foundation).
   ```
7. The autonomous loop takes over from here. The head agent reads state, dispatches
   sub-agents, and the project builds itself.

### Option B: Manual setup (no skill)

1. Copy the `templates/` directory contents into your project root:
   ```bash
   cp -r trinity-protocol/templates/* your-project/
   ```
2. Copy the rule engine into your project:
   ```bash
   cp trinity-protocol/AGENT-GUIDE.md your-project/docs/AGENT-GUIDE.md
   ```
3. Open `DECISIONS.md` and fill in every section with your project's real decisions.
   Every technology decision needs: **Decision**, **Why**, **Do not**.
4. Create milestone plan files in `docs/plans/` with sequential task breakdowns.
5. In `DECISIONS.md` under "Multi-Agent Workflow", document which agents fill which roles.
6. Hand to your head agent:
   ```
   Read docs/AGENT-GUIDE.md in this repo. Run the Session Bootstrap sequence.
   Then execute rule R-011 (Approve Project Foundation).
   ```

### Option C: Head agent with sub-agents (fully autonomous)

If your head agent can spawn sub-agents (e.g., Gemini in Antigravity, or any agent
platform with sub-agent support):

1. Complete Option A or B to create the foundation files
2. Give your head agent this prompt:
   ```
   You are the human-in-the-loop coordinator for this project.

   You have 3 sub-agents available. Assign each one a role from the framework:
   - The Orchestrator
   - The Architect
   - The Builder

   Read docs/AGENT-GUIDE.md. This is the rule engine that drives the entire
   project. Run the Session Bootstrap to understand current state, then begin
   executing the dispatch table starting at the appropriate rule.

   You decide the sequence. Follow the framework.
   ```
3. The head agent reads the rule engine, dispatches sub-agents, and runs the loop.
   You'll only be pulled in via `ESCALATIONS.md` when the system needs a human decision.

## What Happens During a Project

Once the framework is running, here's what the lifecycle looks like:

```
1. Orchestrator creates SPRINT-N.md with tasks, acceptance checks, stop conditions
2. Architect reviews the sprint against DECISIONS.md — approves or blocks
3. Builder creates sprint-N branch, executes tasks via TDD, commits per task
4. Architect reviews the diff — approves merge to main, or requests fixes
5. Orchestrator writes a retrospective — flags deferred items and new constraints
6. Repeat from step 1

If something goes wrong:
- Builder hits a stop condition → writes BLOCKERS.md → Orchestrator resolves
- Sprint blocked 3+ times → Orchestrator evaluates calling a Council session
- Sprint blocked 5+ times → mandatory human escalation via ESCALATIONS.md
- Council produces [MAJOR] decision → human must approve before execution
```

## Reading the Rule Engine

The `AGENT-GUIDE.md` dispatch table uses this format:

```xml
<rule id="R-022">
  <trigger>INDEX.md shows sprint N with status = "approved"</trigger>
  <dispatch>BUILDER</dispatch>
  <action>Execute each task in order using TDD...</action>
  <completion>INDEX.md: status → "in-progress", then "complete" or "builder-blocked"</completion>
  <next>If complete → R-023. If blocked → R-026.</next>
</rule>
```

- **trigger** — what state must be true for this rule to fire
- **dispatch** — which role executes this rule
- **action** — what the role does
- **completion** — what files to update when done
- **next** — which rule fires after this one

Rules are evaluated top-to-bottom. First match wins. Priority rules (R-000 through
R-003) are always checked first — these handle escalations, block thresholds, and
active councils.

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
  AGENT-GUIDE.md                         ← canonical rule engine (the core of everything)
  SKILL.md                               ← initialization skill for Claude Code
  FRAMEWORK-DECISIONS.md                 ← meta-decisions about the framework itself
  templates/
    ACTIVITY.md                          ← event log template
    BLOCKERS.md                          ← dead letter queue template
    DECISIONS.md                         ← architecture decisions template (includes Epistemic Protocol)
    ESCALATIONS.md                       ← human valve template
    INDEX.md                             ← sprint coordination template (includes block counter)
    docs/
      council/
        COUNCIL-TEMPLATE.md              ← 3-round council meeting template
        MEETING-LOG.md                   ← council session index template
      sprints/                           ← sprint files created here by Orchestrator
      plans/                             ← milestone plan files created here by Architect
```

## Origin

Trinity Protocol was developed during the build of a threat intelligence terminal UI
coordinated across three separate AI agents in different IDEs and CLIs.
The framework emerged from the practical need to coordinate agents that couldn't talk
to each other, using only the filesystem as a communication channel.

The core insight: if the repo files are precise enough, they become a complete
communication protocol. Markdown is the medium. Git is the transport.
