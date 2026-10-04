# Agent instructions for PinMAME machine definitions

This file is the operational runbook for the agent continuing the physical-machine definition project. It is generic policy that every session needs: it must not name individual games, quote coverage counts, or pin upstream revisions. The little mutable project state it depends on lives in the short `docs/CURRENT-STATE.md`, and the rules and lessons for particular tasks live in the topic docs listed below. Read the schemas, this file, and that ledger before changing a definition, read each topic doc before the task it covers, and keep the generated catalog/coverage reports synchronized throughout the work.

## Documentation map

| File | Holds | Read |
| --- | --- | --- |
| `docs/INSTRUCTIONS.md` | Policy every session needs: scope, invariants, evidence authority, conflicts, model allocation and the per-game workflow | Always; Claude Code loads it |
| `docs/CURRENT-STATE.md` | Pinned inputs, the scope-exception pointer, standing priorities and open cross-machine corrections | Always; Claude Code loads it |
| `docs/pinside-top100.md` | The standing priority list with each record's generated completion score | Always; Claude Code loads it |
| `docs/SETUP.md` | Prerequisites, tool discovery, agent CLI calls, read-only inputs, the working root, pinned checkouts and the native-library build | When preflight finds something missing or unverified, and before delegating to or reviewing with a model CLI |
| `docs/IDENTITY.md` | Driver grouping, record splits, OPDB identity, `physical_compatibility` and machine families | Step 2 |
| `docs/SOURCES.md` | Finding, retaining, reading, weighing and excerpting sources | Step 3, and before writing a conflict |
| `docs/PLATFORMS.md` | Per-platform read paths, `normally_closed` derivation, flipper columns, special solenoids, address arithmetic and controller-profile notes | Step 4, and before editing `controllers/pinmame/` |
| `docs/SPATIAL.md` | Placement rules and lessons | Step 5 |
| `docs/TESTING.md` | Curator, test and manifest lessons | Steps 6 and 7 |
| `docs/HARNESS.md` | Harness scenarios, runtime evidence and reverse engineering | Before any harness run or Ghidra escalation |
| `docs/PROJECT-GATES.md` | Project-wide completion gates and the final handoff | Before claiming project-level completion |
| `docs/archive/` | The frozen pre-compaction ledger | Search it; never read it whole |

Where new text goes:

- A rule every session needs goes in this runbook. Keep it generic and short.
- A rule for one task goes in that task's topic doc. What a past case taught goes under that doc's
  **Lessons**, naming the commit or knowledge note it came from.
- Mutable project state goes in `docs/CURRENT-STATE.md`. Per-game facts go in the game's knowledge
  note, spatial report and definition.
- State each rule in one place and link to it elsewhere. If a topic doc disagrees with this runbook,
  the runbook wins; fix the topic doc in the same change.

## Preflight

Before beginning a game, confirm the current repository, applicable read-only inputs, writable evidence roots, model tiers, browser access, and the pinned native library needed by that game's gates. Report only genuine unresolved prerequisites; do not fail merely because a tool was installed outside a conventional path.

`docs/SETUP.md` holds the procedure for each check. Read it when something is missing or not yet
verified in this session. These of its rules apply even without reading it:

- A missing capability is a hard gate, but a command absent from `PATH` or an unset variable is not
  proof that it is unavailable. Discover before declaring a blocker, and ask the human for an
  unresolved human-owned tool or read-only input.
- Clone the three public source repositories yourself; never ask the human for them.
- Never install software or create substitute read-only source folders without contributor approval,
  and never modify the user's read-only inputs.
- All writable state lives under the fixed sibling `pinmame-game-defs-working-dir`; never choose
  another location silently.
- Never reuse, promote or search a `.incoming-*` checkout, and never reset, clean or delete an
  unexpected or dirty managed checkout.

## Objective and completion standard

The objective is to cover every physical pinball machine supported by the pinned PinMAME catalog. A definition is `author_ready` only when a table author can use it to fully recreate the physical game: controller variants, switches, outputs, displays, mechanisms, physical behavior, recreation knowledge, evidence provenance, and normalized positions must all be complete and validated. A record that does not meet that standard must remain conspicuously `partial` or `stub`; never promote it for progress credit.

Only physical machines belong in scope. Exclude community rethemes, virtual-only tables, joke drivers, test drivers, non-pinball games and custom ROMs that do not run on the documented physical machine. A later firmware revision or a compatible FreeWPC/community ROM may remain a driver variant of the physical machine when it genuinely runs on that hardware; its release year does not create a new physical game. Do not group unrelated titles merely because they share a theme.

The coordinate convention follows VPX/player view in one normalized `playfield` space:

- `x = 0` is the left side and `x = 1` is the right side.
- `y = 0` is the rear/backglass end and `y = 1` is the front/apron end.
- Record playfield positions for switches, coils/controlled devices, lamps, flashers, and GI emitters. Cabinet/backbox/service devices use a controlled `not_applicable` spatial record rather than invented coordinates.
- Use one placement per physical emitter or device location. Disclose projections, shared emitters, quantities, uncertainty, and exact source roles. Never present a render helper, lightmap object, primitive origin, or script-only surrogate as an observed physical socket.
The project-wide completion gates and the final handoff are in `docs/PROJECT-GATES.md`.

## Pinned baseline and current-state ledger

This runbook is generic policy and must stay free of individual game names, counts, claims, and
pinned revisions. `docs/CURRENT-STATE.md` holds the little mutable project state that has no better
home: the pinned upstream revisions and their baseline role, pointers to the reviewed scope
exceptions and the generated coverage reports, and standing maintainer priorities. Every session
reads it, so it must stay short; it is not a log.

Record work where its reader will look for it, never in the ledger:

- what a game's definition is, why it stays partial, and its mechanism and edition knowledge: the
  game's knowledge note, spatial report and `coverage.missing`;
- what a session did, which models ran, and how review findings were settled: the commit messages,
  the PR description and `review-artifacts`;
- coverage counts: the generated catalog and coverage reports, never copied by hand;
- which games are being worked on: the per-game branches and worktrees themselves (step 1);
- a curation lesson that generalizes beyond one machine: the general rule here when every session
  needs it, otherwise in the topic doc for the task it governs, with the machine that produced it
  named in its knowledge note or commit message.

Update the ledger in the same commit as a change to what it records. The ledger as it stood before
compaction is frozen under `docs/archive/`; search it for history, but never read it whole or append
to it. If an operational pinned input changes, stop, produce a reviewed catalog/source diff, update
every affected hash and count, and include the scope change in the mandatory high-tier model review
and maintainer PR review; never let an upstream checkout drift silently.
## Canonical architecture and artifact ownership

The canonical product is independently versioned, VPE-neutral JSON data. Physical machine identity is primary; PinMAME driver/ROM variants attach to a physical machine, and `machine_family` groups genuine editions without erasing edition-specific hardware. A generated or flattened representation may be consumed elsewhere, but no consumer-specific implementation detail may alter canonical hashes.

Repository artifacts have distinct authority:

- `catalog/pinmame.json` is the generated driver-to-physical-machine catalog and current canonical index. It must map every in-scope driver exactly once and carry definition status and hashes.
- `controllers/pinmame/*.json` defines stable controller groups, common/platform devices, routing adapters, legal address ranges, and revision-scoped transport metadata.
- `machines/author-ready`, `machines/partial`, and `machines/stubs` contain physical-machine records honestly separated by coverage state. Moving a file between them is a validated promotion/demotion, not cosmetic organization.
- `knowledge/<manufacturer>/<machine-id>.md` contains source-linked recreation knowledge, especially mechanism behavior and edition differences that do not yet fit typed schema fields.
- `evidence/` contains portable manifests and compact derived evidence; `reports/` contains generated coverage, queue, conflict, and spatial-audit outputs. Large/source-owned artifacts remain in the configured external roots and are referenced by immutable hashes and locators.
- `rom-maps/` holds supplemental firmware maps (game and mode state, adjustments, audits, sound commands, mode-replay recipes) for one memory layout each, generated by `tools/curate_rom_maps.py`. They are ODbL-licensed as its README states, and never feed a definition, its hashes or its coverage.
- Root `index.json`, `games/`, and `platforms/` are legacy migration inputs and are not the canonical index or current source of truth. Do not update or consume root `index.json` as if its 22-game inventory represented coverage.
- Consumer-owned mappings such as VPE hints, Unity object names, input actions, regex match counts, DOF, B2S, and PUP metadata live outside the canonical catalog. Do not add `device_hint`, `device_item_hint`, `num_matches`, an open-ended consumer extension, or equivalent fields.

The legacy semantic definitions were in the managed integration's game classes, not `pinmame-dotnet`; `pinmame-dotnet` is the native interop wrapper. The legacy corpus is migration evidence, not unquestioned truth: it contains duplicate addresses, repeated RGB IDs, empty inventories, inherited definitions, label mistakes, and platform-specific merge behavior. Preserve anomalies as sourced candidates/conflicts until evidence resolves them; never silently normalize them during import.

## Identity, routing, inheritance, and mechanism invariants

- Keep `machine_id`, `machine_family`, `definition_version`, `controller_id`, exact `driver_id`, stable semantic `device_id`, controller `binding`, and legacy `alias` as distinct concepts. ROM hashes identify evidence/compatibility; ROM bytes never enter Git.
- Canonical semantic IDs are strings. Controller addresses remain signed numeric binding fields so negative diagnostic IDs are representable. A controller-number change may alter a variant binding without renaming the semantic device.
- Preserve required legacy numeric and zero-padded switch aliases such as `7`, `07`, and `007` while compatibility requires them. Alias cycles and ambiguous targets are errors.
- Controller groups have stable IDs scoped by provider authority and direction. Human display names are labels, not identity. Physical `kind` is separate from transport: a flasher routed through a solenoid callback remains a flasher.
- LibPinMAME and Controller Plugin routing are revisioned adapters. Any `ctrl://` URI is derived output, never canonical identity, and the experimental plugin API cannot become the sole representation.
- PinMAME's public switch state must be consumed exactly as delivered. `controller.inversion_applied_by_emulator` is informational and must never be reapplied as a controller-wide inversion; it does not promise that every public input is active-high. Platform and per-game notes must state any public input a driver publishes at a level other than the platform's convention, and the PinMAME revision that does so, while `physical.normally_closed` records real hardware construction separately.
- `physical.normally_closed` is a construction fact about the contact the switch matrix sees, never an inference from how an opto beam rests. Derive it, and every other per-platform question about read paths, flipper columns, special solenoids and synthesized inputs, as `docs/PLATFORMS.md` describes.
- Treat blank, merged, and omitted printed cells as distinct evidence. Preserve literal spelling, capitalization, wire order, and every authoring-relevant table column in the excerpt, including matrix connector pins and transistor identifiers; mark a genuinely blank cell explicitly and never complete it from a repeated wiring pattern or a sibling game. Keep source-literal color names in the excerpt even when the structured definition normalizes them to wiring abbreviations. If a merged cell applies to multiple normalized rows, say that it was repeated rather than presenting the duplicate as separately printed. A missing legend marking is weaker evidence than a positive construction record: when a matrix leaves a cell unshaded but the same manual's board or assembly page names that switch's part as an opto, record the construction from the assembly page, keep the unshaded cell literally in the excerpt, and explain the omission on the device instead of opening a conflict.
- Device kind, spatial applicability, and address availability answer separate questions. In particular, a virtual output has no physical playfield device, but it is `used` when PinMAME publishes meaningful runtime state and `unused` when the address is dead, reserved, or constant zero; never normalize availability solely from `kind` or `spatial.reason`. For a physical output, ROM activity alone never makes an address `used`. Record it `unused` only when the machine's own wiring or driver table proves that no load is fitted and the state PinMAME publishes there is explained, for example a proven prototype-only reset pulse. Keep it `unknown` when no source settles the fitment, or when PinMAME can still publish state there that nothing explains, such as a relay-multiplexed or PIA-driven address whose load is unfitted.
- RGB devices use a parent with explicit channel bindings or uniquely identified channel children. Mirrored/shared bindings must be declared; accidental duplicate numeric IDs are validation failures.
- Reusable physical device models and mechanism instances are separate. A mechanism references actuator/sensor device IDs, topology, ranges/marks, known causal relationships, and evidence; implementation-specific geometry, speed, acceleration, and tuning remain table-owned.
- Use only a small proven relationship vocabulary such as `direct`, `normally_closed_series`, `relay_gated`, `inverted`, and `pulse`, plus an explicit opaque escape hatch when necessary. Do not invent a general electrical scripting language or infer causality from proximity.
- Imports, where present, follow `controller base -> platform variant -> physical machine -> controller/ROM variant -> consumer overlay`, form a DAG, merge collections by stable ID, reject ambiguous scalar writers, and require explicit overrides/tombstones. Prefer shallow composition over hardware-lineage inheritance.

## Provenance, evidence states, and promotion

Every nontrivial assertion references source records carrying kind, immutable revision/hash, exact locator, extractor/tool version, acquisition or generation time, and licensing/attribution data. Manual and VPX-script sources require explicit `license` and `attribution`. IPDB evidence records the verified machine ID, machine page, direct resource URL, acquisition time, and resource hash. Internet Archive evidence records item ID, details URL, original filename, file URL, uploader, rights metadata, acquisition time, and resource hash. The repository's MIT license does not grant redistribution rights for ROMs, manuals, or community tables.

### Record what the source said, not only that it exists

A recorded SHA-256 proves the local copy has not changed under you. It does not tell a reader what the document said, and for the many sources nobody else can open - a local-only manual scan, a community table that cannot be redistributed, a web page that will rot - it conveys nothing at all about content. Do not treat a hash as though it were evidence.

Store the region you actually read as an **excerpt** beside the definition. Excerpts live under `evidence/excerpts/<machine-id>/`, are referenced from the source record by repository path and digest, and are validated fail-closed: a missing file or a digest that no longer matches is an error, not a warning. One source normally carries several, because a manual is cited separately for its switch table, its lamp table and each schematic sheet.

Rules that matter more than they look:

- **Transcribe the whole table region, not the rows you used.** An unclaimed connector pin is only visible if it is in the excerpt. Reading one endpoint per SCR and carrying another machine's list across is what dropped eight real lamp sockets from Kiss; the row that would have exposed it, `A5J3-22 SAME PLAYER SHOOTS AGAIN`, was simply never written down.
- **Cite the game's own document for game-specific facts.** Board-internal wiring is shared between machines that carry the same board, so it may be lifted; which connector branch a harness actually plugs is not, and must come from this game's sheet.
- **An excerpt is itself an assertion.** It is transcribed by the same party making the claim, so it buys self-consistency, a forcing function to open the page, and reviewability - not independent verification. Record `method` and `transcribed_by`, and set `reviewed` only when a curator has visually checked the transcription against the rendered page. OCR cleanup delegated to the low tier stays candidate evidence until it is checked.

A printed table belongs in the transcription. Use a rendered crop only when the fact is a drawing, and make it as `docs/SOURCES.md` describes.

Embedding transcribed tables is a different act from redistributing a document. A connector-pin-to-lamp-name table is factual data, and the excerpt is what makes an assertion legible without shipping the manual. The existing prohibitions are unchanged: ROM bytes, whole manuals, and community VPX tables are never committed.

Keep assertion state fail-closed and distinguish `unknown`, `candidate`, `observed`, `validated`, `conflicted`, and `deprecated`. A toggling output is only an observation, not proof of its semantic identity; failure to observe an address is never proof that it is unused. Exact agreement between sources does not prove independence when they may share ancestry.

When a manual's wiring, parts list, or assembly drawing proves that a lamp, GI string, or flasher is physically on the playfield, backbox, or cabinet while a known-working script binds a visual proxy somewhere else, split the authorities: the manual controls physical and spatial classification, while the script controls runtime binding. Record the disagreement as a conflict and do not promote the proxy coordinate as the physical device's position. Before treating a WPC-95 G.I. string as playfield or backbox, though, take its location from the game's own Power Driver Board connector list or schematic, and check it against the same row's bulb columns: the board brings the same G.I. strings out on more than one header and each game populates different pins, so a pin number means nothing without that game's board page, and a G.I. table can print the right connector under the wrong location column. The board list is not infallible either: when it alone disagrees with the table's location columns, bulb columns and string names, and misprints pins the table uses, record the table and state the disagreement on each G.I. device instead of reclassifying the strings.

### What is not a conflict

A `conflicts` entry means two sources make **incompatible claims about the physical machine** and no evidence available to this project settles which is right. It is a request for someone to go and find that evidence. Anything that does not meet that bar dilutes the ones that do: a reader who finds ten records that need nothing stops reading the eleventh that needs a harness trace.

Four things are not conflicts. The first three were mass-produced here before the rule existed.

**Two names for one device.** A platform record carries generic cabinet labels and a game record carries its own, so they disagree on wording constantly. `ROM Started` against `Game On Relay`, `Coin Button 1` against `Coin 1`, `Lower Right Flipper` against `Right Flipper`, `Tilt` against `Plumb Bob Tilt` — none of these is a disagreement about the machine, and no evidence could ever resolve one because there is nothing to resolve. Compare what the labels *denote*, never the strings. `import-legacy` applies `_names_one_device` before emitting anything and records nothing when the two names agree; a genuine disagreement such as `Ball Roll Tilt` against `Drop Target 2` still becomes a conflict, because those are two different devices claiming one address.

That helper errs deliberately towards keeping conflicts, because a false positive **deletes a real disagreement silently and permanently** while a false negative merely leaves a record someone can close later. Two rules enforce that asymmetry and must not be relaxed. Where both labels state a side, the sides have to agree — side words are stripped as qualifiers, so `Upper Left Flipper` and `Upper Right Flipper` otherwise reduce to the same thing. And equivalence beyond exact equality is an explicit written-out pair, never a subset or an open list of ignorable words: `Right Flipper Button` reduces to `flipper` and `Right Flipper EOS` to `flipper, eos`, and a subset rule merges a button with an end-of-stroke contact. A device-class word — `relay`, `solenoid`, `eos` — is never noise.

**A distinction that cannot reach a recreation.** Flipper end-of-stroke identity is the standing example. An EOS switch exists so a physical coil's power winding is cut before it burns; a virtual recreation has no coil to burn. PinMAME models no EOS at all on these platforms — the driver macros use `FLIP_SWNO` without `FLIP_SOL`, so `core.c`'s EOS simulation never runs and those addresses carry cabinet-button state instead, copied on every update from PinMAME's flipper column, which is where a consumer writes it. Do not open a conflict over which of two names belongs on such an address: state the platform's behaviour in the controller profile once, and label the address for what a consumer actually receives.

Where such a record already exists, **mark it `status: "ignored"` rather than deleting it**. Deleting is the wrong move: those addresses carry `provenance.status = "conflicted"`, and removing the record that explains it leaves an assertion no reader can account for. An ignored conflict keeps the disagreement on the page and out of the way — the validator does not count it toward author readiness, `unresolved_conflicts` must not be listed in `coverage.missing` on its account, and the reference site renders it under "recorded, not blocking" instead of the alert banner.

`status` is `unresolved` by default and absent means unresolved, so a conflict is opted out of blocking deliberately and never by omission. `ignored` requires a `rationale` saying why the answer cannot reach a recreation; the schema enforces that, because a status with no stated reason is just a way to make a blocker disappear. Ignoring a conflict does not wave the machine through: every device assertion must still be `validated` for `author_ready`, so an address left `conflicted` by the disagreement keeps blocking on its own. If the intent is to promote the machine, the device's own provenance has to be settled too — which is a reviewed pass over that address, not a status edit. Take the same care with anything adjacent that carries real information: PinMAME's synthetic flipper power/hold states at `45-48` are fabricated where no CPU driver output exists, but *which physical winding each one corresponds to* is a genuine unresolved question a table author consumes, and it is not EOS naming.

**A defect in a consumed artifact.** A retained VPX table that pulses the wrong address, comments out a lamp binding, or overwrites its own callback is a bug in that table. Nothing about the physical machine is in doubt, and the machine's `conflicts` array is the wrong place to track it: state the defect in the affected device's note, and let the definition record what the machine actually is. Reserve conflicts for the machine.

**A wiring-detail disagreement.** When sources disagree only on a connector, pin, wire colour or board designator (such as a driver transistor number), and agree on the device, its public address and its fitment, nothing a recreation consumes is in doubt. Keep both readings literally in the excerpt and state the disagreement in the device note. In structured data, follow the reading that agreeing independent sources support; when nothing settles it, use the game's own wiring table. Do not open a conflict; mark an existing one `ignored` as described above.

Before writing a conflict, answer in one sentence what evidence would settle it and who could obtain it. If that sentence cannot be written, the entry is an observation and belongs in a device note or the recreation note. If it can, **write it into the record** as a trailing `Resolution path: …` sentence — that clause is the only part of a conflict a reader can act on, and the reference site renders it as its own block. A conflict without one asks a future curator to rediscover the question before they can start on the answer. If the curator writing the entry could obtain that evidence now, obtain it instead of writing the conflict. For example, the resolution path may be a harness run on a ROM the authorized library holds, or the ROM's own service test. A resolution path that names an available, untried run is a deferred task, not an open question, and nothing schedules it.

Track coverage dimensions separately: identity, controller platform, input/output/display enumeration, semantic names, physical kind/wiring/polarity, emulator normalization, diagnostic enumeration, runtime observation, causal exercise, mechanism inventory/behavior, spatial placement, variant differences, recreation notes, provenance, and unresolved conflicts. `coverage.status` is exactly `stub`, `partial`, or `author_ready`, with a machine-readable `coverage.missing` list. Only the completeness validator may justify `author_ready`; no authoring-relevant unknown/conflict, unnamed required address, missing physical/controller variant, incomplete mechanism topology, missing spatial record, or missing recreation note may remain.

The catalog's `completion_score` is generated from the fixed sixteen values permitted in `coverage.missing` and must never be hand-authored. Stubs are always 0, author-ready definitions are always 100, and a partial receives equal credit for every requirement not present in `coverage.missing`, rounded half-up to the nearest whole percent. The schema enum and scorer requirement set must remain identical. This score is only for prioritizing and displaying progress; it does not weaken the fail-closed status, grant publication credit, or prove that a partially satisfied requirement is nearly complete. Changing the requirement set changes every partial score and requires a reviewed catalog migration.

## Evidence authority

Use the known-working VPX script as ground truth for runtime I/O semantics when sources disagree. It is the implementation proven to work in play and therefore controls controller-facing callbacks, switch assertions, output bindings, ball routing, startup behavior, and mechanism causality unless there is concrete evidence that the script is compensating for a table defect.

Use manuals and schematics as ground truth for physical construction, wiring, device presence, connector assignments, normally-open/normally-closed hardware, quantities, assembly topology, and cabinet/backbox placement. Use pinned PinMAME source and its public catalog as ground truth for emulator metadata, driver/clone relationships, controller/display topology, and transport addresses. Preserve disagreements explicitly and keep the definition fail-closed when equal-authority evidence cannot be reconciled.

Use this practical priority order:

1. Known-working retained VPX script for runtime semantics.
2. Official service manual, schematics, parts catalog, and service bulletins for physical facts.
3. Pinned PinMAME source/public API for emulator and driver facts.
4. Retained exact VPX geometry for coordinates and physical layout, reconciled against the manual and playfield image.
5. ROM static analysis, runtime harness traces, and human review for facts unavailable from the sources above.
6. Unverified scripts, screenshots, videos, forum prose, and secondary databases only as leads, never silent authority.

IPDB is useful for identity, dates, model numbers, photos, and manual discovery, but it is not infallible. Cross-check every IPDB machine ID and title against the machine you are actually curating. A VPX header has previously carried another game's identity and silently linked a definition to an unrelated title's IPDB entry, so never accept an ID that came from table metadata alone. Record stable source URLs and exact hashes. When IPDB is Cloudflare-gated, use an authenticated interactive browser, an available browser-automation interface, or Puppeteer. Archive.org is a preferred alternate source for manuals and schematics.

## Source locations and retention

Use the current Git root as the main `master` checkout and integration tree and its sibling `pinmame-game-defs-working-dir` as the external evidence and worktree root. Treat unrelated or user-authored changes in the main checkout as owned by the user; never overwrite, discard, stage, or commit them incidentally.

Where to search for tables, and how to organize retained tables, manuals and ROMs under the working root, is in `docs/SOURCES.md`.

## Model and tool allocation

Be conscious of model cost while matching capability to judgment. These tier assignments always mean the latest available model in the named family. Resolve current provider model metadata at the start of each run, verify that the selected identifier or alias works through its CLI, and record the actual resolved model in that run's evidence. Keep this policy unversioned; historical evidence records the model that actually performed the work.

| Tier | OpenAI through Codex CLI | Anthropic through Claude Code CLI | Default role |
| --- | --- | --- | --- |
| High | Latest GPT Sol at `xhigh` | Latest Opus (`opus`) at `high` effort | difficult curation, escalation, promotion decisions, and independent final review |
| Mid | Latest GPT Terra at `xhigh` | Latest Sonnet (`sonnet`) at `high` effort | structured research, implementation, spatial mapping, and test work with clear evidence |
| Low | Latest GPT Luna at `xhigh` | Latest Haiku (`haiku`) at `high` effort | bounded mechanical extraction, OCR cleanup, inventories, hashes, and report generation |

### Low tier: mechanical and low-judgment work

Delegate bounded, verifiable jobs such as file inventory, VPX object-candidate extraction, exact-name-to-coordinate mapping, device counts, evidence hashing, straightforward OCR cleanup, mechanical report generation, or drafting test fixtures from an already-decided mapping. Do not delegate source-authority decisions, semantic conflict resolution, physical-family identity, custom-mechanism conclusions, promotion decisions, or schema design to the lower-cost tier.

Every delegated prompt must include exact input paths, an exact output scope, the coordinate convention, evidence authority, non-negotiable fail-closed rules, and commands that prove success. Require the worker to report uncertainty rather than resolve it by assumption. The primary contributor must inspect the resulting artifacts and evidence rather than accepting the worker summary.

### Mid tier: structured curation and implementation

Use the mid tier for research synthesis when authoritative sources agree, deterministic curator and fixture implementation from settled requirements, spatial mapping with explicit VPX candidates, test-failure triage, and other work that requires context but not a novel authority decision. Escalate immediately when evidence conflicts, physical identity is ambiguous, a mechanism must be reconstructed, or author-ready promotion depends on the conclusion.

### High tier: curation and escalation

Use GPT Sol or Opus for source-authority conflicts, variant/family identity, physical-versus-runtime disagreements, custom mechanism reconstruction, projection policy, incomplete evidence, reverse-engineering questions, schema changes, integration conflict resolution, and promotion decisions. Inspect the actual retained evidence whenever a decision changes author readiness.

### High-tier model: mandatory pre-submission review

Before opening or updating a PR for maintainer review, have an independent high-tier model perform a read-only review of the exact proposed contribution. Prefer a different provider from the model that performed the primary curation: work led by GPT Sol should be reviewed by Opus, and work led by Opus should be reviewed by GPT Sol. If the other provider's high-tier model is available, cross-provider review is mandatory because it reduces correlated blind spots. Only when the other provider is genuinely unavailable may a fresh, independent high-tier session from the same provider be used; disclose that limitation in the PR.

Give the reviewer the base branch/commit, contribution `HEAD`, `git write-tree` hash, complete base-to-head diff and path list, unstaged/untracked state, retained evidence paths and hashes, acceptance criteria, and fresh gate results. Ask it to find discrete accuracy, provenance, determinism, schema, test, scope, and maintainability problems rather than edit files.

Verify every finding independently, fix valid issues, rerun all affected gates, and repeat the high-tier review after any material change. Record the reviewed `HEAD` and tree hash in the PR description so maintainers can tell whether later pushes invalidated it. A model review is advisory quality control, not project approval, and it never authorizes merge.

Low-severity fixes can be committed without a re-review.

The CLI calls for workers and reviewers are in `docs/SETUP.md`.

### Local tools

- Use `rg` and `rg --files` first for source/file discovery.
- Use `vpxtool` from `PATH` to inspect or extract VPX tables; retain the exact extraction and record file count, byte count, source SHA-256, and a reproducible full-file manifest.
- Use the repository's deterministic curators, catalog builder, coverage writer, validator, overlay renderer, and unit tests instead of ad hoc rewrites.
- Use `apply_patch` for repository edits. Generated catalog/coverage/queue files may be regenerated by their official Python functions.
- Use Poppler/PDF tools for rendering and extraction. Delegate straightforward OCR to a less-expensive vision-capable model, but visually inspect pages that decide mappings or physical mechanisms.
- Use an authenticated interactive browser or the available browser-automation interface for Cloudflare-gated IPDB, VPU, and VPF pages. Use Puppeteer when necessary, and ask the contributor to reauthenticate VPF or VPU if a session expires.
- Use Ghidra only after manuals, PinMAME source, known-working VPX, ROM strings/tables, and the runtime harness fail to resolve an authoring-critical behavior.

## Per-game workflow

### 1. Select and isolate the game

Check the current-state ledger's standing priorities, then the existing per-game worktrees and unmerged branches (`git worktree list`, `git branch --all --no-merged origin/master`) and open PRs/issues to avoid duplicating claimed work. Finish existing partial games before starting untouched games, ordered by physical release date newest first except for explicit maintainer priorities. Finish higher-tier and non-Pro work before opening any new Pro search; do not abandon an already-started Pro contribution merely because Pro searches are otherwise deferred.

Create one branch and one worktree per game under `<working-root>/worktrees/pinmame-game-defs-<slug>`, based on the latest reviewed `master` integration commit. Before creating it, verify that the exact target does not exist and the branch name is unused. Do not mix two games in one staged tree.

The branch and worktree are the claim, so name both after the machine slug. Record the base commit, active model tiers/sessions, evidence roots, and starting coverage status in the game's `review-artifacts` folder and, at submission, in the PR description, not in the current-state ledger.

### 2. Inventory the physical family and variants

Read `docs/IDENTITY.md` first.

Trace every PinMAME root/clone driver for the physical title. Confirm physical manufacture year, manufacturer, model, IPDB identity, editions, display/controller hardware, language revisions, prototypes, conversions, FreeWPC/community firmware, and whether any driver is virtual-only. Group only firmware compatible with the physical machine. Keep distinct physical editions separate when their playfields or hardware differ, even if they will later share a `machine_family` identifier.

Check that no obsolete stub still claims a driver moved into the curated definition. Regenerate the exact catalog after driver grouping changes and add regression tests for historically confusing identities.

### 3. Acquire and pin evidence

Read `docs/SOURCES.md` first.

Search local VPX folders before VPU/VPF. Prefer the exact physical edition; a Premium/LE table is not geometry proof for a Pro. Verify that the table script actually runs the expected ROM family. Extract the VPX with `vpxtool`, retain the original and extracted files, and compare the embedded script with any sidecar.

Acquire the official manual/schematics from the manufacturer, IPDB, Archive.org, Arcade Archive, or another attributable source. Hash the original PDF and record exact page locators. Render pages containing switch, lamp, solenoid, GI, mechanism, connector, ball-path, and playfield diagrams. If text extraction is empty or poor, OCR the relevant pages; always OCR the PDF - Windows 11 has an OCR tool. Use the stealth MCP if a website is Cloudflare gated.

Index the authorized ROM archive and PinMAME sources when needed. A retained extraction-integrity assertion must be reproducible: define the canonical manifest algorithm, include every relative POSIX path with byte size and SHA-256 in sorted order, hash canonical JSON bytes, and test recomputation against the retained extraction. Never hard-code an unexplained manifest digest.

### 4. Build the semantic definition

Read `docs/PLATFORMS.md` before deciding polarity, `normally_closed`, address availability or flipper-column handling, or binding a printed number to a public address.

Start from the existing partial or a deterministic seed. Enumerate all controller inputs, outputs, displays, mechanisms, and driver variants. Give every address a semantic disposition: used, unused, cabinet/service, duplicate/shared, or explicitly unresolved. Preserve matrix ranges and special/direct-switch namespaces exactly; do not silently drop an address because the VPX does not use it.

For each mechanism, document enough knowledge to recreate it: physical topology, moving parts, actuators, sensors and marks, switch/coil causality, ball paths, default/home state, startup behavior, timing clues, reset behavior, jams/failure modes, and edition differences. Keep this prose in `knowledge/<manufacturer>/<machine>.md` even if structured mechanism fields cannot yet express all useful details.

Relationships must express physical or proven causal behavior, not merely proximity or convenient script routing. Do not claim that an outhole coil actuates a trough switch or that a kicker directly actuates a gun mark unless the mechanism really does so.

### 5. Add normalized spatial evidence

Read `docs/SPATIAL.md` first; it holds the rules for factory drawings, baked-mesh primitives, VPX flashers, script bindings and lamp bulbs. Use the exact retained VPX table bounds and object coordinates. Normalize with the repository helper; do not hand-round inconsistently. Prefer exact physical object centers or meaningful wall/trigger centroids. Use a documented projection only when no direct physical object exists and the projection is defensible from manual/table geometry. Assign stable placement IDs and roles, enforce unique IDs, keep coordinates in range with at most six decimal places, and align quantity with placements.

Generate a machine-specific spatial audit report listing exact evidence artifacts, hashes, extraction manifest, transformation, every projection class, unresolved records, and promotion decision. When any authoring-critical placement or semantic conflict remains, keep `coverage.status = partial`, name the missing dimensions, and make the blocker concrete.

### 6. Make generation deterministic

Read `docs/TESTING.md` before writing a curator, test or manifest.

Create or update machine-specific curator scripts and pinned seeds so the canonical definition, knowledge note, and spatial report can be reproduced byte-for-byte. A curator `--check` mode must refuse drift, incomplete inputs, or overwriting an existing author-ready artifact. The seed and promoted artifact should be byte-identical when the workflow intends that invariant.

Update generated catalog, coverage, and curation queue with the official functions:

```powershell
$env:PYTHONPATH = 'src'
@'
from pathlib import Path
from pinmame_game_defs.registry import rebuild_catalog
from pinmame_game_defs.coverage import write_coverage_report
root = Path.cwd()
print(rebuild_catalog(root)["summary"])
print(write_coverage_report(root))
'@ | python -B -
```

### 7. Test fail-closed behavior

Add focused tests for identity/variants, full address enumeration, semantic mappings, mechanisms, exact evidence hashes, provenance roles, spatial positions/projections, source-root verification, deterministic curator output, catalog reconciliation, stale-stub absence, UTF-8-sensitive prose where relevant, and the precise partial/author-ready gate.

Run the complete suite both without optional evidence roots and with retained evidence roots. The no-evidence run must skip external checks cleanly rather than fail or silently weaken canonical validation. The evidence-enabled run must prove exact retained artifacts.

Typical gates are:

```powershell
$env:PYTHONPATH = 'src;tests'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m unittest discover -s tests -p 'test_*.py'
python -B -m pinmame_game_defs validate
python -B -m compileall -q src tools tests
git diff --cached --check
```

Run again with the applicable roots. Derive them automatically for the process rather than asking the human to declare them:

```powershell
$repoRoot = [System.IO.Path]::GetFullPath((& git rev-parse --show-toplevel).Trim())
$workingRoot = Join-Path ([System.IO.DirectoryInfo]::new($repoRoot).Parent.FullName) 'pinmame-game-defs-working-dir'
$env:PINMAME_VPX_SOURCES_ROOT = Join-Path $workingRoot 'vpx-sources'
$env:PINMAME_MANUALS_ROOT = Join-Path $workingRoot 'manuals'
$env:PINMAME_REVIEW_ARTIFACTS_ROOT = Join-Path $workingRoot 'review-artifacts'
python -B -m unittest discover -s tests -p 'test_*.py'
```

Also run each game curator's `--check` path twice where useful to prove idempotence. Confirm that regeneration produces no diff. Do not accept only targeted tests when shared schemas, validators, catalog, coverage, or queues changed.

### 8. Make the per-game commit

Stage only the intended game and necessary generated/shared changes. Verify branch, base commit, staged paths, zero unexplained unstaged/untracked files, and `git diff --cached --check`. Commit one game with a clear prefix, for example `defs: complete <game> spatial definition` or `defs: document <game> blockers` when it remains partial. Never combine another game's changes into that commit.

Normal fixup commits are allowed during contribution development, but the final branch must remain easy for maintainers to review and preserve one logical game change. Follow maintainer guidance on whether fixups should be squashed before submission.

### 9. Prepare, review, and submit the PR

Update the contribution branch against the latest `master` before final review. Resolve conflicts by preserving all newer upstream work and applying the game's delta. Common conflicts are generated catalog/coverage/queue files, pending spatial sets, and hard-count regression tests. A branch started before the ledger was compacted may still append a per-game narrative to `docs/CURRENT-STATE.md`: move anything in it that the game's knowledge note lacks into that note, and drop the ledger hunk. Rebuild generated files and update combined counts from the actual repository; never choose one stale side wholesale.

Run the full gates on the exact clean PR candidate, then obtain the mandatory independent high-tier model review described above. Fix valid findings and repeat both testing and model review until the reviewed `HEAD` and tree hash match the proposed PR exactly. Push the contributor branch and open or update a PR targeting `master`, including evidence locations, coverage status, gate results, and the reviewed hashes. Maintainers perform the authoritative final review and decide whether to approve or merge; contributors and model reviewers must not represent their review as maintainer approval.

### 10. Remove the completed worktree after maintainer disposition

After maintainers merge or otherwise close the PR and all wanted work is preserved remotely, remove the per-game worktree. Resolve and inspect the exact absolute target under `<working-root>/worktrees/`; verify it is the expected directory, not a reparse point, on the expected branch/commit, and completely clean. Use `git worktree remove <exact-path>` without `--force`. Stop if any check or removal fails. Never recursively delete a worktree directory, broaden the target, or discard unexplained files. Prune only stale administrative entries after the directory is safely gone.

Keep evidence archives outside the Git worktree. Removing a completed code worktree must not remove manuals, VPX tables/extractions, review artifacts, or ROM indexes.

### 11. Clean up after yourself

Several agents share the primary checkout and the working root, so anything you leave behind becomes someone else's unexplained mess. When your work has landed, or you abandon it, clean up everything you created before you report the task done. In your final report, say what you removed and what you kept.

- **Worktrees and branches.** Remove every worktree you created for the task, including detached gate and review worktrees, as described in step 10. Delete your local branches once `master` contains their commits. If a branch was rebased or squashed, first confirm that each of its changes is in `master` in some form. If `git worktree remove` fails partway and leaves a directory behind, say so rather than deleting it by hand.
- **The shared primary checkout.** Leave it clean. Do not keep uncommitted edits, staged files, or regenerated catalog and report files there after your commit lands. After a compare-and-swap onto `master`, bring your own paths in the shared checkout up to date with the new commit. Never leave the shared index holding a staged file your commit does not contain: another session's `git add -A` or whole-file commit would ship it and revert newer `master` work.
- **Processes.** Stop anything you started in the background, such as a site dev server, a harness run, a watcher, or a worker or reviewer session. A process left running keeps its directory locked, and then nobody can remove that directory.
- **Scratch files.** Put scratch scripts, logs, and patches in your session scratchpad, never in the repository or the shared checkout. Delete any that ended up in the repository root, including crash dumps and ad hoc helper scripts.
- **Anything you cannot clean up.** Leave it in place and list it with its path, why it is still needed or why removal failed, and who owns it. Do not delete another session's worktree, branch, or uncommitted work because it looks stale. Check first whether it contains anything that is not in `master` and whether a live process still holds it, and report what you find.

## Parallel work and status reporting

Do useful independent work while a worker or reviewer model runs. Separate games into separate worktrees so one review does not block another. Do not edit the same worktree concurrently, and do not let a reviewer mutate the exact tree it is reviewing. At most one contribution tree should be in conflict resolution at a time.

Report status at least hourly while work is ongoing. Include a percentage indicator, completed/in-review/blocked games, exact branches or commits when useful, current author-ready/partial/stub counts, active worker/reviewer state, concrete blockers, next actions, and whether completed worktrees, branches, background processes, and shared-checkout leftovers were cleaned (step 11). The percentage is an implementation-progress indicator, not false machine-coverage credit; author-ready coverage must always be reported separately from partials and stubs.

Keep the live task plan, `catalog/pinmame.json`, `reports/coverage.*`, and `reports/curation-queue.*` synchronized after every material change, and the current-state ledger whenever a pin or standing priority changes. Record why a game stays partial in its `coverage.missing` and knowledge note. The user explicitly asked not to stop until all supported physical PinMAME games are covered or the user says to stop; when blocked on one game, continue safe work on another rather than ending the project.

## Harness and reverse-engineering escalation

Static source extraction can enumerate controller structure but cannot prove every semantic name or
custom mechanism. Use the implemented LibPinMAME gameplay harness for unresolved runtime behavior, and
read `docs/HARNESS.md` before designing a scenario. Whatever the scenario:

- Boot only a legal user-supplied ROM, from a newly created state directory, and never commit ROM
  bytes or NVRAM.
- Retain the complete raw trace and its hashes under the working root; commit only compact derived
  evidence.
- A transition proves that a public address changed under the recorded conditions, not its physical
  identity, polarity, quantity or location, and failure to observe an address never proves it unused.
- Host input readback, such as `PinmameGetSwitch` right after a host write, is never ROM evidence.
- Escalate to Ghidra only after manuals, the VPX script, PinMAME source, ROM tables and harness traces
  fail to settle an authoring-critical fact, as `docs/HARNESS.md` describes.
