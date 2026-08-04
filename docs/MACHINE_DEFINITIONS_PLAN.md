# PinMAME machine definitions: inventory, architecture, extraction, and validation plan

Status: Implementation in progress (2026-08-04, 60%), based on the Opus-reviewed architecture and the discussion in [pinmame-game-defs PR #1](https://github.com/vpinball/pinmame-game-defs/pull/1). The physical-only cleanup was approved and committed at `e53d7c7`, the Ali physical-family correction at `59bf6bb`, AC/DC Vault Edition at `252c740`, Spider-Man Vault Edition at `c4568f5`, AC/DC LED Pro at `2a16295`, the Simpsons Pinball Party IPDB identity correction at `441527b`, The Walking Dead Premium/LE at `5e89ad4`, The Walking Dead Pro at `31e8902`, Iron Man Pro Vault Edition at `d5d585a`, Mustang Premium/LE/Boss at `9630e18`, Mustang Pro at `3c875af`, Star Trek Premium/LE at `2e1de79`, Star Trek Pro at `4b224ec`, the Star Trek Premium trough correction at `3ce4591`, Metallica Premium/LE at `4d730ab`, Metallica Pro at `c00a0c2`, original AC/DC Pro at `96bacc8`, AC/DC Premium/LE/LUCI at `411fd11`, and Avengers Pro at `998a7b3`. The remaining 18 semantic baselines stay fail-closed until each has reviewed coordinate evidence; Terminator 2 remains deferred until all 33 spatial retrofits are complete.

## Implementation status

| Workstream | Status | Current result |
| --- | --- | --- |
| Clean worktree and branch | Complete | Implementation is isolated on `codex/machine-definitions-v1` at `E:\_vpe-2025\.worktrees\pinmame-game-defs-machine-definitions`. |
| VPE-neutral schema and toolchain | In progress | Machine schema v2 adds source-backed device spatial evidence in one global `playfield` coordinate space: normalized VPX/player view with x=0 left, x=1 right, y=0 rear/backglass end, and y=1 front/apron end. v1 stubs and partials remain valid, but author-ready requires v2, validated device spatial records, resolved provenance, controlled N/A reasons, and individual lamp/GI/flasher emitter locations. `physical.location` stays construction prose and is never auto-promoted. A deterministic vpxtool candidate extractor and stdlib-only SVG overlay renderer are available; candidate points do not assert semantic controller mappings. Existing catalog, evidence, controller, manual, and runtime validation remains fail-closed. |
| Author-ready definitions | In progress | The pinned public API returns 2,873 drivers; seven custom-ROM-only virtual-table drivers are excluded, leaving 2,866 in-scope drivers grouped into 785 physical-game records plus one explicitly classified non-game diagnostic. AC/DC Vault, Spider-Man Vault, AC/DC LED Pro, The Walking Dead Premium/LE, The Walking Dead Pro, Iron Man Pro Vault, Mustang Premium/LE/Boss, Mustang Pro, Star Trek Premium/LE, Star Trek Pro, Metallica Premium/LE, Metallica Pro, original AC/DC Pro, AC/DC Premium/LE/LUCI, and Avengers Pro are committed in their per-game branches and integrated in the current tree. The regenerated catalog yields 15/785 author-ready games, 87 partial games, 683 conspicuous game stubs, and 18 remaining spatial retrofits; Scott's diagnostic is separately partial and excluded from the denominator. |
| Semantic evidence import | In progress | Existing C#/JSON data, 55 PinMAME simulations, and 1,493 in-scope scripts from the two pinned VPX corpora have been extracted with provenance. A known-working VPX script has encoded precedence for runtime addresses, callbacks, ball routing, initial state, and mechanism causality; manuals remain authoritative for physical construction and PinMAME for emulator metadata. Ripley's combines the organized official 191-page manual, exact VPW v1.3 script, exact 3.20 ROM hashes, three runtime traces, pinned Whitestar source routing, and visually verified manual pages. It resolves the complete 1-64 matrix, service/flipper inputs and DIP bank, Q1-Q32 physical wiring, optional UK outputs 33-35, public outputs 1-50 including synthetic/flipper-compatibility traps, lamps 1-80, four fused GI strings behind GI 0, one 128x32 DMD plus three indexed native 5x7 mini-DMDs, and the seven declared startup-active switches. |
| Recreation knowledge | In progress | A conspicuous stub note exists for every unresolved root. Complete source-linked Ripley's notes now cover the four-ball path, shooter, two VUKs, visible three-seat lock, seven-detent vari-target with threshold order and tuning baseline, Idol Eye and Shrunken Head magnet causality, three-flipper Whitestar remapping, diverters, top and optional UK posts, six pops, slings, elevated mini-playfield, all lighting circuits, and the native-versus-legacy mini-DMD distinction. Earlier detailed product notes remain unchanged. |
| Static catalog site | Pending after Terminator 2 | Copy the existing `E:\_vpe-2025\pinmame-games` static site into `site/`, configure and verify GitHub Pages for `games.visualpinball.org`, obtain Opus approval, commit, integrate to `main`, push, and verify the deployed endpoint before reporting the exact DNS target. |
| Machine families and edition notes | Pending after spatial retrofits | Add a stable physical-machine family identifier so editions such as AC/DC Pro, Premium, LE, Luci, LED Pro, and Vault resolve under one game family without conflating unrelated machines that share a theme. Research and preserve concise prose explaining the physical and rules/hardware differences among each family's editions. |
| VPE hint patcher sunset | Pending | VPE consumes stable IDs/roles and explicit table mappings; legacy hint matching is not migrated into the canonical catalog. |
| Validation and Opus review | In progress | The physical-only cleanup, Ali correction, AC/DC Vault, Spider-Man Vault, AC/DC LED Pro, TSPP identity correction, Walking Dead Premium/LE, Walking Dead Pro, Iron Man Pro Vault, Mustang Premium/LE/Boss, Mustang Pro, Star Trek Premium/LE, Star Trek Pro, the corrective Star Trek Premium trough/Q22 pass, Metallica Premium/LE, Metallica Pro, original AC/DC Pro, AC/DC Premium/LE/LUCI, and Avengers Pro were approved and committed in their per-game branches. X-Men LE/Pro, Transformers Pro, TRON LE/Pro, Rolling Stones, Avatar, and Dark Knight work remains active or fail-closed in isolated worktrees. Every per-game commit remains gated by a fresh literal Opus `APPROVED` on its exact staged tree. |

### Spatial retrofit sequence

The canonical `playfield` space is defined globally once: normalized VPX/player view with x=0 at left, x=1 at right, y=0 at the rear/backglass end, and y=1 at the front/apron end. Per-machine `physical.location` is construction prose only; it must never be converted into a coordinate automatically. The extractor emits candidate object centers and their source hash, not semantic mappings or canonical placements. Each reviewed title promotes its own explicit sensor/effect/emitter placements with provenance, and GI/flasher/lamp circuits enumerate their individual emitters.

Acquire table candidates in this order: `L:\Visual Pinball\Tables`, `L:\Visual Pinball\Tables Archive`, `vpuniverse.com`, then `vpforums.org`. The local inventory finds title candidates in a primary folder for 31 of the 33 records, archive-only fallbacks for two, and 17 that still require edition disambiguation. The Ali identity correction is complete; its spatial retrofit remains at the 1980 physical-machine position. Spatial retrofit proceeds by physical release year, newest first, one Opus-reviewed commit per title/game, with each active game isolated in its own worktree so review does not block discovery or implementation of the next game. AC/DC Vault Edition (2018), Spider-Man Vault Edition (2016), AC/DC LED Pro (2014), The Walking Dead Premium/LE (2014), The Walking Dead Pro (2014), Iron Man Pro Vault Edition (2014), Mustang Premium/LE/Boss (2014), Mustang Pro (2014), Star Trek Premium/LE (2013), Star Trek Pro (2013), Metallica Premium/LE (2013), Metallica Pro (2013), original AC/DC Pro (2012), AC/DC Premium/LE/LUCI (2012), and Avengers Pro (2012) are committed; 18 spatial records remain before Terminator 2.

### Pinned implementation inputs

| Input | Revision | Current inventory |
| --- | --- | --- |
| `vpinball/pinmame` | `4ec52ff0ac133ac251681518aed2249e19fe26eb` | Fresh Windows x64 LibPinMAME build; public API returns 2,873 drivers. Seven custom-ROM-only virtual-table drivers are excluded, leaving 2,866 in-scope drivers, eight omitted abstract parent containers, and 772 clone-tree roots resolved to 785 physical-game records plus one non-game diagnostic. |
| `vpinball/pinmame-dotnet` | `e3e31eea6cd8eb046b4a8ea3110a31bb19c32b45` | Current managed wrapper and 11 hand-maintained definition source model. |
| `VisualPinball/VisualPinball.Engine.PinMAME` | `cf2030710f9a6ee19fdbeec9cc9fccaba2032a6f` | Current VPE integration and legacy mapping consumer. |
| `sverrewl/vpxtable_scripts` | `0c036bb61b4b4e8c778c37559f6795df8cd1521e` | 1,216 `.vbs` files, of which 1,189 declare `cGameName`. |
| `jsm174/vpx-standalone-scripts` | `15d112648a1b94b9f59eb8b3c335d57283653c50` | 284 `.vbs` files, of which 280 declare `cGameName`. |
| Existing `pinmame-game-defs` corpus | `4ea106d080728648a693af3b4dcabb091eee0a02` | 81 legacy game files, five platform files, and an incomplete hand-maintained index. |

## Executive recommendation

Keep machine definitions in this repository as independently versioned JSON data, not as C# subclasses compiled into every VPE PinMAME package. VPE should download or update the authoring catalog independently, cache it locally, and embed only the resolved definition used by a table into that table's package so runtime playback remains deterministic and offline.

The reviewed physical-machine scope excludes seven PinMAME drivers whose custom ROMs exist only for community virtual tables: `acd_170_ac`, `beachbms`, `beav_butt`, `bubba`, `che_cho`, `rambo`, and `tomjerry`. The scope audit deliberately retains ordinary physical-machine ROM mods and conversions, including `clash` because its ROM is documented for a real Rock Encore conversion, and `mac_zois` because machinaZOIS was a physical pinball art installation despite “Virtual Training Center” appearing in its title.

Do not confuse “generated” with “covered.” PinMAME can generate a complete raw ROM inventory and useful controller structure, but custom ROMs made only for community virtual tables are outside this physical-machine project. Every in-scope driver must correspond to a manufactured or buildable physical machine, and PinMAME usually does not contain the semantic playfield names needed to recreate it. A physical machine is covered only when its resolved definition is author-ready: it completely identifies the switches, lamps/GI, controlled devices, displays and mechanisms needed to recreate the game; gives usable semantic names, kinds, bindings, polarity and cabinet roles where relevant; models variant differences; and has no unresolved conflict or unknown that affects authoring. Build a layered pipeline that distinguishes scaffolds, candidates, observations, validated facts, and author-ready definitions. Seed it from PinMAME and existing VPX/VPE data, then validate it with deterministic service-menu and gameplay scenarios modeled on Kiki. Use Ghidra as a platform-specific supplemental extractor after cheaper sources have been exhausted.

Retain the useful ideas from PR #1—controller-qualified identifiers, hardware-neutral device groups, shared device models, and hierarchical reuse—but revise the format before batch conversion. In particular, the schema must group ROMs under physical machines, route both today's LibPinMAME API and the experimental Controller Plugin API explicitly, exclude VPE authoring hints from canonical data, define deterministic inheritance, and attach provenance and validation evidence.

## Questions this plan answers

- What machine-definition data exists today, who owns it, and how is it consumed?
- What can be extracted from PinMAME for all games, and what exists only for simulated games?
- How should definitions be represented, versioned, distributed, cached, and embedded?
- How should the proposed PR #1 format change before more games are converted?
- How can runtime playthroughs validate mappings without confusing activity with identity or completeness?
- Where is Ghidra useful, and where would it become an expensive dead end?
- How can VPE migrate without breaking existing serialized tables and packages?

## Evidence baseline

The inventory below is tied to these checked-out or inspected revisions so that its counts remain reproducible:

| Source | Revision inspected | Notes |
| --- | --- | --- |
| `pinmame` | `de2985d4b19d13c8046e3b12eb1c1fef578fb8b8` | The locally built LibPinMAME used for runtime inventory; upstream `master` had subsequently advanced to `3a5ce504118c6cb79bd365db12d6baec08708aaf`. |
| `pinmame-dotnet` | `e3e31eea6cd8eb046b4a8ea3110a31bb19c32b45` | Its PinMAME submodule was `81333070d93b955cbe589def97c38a7eed15e056`. |
| `VisualPinball.Engine.PinMAME` | `cf2030710f9a6ee19fdbeec9cc9fccaba2032a6f` | Contains the C# definitions and VPE integration discussed here. |
| `pinmame-game-defs` base | `4ea106d080728648a693af3b4dcabb091eee0a02` | Existing JSON corpus on `master`. |
| `pinmame-game-defs` PR #1 | `e87d57fbb9baf38bdb3786bd7631bcaf10ebb019` | Latest fetched `origin/t2_alt_format` head, converting T2 and WPC to an alternative schema. The local checkout is one commit behind at `46006b0`; its two converted files are invalid JSON, while both files parse at the fetched head. |
| VPX Controller Plugin experiment | `vbousquet/pinmame@a6f6d7266d301249ed09c1b0123f8476513a2228` | Exact fork revision selected by the local VPX build; this API is explicitly marked pre-alpha and unstable. |

Repository-local uncommitted files and unrelated binary/plugin changes were left untouched during this analysis.

## Inventory: current VPE and pinmame-dotnet implementation

### Ownership is different from the initial assumption

The machine definitions are not in `pinmame-dotnet`. That repository contains the managed LibPinMAME interop layer: numeric switch access, changed lamp/GI/solenoid polling, display and audio callbacks, and mech configuration. The hand-maintained semantic mappings live in `VisualPinball.Engine.PinMAME/VisualPinball.Engine.PinMAME/Games`.

This distinction matters because removing the C# definitions does not require redesigning the P/Invoke wrapper first. The first migration can replace only VPE's definition provider and keep the existing LibPinMAME runtime calls.

### Current C# definition inventory

There are 11 concrete game classes: Attack From Mars, Centaur, Creature from the Black Lagoon, Flash Gordon, Medieval Madness, Rock, Rock Encore, Star Trek Enterprise, Terminator 2, The Walking Dead, and TRON Legacy. Four MPU base classes—Bally, SAM, System 80, and WPC—supply shared cabinet switches, flipper coils, and aliases. `PinMameGame` itself supplies the same four direct flipper relationships to every game; they are not separate per-MPU arrays.

The current model is `PinMameGame`, with identity and ROM metadata plus `AvailableSwitches`, `AvailableCoils`, `AvailableLamps`, `AvailableAliases`, and `AvailableWires`. The platform and game lists are merged in C#, and four universal flipper coils are also injected. Numeric controller IDs are translated to semantic IDs through `PinMameIdAlias`.

The migrated 11-game corpus contains 99 ROM IDs, 457 game-specific switches, 260 game-specific coils, 816 game-specific lamps, and 12 game-specific aliases. Shared platform entries are additional. This is a small curated subset of PinMAME's supported catalog.

| Definition ID | Game-specific switches | Game-specific coils | Game-specific lamps | Game-specific aliases | Inventory note |
| --- | ---: | ---: | ---: | ---: | --- |
| `afm` | 50 | 35 | 64 | 0 | Two coil entries share the label “Right Slingshot.” |
| `centaur` | 48 | 16 | 60 | 0 | Coil ID 5 occurs twice. |
| `cftbl` | 41 | 28 | 64 | 0 | Migrated mechanically into the existing JSON corpus. |
| `fg` | 39 | 16 | 0 | 0 | The C# lamp array is explicitly empty. |
| `mm` | 50 | 33 | 64 | 0 | WPC inheritance supplies shared entries. |
| `rock` | 28 | 8 | 51 | 4 | Rock Encore reuses this definition unchanged. |
| `rock_enc` | 28 | 8 | 51 | 0 | Inherits Rock rather than declaring a separate device inventory. |
| `star-trek-stern` | 49 | 29 | 220 | 0 | Large SAM-era lamp inventory includes repeated label text. |
| `t2` | 49 | 32 | 68 | 4 | PR #1's schema experiment uses this definition. |
| `trn` | 44 | 30 | 64 | 0 | SAM-era mapping. |
| `twd` | 31 | 25 | 110 | 4 | Three RGB channels use lamp ID 81 in the legacy model. |

| C# MPU base | Shared switches | Shared coils | Aliases |
| --- | ---: | ---: | ---: |
| Bally | 12 | 5 | 13 |
| SAM | 13 | 4 | 14 |
| System 80 | 11 | 5 | 12 |
| WPC | 12 | 5 | 13 |

The C# data already contains inconsistencies that a schema validator should surface instead of silently accepting: Centaur defines duplicate coil ID 5; The Walking Dead represents three RGB channels with the same lamp ID 81; Flash Gordon has an explicitly empty lamp array; Rock Encore inherits Rock unchanged; and several labels are duplicated or visibly mistyped. These should initially be migrated faithfully and marked as conflicts or candidates, not silently “fixed” without evidence.

### Current consumption and packaging

`PinMameGamelogicEngineInspector` hardcodes instances of all 11 classes for its game selector. `PinMameGamelogicEngine.UpdateCaches` merges aliases and builds lookup dictionaries consumed by VPE mapping. Packaging serializes both the assembly-qualified C# `GameType` and `GameId`; unpacking first uses reflection and then scans loaded types by ID. As a result, the definitions and their type identities ship with every package release and are coupled to assembly releases.

The target state should serialize a stable machine-definition reference and content hash. Reading the legacy `GameType` must remain as a compatibility path, but newly written packages should not depend on a subclass name.

### Current property coverage

Switches carry controller ID, polarity, pulse behavior, description, input-map hints, device matching hints, match count, and a constant hint. Coils carry controller ID, description, matching hints, match count, lamp/unused flags. Lamps add channel, fading steps, source, and lamp type. Wires connect a source semantic ID to a coil, lamp, or GI destination.

These properties mix three domains that must be separated during migration: controller facts, physical-machine facts, and VPE authoring heuristics. A switch number is a controller fact, but consumer-visible polarity is not: PinMAME's `core_setSw` and `core_getSw` already XOR the per-game inversion mask so public state means logically active even for active-low switches. Physical `normally_closed` belongs to physical data, while the emulator's inversion mask is informational provenance that consumers must never reapply. “Left Outlane” is physical-machine metadata. Unity `device_hint`/`device_item_hint` regexes, `num_matches`, and input-map actions are obsolete authoring heuristics: the importer reports and drops them, the schema rejects them, and the VPE hint patcher is sunset instead of being fed by the new catalog.

### Mechs are not currently C# game-definition data

Contrary to the initial description, current `PinMameGame` classes do not declare mechs. Each Unity table authors `PinMameMechComponent` instances with type, timing, length, acceleration/retardation, solenoid mappings, and switch marks. At runtime VPE numbers registered components and sends `PinMameMechConfig` through LibPinMAME. The JSON corpus has already experimented with `mechanisms` in four files, so the migration importer must preserve and classify that data even though it has no direct C# counterpart. The claim in PR #1 that mechs can already be queried from the API does not remove the need for catalog topology: public `PinmameMechInfo` exposes only anonymous type, length, steps, position, and speed, not actuator wiring, switch marks, or semantic identity.

The catalog should describe logical mechanisms—actuators, sensors, topology, expected causal relationships, and known PinMAME simulation hooks—but it should not automatically replace the Unity table's physical timing and geometry. Those physical values are table-implementation data and may legitimately vary between VPE recreations.

## Inventory: existing `pinmame-game-defs`

The repository already provides valuable migration input. It contains 81 game files and five platform files. The original phase migrated the 11 C# definitions, while subsequent extraction added data from VPX VBScript. The local evidence corpora currently expose 1,799 paths under `vpxtable_scripts` and 962 paths under `vpx-standalone-scripts`; committed tools must inventory eligible `.vbs` files precisely, hash each source, extract `cGameName`/controller IDs and I/O candidates, deduplicate table revisions, and keep their provenance distinct. A working-tree inventory at local commit `46006b0`, skipping its syntactically invalid T2 conversion, counted approximately 3,631 switches, 1,996 coils, and 5,198 lamps; these are discovery figures rather than release metrics and must be regenerated from pinned inputs by a committed inventory tool.

The corpus is not yet a dependable database release: `index.json` lists only 22 games despite 81 files; the parseable local files use 16 platform spellings against five platform documents (`dataeast`/`de`, `s11`/`system11`, and several families with no profile); provenance quality ranges from mechanical C# conversion to parser inference; and the PR #1 branch intentionally mixes the new T2/WPC shape with old-schema files. Schema drift also includes `gi`, `flashers`, `gi_strings`, `mechanisms`, `lamp_coils`, `_dof_events`, `_commented_out`, and note fields, while `ij.json` lacks the normal format/version/source envelope. The repository also has no license at the inspected revision despite containing PinMAME- and community-table-derived facts. This is normal experimental state, but it means bulk generation and release must wait for parse/schema validation, generated indexes, a platform alias policy, and a licensing/attribution decision.

The plan should evolve this repository rather than start another data repository. Existing files become import sources into the new canonical model, with their source and confidence preserved.

## Inventory: what PinMAME can provide

### Complete catalog metadata

`PinmameGetGames` returns the complete driver set compiled into a particular LibPinMAME build. A local exploratory query reported 2,854 drivers, including 698 roots and 2,156 clones, but the binary provenance and generator inputs were not captured strongly enough to make those literals a baseline gate. The committed generator must make its pinned build manifest authoritative and record the count it actually returns. The public `PinmameGame` structure provides driver name, clone parent, description, year, manufacturer, flags, and environment-dependent ROM availability, which is enough to generate a revision-stamped driver catalog and candidate family graph.

Clone relationships are not automatically equivalent to “same physical machine wiring.” Some clones are language, revision, bootleg, or modification variants, while some relationships exist for implementation reuse. The generator should propose physical-machine groupings from the clone graph and normalized metadata, then preserve a reviewable exception table.

### Broad structural metadata

After a ROM starts, PinMAME internally knows the hardware generation, configured switch columns, lamp columns, custom solenoid count, common switches, switch/lamp remapping functions, emulator-applied inversion masks, physical output counts/types, display layout, and custom mech handlers. `core_tGameData`, `core_tGlobals`, and physical-output configuration provide much of this data. Inversion is useful to document emulator normalization and test the exporter, but it must not become a consumer-applied polarity instruction.

The stable LibPinMAME ABI does not expose most of these details. Its `GetMax...` functions often return compile-time maxima rather than the active machine's true inventory, and its public game catalog has no playfield device names. The preferred extractor is therefore a small PinMAME-side dump executable built with access to internal structures, emitting versioned seed JSON after machine initialization. A stable, versioned introspection ABI can follow later if VPE also needs these facts live.

### Experimental Controller Plugin API

PR #1 targets the generic Controller Plugin model used by newer VPX work. The exact VPX-selected PinMAME fork exposes inputs and controlled devices as `(groupId, deviceId)` pairs and maps legacy outputs into groups such as main outputs, auxiliary outputs, custom outputs, internal states, GI, lamps, and emulated mechs. It provides actual machine-dependent lists and generic labels such as `Switch #23`, `Output #05`, and `Lamp #31`.

This is useful for enumeration and routing, but it does not solve semantic naming: its labels are generated from controller addresses. It is also explicitly documented as pre-alpha, currently lives in a fork rather than the inspected `vpinball/pinmame` master, and is not what VPE's C# runtime consumes today.

The schema should therefore use hardware-neutral group identifiers as its canonical address model while defining transport adapters for both LibPinMAME and Controller Plugin group IDs. Controller Plugin group identity is scoped by provider authority and direction because inputs and controlled devices both legitimately use exact group `0x0001`; controlled-device group `0x0001` is the main output subgroup, while `(groupId & 0xff00) == 0x0000` is only its broader output family. VPE need not block the data project on switching controller APIs.

### Simulation source metadata

`pinmame/src/wpc/sims` contains 55 machine simulation drivers: 32 full and 23 preliminary. All have simulation state data; 42 mention custom mech handling; 28 expose mech queries; and 22 include lamp layouts. Source scanning found roughly 2,328 named switch macros and 829 named solenoid macros.

These files are the richest PinMAME-native semantic source because state names and macros often identify troughs, targets, ejects, motors, and solenoids. The 55 simulations cover only a small minority of the root drivers observed in the local build, and preliminary simulations can be incomplete. The committed inventory will calculate the exact ratio for its pinned manifest. Extracted identifiers must carry their exact source location and must begin as candidates unless independently verified.

### Other PinMAME sources

Driver declarations and `PinmameGetGames` cover ROM metadata and clone families. `core_tLampDisplay` carries visual coordinates and colors, not semantic names. MAME input ports and `-listxml` primarily describe cabinet/emulator controls and DIP switches, not every playfield switch, coil, and lamp. Platform driver code supplies mappings and physical output types but usually not game-specific labels.

The practical generation ceiling from PinMAME alone is therefore: 100% catalog identity, broad hardware/address structure after initialization, partial semantic mappings for the 55 simulation drivers, and sparse mechanism semantics. It cannot produce trustworthy human-readable definitions for every machine by itself.

### Automation feasibility matrix

| Source | Expected reach | Facts it can supply | Initial status | Primary limitation |
| --- | --- | --- | --- | --- |
| `PinmameGetGames` | Every compiled driver | Driver ID, clone parent, description, year, manufacturer, flags | Generated | Clone graph is not guaranteed to equal physical-machine identity; ROM availability is environment-dependent. |
| PinMAME initialized internal state | Every runnable driver | Hardware generation, real address groups/counts, remaps, emulator-normalization masks, displays, output types, hook presence | Generated | Requires a PinMAME-side exporter; inversion is informational and must not be reapplied by consumers. |
| PinMAME `comSw`, `invSw`, and `mech_tInitData` | Platform/game definitions where present | WPC start/tilt/slam/coin-door/shooter identities, internal active-low normalization, and explicit mech actuator/switch topology | Generated or candidate by field | Coverage is uneven; `invSw` describes emulator internals, while mech arrays need semantic source locators and review. |
| Experimental Controller Plugin API | Every runnable driver supported by the fork | Enumerated inputs/devices, generic names, group and device IDs, derived `ctrl://` addresses | Generated, revision-scoped | Pre-alpha fork API and generic labels do not provide playfield semantics. |
| `src/wpc/sims` | 55 current simulation drivers | Named switch/solenoid macros, state names, lamp layout, partial mech topology | Candidate | Only 32 full and 23 preliminary simulations; runtime reuse has a switch-ownership gate. |
| Existing VPE C# | 11 machines / 99 ROM IDs | Curated names, aliases, hints, direct wires | Candidate until migrated and checked | Hand-maintained, includes known duplicates/collisions, compiled into releases. |
| Existing JSON and VPX script extraction | 81 current files plus the pinned `vpxtable_scripts` and `vpx-standalone-scripts` corpora | Names, mappings, callback behavior, ball routing, and mechanism implementations | Candidate or validated after exact-script review | Mixed schemas and parser inference require care, but a known-working VPX table script is the project tie-breaker for controller addresses, callback behavior, ball routing, and mechanism causality. |
| IPDB machine records and hosted manuals | Browser-mediated lookup because Cloudflare gates unattended clients | Manufacturer/model identity, features, manuals, parts lists, schematics, switch/lamp/solenoid tables, and service bulletins | Candidate or validated after exact page reconciliation | Record the IPDB machine ID and resource URL; hash every acquired document; respect document ownership and do not assume redistribution rights. |
| Internet Archive items | Public item metadata and download interfaces | Alternate manual scans, schematics, parts lists, service bulletins, OCR derivatives, and stable item identifiers | Candidate or validated after document reconciliation | Preserve item/file identifiers, uploader and rights metadata; prefer original scans over generated OCR PDFs; deduplicate against IPDB by SHA-256. |
| ROM service diagnostics | Broad but platform/revision dependent | ROM-presented input/output names, emulator-normalized active-state behavior, enumeration, output correlation | Observed or validated with trace | Cannot recover physical normally-closed wiring by toggling LibPinMAME's already normalized public switch state. |
| Gameplay scenarios / digital twin | Incremental per curated machine | Causal actuator-sensor relationships and end-to-end behavior | Validated | Physical playfield is absent from emulation and must be modeled. |
| Static ROM screening and Ghidra | Targeted platforms only | Diagnostic tables, strings, dispatch/mech relationships where present | Candidate, then validated separately | Architecture diversity, bank switching, sparse strings, and high maintenance cost. |

### Source map for implementation

| Path | Role in this plan |
| --- | --- |
| `VisualPinball.Engine.PinMAME/VisualPinball.Engine.PinMAME/PinMameGame.cs` | Current abstract C# definition model, universal coils, direct flipper wires, and merge helpers. |
| `VisualPinball.Engine.PinMAME/VisualPinball.Engine.PinMAME/Games` | Eleven concrete hand-maintained definitions. |
| `VisualPinball.Engine.PinMAME/VisualPinball.Engine.PinMAME/MPUs` | Four current shared C# platform definitions and negative diagnostic aliases. |
| `VisualPinball.Engine.PinMAME/VisualPinball.Engine.PinMAME.Unity/Runtime/PinMameGamelogicEngine.cs` | Definition consumption, legacy alias behavior, bare-integer lamp/GI cache, reflection packaging, and mech registration. |
| `pinmame-dotnet/src/PinMame/PinMame.cs` and `PinMameApi.cs` | Managed numeric LibPinMAME API and native bindings. |
| `pinmame-dotnet/src/PinMame/PinMameMechConfig.cs` | Managed mech configuration passed from VPE-authored components. |
| `pinmame/src/libpinmame/libpinmame.h` and `libpinmame.cpp` | Public catalog/runtime ABI, environment-dependent ROM availability, and potential introspection entry point. |
| `pinmame/src/wpc/core.h`, `sim.h`, and `sims` | Internal hardware/game structures and partial semantic simulation data. |
| `pinmame/src/libpinmame/libpinmame.cpp` (`SetupMsgApi`) | Generic group/device transport IDs consumed by controller integrations. |
| `Kiki/tools/profilegen`, `Kiki/tools/playtest`, and `Kiki/docs/NEW_GAME_PLAYBOOK.md` | Fail-closed static extraction, replayable evidence, and causal scenario methodology. |

## Inventory: transferable lessons from Kiki

Kiki's strongest reusable idea is not Ghidra itself; it is the separation between inventory, provenance, and proof. Its profile generator uses exact-version signatures, dataflow checks, uniqueness requirements, sibling ordering, image-base validation, and fail-closed `verified` flags. A generated value is not accepted merely because a pattern matched once.

Its runtime harness records semantic display state, exact input actions, output histories, causal bookmarks, checkpoints, and bounded scenarios. Scenarios can pulse a switch, mark output history, wait for a particular output after the mark, synthesize a physical response, and assert the resulting display or controller state. Recordings are durable evidence; transient save states are only acceleration aids.

The PinMAME project should copy those principles: exact ROM and emulator hashes, reproducible extractors, explicit verification levels, scenario evidence, and fail-closed promotion. It should not copy Kiki's platform-specific binary addresses or assume that one ROM signature strategy generalizes across decades of CPU architectures.

## Assessment of PR #1's proposed format

### Ideas to keep

- Keep controller-qualified identities, using an unambiguous string such as `pinmame.t2` rather than two adjacent namespace values.
- Keep hierarchical reuse for controller families, platform variants, physical machines, and true wiring variants.
- Keep hardware-neutral input/device groups so the model can represent Bally 6803, WPC, SAM nodeboards, extension boards, DIP switches, and future controllers without pretending every output is a WPC lamp or solenoid.
- Keep reusable device models when they add physical information such as coil model, bulb type, motor characteristics, or relay behavior.
- Keep a generated index so consumers can find one physical machine first and then choose a compatible ROM.

### Changes required before batch conversion

- Separate physical machine identity from controller driver identity. PR #1 already has an abstract T2 node imported by ROM-variant nodes, which is the right reuse shape, but machine and ROM nodes are untyped members of the same `games[]` array and share a controller-scoped identifier namespace. Preserve the variant-import pattern while giving physical machines, controller platforms, and PinMAME driver variants distinct typed layers and namespaces.
- Replace display names such as `group_name: "Switch Matrix"` as identity with stable machine-readable group IDs. Human labels belong in group definitions and may be localized later.
- Make routing explicit through group definitions. Each group should identify provider authority, direction, and logical kind and provide optional adapter bindings such as `libpinmame.channel = "solenoid"` and `controller_plugin.group_id = 1`, with the plugin numbering contract pinned to a source revision. This resolves the PR discussion without making the schema depend exclusively on either API.
- Keep device classification separate from routing. `kind: flasher` tells the editor what the physical device is; a controller binding tells the runtime where its state comes from. A flasher may be routed through a legacy solenoid channel without becoming a solenoid in the physical model.
- Define imports as a directed acyclic graph with typed layers and deterministic merge rules. Arbitrary multi-inheritance with unspecified precedence will produce silent resets and hard-to-review results.
- Separate reusable device model IDs such as `coil.ae-26-1200` from mechanism instances such as `t2.gun`. A motor instance may reference a device model, but the two are not the same concept.
- Make stable semantic device IDs canonical and legacy aliases mandatory during migration. The importer must preserve current numeric IDs plus the zero-padded switch spellings accepted by `UpdateCaches`, including values such as `"7"`, `"07"`, and `"007"`; removing aliases without this rule breaks already serialized mappings.
- Define all semantic identifiers as canonical strings while keeping signed numeric controller addresses in typed binding fields. This eliminates PR #1's current string/integer ID mixture while preserving negative Bally, SAM, and System 80 diagnostic switch addresses.
- Drop `device_hint`, `device_item_hint`, `num_matches`, and VPE input-map actions during migration with a machine-readable report. Portable cabinet semantics such as start, coin, service, and flipper controls become namespaced logical roles; VPE owns role-to-input-action configuration. Noncanonical consumer metadata such as DOF/B2S/PUP stays in external overlays and is never required to resolve a machine definition.
- Add field- or assertion-level provenance and validation. File-level `_source` cannot represent a definition assembled from PinMAME, a manual, a VPX script, and a runtime diagnostic.
- Replace unrestricted `wires` with a small relationship/circuit vocabulary for common cases and an opaque extension escape hatch. Do not attempt a general electrical or EM scripting language in schema version 1.
- Add JSON Schema, semantic validators, canonical formatting, generated indexes, and compatibility fixtures before converting the remaining corpus.
- Make raw JSON parseability the first CI gate. Use PR #1's current `group_name`/`group_id` mismatch, mixed ID types, `gi`/`GI` model-reference mismatch, and conflicting WPC/Fliptronic output 31 definitions as concrete failing resolver/linter fixtures rather than repairing them implicitly.

## Proposed repository and artifact model

Use five artifact types with distinct responsibilities:

1. `catalog/index.json` is generated from PinMAME and the curated machine registry. It maps every in-scope PinMAME driver ID to a physical machine, definition file, definition version, compatibility status, and content hash; custom-ROM-only virtual-table drivers are rejected before stub generation.
2. `controllers/pinmame/*.json` defines stable controller groups, platform layouts, common cabinet inputs, routing adapters, address constraints, and platform-specific extraction metadata.
3. `machines/<manufacturer>/<machine-id>.json` defines one physical machine, its controller variants, inputs, controlled devices, logical mechanisms, relationships, aliases, provenance, and author-readiness state without VPE-specific fields.
4. `knowledge/<manufacturer>/<machine-id>.md` preserves source-linked recreation knowledge that is useful but not yet stable enough for a schema: custom-mechanism operation, actuator/sensor causality, ball paths and state transitions, startup/home behavior, service adjustments, timing clues, unusual wiring, physical assembly notes, ROM expectations, and implementation pitfalls.
5. `overlays/*.json` contains narrowly scoped project-local corrections that can be promoted to canonical facts after validation. Consumer-owned VPE, DOF, B2S, or PUP configuration lives outside the canonical catalog and cannot affect its hashes or resolver output.
6. `evidence/<machine-id>/<run-id>/` stores immutable manifests, scenario results, compact event traces, extracted display text, and artifact hashes. Large recordings or images may live in release/object storage with content-addressed references rather than Git.

Keep author-edited source documents normalized and readable. Generate a resolved, flattened representation for consumers and tests; never require VPE runtime code to implement the full inheritance engine.

### Proposed identity hierarchy

- `machine_id`: stable physical product identity, for example `williams.terminator-2.1991`.
- `definition_version`: semantic version of the curated machine definition, independent of VPE and PinMAME releases.
- `controller_id`: controller namespace, initially `pinmame`.
- `driver_id`: exact PinMAME ROM set name such as `t2_l8`.
- `rom_identity`: optional region hashes for evidence and compatibility; hashes are recorded, ROM bytes are never stored.
- `device_id`: stable semantic instance ID such as `switch.trough.left` or `device.gun.motor`, distinct from its numeric controller binding.
- `binding`: controller address comprising provider authority, direction, group plus signed device number and, where needed, channel or matrix coordinates.
- `alias`: a deprecated or consumer-facing alternate ID that resolves to one stable device ID.

Changing a controller number should not force every VPE table mapping to change. The stable device ID remains constant while a controller-variant patch changes the binding.

### Proposed group and routing model

Controller profiles should define groups once and devices should refer to them by stable ID. An abbreviated example follows:

```json
{
  "id": "pinmame.output.main",
  "authority": "pinmame",
  "direction": "controlled_device",
  "label": "Main driver outputs",
  "transports": {
    "libpinmame": { "channel": "solenoid" },
    "controller_plugin": { "group_id": 1, "contract_revision": "a6f6d7266d301249ed09c1b0123f8476513a2228" }
  }
}
```

A device instance then separates identity, physical kind, and routing:

```json
{
  "device_id": "device.gun.motor",
  "label": "Gun motor",
  "kind": "motor",
  "model": "motor.t2-gun",
  "binding": { "group": "pinmame.output.main", "device": 11 }
}
```

This supports VPE's current event routing, the experimental plugin API, and non-WPC hardware without duplicating transport knowledge on every device. Group-ID uniqueness is scoped by `(authority, direction)`, so input group 1 and controlled-device group 1 are distinct. Groups may declare a transport unavailable; validators should reject a definition that cannot be routed by a declared consumer compatibility target.

The resolver should also generate VPX Controller Plugin resource URIs where the adapter contract is available, for example `ctrl://pinmame/device?grp=1&io=11`, while keeping that URI derived rather than canonical. This makes the catalog useful to existing `ctrl://` consumers without allowing an unstable pre-alpha URI contract to become the machine's identity.

### Device and mechanism model

Use a small, extensible `kind` taxonomy: `switch`, `dip_switch`, `coil`, `flasher`, `lamp`, `rgb_lamp`, `gi`, `motor`, `servo`, `magnet`, `relay`, `display`, and `virtual`. Physical model references are optional and must never be required merely to name an I/O address. Controller binding numbers are signed integers because existing platform aliases use negative diagnostic IDs; a controller profile decides which negative or out-of-band ranges are legal.

Keep polarity ownership explicit: `controller.inversion_applied_by_emulator` documents PinMAME's internal normalization and is forbidden as a runtime transform, while `physical.normally_closed` describes the real switch. VPE-specific idle behavior belongs in the table mapping rather than this catalog. A linter must reject consumer-visible inversion on controller profiles whose public API already reports logical active state.

Model RGB devices as a parent device with explicit channel bindings or as uniquely identified channel children. Never rely on duplicate numeric IDs being inserted into a dictionary. The schema validator must distinguish legal mirrored/channel bindings from accidental duplicates.

Logical mechanisms should reference actuator and sensor device IDs and describe known relationships, ranges, positions, and controller ownership. A mechanism may have a catalog-level topology and validation scenarios while VPE's table overlay supplies Unity-specific speed, acceleration, geometry, and switch marks.

For non-emulated circuits, schema version 1 should support only declarative relationships such as `direct`, `normally_closed_series`, `relay_gated`, `inverted`, and `pulse`. Complex EM logic or scripted wiring belongs in an explicitly named consumer extension until real examples justify a portable grammar.

### Inheritance and merge rules

Allow imports only in the order `controller base -> platform variant -> physical machine -> controller/ROM variant -> consumer overlay`. Every document declares its layer, and importing the same or a higher layer is invalid.

Imports form a DAG. Cycles, ambiguous duplicate providers, and multiple parents writing the same scalar without an explicit override are validation errors. Collections merge by stable IDs, not array position or controller number. Deletion requires an explicit tombstone. A generated resolver emits a provenance trace for every final field so reviewers can see which layer won.

Prefer shallow composition. Hardware lineage such as System 11 to Whitestar to SAM does not by itself justify inheriting all machine definitions; import only shared controller capabilities that are behaviorally compatible.

### Provenance and validation states

Each nontrivial assertion should reference one or more source records. A source record includes kind, repository/document, immutable revision or hash, locator, extractor version, timestamp, and licensing/attribution fields. `license` and `attribution` are mandatory for `vpx_script` and `manual` records and optional only when the source policy explicitly permits omission. Source kinds initially include `vpe_csharp`, `pinmame_catalog`, `pinmame_core`, `pinmame_sim`, `vpx_script`, `manual`, `service_bulletin`, `service_diagnostic`, `rom_static_analysis`, `runtime_scenario`, and `human_review`. IPDB sources additionally record `ipdb_machine_id`, the machine-page URL, the direct resource URL, acquisition timestamp, and resource SHA-256. Internet Archive sources record the item identifier, item details URL, original filename, file URL, uploader, rights/license metadata, acquisition timestamp, and resource SHA-256. The repository stores extracted facts and locators by default rather than redistributing the document.

Use fail-closed states: `unknown`, `candidate`, `observed`, `validated`, `conflicted`, and `deprecated`. “Observed output 11 toggled” is not equivalent to “output 11 is the gun motor,” and failure to observe an output is not evidence that it is unused.

Evidence precedence is domain-specific. A known-working VPX script is ground truth when sources disagree about controller addresses, callbacks, ball routing, or mechanism causality. The physical manual wins for wiring, connector and wire colors, part numbers, switch construction and polarity, and assembly geometry. Pinned PinMAME source wins for emulator group routing, display layout, output typing, and normalization performed by the public API. A lower-priority source may still open a conflict when the higher-priority source is ambiguous, incomplete, or demonstrably implements a virtual simplification rather than the physical mechanism.

Definitions should expose coverage dimensions instead of one misleading verified boolean: catalog identity, address enumeration, semantic naming, physical wiring/type, emulator normalization, diagnostic enumeration, runtime observation, causal exercise, mechanism coverage, and ROM-variant coverage.

Coverage lifecycle is separate from assertion confidence. Every definition has `coverage.status` with exactly one of `stub`, `partial`, or `author_ready`, plus `coverage.missing` as a machine-readable list of unmet authoring requirements. Catalog generation creates visibly labeled `stub` records; evidence merging may advance them to `partial`; only the completeness validator may produce `author_ready`. A definition cannot be `author_ready` while any required address is unnamed, any authoring-relevant conflict is unresolved, any known mechanism lacks its actuator/sensor topology, a supported physical/controller variant is unaccounted for, or its recreation-knowledge note is missing. Indexes and consumer APIs must carry this status and must never present `stub` or `partial` as a usable complete definition.

Recreation notes are evidence-aware working knowledge, not an unreviewed extension object. Each claim names its source and locator and distinguishes measured behavior from inference. Notes use a common heading template for overview, playfield devices, custom mechanisms, ball-state transitions, controller interactions, service/setup information, timing and tuning observations, recreation guidance, unresolved questions, and sources. Machines with no identified custom mechanism still receive a short note documenting the evidence checked and that result. A later RFC may promote recurring facts into typed fields, but the initial implementation must not discard them while waiting for that schema.

Project completion is measured over unique physical machines, not ROM count: every in-scope PinMAME driver must resolve to a manufactured or buildable physical machine, and every such machine must resolve to an `author_ready` definition. Custom ROMs made only for community virtual tables are explicitly out of scope; ROM revisions and physical conversions remain when they can run on the corresponding hardware. ROM clones may inherit a shared complete definition when hardware and playfield I/O are identical; actual variant differences require explicit overrides. Generated stubs prove catalog reachability only and contribute zero to author-ready coverage.

## Storage, release, and VPE consumption

### Repository releases

Publish the catalog independently from VPE as immutable versioned artifacts. Each release should include source JSON, JSON Schemas, generated index, flattened definitions, a manifest containing all SHA-256 hashes, the PinMAME source revision used for generation, a compatibility summary, and a detached signature verifiable by a public key pinned in the first supporting editor release.

Use semantic versioning for the schema and catalog, but pin consumption by exact catalog version plus content hash. A schema-breaking change is a catalog major version; adding definitions or evidence is normally minor; correcting labels or hints without changing bindings is patch; changing controller bindings should be called out and may require a minor release plus migration data.

### Authoring and runtime lifecycle

The VPE editor downloads a small signed/hashed index, lets the author choose a physical machine and then a ROM variant, downloads the selected resolved definition, and stores it in a cache. Opening an existing table uses its pinned definition even when the catalog has advanced; updates are offered explicitly and produce a visible diff.

When a table is packed, embed the resolved definition for only the selected machine and variant, plus its identity, catalog version, and hash. The player must not contact a registry to start a table. This eliminates shipping the entire catalog with every VPE release without making runtime execution depend on mutable network data.

Use HTTPS, signed manifests, content hashes, and strict schema validation from the first remote catalog release. Treat downloaded JSON as untrusted: cap file sizes and graph depth, disallow code execution, bound or eliminate user-provided regex evaluation, and validate every referenced ID.

### VPE migration compatibility

Introduce a typed `PinMameMachineDefinition` DTO, resolver, and provider interface. Implement providers for embedded resolved JSON, local authoring cache, and the legacy C# definitions. Keep runtime maps typed by `(group, device, channel)` rather than bare integer to prevent collisions across switch/lamp/GI spaces. This fixes a live collision in the current engine, where lamp and GI callbacks both query `_pinMameIdToLampIdMapping` by bare integer.

Add a one-way migration command that converts a selected legacy `PinMameGame` subclass to a pinned JSON definition and shows anomalies before saving. It must emit numeric and zero-padded legacy aliases for switches and preserve platform-specific merge behavior, including WPC's child-wins deduplication and Bally's concatenation behavior. Continue reading `GameType` from old packages, but write stable machine ID, driver ID, definition version, and hash for all new packages. Remove the concrete C# definitions only after compatibility fixtures prove old tables still load.

Portable cabinet semantics use logical roles such as `cabinet.start`, `cabinet.coin.1`, `service.up`, and `flipper.lower.left`; VPE maps those roles to its own input system. Compatibility aliases may be namespaced `vpe-legacy` only when required to load already serialized IDs. There is no open-ended `extensions.vpe` object, and neither Unity object names nor regex match counts are catalog data.

Do not couple the first migration to adopting VPX's Controller Plugin API. Add transport adapters behind the provider. A later API change should alter routing code and controller profiles, not every machine definition.

## Automated generation pipeline

### Stage A: reproducible PinMAME catalog

Build `tools/pinmame-catalog` to load or link a specific LibPinMAME build, call `PinmameGetGames`, and emit every in-scope physical-machine driver with description, year, manufacturer, clone parent, flags, and generator revisions. Maintain an explicit reviewed exclusion set for custom-ROM-only virtual tables so they cannot regenerate as stubs. `PinmameGame.found` depends on the local ROM path, so exclude it from the canonical hashed catalog and emit it only in an optional local availability report generated with an explicit ROM-path policy. Generate candidate physical-machine families and an exception report; never silently change curated family assignments.

Acceptance gate: every in-scope driver returned by the pinned build appears exactly once in the catalog; every reviewed virtual-only exclusion is absent; every retained clone parent resolves; generated output is byte-for-byte reproducible; and a catalog diff clearly separates added/removed drivers, metadata changes, scope changes, and family-assignment changes.

### Stage B: PinMAME internal structure exporter

Add a PinMAME-side `machine-definition-dump` executable or build-only exporter that initializes one driver and serializes hardware generation, active input/device groups, true counts, remapping functions, common inputs, emulator-applied inversion metadata, physical output types, displays, custom output ranges, and presence of mech/simulation hooks. Mark inversion as `controller.inversion_applied_by_emulator` or equivalent informational metadata that runtime consumers cannot apply. Prefer compiled access to preprocessed structures over regex parsing C macros.

Keep this exporter out of the stable LibPinMAME ABI initially. Once its data model survives multiple platforms, expose a versioned introspection ABI if live consumers need it. Reconcile exporter output with both legacy LibPinMAME numbering and experimental Controller Plugin group numbering.

Acceptance gate: sample machines from WPC, System 11, Bally, Gottlieb, Data East/Sega, Whitestar, and SAM round-trip into group/address inventories, and every emitted fact carries the PinMAME commit and driver ID that produced it.

### Stage C: semantic source extractors

Implement PinMAME semantic extractors using the compiler/preprocessor or a small Clang-based parser. Capture `core_gameData->wpc.comSw` common switch identities, `invSw` as emulator-normalization metadata, `mech_tInitData` actuator/switch topology, named simulation switch/solenoid macros, simulation states, lamp layouts, and mech handlers with source locations. Import the existing VPE C# and old JSON corpus through dedicated migration adapters. Implement a deterministic VPX VBScript evidence extractor over both `vpxtable_scripts` and `vpx-standalone-scripts`: discover ROM/controller IDs, switch constants/usages, solenoid callbacks, lamps/GI, mechs, and stable labels; hash inputs; group revisions; emit candidates and conflicts; and never promote parser inference above candidate status.

Add an IPDB manual acquisition manifest driven through an interactive browser session so Cloudflare is handled normally. Match physical-machine candidates by title, manufacturer, year, model and IPDB ID; retain the human-verifiable machine-page association; inventory manuals, parts lists, schematics, and service bulletins; and download only the resources selected for unresolved coverage gaps. A document extractor should OCR or parse switch matrices, lamp tables, solenoid tables, connector assignments, fuse/interlock details, and mechanism diagrams with page/table locators. Conflicts with PinMAME or table scripts remain explicit until reconciled. Never fetch ROM resources as part of this workflow.

Query Internet Archive metadata for the same unresolved machine/document targets, retain stable item/file identifiers and rights metadata, select original PDF/image files rather than derivative OCR PDFs when available, and deduplicate the resulting documents against IPDB by SHA-256. For this implementation run, keep acquired documents in the reusable local cache `E:\_vpe-2025\pinmame-manuals\by-machine\<machine-id>\<source-id>\` with an adjacent `manifest.json`; the repository tracks the portable manifest schema and extracted facts, while the cache remains outside Git.

Tier document processing by cost. Use deterministic PDF text/table extraction and local OCR first; use a low-cost visual model such as Claude Haiku for straightforward page transcription, OCR repair, and table normalization; and escalate only ambiguous schematics, semantic conflicts, or validation decisions to a stronger reasoning model. Every model-produced assertion retains the document hash, page/region locator, model/version, prompt-template version, and review state, and low-cost-model output remains candidate evidence until mechanically reconciled or reviewed.

Merge candidates by physical machine and controller binding. Exact agreement increases confidence but does not automatically establish correctness if sources share ancestry. Disagreement creates a first-class conflict report that blocks validated status while preserving every candidate.

Acceptance gate: the 11 current C# definitions reproduce without silent data loss; all 55 PinMAME simulations generate candidate reports; every populated WPC `comSw` entry is emitted; every discovered `mech_tInitData` array becomes a source-located topology candidate; inversion output reconciles with `coreGlobals.invSw` but is marked non-consumable; and source regeneration produces no unexplained diff.

### Stage D: diagnostic and playthrough harness

Build a headless harness around LibPinMAME with an isolated per-run ROM/NVRAM directory, pinned ROM hashes, pinned PinMAME commit, deterministic clock/random controls where possible, and a run manifest. Capture all input changes, controlled-device changes, display frames/segments, sound commands where useful, and checkpoints with monotonic timestamps. Do not commit NVRAM blobs: store a hash plus a reproducible seed procedure because NVRAM can contain data derived from ROM execution.

Create platform adapters for cabinet/service switches, NVRAM initialization, diagnostic-menu navigation, display decoding, and output-group addressing. Favor service diagnostics because they systematically enumerate switch, lamp, flasher, solenoid, and sometimes mech names without requiring full gameplay. Decode alphanumeric displays directly. For validation-grade DMD labels, use deterministic glyph/font templates or platform-specific exact text extraction against retained frames, fail closed on unknown glyphs, and require exact normalized text. Confidence-scored OCR may propose candidates for human review but can never promote a field to validated status.

Implement declarative scenarios inspired by Kiki with race-free compound actions: `pulse-wait-output` marks history before closing a switch; `hold-until-output` and `hold-pulse-sequence-wait-output` cover scoops and VUKs; `wait-output-state` samples multi-output conditions atomically; and lower-level `set-host-input`, `wait-display`, `mark-output-history`, `wait-output-since`, `assert-output`, `checkpoint`, `restore`, and bounded alternatives remain available. Every wait has a timeout and every scenario records preconditions, actions, observations, and postconditions. Reading back a host-requested input only confirms what the harness wrote and can never raise validation status; ROM acceptance requires independent display, output, or state evidence.

Switch diagnostic scenarios should iterate candidate addresses, assert whether the ROM reports a switch, capture its displayed label, record the emulator-normalized active/inactive response, and restore the switch. They must not infer physical normally-closed wiring from `PinmameSetSwitch`, because PinMAME has already applied its inversion mask. Output diagnostic scenarios should correlate the currently displayed test item with precisely marked output changes. A correlation becomes evidence, not an automatic rename, until ambiguity and mirrored outputs are resolved.

Gameplay scenarios should model causal physical transactions: pulse an eject coil, synthesize the corresponding opto transition through a machine adapter, and assert the ROM advances. The harness cannot discover physical causality from PinMAME alone because the emulator does not contain the real playfield. PinMAME simulation state machines are only a potential oracle: shipped LibPinMAME initializes and runs them only when keyboard handling is enabled, and that path may take switch ownership away from host-driven `PinmameSetSwitch`. A Phase 0 spike must determine whether simulator state can coexist with host-owned inputs or whether LibPinMAME needs a new simulation-control API. Until that gate passes, causal gameplay relies on a curated digital-twin adapter and simulation reuse remains conditional.

Acceptance gate: a run is replayable from its manifest; the same ROM/NVRAM seed produces equivalent normalized traces; a deliberately wrong switch, output, physical idle-state/digital-twin assumption, and mechanism relationship each cause a clear failure; illegal consumer re-inversion fails schema/lint validation; and no validation status is promoted merely because an address toggled during attract mode.

### Stage E: scaling and continuous validation

Shard runs by physical machine and ROM variant. Open CI can validate schemas, generated catalogs, source extractors, and definitions without ROMs. ROM-dependent jobs run only in authorized infrastructure where users supply legally obtained ROMs; artifacts contain hashes and traces, never ROM bytes.

Build a coverage dashboard showing driver catalog coverage, physical-machine grouping, structural extraction, named-device coverage, conflicts, diagnostic coverage, gameplay scenarios, and mechanism coverage. Allow contributors to upload signed or content-addressed run bundles for review; server-side validation reruns schema and trace checks before evidence can be referenced by a definition.

Roll out in waves without violating the overall newest-to-oldest processing order: use the applicable legacy C# and PinMAME simulation records as golden fixtures within each chronological cohort; keep clone, conversion, and controller variants together; and use extractor or diagnostic similarity only as a tie-breaker inside the same year. Sort by the newest credible physical release year, then manufacturer and title for reproducibility, and place unknown-year candidates last. Generate and version this queue so progress reports and manual acquisition follow the same order.

## Ghidra evaluation

Do not start with a universal ROM reverse-engineering pipeline. PinMAME spans many CPUs, bank-switching schemes, memory maps, compiler/assembly styles, display systems, and diagnostic implementations. Many ROMs contain numeric tables but no human-readable playfield strings, and some labels may exist only in manuals or display-generation code.

Before opening Ghidra, run a cheap feasibility screen over candidate ROM images for printable or segment-encoded device-name strings, diagnostic table shapes, stable address tables, and sibling-revision similarity. Kiki benefits from ELF metadata and a master device table with names and manual IDs; many legacy pinball ROMs have none of those advantages. Only platforms that pass this screen enter a bounded pilot. Select one exact ROM from each accepted platform, create platform-specific Ghidra loaders or memory maps, identify diagnostic switch/output tables and display-string references, and test whether stable signatures reproduce on sibling revisions. Use Kiki-style uniqueness, bounds, ordering, and exact-hash verification; fail closed when multiple candidates exist.

Promote Ghidra extraction for a platform only if it yields semantic data that the runtime diagnostic cannot obtain, reproduces across multiple revisions, and costs less to maintain than manual curation. Otherwise keep it as an investigation tool for individual conflicts and mechanism logic.

## Detailed implementation phases

### Phase 0: freeze the baseline and decide the RFC

Deliverables:

- Commit this architecture document plus an inventory script that re-derives every count from pinned source/build manifests; remove hand-maintained counts from acceptance gates.
- Update the local PR #1 checkout to its valid fetched head or supersede its two converted documents with valid fixtures; raw JSON parseability precedes schema validation.
- Run a bounded LibPinMAME simulation-control spike to answer whether a `src/wpc/sims` state machine can run while the host owns switch input; record the required API patch if it cannot.
- Add a repository license, a per-source attribution policy, and an explicit legal/project decision on redistributing names derived from community VPX scripts; require attribution metadata before those sources enter a signed release.
- Turn the schema decisions into an RFC with five worked examples: T2 with WPC/Fliptronic output conflicts and lower-flipper power/hold semantics, a Bally machine with negative diagnostic IDs, The Walking Dead with RGB and GI namespace overlap, one existing JSON mechanism, and a legacy direct-flipper relationship.
- Record explicit decisions for typed identity namespaces, canonical string IDs and signed numeric bindings, authority/direction-scoped groups, mandatory legacy/zero-padded aliases, polarity ownership after PinMAME normalization, Fliptronic power/hold binding ownership, the exclusion of VPE hints, provenance states, signed release/version policy, and catalog-versus-Unity mechanism ownership.
- Stop bulk conversion on PR #1 until the RFC fixtures and validators exist; continue discussion using the fetched T2/WPC data as test input.

Exit gate: maintainers agree on the distinction between physical kind and controller transport, the physical-machine/ROM hierarchy, VPE's LibPinMAME compatibility path, the legacy alias rule, and whether simulator state is usable by the harness without losing host input control.

### Phase 1: schema, resolver, and repository quality gates

Deliverables:

- JSON Schema 2020-12 documents for controller profiles, machines, resolved definitions, and catalog indexes; defer overlay and evidence-manifest schemas until their Phase 2 and Phase 5 producers are designed.
- A deterministic resolver with typed-layer DAG validation, explicit overrides/tombstones, stable-ID merges, and per-field provenance traces.
- A first CI gate that parses every JSON document without recovery, followed by schema validation.
- A semantic linter for duplicate bindings, signed-address range violations, dangling or case-mismatched model IDs, unsupported transports, alias cycles, clone-family inconsistencies, conflicting channel use, mixed identifier types, ambiguous multi-parent scalars, and forbidden cross-layer fields.
- A canonical formatter and generated index; CI rejects hand-edited generated files and stale indexes.
- Fixtures in which every linter rule has a known failing case, including PR #1's `group_name`/`group_id`, `gi`/`GI`, integer/string ID, and output 31 conflicts.
- A one-machine golden importer for T2 so the Phase 1 vertical slice can compare the resolved schema against actual C# behavior; the reusable 11-machine importer remains Phase 2 work.
- Polarity fixtures proving T2's normalized public switch state carries no consumer-applied inversion, with a failing case for a forbidden runtime re-inversion field.

Exit gate: all valid fixtures validate; every linter rule rejects its failing fixture; invalid imports and ambiguous merge precedence fail; a resolved T2 reproduces current requested switch/coil/lamp sets and numeric/zero-padded alias resolution; and flattened output is byte-reproducible.

### Phase 2: import the existing corpus without overstating confidence

Deliverables:

- Importers for current C# definitions, old `pinmame-game-defs` JSON, PR #1 T2/WPC JSON, and deterministic outputs from both local VPX script corpora.
- A canonical platform-ID alias table covering all 16 observed spellings, including `dataeast`/`de` and `s11`/`system11`. Phase 2 resolves only the WPC, SAM, Bally, and System 80 families backed by current profiles; it imports all other files losslessly as unresolved candidates and defers their source-to-resolved gate until Phase 3 generates profiles.
- A migration report for every field, including explicitly dropped VPE hints, renamed data, unresolved platform IDs, duplicate addresses, source quality, and the corpus-only `gi`, `flashers`, `gi_strings`, `mechanisms`, `lamp_coils`, DOF, commented-out, and note fields.
- Curated physical-machine records for the 11 golden machines and aliases from their 99 ROM IDs.
- Conflict files or issue-ready reports for known anomalies rather than silent normalization, including the no-provenance `ij.json` case.
- Golden comparisons that reproduce actual per-MPU merge behavior, including WPC child-wins deduplication and Bally concatenation, rather than imposing the new merge rules retroactively during import.

Exit gate: a source-to-resolved comparison for the four currently profiled families proves that no usable legacy field vanished; every other corpus file has a lossless unresolved migration report; and every imported assertion has provenance and a fail-closed state.

### Phase 3: complete PinMAME catalog and structural extraction

Deliverables:

- `pinmame-catalog`, physical-family candidate generator, family exception table, and catalog diff reporter.
- PinMAME internal structure exporter and controller-profile generator.
- Simulation semantic extractor for the 55 current simulation drivers.
- Explicitly labeled `coverage.status: "stub"` seed definitions for every root family, each listing the authoring requirements still missing.

Exit gate: every in-scope driver returned by the pinned build resolves to exactly one catalog record and candidate physical machine; every reviewed virtual-only exclusion stays absent; every retained clone parent resolves; the generated manifest records the actual count; selected cross-platform samples enumerate correctly; no generic generated label is presented as a validated semantic name; and every structurally generated record is visibly classified as a stub until the author-readiness validator proves otherwise.

### Phase 4: VPE data-provider migration

Deliverables:

- Typed C# DTOs and validators generated or maintained from the schema.
- Catalog/cache/embedded/legacy providers and a resolver integration in the editor.
- A physical-machine-first, ROM-second selector driven by the generated index.
- Package serialization using stable IDs, exact definition version, and hash; selected resolved definition embedded at pack time.
- Legacy read/migration support and regression fixtures for existing table packages, including a saved switch mapping using `"07"` and a lamp/GI pair sharing the same numeric address.
- A reverse resolver from stable semantic device IDs to LibPinMAME channel integers for every mech actuator and sensor, validation that every authored mech reference resolves, and a hard error rather than the current silent coil-ID `0` fallback.
- A regression fixture for a saved table with an authored `PinMameMechComponent`, including its coil mappings and switch marks.

Exit gate: existing tables load with identical requested-device, alias, and mech behavior; unresolved mech references fail before starting PinMAME; a newly authored table does not require a C# game subclass; its player package runs offline with only its selected definition; and catalog updates do not silently alter a saved table.

### Phase 5: harness pilot and verification levels

Deliverables:

- Headless deterministic runner, trace format, display capture/decoder, scenario engine, and isolated NVRAM management.
- WPC service-menu adapter and scenarios for T2 plus at least two other WPC machines.
- One non-WPC platform adapter to prove the abstraction is not WPC-specific.
- Conditional on the Phase 0 spike, Kiki-style causal gameplay scenarios for trough launch, an eject, a target sequence, and one motorized mechanism; otherwise implement them against a curated host-owned digital twin and treat PinMAME simulations as future work.
- Coverage computation and evidence-to-definition promotion tooling.

Exit gate: for the resolved T2 fixture, at least 95% of declared switch addresses are enumerated and labeled with deterministic diagnostic display evidence, at least 90% of declared controlled-device addresses are correlated with diagnostic output evidence, every unexplained exclusion is listed, all four legacy flipper relationships are represented, the gun motor is causally exercised, wrong-switch/wrong-output/wrong-physical-idle-state/wrong-mechanism faults each fail clearly, forbidden consumer re-inversion fails linting, and two cold runs from the same generated NVRAM seed produce equivalent normalized traces. Source, observation, and validation states must remain distinguishable, and evidence must be reviewable without the original developer's save state.

### Phase 6: targeted static analysis and scaled contribution

Deliverables:

- Three-platform Ghidra feasibility report with maintenance-cost recommendation for each platform.
- Additional diagnostic adapters prioritized by machine coverage and shared menu behavior.
- Contributor run-bundle tooling, evidence review workflow, and public coverage dashboard.
- Definition release automation independent from VPE releases.

Exit gate: the project can add or correct a machine through a repeatable source/extract/test/review/release workflow without editing VPE or shipping the entire catalog in a VPE package.

## Test strategy

### Schema and resolver tests

- Validate every source and generated artifact against its schema and semantic rules.
- Property-test import ordering, alias resolution, tombstones, duplicate bindings, RGB channels, and variant patches.
- Snapshot flattened definitions and provenance traces for representative platforms.
- Ensure an unsupported transport fails at authoring or packaging time, not during gameplay.
- Verify group-ID uniqueness is scoped by provider authority and direction, so input group 1 and controlled-device group 1 coexist while duplicates within one scoped namespace fail.

### Extractor tests

- Pin each extractor fixture to source commit, driver ID, and relevant source hashes.
- Regenerate and compare committed outputs byte-for-byte.
- Require unique matches and explicit expected cardinality for static signatures.
- Compare PinMAME catalog results obtained through the public ABI with driver-list source generation.
- Reconcile true initialized counts with emitted device lists and flag mismatches.

### VPE compatibility tests

- Load serialized packages for each of the 11 legacy classes and compare requested switch/coil/lamp IDs and alias resolution.
- Include numeric and zero-padded saved switch IDs, negative diagnostic aliases, per-MPU merge ordering/deduplication, and a lamp/GI numeric collision.
- Pack the same table twice and compare embedded resolved definition hashes.
- Exercise offline playback after clearing the authoring cache.
- Verify catalog update, rollback, missing definition, hash mismatch, and incompatible schema behaviors.

### Harness tests

- Unit-test trace normalization, timestamp ordering, atomic pulse/hold/wait semantics, deterministic display glyph decoding, exploratory OCR isolation, and timeout diagnostics.
- Use a fake controller to prove scenarios reject mirrored or out-of-order output events.
- Run boot, service diagnostic, and gameplay suites separately so failures identify the affected evidence level.
- Keep NVRAM seeds and service-menu language fixed in each scenario manifest.

## Success metrics

- Catalog coverage: 100% of the driver list and clone edges reported in the pinned generated manifest are represented; the literal count is an output, not a hand-maintained requirement.
- Packaging: a VPE player package contains only the selected resolved definition and needs no catalog network access.
- Migration: all 11 legacy classes and 99 ROM IDs have compatibility fixtures before their C# implementations are retired.
- Reproducibility: generated catalog, structure, simulation seeds, index, and flattened definitions have unexplained-diff count zero.
- Evidence: every validated semantic mapping points to reproducible evidence; every candidate without proof remains visibly a candidate.
- Harness: per-machine coverage reports distinguish declared, enumerated, named, observed, causally exercised, and variant-tested devices.
- Quality: duplicate bindings, stale indexes, dangling imports, alias cycles, and unsupported routing cannot merge to the release branch.

## Key risks and mitigations

| Risk | Consequence | Mitigation |
| --- | --- | --- |
| PinMAME contains generic addresses but few semantic names | Automation appears more complete than it is | Separate structural generation from semantic validation and display coverage dimensions. |
| Clone families hide wiring changes | One definition is incorrectly applied to several ROMs | Permit variant patches, preserve ROM hashes, and require family exceptions/review. |
| Runtime activity is mistaken for identity or completeness | Incorrect labels gain validated status | Require diagnostic context or causal scenario evidence; absence of activity never means unused. |
| Service menus differ by platform, revision, language, and NVRAM | Harness is brittle or nondeterministic | Pin language/NVRAM/ROM, implement platform adapters, bound alternatives, and retain traces. |
| Physical mechs do not exist inside emulation | Playthrough cannot validate causal topology | Use PinMAME simulations where available and curated digital-twin adapters elsewhere. |
| Universal Ghidra effort expands across many CPUs | High maintenance with limited semantic yield | Gate per-platform pilots on incremental data value and reproducibility. |
| Existing JSON is mixed-quality and mixed-schema | Silent loss or false confidence during migration | Dedicated importers, migration reports, provenance, conflicts, and golden fixtures. |
| Controller Plugin API changes | Definitions churn or VPE breaks | Canonical stable groups plus authority/direction-scoped, revisioned transport adapters and derived `ctrl://` URIs; do not make the WIP API the only representation. |
| LibPinMAME simulations take host switch ownership | Simulation-based causal tests cannot drive arbitrary inputs | Resolve in a Phase 0 spike, budget a dedicated simulation-control API, and keep host-owned digital-twin scenarios as the baseline. |
| PinMAME inversion is applied again by a consumer | Active-low/opto switches behave backwards | Treat public switch state as normalized, separate physical normally-closed authoring data, and reject runtime re-inversion. |
| Semantic IDs do not reverse-resolve for authored mechs | Coils silently become ID 0 and mechanisms fail | Validate every mech reference, hard-fail unresolved IDs, and regression-test saved mech components. |
| Remote catalog is unavailable or compromised | Authoring or runtime failure | Cache exact versions, embed selected definitions, validate signed manifests and hashes, and enforce strict resource limits. |
| Repository/source licensing is undefined | Independent signed releases cannot be distributed safely | Choose a repository license and attribution policy in Phase 0, require source license metadata, and decide treatment of VPX-derived names before release. |
| ROM, NVRAM, and manual licensing | CI cannot reproduce or redistribute inputs | Never store ROMs/manual scans or generated NVRAM blobs; store hashes, locators, generated seed procedures, derived facts, and source licensing metadata. |

## Decisions to make in the RFC

The following choices should be explicit before schema implementation; the recommendation is included to prevent open-ended design drift:

- Repository: evolve `pinmame-game-defs` in place, preserving old files on a migration branch or tagged release.
- Primary hierarchy: physical machine first, controller/ROM variants second.
- Canonical routing: stable logical group IDs scoped by provider authority and direction, with separate LibPinMAME and revisioned Controller Plugin transport mappings plus derived `ctrl://` URIs.
- Runtime format: generated flattened JSON embedded per table; source inheritance is authoring/build-time only.
- Stable mapping key: semantic string device ID, with signed numeric controller binding allowed to vary by variant and mandatory legacy numeric/zero-padded aliases during migration.
- Polarity ownership: PinMAME exposes normalized active state; emulator inversion is informational, physical normally-closed state is machine data, and VPE idle behavior stays in table-owned mapping configuration.
- Fliptronic flippers: decide whether a stable flipper device maps to power, hold, or a two-actuator mechanism and which controller/machine layer owns each binding.
- Consumer hints: absent from canonical definitions. Portable cabinet roles remain; VPE matching and other consumer configuration stay in their owning projects.
- Mechs: catalog stores logical topology/evidence; Unity components retain implementation-specific physical configuration.
- Complex wires/EM logic: limited declarative relationships in version 1, consumer extension for the rest.
- Validation: fail-closed multi-dimensional status backed by immutable evidence.
- Distribution: independently signed catalog releases, cached by the editor and pinned by content hash.
- Licensing: repository license and required per-source attribution are release prerequisites, with an explicit policy for VPX-script-derived names.
- Ghidra: targeted platform pilots after runtime and source extraction, not the primary all-games generator.

## Immediate next work package

The RFC/validator vertical slice, catalog generator, legacy import, two-corpus VPX extraction, organized manual acquisition/extraction, ROM corpus indexer, and DMD-capable reusable LibPinMAME service/gameplay harness are implemented. The Ali identity correction plus AC/DC Vault, Spider-Man Vault, AC/DC LED Pro, The Walking Dead Premium/LE, The Walking Dead Pro, Iron Man Pro Vault, Mustang Premium/LE/Boss, Mustang Pro, Star Trek Premium/LE, Star Trek Pro, Metallica Premium/LE, Metallica Pro, original AC/DC Pro, AC/DC Premium/LE/LUCI, and Avengers Pro spatial retrofits are committed in their per-game branches. TSPP's incorrect IPDB 6154 identity was traced to a bad third-party VPX header, corrected to 4674, and committed at `441527b` without altering pinned/generated third-party evidence. The other 18 semantic baselines remain fail-closed for spatial placement. Mechanical VPX extraction now produces compact per-game evidence packets for controller-address candidates, exact coordinates, multiplicity, and unresolved records; sibling editions reuse a family base plus explicit edition overlays, while root review remains mandatory for manual/script conflicts and custom mechanisms. The next work package is ordered as follows:

1. Complete the already-active X-Men LE/Pro, Transformers Pro, TRON LE/Pro, Rolling Stones, Avatar, and Dark Knight worktrees newest-first; keep unsupported editions fail-closed, preserve every current pass, do not begin further Pro editions until the end, process Ali's spatial work later at 1980, and finish the remaining 18 pending records before Terminator 2.
2. Prefer a known-working VPX script for controller-facing runtime semantics, official/manual evidence for physical construction and wiring, and pinned PinMAME source for transport topology; acquire manuals into the reusable external cache and record exact hashes and page locators.
3. For each machine, write recreation knowledge for custom mechanisms, ball paths, startup state, timing, geometry clues, and authoring pitfalls; keep the definition partial whenever any authoring-critical behavior remains unvalidated.
4. After the spatial retrofits, add stable machine-family identifiers and researched prose for edition differences without grouping unrelated physical titles merely because they share a theme.
5. After Terminator 2, copy and verify the static catalog site, obtain its separate Opus approval, and deploy it to GitHub Pages.
6. Keep schema validation, exact catalog reachability, coverage reporting, and regression tests green after every curation batch; no game is committed before its own fresh Opus approval.

## Opus review disposition

Opus reviewed the complete draft at high effort in one persistent Claude Code session, inspected the surrounding repositories, and returned an initial verdict of **ready with changes**. A correction round in the same session retracted two review mistakes after direct source reconciliation: controlled-device group `0x0001` is the exact main output group while `0x0000` is only the masked family, and fetched PR head `e87d57f` is valid JSON while the local branch at `46006b0` is the invalid one-commit-behind copy. Both corrections and their surviving recommendations are represented explicitly in this plan.

The first revision accepted mandatory numeric and zero-padded legacy aliases; authority/direction-scoped plugin routing and derived `ctrl://` URIs; namespaced consumer extensions; a live lamp/GI collision regression; negative diagnostic addresses; real per-MPU legacy merge behavior; removal of environment-dependent ROM availability from canonical hashes; explicit corpus schema drift; relational rather than hardcoded driver-count gates; a Phase 0 simulation-control spike; a cheap pre-Ghidra feasibility screen; signed manifests from the first remote release; non-committed NVRAM seed procedures; and measurable T2 harness criteria. The later implementation decision intentionally supersedes the VPE-extension portion: canonical definitions reject VPE hints and consumer configuration stays outside the catalog.

Opus then performed a full read of the revised document and found further material gaps, all of which were accepted into the plan: PinMAME-normalized polarity ownership; mech reverse resolution with hard failures; a Phase 1 T2 golden importer; deterministic validation-grade DMD glyph decoding; race-free Kiki scenario primitives and the prohibition on treating host input readback as ROM evidence; extraction of `comSw`, `invSw`, and `mech_tInitData`; repository/source licensing; an explicit Fliptronic power/hold decision; scoping Phase 2 resolution to existing controller profiles; and correction of the globally inherited four wires that had been misreported per MPU.

Opus's authority/direction namespacing and derived-URI recommendations were accepted. Building integrations for DOF, B2S, and PUP is outside this implementation scope; their consumer-owned metadata is not part of canonical machine definitions and can be designed independently.

After these revisions, Opus completed a final full-file approval pass in the same persistent session and returned **APPROVED**. It confirmed that all blocker/major findings are integrated at the relevant schema, linter, extractor, migration, harness, and phase-gate levels; that the two retractions are represented fairly; and that the phases are implementable in the stated order without contradiction.
