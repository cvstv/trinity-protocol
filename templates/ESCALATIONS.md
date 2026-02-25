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
**Related:** [sprint/council ref, e.g., Sprint 5 or Council 2]
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
- OPEN escalations block all work on the related sprint or council item.
- The Orchestrator must append to ACTIVITY.md when creating and resolving escalations.
- Resolved escalations stay in this file (append-only history). Do not delete them.
