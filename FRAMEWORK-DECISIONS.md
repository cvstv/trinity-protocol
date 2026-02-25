# Trinity Protocol — Framework Decisions

Meta-decisions about the framework itself. Not a project template — this is the
architectural law for Trinity Protocol as a product.

---

## What This Framework Is (and Is Not)

**It is:** A filesystem-based coordination protocol for AI agents that cannot
communicate directly. A state machine implemented in markdown. A dispatch table
that turns repo state into agent actions.

**It is NOT:**
- A chatbot framework (no conversational memory, no message passing between agents)
- An API or SDK (no code to install, no runtime dependencies)
- A CI/CD pipeline (it orchestrates agent work, not deployments)
- A project management tool (it coordinates agents, not humans — though humans can operate it)
- An ML/AI training framework (it coordinates existing agents, doesn't train them)

---

## Design Decisions

### Markdown as the sole medium

**Decision:** All protocol state is stored in markdown files. No database, no config
files, no binary formats.

**Why:** Markdown is readable by humans and AI agents alike. It's version-controlled
by git natively. It requires no runtime, no parser, no dependencies. Any agent that
can read files can participate in the protocol.

**Do not:** Add a database, a config file format (TOML/YAML/JSON), or any binary
state file. If it can't be expressed in markdown, it doesn't belong in the protocol.

### XML tags for machine-critical fields only

**Decision:** Use XML tags (`<role>`, `<rule>`, `<trigger>`, `<status>`, etc.) for
fields that the head agent must parse unambiguously. Use plain markdown for everything
else.

**Why:** XML tags are unambiguous delimiters that AI models parse reliably. Markdown
headers can be misinterpreted. But wrapping everything in XML makes files unreadable
for humans. The hybrid approach preserves readability while ensuring parsing accuracy
where it matters.

**Do not:** Convert entire files to XML. Do not use XML for prose content, discussion,
or documentation sections.

### Three roles, not two or four

**Decision:** Exactly three roles: Orchestrator, Architect, Builder.

**Why:** Three creates natural tension — planning vs. review vs. execution. Two roles
collapse review into either planning or execution, losing the security gate. Four or
more roles create coordination overhead that exceeds the benefit for most projects.

**Do not:** Add a fourth role. If a project needs specialized expertise, assign it
as a focus area within an existing role, don't create a new role.

### Roles are model-agnostic

**Decision:** Roles are defined by responsibility, not by which AI model fills them.
Any model can fill any role. The user assigns roles.

**Why:** Models change. New models appear. Pricing changes. Availability changes.
A framework locked to specific models becomes obsolete when those models do. Roles
defined by responsibility are permanent.

**Do not:** Reference specific model names (Claude, Gemini, GPT, Codex, etc.) in
the protocol files. Document model assignments in the project's DECISIONS.md only.

### Protected main branch with sprint branching

**Decision:** No role commits directly to `main` after the initial foundation commit.
All work happens on `sprint-N` branches. The only path to `main` is through the
Architect's merge gate.

**Why:** Agents make mistakes. Sprints get blocked. If broken code lands on `main`,
every subsequent agent starts from a broken state. Sprint branches isolate in-progress
work so `main` always represents the last known good state.

**Do not:** Allow any rule to bypass the branching strategy. Do not add a
"quick commit to main" escape hatch — that's how invariants erode.

### Append-only ACTIVITY.md

**Decision:** ACTIVITY.md is append-only. No edits, no deletions, no reformatting
of existing entries.

**Why:** Event sourcing. The full project history must be reconstructable from the
log at any point. If entries can be edited, the log is unreliable and agents cannot
trust it for context recovery.

**Do not:** Add "edit" or "delete" operations to ACTIVITY.md. If an entry is wrong,
append a correction entry — never modify the original.

### Council at 3 blocks, escalation at 5

**Decision:** If a single sprint accumulates 3+ blocks, the Orchestrator evaluates
a council session. At 5+ blocks, mandatory human escalation.

**Why:** 3 blocks on one sprint is a signal that the problem is architectural, not
implementational. Continuing the sprint loop wastes tokens. 5 blocks means the
autonomous system has failed to resolve it and human judgment is needed. These
thresholds were derived from real project experience (intel_cli Sprint 5 hit 5+
blocks on a chmod invariant issue that needed human-level architectural review).

**Do not:** Change these thresholds without documenting why. Do not remove the
mandatory escalation at 5 — that's the safety valve.

### Two-round council with conclusions

**Decision:** Council sessions have exactly: Round 0 (pre-meeting notes), Round 1
(responses), Round 2 (final positions), then Orchestrator conclusions.

**Why:** Two response rounds are sufficient for most deliberations. One round doesn't
allow counter-arguments. Three or more rounds produce diminishing returns and waste
tokens. The Orchestrator conclusions provide a clear decision point.

**Do not:** Add more rounds to the default council template. If a council needs
extended deliberation, the Orchestrator can call a second council on the same topic.

---

## Rejected Approaches

### Real-time agent communication

Considered having agents communicate via API calls, shared memory, or message
queues. Rejected because: most AI agent setups don't support real-time inter-agent
communication. The filesystem approach works with any agent that has repo access,
regardless of platform.

### YAML/JSON for state files

Considered using structured data formats for INDEX.md and ACTIVITY.md. Rejected
because: markdown is readable in any editor, renders on GitHub, and doesn't require
a parser. The XML hybrid approach provides machine-readability where needed without
losing human readability everywhere else.

### Single monolithic protocol file

Considered putting everything in one large AGENT-GUIDE.md. Rejected because:
separation of concerns matters. DECISIONS.md is law (read before every action).
INDEX.md is state (read to determine dispatch). ACTIVITY.md is history (read at
bootstrap). Combining them would force agents to parse irrelevant content on every read.

---

## Accepted Trade-offs

| Trade-off | Accepted because |
|-----------|-----------------|
| Human must copy AGENT-GUIDE.md into each project | Keeps projects self-contained and forkable. The skill automates this. |
| No enforcement mechanism for rules | Agents are trusted to follow the protocol. Violations are caught at review gates (Architect). |
| Council adds token cost | Only triggered at 3+ blocks — the alternative (continuing a broken sprint loop) costs more. |
| ACTIVITY.md grows unbounded | Append-only is non-negotiable. The bootstrap uses tiered reading (first 10 + last 30) to manage long logs. |
| No automated testing of protocol compliance | The protocol is markdown — there's nothing to unit test. Compliance is verified by the Architect role at review gates. |

---

*Last updated: 2026-02-24.*
