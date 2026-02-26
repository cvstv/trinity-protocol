# Escalations

When the autonomous loop cannot proceed without human input, the Orchestrator writes here.
The loop pauses until the human responds. No agent may act on the escalated item until
the human writes a decision below the escalation entry.

---

## Format

```markdown
## Escalation E-[N]: [short title]

**Date:** YYYY-MM-DD
**Triggered by:** [role] during [action name]
**Related:** [sprint ref, e.g., Sprint 5 or DECISIONS.md proposal]
**Status:** OPEN | RESOLVED

### What needs to be decided
[One paragraph: the specific decision the human must make]

### Why this cannot be decided autonomously
[Which rule, threshold, or ambiguity triggered the escalation]

### Options
1. [Option A] — [consequence]
2. [Option B] — [consequence]
3. [Option C, if applicable] — [consequence]

### Human Decision
[Human writes here. One line is fine. The Orchestrator reads this and resumes.]

### Resolution
[Orchestrator writes: what was done with the human's decision, date, outcome]
```

## Rules

- Every escalation gets a sequential number: E-1, E-2, E-3...
- OPEN escalations block all work on the related sprint or decision.
- The Orchestrator must append to ACTIVITY.md when creating and resolving escalations.
- Resolved escalations stay in this file (append-only history). Do not delete them.

---

## Escalation Triggers

Escalations are created when:
1. A sprint accumulates 5+ blocks (R-001 — mandatory).
2. The Orchestrator and Architect disagree on a DECISIONS.md change (R-041 rejection
   that cannot be revised to mutual satisfaction).
3. Any role encounters a decision that genuinely exceeds autonomous authority.

### Example: Orchestrator-Architect Disagreement

```markdown
## Escalation E-2: DECISIONS.md change — database migration strategy

**Date:** 2026-03-15
**Triggered by:** ORCHESTRATOR during Decision Protocol (R-041 rejection)
**Related:** DECISIONS.md proposal — switch from SQLite to PostgreSQL
**Status:** OPEN

### What needs to be decided
Orchestrator proposed switching from SQLite to PostgreSQL after Deep Analysis
revealed concurrent access issues blocking Sprint 4. Architect rejected because
the migration violates the "local-first, no server dependencies" security invariant.

### Why this cannot be decided autonomously
Decision Protocol requires Architect approval for DECISIONS.md changes.
Architect rejected. The two roles cannot agree — this is a fundamental
trade-off between capability and constraint.

### Options
1. Accept migration to PostgreSQL — gains concurrent access, loses local-first
2. Keep SQLite with WAL mode workaround — preserves constraint, limits concurrency
3. Use SQLite for local, PostgreSQL optional for team use — hybrid approach

### Human Decision
[Human writes here]

### Resolution
[Orchestrator writes resolution after human decides]
```
