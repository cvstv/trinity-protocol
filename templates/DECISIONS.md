# [Project Name] — Architecture Decisions

**Every role working on this repo must read this file before any action. No exceptions.**

This captures the WHY behind decisions. Plan files tell you what to build.
This tells you why it was built that way — so you don't accidentally undo it.

---

## Epistemic Protocol

<protocol id="EP-1">
Before any action: if you are not certain of the current project state, re-read
ACTIVITY.md (last 10 entries), INDEX.md, and this file. This costs tokens. It costs
far fewer tokens than undoing a wrong action two milestones into a project.

If you are about to guess, assume, or infer something you could verify by reading
a file — stop. Do not proceed on assumptions. Every state change in this project
is logged. The answer exists. Find it.

If you find yourself mid-action realizing you don't understand what you're touching —
stop, log what you've done so far to ACTIVITY.md, and surface the uncertainty. An
incomplete logged action is recoverable. A confident wrong action is not.
</protocol>

---

## Decision Protocol

<protocol id="DP-1">
If a single sprint accumulates 3 or more entries in the Blocks column of INDEX.md,
the Orchestrator MUST perform a Deep Analysis before the sprint is attempted again:
read all blockers, the sprint file, the last retro, and this file. Analyze root cause
pattern. Make a tactical decision (rewrite sprint, hotfix, defer tasks, or continue).
Log full reasoning to ACTIVITY.md.

If a single sprint accumulates 5 or more blocks, the Orchestrator MUST escalate
to human-review via ESCALATIONS.md before any further action on that sprint.

Changes to this file (DECISIONS.md) require the Decision Protocol:
Orchestrator proposes → Architect reviews → if approved, Architect applies.
If Orchestrator and Architect disagree, escalate to human via ESCALATIONS.md.
</protocol>

---

## What This Tool Is (and Is Not)

**It is:** [one sentence — from project foundation conversation]

**It is NOT:**
- [each explicit exclusion — one per bullet]

Core abstraction: **[the central pipeline or concept this project serves]**

If a feature doesn't serve that abstraction, it doesn't belong.

---

## Technology Decisions

### [Decision name]

**Decision:** [what was chosen]
**Why:** [reasoning]
**Do not:** [hard constraint — what must never be done regarding this decision]

<!-- Repeat for each major technology decision -->

---

## Security Invariants

<!-- Non-negotiable rules. The Architect review gate will block any diff that violates these. -->
<!-- Each invariant must include a violation example. -->

---

## Rejected Approaches

### [Approach name]
[what was considered, why it was rejected]

---

## Accepted Trade-offs

| Trade-off | Accepted because |
|-----------|-----------------|
| [known limitation] | [why it's acceptable for now] |

---

*Last updated: [date]. Update this file when architectural decisions change.*
