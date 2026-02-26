# Trinity Protocol — Agent Guide

This is the runtime protocol for an autonomous multi-agent development system.
The repository is the only shared state. Agents coordinate through files by design —
every action logged, every decision tracked, every review documented.

This document is a **decision table** — the head agent reads project state from the
files, pattern-matches against rules, and dispatches the correct role to its sub-agents.

---

## The Trinity

Three roles. All engineers. Separated by responsibility, not capability.

<roles>
  <role id="ORCHESTRATOR" level="L3">
    Senior architect, sprint planner, decision protocol authority.
    Responsibilities: strategic planning, scope control, sprint creation, blocker resolution,
    deep analysis, retrospectives. Owns the project schedule. This is the head agent role.
  </role>
  <role id="ARCHITECT" level="L2">
    Principal engineer, logic refiner, security gate, merge gate.
    Responsibilities: architecture decisions, code review, DECISIONS.md ownership,
    invariant enforcement, diff approval. Nothing merges without this role's sign-off.
  </role>
  <role id="BUILDER" level="L1">
    Implementation specialist, TDD executor, commit author.
    Responsibilities: writing code, running tests, committing per task, precise literal
    execution of sprint specs. Stops and reports when blocked — never guesses.
  </role>
</roles>

### Role Assignment

The framework operates in **fully autonomous mode**. The head agent assumes the
Orchestrator role and spawns two sub-agents: one assigned Architect, one assigned
Builder. The head agent reads state, matches rules, and dispatches the appropriate
sub-agent. No manual routing. No hybrid mode.

The Orchestrator is always the head agent because it reads state and dispatches
work — that's exactly what a head agent does. Making the head agent the Architect
or Builder would invert the authority model.

Document the role-to-agent mapping in DECISIONS.md under "Multi-Agent Workflow."

---

## Session Bootstrap

When any role starts a new session, loses context, or is uncertain about project state,
execute this **in full** before any action. Do not skip steps. Do not skim.

<bootstrap>

  <phase name="ORIENT" purpose="Reconstruct full project awareness">
    <step order="1">
      Read DECISIONS.md — full file, every section.
      This is the law. Know what this project is, what it is not, every technology
      decision, every security invariant, every rejected approach. If you cannot
      summarize every "Do not:" line from memory after reading, read it again.
    </step>
    <step order="2">
      Read INDEX.md — full table.
      Count total sprints. Note the highest sprint number. Read every status and
      every Blocks value. Identify: which sprints are merged, which are active,
      which are blocked. This tells you the project's age and current position.
    </step>
    <step order="3">
      Read ACTIVITY.md — full file if under 200 lines. If over 200 lines, read
      the first 10 lines (project origin) AND the last 30 lines (recent state).
      The first entries tell you how this project started. The last entries tell
      you what just happened and who acted last.
    </step>
    <step order="4">
      Read BLOCKERS.md — full file. Note any OPEN blockers.
    </step>
    <step order="5">
      Read ESCALATIONS.md — full file. Note any OPEN escalations.
      An open escalation means the loop is PAUSED. Do not proceed past R-000.
    </step>
  </phase>

  <phase name="FOCUS" purpose="Load active work context">
    <step order="6">
      From INDEX.md, identify the active sprint (any status that is not "merged").
      Read the full SPRINT-N.md for that sprint.
    </step>
    <step order="7">
      If the most recent retro exists (SPRINT-N-retro.md for the last merged sprint),
      read it. It contains deferred items and architectural flags that affect what
      happens next.
    </step>
  </phase>

  <phase name="REPORT" purpose="Prove context is loaded before acting">
    <step order="8">
      Output a state report before taking any action:
      - Project: [name from DECISIONS.md]
      - Total sprints: [N merged, N active, N blocked]
      - Current sprint: [N — status — Blocks: N]
      - Last 3 ACTIVITY.md entries: [summary]
      - Open blockers: [none | B-N summary]
      - Open escalations: [none | E-N summary]
      - My role: [ORCHESTRATOR | ARCHITECT | BUILDER]
      - Next rule to fire: [rule ID from dispatch table]
    </step>
  </phase>

</bootstrap>

**If you cannot fill every field in the state report, you have not read enough.
Go back and read what you're missing. Do not proceed on partial context.**

---

## The Files (Protocol Nodes)

File names below are shorthand. When the skill initializes a project, it places
files at specific paths (e.g., `INDEX.md` → `docs/sprints/INDEX.md`). The deployed
`AGENT-GUIDE.md` in your project will use the actual paths. If a file isn't where
you expect it, check the project root and `docs/` subdirectories.

<files>
  <file name="ACTIVITY.md" role="Event log">
    <writes>All roles (append after every action)</writes>
    <reads>All roles (first at session start)</reads>
  </file>
  <file name="DECISIONS.md" role="Policy store — architectural law">
    <writes>Architect (on decision changes)</writes>
    <reads>All roles (before every action)</reads>
  </file>
  <file name="INDEX.md" role="Coordination table — sprint status + block counts">
    <writes>All roles (status updates after every action)</writes>
    <reads>All roles (to determine next dispatch)</reads>
  </file>
  <file name="BLOCKERS.md" role="Dead letter queue — unprocessable work">
    <writes>Builder (on stop conditions)</writes>
    <reads>Orchestrator (to resolve), all roles (awareness)</reads>
  </file>
  <file name="ESCALATIONS.md" role="Human valve — pauses loop for human input">
    <writes>Any role (when autonomous decision exceeds authority)</writes>
    <reads>Human (to decide), Orchestrator (to resume after decision)</reads>
  </file>
  <file name="docs/sprints/SPRINT-N.md" role="Sprint specification">
    <writes>Orchestrator (creates), Orchestrator (fixes if blocked)</writes>
    <reads>Architect (review), Builder (execute)</reads>
  </file>
  <file name="docs/plans/*.md" role="Milestone roadmap">
    <writes>Architect (planning phase)</writes>
    <reads>Orchestrator (sprint creation), Builder (context)</reads>
  </file>
</files>

---

## Branching Strategy

`main` is protected. No role commits directly to `main`. Ever.

<branching>
  <branch name="main" protected="true">
    Production-ready code only. Updated exclusively via merge after Architect
    approval (R-023). The Architect is the merge gate.
  </branch>
  <branch name="sprint-N" created-by="BUILDER" from="main">
    Created when Builder begins executing a sprint (R-022).
    All task commits happen here. Branch is merged to main after Architect
    approves the diff review (R-023). Deleted after merge.
  </branch>
  <branch name="sprint-N-hotfix" created-by="BUILDER" from="sprint-N">
    Created when a hotfix sprint is dispatched. Merged back into the parent
    sprint branch (or main if the parent sprint is already merged).
  </branch>
</branching>

### Branch Rules

1. Builder creates `sprint-N` from `main` at the start of R-022.
2. All task commits go to `sprint-N`. Never to `main`.
3. When the Architect approves the diff (R-023 → status "merged"), the sprint
   branch is merged to `main` and deleted.
4. If a sprint is blocked mid-execution, the sprint branch persists. Work resumes
   on the same branch after the block is resolved.
5. Hotfix branches are `sprint-N-hotfix`, branched from the sprint they're fixing.

---

## Commit Convention

Every task commit by the Builder must follow:

```
feat(sprint-N): task-X — [subject]
```

Hotfix commits: `fix(sprint-N): [description]`
Decision updates: `docs: update DECISIONS.md — [description]`

---

## Dispatch Table — The Rule Engine

The head agent reads INDEX.md and ESCALATIONS.md to determine which rule fires
next. Rules are evaluated top-to-bottom. First match wins.

### Priority Rules (always check first)

<rule id="R-000">
  <trigger>ESCALATIONS.md contains any entry with <status>OPEN</status></trigger>
  <dispatch>PAUSE</dispatch>
  <action>Do not proceed on any item related to the open escalation. Wait for human.</action>
  <next>Human writes decision → Orchestrator: Resume from escalation</next>
</rule>

<rule id="R-001">
  <trigger>INDEX.md shows any sprint with Blocks >= 5</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>Mandatory escalation. Write to ESCALATIONS.md. Set sprint status to human-review.</action>
  <next>R-000 (wait for human)</next>
</rule>

<rule id="R-002">
  <trigger>INDEX.md shows any sprint with Blocks >= 3 AND Blocks < 5</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Deep Analysis. Pause the sprint loop. Read all open BLOCKERS.md entries, the full
    sprint file, the last retro, and DECISIONS.md. Analyze the root cause pattern across
    all blocks — are they related? Is the sprint plan flawed? Is a dependency missing?
    Is an architectural decision wrong?

    Make a tactical decision:
    A) Rewrite the sprint plan (bad scoping or task ordering).
    B) Create a hotfix sprint (missing prerequisite or dependency).
    C) Defer blocked tasks to next sprint (not on critical path).
    D) Continue with logged justification (blocks are resolved, pattern is understood).

    If analysis reveals a DECISIONS.md change is needed, route to R-040.
    Log full reasoning to ACTIVITY.md.
  </action>
  <next>Route to appropriate sprint rule based on decision (R-020, R-021, R-022, or R-040)</next>
</rule>

### Kickoff Rules (run once per project)

<!-- R-010 through R-013 are executed during Phase 1 (Setup) by the /trinity-protocol
     skill. They are NOT part of the autonomous execution loop. The autonomous loop
     begins at R-011 (Approve Foundation) or R-020 (first sprint) depending on state. -->

<rule id="R-010">
  <trigger>DECISIONS.md contains only template content (no populated sections)</trigger>
  <dispatch>ARCHITECT</dispatch>
  <action>
    Run Project Foundation. This is handled by the /trinity-protocol skill during
    Setup — a conversational session with the human to populate DECISIONS.md and
    create docs/plans/*.md with real content. Commit foundation files.
    If encountered during autonomous execution, escalate to human (R-000) —
    the skill must be run first.
  </action>
  <completion>
    INDEX.md: no changes (no sprints yet)
    RUN: python ./.trinity/bin/trinity-log.py "<role>ARCHITECT</role> — <action>Project Foundation</action> — DECISIONS.md + N plan files committed"
  </completion>
  <next>R-011</next>
</rule>

<rule id="R-011">
  <trigger>ACTIVITY.md shows Project Foundation complete AND no "Approve Foundation" entry</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Review DECISIONS.md + all docs/plans/*.md as senior architect.
    Check: decisions sound? constraints complete? scope realistic? dependencies sequenced?
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Approve Foundation</action> — [approval or changes-needed]"
  </completion>
  <next>If approved → R-012. If changes needed → R-010 (Architect revises).</next>
</rule>

<rule id="R-012">
  <trigger>Foundation approved AND no "Project Scaffolding" entry in ACTIVITY.md</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Create project shell — directory structure, dependency files, CI skeleton.
    No feature code. Verify current package versions.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Project Scaffolding</action> — [commit hash]"
  </completion>
  <next>R-013</next>
</rule>

<rule id="R-013">
  <trigger>Scaffolding committed AND no "Review Scaffold" entry in ACTIVITY.md</trigger>
  <dispatch>ARCHITECT</dispatch>
  <action>
    Security review of scaffold: no secrets in config templates, dep versions not
    known-vulnerable, CI config safe, directory structure matches plans.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-log.py "<role>ARCHITECT</role> — <action>Review Scaffold</action> — [review result]"
  </completion>
  <next>If approved → R-020 (sprint loop begins). If blocked → R-012 (Orchestrator fixes).</next>
</rule>

### Sprint Loop Rules

<rule id="R-020">
  <trigger>No sprint in INDEX.md with sprint_status in [in-review, approved, in-progress, builder-blocked, complete, diff-blocked] — i.e., all prior sprints are merged or no sprints exist</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Create next sprint. Read DECISIONS.md, BLOCKERS.md, INDEX.md, all prior retros,
    and the relevant milestone plan file.
    Write docs/sprints/SPRINT-N.md. 
    Rules: under 8 tasks, strict sequential order, exact file paths, acceptance checks,
    stop conditions. Do not reference modules that don't exist yet.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-transition.py "in-review"
    RUN: python ./.trinity/bin/trinity-block.py reset
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Create Sprint N</action> — created SPRINT-N.md"
  </completion>
  <next>R-021</next>
</rule>

<rule id="R-021">
  <trigger>INDEX.md shows sprint_status: in-review</trigger>
  <dispatch>ARCHITECT</dispatch>
  <action>
    Review SPRINT-N.md against DECISIONS.md. Check: task order, security invariants,
    scope creep, BLOCKERS.md conflicts. Verify no prior sprint is still active.
  </action>
  <completion>
    If blocked: RUN: python ./.trinity/bin/trinity-block.py increment
    RUN: python ./.trinity/bin/trinity-transition.py "[approved or blocked]"
    RUN: python ./.trinity/bin/trinity-log.py "<role>ARCHITECT</role> — <action>Review Sprint N</action> — [review result]"
  </completion>
  <next>If approved → R-022. If blocked → R-025.</next>
</rule>

<rule id="R-022">
  <trigger>INDEX.md shows sprint_status: approved</trigger>
  <dispatch>BUILDER</dispatch>
  <action>
    RUN: python ./.trinity/bin/trinity-transition.py "in-progress" immediately.
    Execute each task in order using TDD. Commit per task with convention.
    Stop conditions: if tests fail after 2 attempts, STOP. Write BLOCKERS.md entry.
  </action>
  <completion>
    If blocked: RUN: python ./.trinity/bin/trinity-block.py increment
    RUN: python ./.trinity/bin/trinity-transition.py "[complete or builder-blocked]"
    SPRINT-N.md: append Execution Summary (task, commit hash, deviations)
    RUN: python ./.trinity/bin/trinity-log.py "<role>BUILDER</role> — <action>Execute Sprint N</action> — [completion or blocked entry]"
  </completion>
  <next>If complete → R-023. If blocked → R-026.</next>
</rule>

<rule id="R-023">
  <trigger>INDEX.md shows sprint_status: complete</trigger>
  <dispatch>ARCHITECT</dispatch>
  <action>
    Review full diff. Check security invariants, architecture compliance,
    implementation matches sprint intent. No out-of-scope changes.
  </action>
  <completion>
    If blocked: RUN: python ./.trinity/bin/trinity-block.py increment
    RUN: python ./.trinity/bin/trinity-transition.py "[merged or diff-blocked]"
    RUN: python ./.trinity/bin/trinity-log.py "<role>ARCHITECT</role> — <action>Review Diff N</action> — [review result]"
  </completion>
  <next>If merged → R-024. If diff-blocked with minor fix → R-027. If diff-blocked with major issue → R-025.</next>
</rule>

<rule id="R-024">
  <trigger>INDEX.md shows sprint_status: merged</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Sprint retrospective. Compare planned vs actual. Identify deferred items,
    new constraints, gaps. Write docs/sprints/SPRINT-N-retro.md.
    If architectural observations: flag for Architect to update DECISIONS.md.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Sprint Retrospective N</action> — [retro entry short summary]"
  </completion>
  <next>If architectural flags → R-028. Then → R-020 (next sprint).</next>
</rule>

### Recovery Rules

<rule id="R-025">
  <trigger>INDEX.md shows sprint_status: blocked</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Read Architect's fix list from ACTIVITY.md or SPRINT-N.md review comments.
    Address only the specific fixes listed — do not re-scope, reorder, or add tasks.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-transition.py "in-review"
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Fix Blocked Sprint N</action> — [fix entry]"
  </completion>
  <next>R-021 (Architect re-reviews)</next>
</rule>

<rule id="R-026">
  <trigger>INDEX.md shows sprint_status: builder-blocked</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Read BLOCKERS.md. Decide:
    A) Create hotfix sprint (SPRINT-N-hotfix.md) to fix root cause first.
    B) Update SPRINT-N.md acceptance criteria and defer blocked task to next sprint.
    Remove resolved BLOCKERS.md entry.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-transition.py "[in-review or approved]"
    BLOCKERS.md: update resolved entry
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Resolve Blocker N</action> — [resolution entry]"
  </completion>
  <next>If hotfix → R-021 (review hotfix). If deferred → R-022 (resume sprint).</next>
</rule>

<rule id="R-027">
  <trigger>INDEX.md shows sprint_status: diff-blocked AND Architect flagged minor fix</trigger>
  <dispatch>BUILDER</dispatch>
  <action>
    Targeted fix. Architect specified exact file, line, and change required.
    Make only that change. Run only the affected test. Commit with fix convention.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-transition.py "complete"
    RUN: python ./.trinity/bin/trinity-log.py "<role>BUILDER</role> — <action>Targeted Fix N</action> — [targeted fix entry]"
  </completion>
  <next>R-023 (Architect re-reviews diff)</next>
</rule>

<rule id="R-028">
  <trigger>Retro flagged architectural observation for DECISIONS.md</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Draft proposed DECISIONS.md change based on retro observation.
    Route to Decision Protocol for Architect review before applying.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Propose Decision Update</action> — [summary of proposed change]"
  </completion>
  <next>R-040 (Decision Protocol)</next>
</rule>

### Decision Protocol Rules

<rule id="R-040">
  <trigger>Orchestrator proposes a change to DECISIONS.md (from R-024 retro flag,
    R-002 deep analysis, or any other source)</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Draft the proposed DECISIONS.md change. Write the full entry (Decision, Why,
    Do not) using the `trinity-log.py` script. Do not modify DECISIONS.md yet.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Propose Decision Update</action> — [summary of change and reasoning]"
  </completion>
  <next>R-041</next>
</rule>

<rule id="R-041">
  <trigger>Unreviewed DECISIONS.md proposal exists in ACTIVITY.md log</trigger>
  <dispatch>ARCHITECT</dispatch>
  <action>
    Review the proposed DECISIONS.md change against existing decisions, security
    invariants, and project constraints. Check for contradictions with existing
    entries. Approve or reject with reasoning.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-log.py "<role>ARCHITECT</role> — <action>Review Decision Proposal</action> — [approval or rejection with reasoning]"
  </completion>
  <next>If approved → R-042. If rejected → Orchestrator revises (back to R-040)
    or escalates disagreement to human (R-000).</next>
</rule>

<rule id="R-042">
  <trigger>Architect approved a DECISIONS.md proposal</trigger>
  <dispatch>ARCHITECT</dispatch>
  <action>
    Apply the approved change to DECISIONS.md under the correct section.
    Must include: Decision, Why, Do not (hard constraint).
    Commit with docs convention.
  </action>
  <completion>
    DECISIONS.md: updated with new entry
    RUN: python ./.trinity/bin/trinity-log.py "<role>ARCHITECT</role> — <action>Apply Decision Update</action> — [summary + commit hash]"
  </completion>
  <next>Return to calling rule (R-024 retro flow → R-020, or sprint loop)</next>
</rule>

### Mid-Sprint Rules

<rule id="R-030">
  <trigger>Builder raises mid-sprint concern that is not a full stop condition</trigger>
  <dispatch>ORCHESTRATOR</dispatch>
  <action>
    Review current sprint progress. Decide:
    A) Continue — sprint is on track.
    B) Scope-reduce — mark affected task as DEFERRED in SPRINT-N.md.
    C) Hotfix first — create SPRINT-N-hotfix.md.
  </action>
  <completion>
    RUN: python ./.trinity/bin/trinity-log.py "<role>ORCHESTRATOR</role> — <action>Mid-Sprint Check</action> — [decision]"
  </completion>
  <next>Resume sprint execution</next>
</rule>

---

## Invariant Rules (Always Active)

These rules are not triggered by state — they are constraints that apply to every action.

<invariant id="I-001">
  Every action by any role MUST append exactly one line to ACTIVITY.md using the `trinity-log.py` script.
  No silent actions. If ACTIVITY.md is stale, the system makes wrong decisions.
</invariant>

<invariant id="I-002">
  Every role MUST read DECISIONS.md before taking any action.
  The Epistemic Protocol in DECISIONS.md takes priority over continuing.
</invariant>

<invariant id="I-003">
  The YAML frontmatter in INDEX.md (`sprint_status`, `blocks`, `active_role`) must be updated after every state change using the `trinity-block.py` and `trinity-transition.py` scripts.
  INDEX.md YAML frontmatter is the system heartbeat.
</invariant>

<invariant id="I-004">
  The Builder never edits out-of-scope files. Stop and write BLOCKERS.md instead.
</invariant>

<invariant id="I-005">
  The Architect is the merge gate. Nothing merges without an Architect diff review.
</invariant>

<invariant id="I-006">
  The Orchestrator never writes feature code. It plans, scaffolds structure, and resolves.
</invariant>

<invariant id="I-007">
  When uncertain, stop. Read. The answer is in the files.
  A wrong action costs more than the tokens spent reading.
</invariant>

<invariant id="I-008">
  No role commits directly to main. All work happens on sprint branches.
  The only path to main is through the Architect's merge gate (R-023).
</invariant>

---

## The Loop (Visual)

```
[KICKOFF — run once]
R-010: Architect — Project Foundation    → DECISIONS.md + plans committed
R-011: Orchestrator — Approve Foundation → approves or sends back
R-012: Orchestrator — Project Scaffolding → directory + deps committed
R-013: Architect — Review Scaffold       → security gate

[SPRINT LOOP — repeat]
R-020: Orchestrator — Create Sprint      → SPRINT-N.md, INDEX row
R-021: Architect — Review Sprint         → approved / blocked
  └─ blocked (R-025)                     → Orchestrator fixes → R-021
R-022: Builder — Execute Sprint          → branch sprint-N from main → complete / builder-blocked
  ├─ mid-sprint (R-030)                  → Orchestrator: continue / reduce / hotfix
  └─ builder-blocked (R-026)              → Orchestrator resolves → R-021 or R-022
R-023: Architect — Review Diff           → merged / diff-blocked
  ├─ minor fix (R-027)                   → Builder: targeted fix → R-023
  ├─ major issue                         → R-025 (blocked path)
  └─ approved                            → merge sprint-N → main, delete branch
R-024: Orchestrator — Retrospective      → retro committed
  └─ architectural flag (R-028)          → Architect: Update DECISIONS.md

[DEEP ANALYSIS — triggered by R-002 at 3+ blocks]
R-002: Orchestrator — Deep Analysis      → read all blockers, analyze pattern
                                         → rewrite sprint / hotfix / defer / continue
                                         → if architectural issue → R-040

[DECISION PROTOCOL — triggered by R-028 retro flag or R-002 analysis]
R-040: Orchestrator — Propose change     → draft DECISIONS.md entry to ACTIVITY.md
R-041: Architect — Review proposal       → approved / rejected
R-042: Architect — Apply change          → DECISIONS.md updated, committed
  └─ rejected                            → Orchestrator revises (R-040) or escalates (R-000)

[ESCALATION — triggered by R-001 or Orchestrator-Architect disagreement]
R-000: PAUSE                             → human decides in ESCALATIONS.md
                                         → Orchestrator resumes

[INVARIANTS — always active]
I-001 through I-008: apply to every action regardless of state
```
