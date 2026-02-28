# 🔺 Trinity Protocol
![Version](https://img.shields.io/badge/version-2.0-blue.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success.svg?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)

An **autonomous multi-agent coordination framework** where the repository is the *only* shared state.

> [!IMPORTANT]
> **If you just got here:** This repo is the framework itself, not a project you edit directly.
> You install one file (`SKILL.md`) into Claude Code, then it uses everything here to set up
> YOUR project with fully populated coordination files. The README below explains how it all works.

## ⬢ What This Is

Three AI agent roles build a project together, coordinating through markdown files
in a git repo. The files aren't a workaround. **They ARE the protocol.** Every decision,
every action, every review is tracked in the repo, creating an accountability trail
that makes the whole system auditable and recoverable.

The files also serve as persistent context. Agents don't carry memory between sessions.
When a new session starts, the agent reads the markdown files and reconstructs the
full project state: what was decided, what happened, what's blocked, what's next.

```text
👑 ORCHESTRATOR   the head agent. Plans sprints, resolves blockers, runs the dispatch loop.
🛡️ ARCHITECT      sub-agent. Reviews plans, reviews code, gates merges, owns DECISIONS.md.
🔨 BUILDER        sub-agent. Writes code via TDD, commits per task, stops when blocked.
```

## ◩ V2 Architecture: The "Signal" and "Actuator" Split

Trinity Protocol V2 operates on a strict split between machine-state and human-nuance:

1. **State variables live in YAML Frontmatter**. (e.g., Block counters, sprint statuses).
2. **Context and nuance live in Markdown bodies**. (e.g., Code reviews, architectural invariants).
3. **Execution is handled by deterministic Python scripts**. (e.g., `trinity-log.py`, `trinity-transition.py`).

By offloading the mechanical work of formatting log files and updating state variables to local Python scripts (`.trinity/bin/`), the AI agents save massive amounts of tokens, preserve their context windows, and execute actions with deterministic speed.

> [!NOTE]
> **Requirements:** Because of the V2 Actuator scripts, the environment running the AI agents MUST have Python installed natively.

All three are engineers. The separation exists for accountability: the entity that
plans doesn't review its own plans, and the entity that writes code doesn't approve
its own diffs.

The head agent (Orchestrator) reads a **dispatch table**, which is a set of numbered
rules that map repo state to actions. It evaluates rules top-to-bottom, first match
fires, and it dispatches the appropriate sub-agent to execute. The project builds itself.

## ⟡ Two-Phase Model

### Phase 1: Setup (Human + Skill)

You run `/trinity-protocol` in Claude Code. It's a conversational session that:

1. Captures your project idea: what it is, what it's NOT, tech stack, constraints
2. Produces fully populated coordination files (not templates, real content)
3. Researches UI design references if your project has a frontend
4. Installs dependencies and scaffolds the project structure
5. Commits the foundation to `main`

By the end, the repo is ready for the autonomous loop.

### Phase 2: Execution (Fully Autonomous)

You give the head agent an initial prompt. It assumes the Orchestrator role, spawns
two sub-agents (Architect and Builder), and runs the dispatch loop:

```
Head agent reads INDEX.md and ESCALATIONS.md
  > matches state against rules in AGENT-GUIDE.md
  > dispatches the appropriate sub-agent
  > sub-agent executes, updates state files
  > loop repeats
```

The human only comes back when the system writes to `ESCALATIONS.md`.

## ⬡ How the Dispatch Table Works

`AGENT-GUIDE.md` contains numbered rules. Each rule has a trigger (repo state),
a dispatch target (which role), and an action. The head agent evaluates top-to-bottom:

```text
ESCALATIONS.md has OPEN entry      >  PAUSE               >  wait for human
INDEX.md shows Blocks >= 5         >  ORCHESTRATOR         >  mandatory human escalation
INDEX.md shows Blocks >= 3         >  ORCHESTRATOR         >  deep analysis of root cause
INDEX.md shows sprint approved     >  BUILDER              >  execute on sprint-N branch
INDEX.md shows sprint complete     >  ARCHITECT            >  review diff, gate merge
INDEX.md shows sprint merged       >  ORCHESTRATOR         >  retrospective, next sprint
```

First match wins. Priority rules (escalations, block thresholds) always check first.

## ▤ All State Lives in Markdown

| File | Purpose |
|------|---------|
| `ACTIVITY.md` | Append-only event log. Every action by every role. |
| `DECISIONS.md` | Architectural law. What was decided, why, and what's forbidden. |
| `INDEX.md` | Sprint status directory. Contains the YAML State Machine heartbeat. |
| `BLOCKERS.md` | Dead letter queue. Work that hit a stop condition. |
| `ESCALATIONS.md` | Human valve. Pauses the loop for human decisions. |
| `AGENT-GUIDE.md` | The dispatch table. The core of everything. |
| `.trinity/bin/*.py`| Deterministic execution scripts. The actuator tools (`trinity-log.py`, `trinity-block.py`, `trinity-transition.py`, `trinity-test.py`). |

Every file serves double duty: it's project documentation AND runtime state for
the agents. There's no separate coordination system. The repo IS the protocol.

## ◒ Setup

### Step 1: Install the initialization skill

```bash
git clone https://github.com/cvstv/trinity-protocol.git
mkdir -p ~/.claude/skills/trinity-protocol
cp trinity-protocol/SKILL.md ~/.claude/skills/trinity-protocol/SKILL.md
```

Restart Claude Code. `/trinity-protocol` will appear as a slash command.

Or tell Claude directly:
> "Read SKILL.md from [path] and copy it to ~/.claude/skills/trinity-protocol/SKILL.md"

### Step 2: Initialize your project

```bash
mkdir my-project && cd my-project && git init
```

Run `/trinity-protocol` in Claude Code. It asks about your project (what it is,
tech stack, security constraints, milestones) then produces fully populated
coordination files and scaffolds the project. No templates. No placeholders.

### Step 3: Hand to the head agent

Open your head agent (any agent with sub-agent capability) and give it:

```text
You are running the Trinity Protocol autonomous loop for this project.

You are the Orchestrator. Spawn two sub-agents:
- One assigned ARCHITECT
- One assigned BUILDER

Read docs/AGENT-GUIDE.md. This is the dispatch table that drives everything.
Run the Session Bootstrap to load project state, then begin executing at R-011
(Approve Project Foundation).

You read state, match rules, dispatch sub-agents. Follow the framework.
```

The head agent takes over. It creates sprints, dispatches sub-agents, reviews
code, and resolves blockers, all autonomously.

## ◪ When You Get Pulled Back In

The system writes to `ESCALATIONS.md` and pauses when it needs you:

- **5+ blocks on a sprint.** Mandatory human escalation. Something systemic is wrong.
- **Orchestrator-Architect disagreement.** They can't agree on a DECISIONS.md change.
  You break the tie.
- **Any role genuinely uncertain.** Escalates instead of guessing.

Read the escalation, write your decision inline, and the loop resumes.

## ◫ The Sprint Lifecycle

```text
Orchestrator creates SPRINT-N.md        >  tasks, acceptance checks, stop conditions
Architect reviews against DECISIONS.md   >  approves or blocks
Builder branches sprint-N from main      >  executes tasks via TDD, commits per task
Builder executes Automated Gates         >  runs trinity-test.py to verify passing tests
Architect reviews test gates and diff    >  approves merge to main, or blocks
Orchestrator writes retrospective        >  flags deferred items and new constraints
> repeat

Failure paths:
  Builder code/tests blocked >  BLOCKERS.md      >  Orchestrator resolves
  Sprint blocked 3+ times    >  Deep Analysis    >  Orchestrator analyzes root cause,
                                                    makes tactical decision
  Sprint blocked 5+ times    >  ESCALATIONS.md   >  Human decides
  DECISIONS.md needs change   >  Decision Protocol > Orchestrator proposes,
                                                    Architect reviews
```

## ◈ Key Concepts

**Autonomous dispatch.** The head agent reads file state and matches rules.
No human routing between agents.

**Epistemic protocol.** Every role must verify project state before acting.
If uncertain, stop and read. Never guess. Never proceed on partial context.

**Protected main.** All work happens on sprint branches. Only the Architect's
merge gate (R-023) can push to main.

**Block counter.** INDEX.md tracks blocks per sprint. 3+ triggers Deep Analysis
(Orchestrator pauses to analyze root cause). 5+ triggers mandatory human escalation.

**Deep Analysis.** When blocks pile up, the Orchestrator stops the sprint loop,
reads all blockers, and analyzes the pattern. It makes a tactical call: rewrite
the sprint, create a hotfix, defer tasks, or continue with justification.

**Decision Protocol.** Changes to DECISIONS.md (architectural law) require
Orchestrator proposal + Architect review. Disagreements escalate to human.
This prevents unilateral erosion of project constraints.

**Design reference.** For projects with a UI, the setup skill researches real
design examples and the human picks a visual direction. This gives the Builder
a concrete target instead of inventing UI design from scratch.

**Model-agnostic.** Roles aren't tied to specific AI models. Use whatever you have.

## ▩ What's in This Repo

```text
trinity-protocol/
  README.md                  you are here
  AGENT-GUIDE.md             the dispatch table (copied into your project by the skill)
  SKILL.md                   the initialization skill (you install this into Claude Code)
  FRAMEWORK-DECISIONS.md     why the framework was designed this way
  templates/
    ACTIVITY.md              event log format
    BLOCKERS.md              dead letter queue format
    DECISIONS.md             architecture decisions format
    ESCALATIONS.md           human valve format
    INDEX.md                 sprint coordination format
    docs/
      sprints/               sprint files go here
      plans/                 milestone plans go here
```

The `templates/` directory contains file formats that the SKILL uses when setting
up your project. You don't need to touch them directly.

## ◧ Origin

Built during a real project: a threat intelligence terminal UI coordinated
across three AI agents. The framework started as manual routing (human
copy-pasting between separate agent sessions) and evolved into fully autonomous
after real-world use showed that manual routing was slow and error-prone.
Autonomous dispatch with the right guardrails (block counters, escalation
thresholds, merge gates) produced better results faster.

Markdown is the medium. Git is the transport. The repo is the protocol.
