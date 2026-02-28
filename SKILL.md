---
name: trinity-protocol
description: Use when starting a new project requiring autonomous AI coordination, or returning to an existing Trinity Protocol project to plan improvements. Runs a conversational session to produce fully populated coordination files for a V2 autonomous agent system where a head agent orchestrates sub-agents via repo files.
---

# Trinity Protocol: Project Initialization & Re-Entry

## What You Are Building

You are setting up an **autonomous agent coordination system**, a filesystem-based
state machine where the repo is the only shared brain.

The agents coordinate through the filesystem **by design**, not as a workaround,
but because files create the accountability trail. Every action is logged, every
decision is documented, every review is tracked. The repo is the single source of
truth that makes the system auditable, recoverable, and transparent.

Every file you create is a node in a distributed coordination protocol:

| File | Protocol role |
|------|--------------|
| `ACTIVITY.md` | Event log — append-only, any agent reconstructs project history from this |
| `DECISIONS.md` | Policy store — architectural law that constrains all future agent actions |
| `docs/plans/*.md` | Roadmap — the complete task breakdown agents will execute against |
| `docs/sprints/INDEX.md` | Coordination table — contains the YAML state machine (status, blocks, role) |
| `BLOCKERS.md` | Dead letter queue — unprocessable work routed here for resolution |
| `ESCALATIONS.md` | Human valve — pauses the autonomous loop for human decisions |
| `docs/AGENT-GUIDE.md` | Runtime protocol — the full rule engine that drives the system |
| `.trinity/bin/*` | Actuators — Python scripts that safely parse and update the YAML state |

This is Infrastructure as Code for AI orchestration. Markdown is the medium.
Git is the transport. The repo is the nervous system. The shell is the actuator.

## When to Use

- You are in a git-initialized directory (or will run `git init`)
- The human has a project idea (rough or detailed, either works)
- The user has a head agent capable of spawning and orchestrating sub-agents (e.g., Claude Code, advanced IDE agents).
- The system will run fully autonomously with the head agent dispatching sub-agents.
- **OR:** The project already has Trinity coordination files and the human wants to
  iterate — add features, fix issues, or improve what exists.

**NOT for:** single-agent projects, or manual copy-pasting between chat windows. This is a V2 Autonomous-only framework.

## Path Detection

Before starting any conversation, determine which path to take:

1. **New project** — No coordination files exist. Run the full Foundation conversation
   (Phases 1-8 below).
2. **Existing project, inject protocol** — Code exists but no Trinity files. Run the
   Foundation conversation adapted for existing code.
3. **Re-entry** — Trinity coordination files already exist (DECISIONS.md, ACTIVITY.md,
   INDEX.md, AGENT-GUIDE.md, `.trinity/bin/`). Skip the Foundation entirely and jump
   to the **Re-Entry** section at the bottom of this document.

Detection is conversational, not automated. Ask the human what they're here for if
it's not obvious from context.

## The Three Roles

The Trinity Protocol defines three roles. Roles are **not tied to any specific
model or platform.** In this framework, the head agent assumes Orchestrator, and spawns the sub-agents.

<roles>
  <role id="ORCHESTRATOR" level="L3">
    Senior architect, sprint planner, decision protocol authority. This is the
    head agent role. Responsibilities: strategic planning, scope control, sprint
    creation, blocker resolution, deep analysis, retrospectives.
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
produce fully populated coordination files, not placeholders. By the end, the repo
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

Explain the autonomous model:
- **"This framework runs fully autonomously. Your head agent becomes the Orchestrator
  and spawns two sub-agents: one Architect, one Builder."**
- **"Which AI platform and model will run the head agent?"** — document in DECISIONS.md.
- **"Does your platform support sub-agents / tool use?"** — if not, explain that
  sub-agent capability is a hard requirement. The framework cannot be used manually.
- Document the Orchestrator/Architect/Builder agent models in DECISIONS.md under Multi-Agent Workflow.

### Phase 6: UI design research (if applicable)

If the project includes a frontend, UI, dashboard, or any visual interface:

- Research real UI examples, dashboards, and design systems that match the project's
  domain and visual style. Use web search to find concrete references.
- Present 3-4 options to the human with descriptions of each design's strengths:
  layout approach, color scheme, component style, interaction patterns.
- **"Which of these matches the look and feel you want? Or a combination?"**
- Document the human's choice in DECISIONS.md under a **"Design Reference"** section
  with: the selected reference(s), what specifically to emulate (layout, typography,
  color palette, component style), and what NOT to copy.
- This gives the Builder a concrete visual target during autonomous execution
  instead of guessing at UI design.

**Skip this phase** if the project has no visual interface (CLI-only, backend service,
library, etc.).

### Phase 7: Install dependencies and scaffold

Based on the technology decisions from Phase 2:
- Install required dependencies (`npm init`, `pip install`, `cargo init`, etc.)
- Create the project directory structure matching the milestone plans
- Set up any config files, CI skeleton, or tooling the project needs
- Verify all tools and dependencies are available and working

### Phase 8: Scaffold internal python actuators

Create the `.trinity/bin/` directory to house the V2 actuator scripts:
- `mkdir -p .trinity/bin`
- Copy the 4 python scripts from the Trinity framework repo (`trinity-log.py`, `trinity-block.py`, `trinity-transition.py`, `trinity-test.py`) into `.trinity/bin/`. (e.g., fetching from GitHub raw URLs or copying from the cloned repo).
- Ensure they have execution permissions: `chmod +x .trinity/bin/*.py`. 
- **Explain to the user:** "These scripts handle all YAML frontmatter state changes. Agents are forbidden from manually editing the YAML blocks to prevent corruption."

Commit the scaffold to `main` before creating the coordination files.
This handles R-012/R-013 during setup so the autonomous loop can begin
directly at sprint planning.

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
- **Decision Protocol** — copy from template (universal)
- **Technology Decisions** — from Phase 2 (each must have Decision, Why, Do not)
- **Security Invariants** — from Phase 3 (each with violation example)
- **Rejected Approaches** — from Phase 2 and 3
- **Accepted Trade-offs** — known limitations, why they're acceptable
- **Design Reference** — from Phase 6 (if project has a UI — selected design direction)
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

Copy from template. Ensure it contains the strict YAML frontmatter block for the state machine:
```yaml
---
sprint_status: none
blocks: 0
active_role: ORCHESTRATOR
tests_passing: true
---
```
Empty table body — the Orchestrator adds the first row when it creates Sprint 1.

### 5. `BLOCKERS.md`

Copy from template. Empty — the Builder writes the first entry if it hits a stop condition.

### 6. `ESCALATIONS.md`

Copy from template. Empty — the Orchestrator writes the first entry when it needs
human input.

### 7. `.trinity/bin/` — Execution Handlers
Ensure the 4 `.py` actuator scripts are present in this directory and executable. These scripts must be used by the protocol agents to manipulate the YAML state.

### 8. `docs/AGENT-GUIDE.md`

This is the runtime protocol — the full rule engine that drives the autonomous loop.
Copy from the canonical AGENT-GUIDE.md in the Trinity Protocol repo, then customize:
- Replace all generic paths with the actual project directory name
- Ensure all rule actions reference the correct project file paths

## After Creating Everything

Commit all files to `main` (this is the only direct commit to main — foundation setup):

```bash
git add ACTIVITY.md DECISIONS.md BLOCKERS.md ESCALATIONS.md \
       docs/plans/ docs/sprints/INDEX.md docs/AGENT-GUIDE.md .trinity/bin/
git commit -m "docs: project foundation — Trinity Protocol initialized"
```

Then output exactly:

```
Foundation complete.

The repo is now a live coordination protocol. Start your head agent and give it
this prompt:

---
You are running the Trinity Protocol autonomous loop for this project.

You are the Orchestrator. Spawn two sub-agents:
- One assigned ARCHITECT
- One assigned BUILDER

Read docs/AGENT-GUIDE.md — this is the dispatch table that drives everything.
Run the Session Bootstrap to load project state, then begin executing at R-011
(Approve Project Foundation).

**CRITICAL RULE:** Never manually edit the YAML frontmatter in `INDEX.md`. You MUST use the Python actuator scripts in `.trinity/bin/` for all state changes and logging. Failure to do so will corrupt the protocol state.

You read state → match rules → dispatch sub-agents. Follow the framework.
---

All future work happens on sprint branches — main is protected after this commit.
```

---

## Re-Entry: Iterating on an Existing Project

This section activates when the project already has Trinity coordination files.
The human is coming back to improve, extend, or fix what the autonomous loop built.

This is the same conversational approach as Foundation — ask questions, understand
what the human wants, then produce real plans. But the starting point is a working
project, not a blank repo.

### R-Phase 1: Project health check

Read the project state before asking anything:

1. Read `ACTIVITY.md` — full history (or last 30 entries if very long)
2. Read `docs/sprints/INDEX.md` — sprint completion status and YAML state
3. Read `DECISIONS.md` — current architectural constraints
4. Read `BLOCKERS.md` — any unresolved blockers
5. Read `ESCALATIONS.md` — any unresolved escalations
6. List the source code structure (`ls` or `find` on the source directories)

Then present a brief summary based on what you find:

- **All sprints done:** "Here's where the project stands — all N milestones complete,
  X total tasks done. The app currently does [functional summary]."
- **Mid-sprint:** "Looks like you're mid-sprint — Sprint N is active with X of Y tasks
  done. What's going on — want to finish this sprint or change direction?"
- **Open blockers:** "There are N unresolved blockers. Let's deal with those before
  planning new work."
- **Open escalations:** "There are open escalations waiting for your input. Let's
  resolve those first."

Adapt to whatever state you find. Don't assume all sprints are done.

### R-Phase 2: What worked and what didn't

Ask:
- **"What's working well? What are you happy with?"**
- **"What's broken, annoying, or missing?"** — these become the next milestones
- **"Anything the agents got wrong that needs fixing?"** — bad patterns, wrong
  architecture, things that should be refactored
- **"Any new features you want to add?"**
- **"Has anything changed about who this is for or how you use it?"** — scope
  changes affect DECISIONS.md

### R-Phase 3: Prioritize improvements

Based on answers, categorize into:
- **Bugs/fixes** — things that are broken (highest priority)
- **Quality improvements** — refactoring, better error handling, performance
- **New features** — additions to scope
- **Polish** — UX, visual, documentation

Propose a prioritized milestone plan:
- **"Here's what I'd tackle in order:"** — with reasoning for the sequence
- Each milestone: goal in one sentence, approximate task count, key deliverables
- Ask: **"Does this priority order make sense? Anything you'd move up or down?"**

### R-Phase 4: UI design research (if applicable)

If the iteration involves UI changes, new screens, or visual overhaul:
- Research updated design references as in Foundation Phase 6
- Present options, get the human's choice, update DECISIONS.md Design Reference

**Skip** if iteration is backend-only, bug fixes, or non-visual changes.

### R-Phase 5: Archive and compress

Before creating new plans, clean up the coordination files to keep them lean
for the next cycle of agent work.

#### Archive ACTIVITY.md

1. Determine the cycle number (count existing `docs/archive/ACTIVITY-cycle-*.md` files + 1)
2. Copy the current `ACTIVITY.md` to `docs/archive/ACTIVITY-cycle-N.md`
3. Replace `ACTIVITY.md` with a fresh file containing:
   - The standard header
   - A **"Previous Cycles"** summary block — one line per previous cycle summarizing
     what was accomplished (e.g., "Cycle 1 (M1-M4): Built core VT client with tabbed
     UI, 17 tasks completed across 4 sprints")
   - A separator
   - A new re-entry log entry

Example:
```markdown
# Activity Log

All entries are append-only. Format: `[date] <role>ROLE</role> — <action>Action</action> — outcome`

---

## Previous Cycles

- **Cycle 1 (M1-M4):** Built core Scout app — VT API client, CustomTkinter tabbed UI,
  5 endpoint tabs, error handling and polish. 20 tasks across 4 sprints.

---

[2026-02-26] <role>ARCHITECT</role> — <action>Re-Entry: Cycle 2</action> — New milestones planned: [list of new milestones]
```

#### Archive resolved blockers

1. If `BLOCKERS.md` has resolved entries, move them to `docs/archive/BLOCKERS-cycle-N.md`
2. Keep only open blockers (if any) in the live file

#### Create archive directory

```bash
mkdir -p docs/archive
```

### R-Phase 6: Update coordination files

Based on the conversation:

1. **Update DECISIONS.md:**
   - Add new decisions with Decision/Why/Do not fields
   - Update existing decisions if scope or technology changed
   - Add new Rejected Approaches if alternatives were discussed
   - Mark superseded decisions with `[SUPERSEDED by: new decision]` — do not delete them
   - Update Design Reference if UI direction changed

2. **Create new milestone plans** in `docs/plans/`:
   - Same format as originals: `[YYYY-MM-DD]-[project]-[milestone-topic].md`
   - Sequential tasks, TDD-shaped, file paths, acceptance criteria
   - Tasks must not reference modules that don't exist yet (check the existing codebase)

3. **Reset INDEX.md YAML frontmatter** for the new cycle:
   ```yaml
   ---
   sprint_status: none
   blocks: 0
   active_role: ORCHESTRATOR
   tests_passing: true
   ---
   ```
   **Keep all existing sprint table rows.** They are history. New sprints append below.

4. **Commit to main** (re-entry is the only other allowed direct main commit):
   ```bash
   git add ACTIVITY.md DECISIONS.md docs/plans/ docs/sprints/INDEX.md \
          docs/archive/ BLOCKERS.md
   git commit -m "docs: re-entry cycle N — [summary of new milestones]"
   ```

### R-Phase 7: Relaunch prompt

Output the re-entry prompt for the head agent:

```
Iteration cycle ready.

Give your head agent this prompt:

---
You are resuming the Trinity Protocol autonomous loop for this project.

You are the Orchestrator. Spawn two sub-agents:
- One assigned ARCHITECT
- One assigned BUILDER

Read docs/AGENT-GUIDE.md — this is the dispatch table that drives everything.
Run the Session Bootstrap to load project state. New milestone plans have been
added to docs/plans/. The INDEX.md has been reset for the next sprint cycle.

Begin at R-012 (Create Sprint) — the foundation is already approved from the
previous cycle. Pull tasks from the new milestone plans.

**CRITICAL RULE:** Never manually edit the YAML frontmatter in `INDEX.md`. You MUST
use the Python actuator scripts in `.trinity/bin/` for all state changes and logging.
Failure to do so will corrupt the protocol state.

You read state → match rules → dispatch sub-agents. Follow the framework.
---

All work happens on sprint branches — main is protected.
```

### Re-Entry Rules

- **Do not re-scaffold.** The project structure, actuator scripts, and AGENT-GUIDE.md
  already exist. Only update DECISIONS.md and add new plans.
- **Do not delete old plans.** They are history. New plans get new date-stamped files.
- **Do not delete ACTIVITY.md entries.** Archive them, summarize them, but the raw
  originals are preserved in `docs/archive/`.
- **Do not clear the sprint table.** Old sprint rows stay. New sprints append below.
- **Preserve existing DECISIONS.md entries.** Add new ones, update changed ones,
  mark superseded ones, but never delete previous decisions.
- **The AGENT-GUIDE.md rules don't change.** The same state machine drives new sprints.
  Only update AGENT-GUIDE.md if the process itself needs to change (rare).
- **Archive before creating.** Always run R-Phase 5 before R-Phase 6 to keep files lean.

---

## What NOT to Do

- Do not create Sprint 1. That is the Orchestrator's job after approving the foundation.
- Do not leave template placeholders. Every file must have real content.
- Do not skip the "Do not:" line on any DECISIONS.md entry.
- Do not write an AGENT-GUIDE.md with generic paths. Use the actual project name.
- Do not commit directly to main after this foundation commit (exception: re-entry
  cycle commits). All subsequent work goes on sprint branches.
- Do not guess. If you're unsure, ask the human.
