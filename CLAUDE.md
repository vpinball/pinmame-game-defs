# Claude Code instructions

@docs/INSTRUCTIONS.md

## Model roles

- Use `opus` at `high` effort for primary high-tier curation, escalation, and promotion decisions.
- Delegate bounded mid-tier work to `sonnet` at `high` effort.
- Delegate bounded low-tier and mechanical work to `haiku` at `high` effort.
- Use `gpt-5.6-sol` at `xhigh` through the Codex CLI for the mandatory independent read-only review. Start a fresh reviewer session against the exact proposed tree and follow the cross-provider review requirements in the imported runbook.
- Do not use the reviewing model to author or repair the contribution it is reviewing. Independently verify its findings, make fixes with the appropriate curation model, rerun the gates, and obtain a fresh review after material changes.
