# Active Blockers

The Builder writes here when it hits a stop condition during sprint execution.
The Orchestrator reads this to decide resolution path.

Remove an entry only after it is resolved (hotfix sprint written or acceptance criteria updated).

---

## Format

```xml
<blocker id="B-[N]">
  <sprint>SPRINT-N</sprint>
  <task>Task X — [task name]</task>
  <file>[path/to/file.py:line_number]</file>
  <error>[exact error message]</error>
  <root-cause>[one sentence]</root-cause>
  <out-of-scope>[why the Builder did not fix it]</out-of-scope>
  <suggested-fix>[what needs to change]</suggested-fix>
  <status>OPEN | RESOLVED</status>
</blocker>
```

## Rules

- Every blocker gets a sequential ID: B-1, B-2, B-3...
- Builder MUST stop executing the sprint after writing a blocker. Do not attempt more tasks.
- Orchestrator reads this file when INDEX.md shows `builder-blocked`.
- Resolved blockers stay in the file with `<status>RESOLVED</status>` for history.

---
