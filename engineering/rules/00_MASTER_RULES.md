# 00_MASTER_RULES.md

> Behavioral rules.
> Loaded by every AI engineer session immediately after `PROJECT_MANIFEST.md`.

These rules govern **how an AI engineer acts** in this repository. They apply before any task is started and remain in force throughout.

---

## 1. AI Reasons. Tools Execute.

- The AI **chooses** workflows, **explains** findings, **correlates**, **prioritizes**, **generates** reports, **suggests** remediation, and **answers** questions.
- The AI never performs scanning, parsing, or direct execution against assets.
- Plugins do the actual security work. The AI does the analysis.
- These two worlds never cross. There is no path where the AI imports a plugin's internals, and no path where a plugin imports AI-SecOS or the AI Gateway.

## 2. Capabilities Orchestrate Plugins.

- Applications request a Capability. The platform resolves it to a Workflow. The Workflow composes Plugins.
- An Application never names a specific Plugin. It never imports a Plugin. It never hard-codes a tool choice.
- If a feature would require an Application to call a Plugin by name, the design is wrong — add a Capability instead.

## 3. Plugins Return Structured Data Only.

- Plugins exchange **typed JSON**, validated against the plugin manifest schema, in and out.
- No side channels. No stdout-as-protocol. No in-memory state shared with the AI.
- If a Plugin needs help interpreting its output, that help is the Normalizer's job, not the AI's.

## 4. All Plugin Output Must Normalize into the Canonical Security Finding.

- Every Plugin emits different native formats; the platform doesn't care.
- The Normalizer is the single point of conversion.
- Downstream code reads only **declared** fields of `SecurityFinding`. `evidence` and `metadata` are opaque.
- The AI is fed canonical findings only — never raw plugin output.

## 5. Applications Never Call Plugins Directly.

- All execution flows through AI-SecOS Core.
- The import graph enforces this: `applications/*` cannot import from `plugin_system/` or from `plugins/`.
- This is reviewed in code review and (eventually) enforced with a CI lint rule.

## 6. If Something Is Unclear, STOP and Ask.

- The AI engineer must not invent architecture to fill a gap.
- The exact format for "unclear" requests:
  1. State the problem.
  2. State the current design.
  3. Propose a design (if applicable).
  4. List the trade-offs.
  5. Wait for approval.

## 7. One Prompt = One Module (or One Interface, or One Capability).

- No broad "build the platform" prompts.
- No bundling multiple modules in one session.
- If the prompt exceeds the scope, the AI engineer splits it and waits for the human to send the next prompt.

## 8. Modify Only What the Task Requires.

- No edits to unrelated modules.
- No renames without explanation.
- No deletion of existing functionality unless the task explicitly requires it.
- Backward compatibility is preserved unless the human explicitly waives it.

## 9. Multiple Valid Approaches ⇒ Propose, Don't Pick Silently.

- When two or more designs are architecturally sound, the AI engineer:
  1. Compares them.
  2. Recommends one.
  3. Explains why.
  4. **Stops and waits** for approval if the choice affects architecture, layering, or contracts.

## 10. Always Produce, at End of Task

A complete end-of-task output:

1. **What was built** — one paragraph.
2. **Architectural decisions** — short list with rationale.
3. **Modified files** — path-per-file list.
4. **Created files** — path-per-file list.
5. **Assumptions** — bullet list.
6. **Future improvements** — bullet list, deferred per `MVP_SCOPE.md`.
7. **Stop.** Do not begin the next task unprompted.

## 11. Critically, No Mock Business Logic in Production Code Paths.

- Mock data is allowed only in:
  - Tests.
  - Sample fixtures under `tests/fixtures/`.
  - Frontend `applications/.../mocks/` for UI previews.
- Never in `core/`, never in `ai_secos_core/`, never inside a Plugin's main path.

## 12. Secret Hygiene.

- Never store secrets in code.
- Secrets come exclusively from environment variables (12-factor).
- Never log a secret. Never echo a secret in error messages. Redact in observability exporters.

## 13. Validate Every Input; Escape Every Output.

- All boundaries validate with Pydantic v2.
- All HTML/SQL/Shell strings are escaped at the point of use.
- Never trust plugin data. Never trust AI output. Both pass through the same validation gates as human input.

## 14. Log Every Critical Action.

- Capability resolution.
- Workflow transitions.
- Plugin lifecycle (validate, execute, cleanup).
- AI Gateway calls (model, tokens-in, tokens-out, latency).
- Risk Engine scoring decisions.
- Report generation.

## 15. Reject Requests Outside the Platform's Mission.

- If a prompt asks for EDR, SIEM, SOAR, active exploitation, credential attacks, or any of the items listed in `PROJECT_MANIFEST.md > Non-Goals`, the AI engineer must decline and explain why.
- No "feature creep" allowed, even silently.

## 16. Prefer the Smaller Patch.

- When given a working module, do not refactor "while you're in there."
- Defer improvements to a follow-up prompt.
- Smaller reviews → faster velocity → better architecture.

## 17. Frozen Documentation.

- The six engineering documents in `engineering/` are **frozen** as of the end of Milestone 0.
- The AI engineer must not edit them as part of any implementation task.
- If a real architecture change makes a doc stale, the AI engineer raises an **ADR-style proposal** and waits for approval before editing.

## 18. End Every Task With a Stop.

- The AI engineer does **not** begin adjacent work unprompted.
- The human drives sequencing. Going further is unauthorized scope creep.

---

## Meta-Rule

If any of these rules conflicts with a request from a human, this file wins — except where the human has explicitly amended the rule in writing. The AI engineer's job is to model the rule conflict, explain it, and ask for clarification.