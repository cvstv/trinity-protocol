---
name: trinity-protocol
description: Use when starting a new project with 2+ AI agents coordinating via repo files — runs a conversational architecture session to produce a fully populated autonomous agent coordination system
---

# Trinity Protocol — Project Initialization

## What You Are Building

You are setting up an **autonomous agent coordination system** — a filesystem-based
state machine where the repo is the only shared brain.

This exists because the agents working on this project **cannot talk to each other.**
They run in separate sessions with no shared context window, no shared memory, and
no API to call each other. The ONLY channel they share is the filesystem.

Every file you create is a node in a distributed coordination protocol:

| File | Protocol role |
|------|--------------|
| `ACTIVITY.md` | Event log — append-only, any agent reconstructs project history from this |
| `DECISIONS.md` | Policy store — architectural law that constrains all future agent actions |
| `docs/plans/*.md` | Roadmap — the complete task breakdown agents will execute against |
| `docs/sprints/INDEX.md` | Coordination table — status, role, date, block count per sprint |
| `BLOCKERS.md` | Dead letter queue — unprocessable work routed here for resolution |
| `ESCALATIONS.md` | Human valve — pauses the autonomous loop for human decisions |
| `docs/AGENT-GUIDE.md` | Runtime protocol — the full rule engine that drives the system |
| `docs/council/MEETING-LOG.md` | Council index — tracks deliberation sessions |

This is Infrastructure as Code for AI orchestration. Markdown is the medium.
Git is the transport. The repo is the nervous system.

## When to Use

- You are in a git-initialized directory (or will run `git init`)
- The human has a project idea (rough or detailed — either works)
- 2+ AI agents with repo access will coordinate work
- The system will run autonomously with a head agent dispatching sub-agents,
  OR a human will manually route prompts between separate agent sessions

**NOT for:** single-agent projects, or agents sharing one conversation window.

## The Three Roles

The Trinity Protocol defines three roles. Roles are **not tied to any specific
model or platform.** The user assigns roles based on their available tools.

<roles>
  <role id="ORCHESTRATOR" level="L3">
    Senior architect, project manager, sprint planner, council chair.
    Responsibilities: strategic planning, scope control, sprint creation, blocker
    resolution, council facilitation, retrospectives.
  </role>
  <role id="ARCHITECT" level="L2">
    Principal engineer, logic refiner, security gate, merge gate.
    Responsibilities: architecture decisions, code review, DECISIONS.md ownership,
    invariant enforcement, diff approval.
  </role>
  <role id="BUILDER" level="L1">
    Implementation specialist, TDD executor, commit author.
    Responsibilities: writing code, running tests, committing per task, precise
    literal execution of sprint specs.
  </role>
</roles>

## The Conversation

This is NOT a template scaffolder. This is a **conversational project foundation session.**

You will have a real conversation with the human to understand their project, then
produce fully populated coordination files — not placeholders. By the end, the repo
is ready for the autonomous loop to begin.

### Phase 1: What is this?

Ask:
- **"What's the project? One or two sentences."**
- **"What should this explicitly NOT be?"** — critical. The "is not" section of
  DECISIONS.md prevents scope creep from day one. Push for specifics.
- **"Who is this for?"** — single user? team? public? Shapes security invariants.

### Phase 2: Technology

Ask:
- **"Tech stack — or is that open for me to recommend?"**
- If they have a stack: **"Why that stack?"** — the reasoning becomes the "Why" field
  in DECISIONS.md.
- If split architecture: **"Where does the boundary live? What crosses it?"**
- **"Any dependencies you want? Any you don't want?"** — pre-populates Rejected Approaches.

### Phase 3: Security and constraints

Ask:
- **"Any hard security or privacy requirements?"**
- **"What's the deployment model?"** — local-only? containerized? cloud?
- **"Anything you've tried before that didn't work?"** — populates Rejected Approaches.

### Phase 4: Scope and milestones

Based on everything above, propose:
- A milestone breakdown (3-6 milestones for a typical project)
- Each milestone: goal in one sentence, approximate task count, key deliverables
- Ask: **"Does this breakdown match how you think about the project?"**

### Phase 5: Agent setup

Ask:
- **"How are you running agents? One head agent with sub-agents? Separate sessions
  you'll route manually? Hybrid?"**
- **"Which agents/models are you using for each role?"**
- Document the answer in DECISIONS.md under Multi-Agent Workflow.

### Adaptive follow-ups

Based on answers, ask domain-specific follow-ups. Examples:
- Database mentioned: "Relational or document? Single-user or concurrent?"
- TUI/GUI mentioned: "Primary interaction model? Keyboard-driven?"
- APIs mentioned: "Which ones? Free tier limits? Auth model?"
- Local-first mentioned: "Where does data live? File permissions?"

**Stop asking when you have enough to write every section of DECISIONS.md without
guessing.** If you're guessing, you're missing a question.

## What to Create

After the conversation, create ALL of the following. Every file is populated with
real project content — no template placeholders, no `[fill this in]` markers.

### 1. `ACTIVITY.md`

Seed with the first entry (the foundation commit you're about to make).
Use the format from the template: `[date] <role>ARCHITECT</role> — <action>Project Foundation</action> — [outcome]`

### 2. `DECISIONS.md`

Populated from the conversation. Required sections — skip none:
- **What This Is (and Is Not)** — from Phase 1
- **Epistemic Protocol** — copy from template (this is universal, not project-specific)
- **Council Trigger Rules** — copy from template (universal)
- **Technology Decisions** — from Phase 2 (each must have Decision, Why, Do not)
- **Security Invariants** — from Phase 3 (each with violation example)
- **Rejected Approaches** — from Phase 2 and 3
- **Accepted Trade-offs** — known limitations, why they're acceptable
- **Multi-Agent Workflow** — from Phase 5 (role-to-agent mapping)

Every decision MUST have a "Do not:" line. If you can't write one, the decision
isn't specific enough — go back and ask.

### 3. `docs/plans/` — Milestone plan files

One file per milestone:
```
docs/plans/[YYYY-MM-DD]-[project]-[milestone-topic].md
```

Each plan: milestone goal, strict sequential task list, each task with exact file
paths, test commands, acceptance criteria. TDD-shaped: write test, implement, verify.

**Critical:** a task must never reference a module that a prior task hasn't created yet.

### 4. `docs/sprints/INDEX.md`

Copy from template. Empty table — the Orchestrator adds the first row when it
creates Sprint 1.

### 5. `BLOCKERS.md`

Copy from template. Empty — the Builder writes the first entry if it hits a stop condition.

### 6. `ESCALATIONS.md`

Copy from template. Empty — the Orchestrator writes the first entry when it needs
human input.

### 7. `docs/council/MEETING-LOG.md`

Copy from template. Empty — the Orchestrator writes the first row when a council is called.

### 8. `docs/AGENT-GUIDE.md`

This is the runtime protocol — the full rule engine that drives the autonomous loop.
Copy from the canonical AGENT-GUIDE.md in the Trinity Protocol repo, then customize:
- Replace all generic paths with the actual project directory name
- Update the role assignment section with the human's Phase 5 answers
- Ensure all rule actions reference the correct project file paths

## After Creating Everything

Commit all files to `main` (this is the only direct commit to main — foundation setup):

```bash
git add ACTIVITY.md DECISIONS.md BLOCKERS.md ESCALATIONS.md \
       docs/plans/ docs/sprints/INDEX.md docs/AGENT-GUIDE.md \
       docs/council/MEETING-LOG.md
git commit -m "docs: project foundation — Trinity Protocol initialized"
```

Then output exactly:

```
Foundation complete.

Next step: Hand to Orchestrator → R-011 (Approve Project Foundation)

The repo is now a live coordination protocol. The AGENT-GUIDE.md rule engine
determines every subsequent action. All future work happens on sprint branches —
main is protected after this commit.
```

## What NOT to Do

- Do not create Sprint 1. That is the Orchestrator's job after approving the foundation.
- Do not scaffold the project structure (directories, dependency files). That is
  the Orchestrator's job after approval.
- Do not leave template placeholders. Every file must have real content.
- Do not skip the "Do not:" line on any DECISIONS.md entry.
- Do not write an AGENT-GUIDE.md with generic paths. Use the actual project name.
- Do not commit directly to main after this foundation commit. All subsequent work
  goes on sprint branches.
- Do not guess. If you're unsure, ask the human.
