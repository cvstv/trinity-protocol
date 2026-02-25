# Activity Log

Append-only event log. Every role appends exactly one line after completing any action.
The autonomous loop and any agent can reconstruct full project history from this file.

Do not edit or delete previous entries. Do not reformat existing lines.

---

## Format

```
[YYYY-MM-DD HH:MM] <role>ROLE_NAME</role> — <action>Action Name</action> — [outcome]
```

## Roles

```xml
<role>ORCHESTRATOR</role>   <!-- Head coordinator, sprint planner, council chair -->
<role>ARCHITECT</role>      <!-- Logic refiner, security gate, merge gate -->
<role>BUILDER</role>        <!-- TDD executor, implementation, commits -->
<role>HUMAN</role>          <!-- Human-in-the-loop decisions via ESCALATIONS.md -->
```

## Rules

- One line per action. No multi-line entries.
- Append at the bottom. Never insert above existing entries.
- Use the exact role tags above. The head agent parses these.
- Every action in the protocol MUST produce an ACTIVITY.md entry. No silent actions.

---
