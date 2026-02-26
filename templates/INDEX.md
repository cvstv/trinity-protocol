# Sprint Index

Read this before creating, modifying, or dispatching any sprint.
Use the next available sprint number. Update Status + Role + Date + Blocks after every state change.

| Sprint | File | Status | Role | Date | Milestone | Tasks | Blocks |
|--------|------|--------|------|------|-----------|-------|--------|

## Status Values

| Status | Set by | Meaning | Next action |
|--------|--------|---------|-------------|
| `in-review` | Orchestrator | Sprint written, awaiting Architect review | Architect: Review Sprint |
| `approved` | Architect | Ready for Builder to execute | Builder: Execute Sprint |
| `blocked` | Architect | Security or dependency violations | Orchestrator: Fix Blocked Sprint |
| `in-progress` | Builder | Builder is actively executing | (wait for completion) |
| `builder-blocked` | Builder | Hit a stop condition, blocker written | Orchestrator: Resolve Blocker |
| `complete` | Builder | All tasks committed and passing | Architect: Review Diff |
| `diff-blocked` | Architect | Diff review found violations | Builder: Targeted Fix |
| `merged` | Architect | Diff reviewed and approved | Orchestrator: Sprint Retrospective |
| `human-review` | Any role | Escalated to human, loop paused | Human responds in ESCALATIONS.md |

## Block Counter Rules

The `Blocks` column increments by 1 every time a sprint enters any blocked state:
`blocked`, `builder-blocked`, `diff-blocked`.

- Blocks >= 3 on a single sprint: Orchestrator MUST perform Deep Analysis — pause the
  sprint loop, read all blockers, analyze root cause pattern, make tactical decision
  (rewrite sprint, hotfix, defer, or continue with logged justification).
- Blocks >= 5 on a single sprint: Orchestrator MUST escalate to human-review before proceeding.
