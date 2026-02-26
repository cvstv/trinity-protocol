# Trinity Protocol: Framework Decisions

Meta-decisions about the framework itself. Not a project template. This is the
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
- A project management tool (it coordinates agents, not humans, though humans can operate it)
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

**Why:** Three creates natural tension: planning vs. review vs. execution. Two roles
collapse review into either planning or execution, losing the security gate. Four or
more roles create coordination overhead that exceeds the benefit for most projects.

In the autonomous model, the head agent assumes the Orchestrator role and spawns
two sub-agents (Architect and Builder). The three-role separation remains because
it preserves the review chain: the entity that plans does not review its own plans,
and the entity that writes code does not approve its own diffs.

**Do not:** Add a fourth role. If a project needs specialized expertise, assign it
as a focus area within an existing role, don't create a new role.

### Head agent is Orchestrator

**Decision:** The head agent always assumes the Orchestrator role. It dispatches
Architect and Builder as sub-agents. This is the only supported configuration.

**Why:** The Orchestrator reads state and dispatches work, which is exactly what
a head agent does. Making the head agent the Architect or Builder would invert
the authority model (a reviewer dispatching its own reviewer, or an executor
dispatching its own planner). The Orchestrator also owns the escalation path
to human. As the head agent, it can communicate directly with the user.

**Do not:** Support configurations where the head agent is Architect or Builder.
Do not support manual routing or hybrid modes. The framework is autonomous-only.

### Architectural changes require Architect review

**Decision:** Any change to DECISIONS.md must go through the Decision Protocol:
Orchestrator proposes, Architect reviews, Architect applies if approved. Disagreements
escalate to human.

**Why:** DECISIONS.md is architectural law. The Orchestrator could modify it unilaterally
in autonomous mode, but that removes the review gate that catches scope creep and
constraint erosion. The Architect's independence on DECISIONS.md changes preserves
the same integrity that the merge gate (R-023) provides for code.

**Do not:** Allow the Orchestrator to modify DECISIONS.md directly. Do not allow
the Builder to propose DECISIONS.md changes (route through Orchestrator).

### UI design research during setup

**Decision:** If a project includes a frontend or visual interface, the `/trinity-protocol`
skill researches real UI examples and presents options to the human during setup.
The human's choice is documented in DECISIONS.md as a design reference.

**Why:** AI agents are notoriously bad at designing attractive UIs from scratch.
They default to generic layouts and bland aesthetics. By researching existing designs
that match the project's domain and having the human pick a visual direction during
setup, the Builder has a concrete reference to work from during autonomous execution.

**Do not:** Skip this phase for projects with a UI. Do not let the Builder invent
UI designs without a documented design reference in DECISIONS.md.

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
"quick commit to main" escape hatch. That's how invariants erode.

### Append-only ACTIVITY.md

**Decision:** ACTIVITY.md is append-only. No edits, no deletions, no reformatting
of existing entries.

**Why:** Event sourcing. The full project history must be reconstructable from the
log at any point. If entries can be edited, the log is unreliable and agents cannot
trust it for context recovery.

**Do not:** Add "edit" or "delete" operations to ACTIVITY.md. If an entry is wrong,
append a correction entry. Never modify the original.

### Deep Analysis at 3 blocks, escalation at 5

**Decision:** If a single sprint accumulates 3+ blocks, the Orchestrator performs
a Deep Analysis: pauses the sprint loop, reads all blockers, analyzes root cause
patterns, and makes a tactical decision (rewrite sprint, hotfix, defer, or continue
with logged justification). At 5+ blocks, mandatory human escalation.

**Why:** 3 blocks on one sprint signals an architectural problem, not an implementation
one. The Orchestrator pauses to think rather than continuing a broken loop. 5 blocks
means the autonomous system has failed to resolve it and human judgment is needed.
These thresholds were derived from real project experience (intel_cli Sprint 5 hit 5+
blocks on a chmod invariant issue that needed human-level architectural review).

**Do not:** Change these thresholds without documenting why. Do not remove the
mandatory escalation at 5. That's the safety valve. Do not skip reading all
blockers during Deep Analysis. The pattern requires the full picture.

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

### Multi-round council deliberation

Originally the framework used 3-round council sessions (pre-meeting notes, responses,
final positions, conclusions) when sprints hit 3+ blocks. Rejected for autonomous mode
because: when the head agent IS the Orchestrator and can spawn sub-agents directly,
multi-round async deliberation is unnecessary overhead. The Orchestrator can reason
through blockers directly via Deep Analysis, and architectural changes go through the
Decision Protocol (Orchestrator proposes, Architect reviews) which achieves the same
review integrity with far less token cost. Council sessions were designed for manual
mode where agents couldn't communicate. That mode is no longer supported.

### Manual routing and hybrid modes

Originally the framework supported three modes: fully autonomous, manual routing
(human copy-pastes between separate agent sessions), and hybrid (human fills some
roles). Rejected because: supporting multiple modes created inconsistencies throughout
the framework. Manual routing is slow and error-prone. The framework now commits to
fully autonomous mode only, with the head agent as Orchestrator and two sub-agents.

### Single monolithic protocol file

Considered putting everything in one large AGENT-GUIDE.md. Rejected because:
separation of concerns matters. DECISIONS.md is law (read before every action).
INDEX.md is state (read to determine dispatch). ACTIVITY.md is history (read at
bootstrap). Combining them would force agents to parse irrelevant content on every read.

---

## Accepted Trade-offs

| Trade-off | Accepted because |
|-----------|-----------------|
| No enforcement mechanism for rules | Agents are trusted to follow the protocol. Violations are caught at review gates (Architect). |
| Deep Analysis pauses sprint loop | Only triggered at 3+ blocks. The pause is intentional. Continuing a broken sprint loop costs more than stopping to analyze. |
| ACTIVITY.md grows unbounded | Append-only is non-negotiable. The bootstrap uses tiered reading (first 10 + last 30) to manage long logs. |
| No automated testing of protocol compliance | The protocol is markdown. There's nothing to unit test. Compliance is verified by the Architect role at review gates. |
| UI design research adds setup time | Only for projects with a UI. The alternative (agents guessing at design) produces worse results and wastes autonomous execution tokens on UI rework. |

---

*Last updated: 2026-02-25.*
