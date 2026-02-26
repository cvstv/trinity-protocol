---
sprint_status: none
active_sprint: 0
blocks: 0
active_role: ORCHESTRATOR
tests_passing: false
---

# Sprint Index

**Read this before creating, modifying, or dispatching any sprint.**
The state of the protocol is driven entirely by the YAML variables above. 

> Do not edit the YAML block manually unless you are an agent bypassing the CLI tools. 
> Use `./.trinity/bin/trinity-transition`, `./.trinity/bin/trinity-block`, and `./.trinity/bin/trinity-test.py`.

## Status Values

| Status | Meaning |
|--------|---------|
| `in-review` | Sprint written, awaiting Architect review |
| `approved` | Ready for Builder to execute |
| `blocked` | Security or dependency violations |
| `in-progress` | Builder is actively executing |
| `builder-blocked` | Hit a stop condition, blocker written |
| `complete` | All tasks committed and passing |
| `diff-blocked` | Diff review found violations |
| `merged` | Diff reviewed and approved |
| `human-review` | Escalated to human, loop paused |

## Block Counter Rules

The `blocks` variable increments by 1 every time a sprint enters any blocked state:
`blocked`, `builder-blocked`, `diff-blocked`.

- Blocks >= 3 on a single sprint: Orchestrator MUST perform Deep Analysis — pause the
  sprint loop, read all blockers, analyze root cause pattern, make tactical decision.
- Blocks >= 5 on a single sprint: Orchestrator MUST escalate to human-review before proceeding.
