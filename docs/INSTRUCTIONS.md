# Agent instructions for PinMAME machine definitions

This file is the operational runbook for the agent continuing the physical-machine definition project. It is generic policy: it must not name individual games, quote coverage counts, or pin upstream revisions. All of that mutable state lives in `docs/CURRENT-STATE.md`. Read the schemas, this file, and that ledger before changing a definition, and keep the ledger and the generated catalog/coverage reports synchronized throughout the work.

## Mandatory prerequisites and discovery

Required capabilities are a hard gate, but a command missing from `PATH` or an unset convenience variable is not itself proof that the capability is unavailable. Start in this repository, derive its root with `git rev-parse --show-toplevel`, and inspect `PATH`, common installed-tool locations, workspace-provided runtimes, sibling repositories, and existing project folders. Record the resolved commands, versions, and external roots. If an applicable human-owned tool or read-only input still cannot be resolved, ask the human to provide its executable or folder before declaring that line of work blocked. The three public source repositories managed below are the exception: clone them automatically and report clone/network failures instead of asking the human for checkout paths. Abort only after reasonable discovery plus any applicable human request shows that a required capability or source is genuinely unavailable; do not silently omit the affected evidence or replace it with a weaker source/model. Do not install software or create substitute read-only source folders without contributor approval.

### Tool capabilities and download sources

| Capability | Used for | Installation or download source |
| --- | --- | --- |
| Git 2.23 or newer (`git`) | branches, worktrees, pinned filtered clones, exact-state review, commits, and PR preparation | [Git downloads](https://git-scm.com/downloads) |
| Python 3.11 or newer plus this package's dependencies | deterministic curators, catalog generation, validation, the PinMAME harness, PDF parsing, and tests | [Python downloads](https://www.python.org/downloads/); install this repository with `python -m pip install -e .` in an isolated environment when dependencies are not already available |
| ripgrep (`rg`) | first-choice source and file discovery | [ripgrep releases](https://github.com/BurntSushi/ripgrep/releases) |
| `vpxtool` | VPX identity inspection, script/object extraction, and spatial evidence | [vpxtool releases](https://github.com/francisdb/vpxtool/releases); record the exact version in evidence, and use v0.33.3 only when reproducing artifacts explicitly pinned to `vpxtool git:v0.33.3` |
| An archive extractor capable of RAR and ZIP, normally 7-Zip | inspecting and extracting retained VPX, ROM, and manual archives | [7-Zip downloads](https://www.7-zip.org/download.html) |
| A working PDF extraction/rendering toolchain, normally Poppler's `pdfinfo`, `pdftotext`, and `pdftoppm` plus the Python dependencies | PDF identity checks, text extraction, and rendered manual pages | [Poppler Windows builds](https://github.com/oschwartz10612/poppler-windows/releases) |
| OpenAI Codex CLI (`codex`), installed, authenticated, and working non-interactively when OpenAI models are used | running `gpt-5.6-sol`, `gpt-5.6-terra`, or `gpt-5.6-luna` workers and reviewers | [Codex CLI documentation](https://developers.openai.com/codex/cli) |
| Claude Code CLI (`claude`), installed, authenticated, and working non-interactively when Anthropic models are used | running `opus`, `sonnet`, or `haiku` workers and reviewers | [Claude Code setup](https://docs.anthropic.com/en/docs/claude-code/getting-started) and [CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage) |
| Working CLI access to the model tiers required by the allocation policy below | high-judgment curation, economical delegated extraction, and mandatory pre-submission review | At least one high-tier CLI is mandatory; when another provider's high-tier model is available, its CLI must also work so the final review can be cross-provider |
| An authenticated interactive browser or working browser automation | Cloudflare-gated IPDB/VPU/VPF research and downloads | [Google Chrome](https://www.google.com/chrome/) or [Puppeteer](https://pptr.dev/guides/installation) |
| Pinned PinMAME source and a compatible built native library | authoritative driver inventory and runtime-harness traces | [vpinball/pinmame](https://github.com/vpinball/pinmame); if no compatible library can be found, use the concrete CMake preparation and out-of-source build recipe below with a suitable C/C++ toolchain |

Tool names above are conventional, not mandatory installation paths. Locate an existing executable first, run a small version/smoke check, and use its fully qualified path when it is not on `PATH`. For the native library, search the final agent-managed PinMAME checkout and `<working-root>/builds/pinmame` for `pinmame64.dll`, `libpinmame.dll`, `libpinmame.so`, or `libpinmame.dylib`, explicitly excluding every `.incoming-*` tree; use `PINMAME_LIBRARY_PATH` only as an optional disambiguation override. If multiple plausible libraries exist, identify the one built from the pinned revision instead of choosing by filename alone.

### Agent CLI operation

Do not treat an installed executable as proof that an agent CLI works. For every provider intended for the contribution, run its version and doctor commands, verify authentication, and make a small non-interactive call using each required model alias. Run `codex --version` and `codex doctor` for Codex; run `claude --version` and `claude doctor` for Claude Code. If an applicable CLI cannot authenticate, select the named model, read the required files, or return output, fix it before delegating work or starting review. Record genuine provider unavailability rather than pretending that an inaccessible model performed a review.

Use PowerShell here-strings or prompt files for substantial prompts so shell expansion and quoting do not alter the instructions. Resolve and validate `$worktree` first. Codex models use `xhigh` reasoning for this project; Claude models use `high` effort. Typical non-interactive worker calls are:

```powershell
$prompt = @'
Read docs/INSTRUCTIONS.md, then perform only the bounded task described below.
Report uncertainty and do not guess.
'@

$prompt | codex exec -C $worktree -m gpt-5.6-terra -c 'model_reasoning_effort="xhigh"' -s workspace-write -

Push-Location -LiteralPath $worktree
try {
	claude -p --model sonnet --effort high --permission-mode acceptEdits $prompt
} finally {
	Pop-Location
}
```

Select `gpt-5.6-sol`, `gpt-5.6-terra`, or `gpt-5.6-luna` with Codex's `-m` option and `opus`, `sonnet`, or `haiku` with Claude Code's `--model` option. Run a reviewer without edit permission: use `codex review` against the intended base or a Codex read-only sandbox, and use Claude Code with `--permission-mode plan`. Typical review calls are:

```powershell
$reviewPrompt = @'
Perform an independent read-only review of the exact contribution tree.
Report only discrete, actionable findings; do not edit files.
'@

$reviewPrompt | codex -C $worktree review -c 'model="gpt-5.6-sol"' -c 'model_reasoning_effort="xhigh"' --base master -

Push-Location -LiteralPath $worktree
try {
	claude -p --model opus --effort high --permission-mode plan $reviewPrompt
} finally {
	Pop-Location
}
```

Start each CLI in the exact game worktree and explicitly grant access only to required external evidence roots. Capture the final response under the sibling working directory's `review-artifacts` folder together with the reviewed commit and tree hashes.

Ghidra is escalation-only rather than part of every game's startup check. When a game reaches the Ghidra escalation described later, [download Ghidra from the NSA project](https://github.com/NationalSecurityAgency/ghidra/releases), verify it launches, and stop that game if it is unavailable; do not replace reverse engineering with speculation.

### Existing read-only inputs

Resolve these inputs from contributor configuration, already mounted storage, or sensible sibling directories. Environment-variable names are portable labels and optional overrides, not a demand that every shell predefine them. An unset variable must never cause immediate refusal. When an applicable input cannot be discovered, ask the human for its location; combine multiple unresolved inputs into one concise request when practical. Treat the resolved contents as read-only during curation.

| Location label | Existing input |
| --- | --- |
| Current Git root | This `pinmame-game-defs` checkout, derived from the working directory; no separate root variable is needed |
| `<working-root>/source-checkouts/pinmame` | Agent-managed pinned `vpinball/pinmame` checkout |
| `<working-root>/source-checkouts/vpxtable_scripts` | Agent-managed pinned `sverrewl/vpxtable_scripts` corpus |
| `<working-root>/source-checkouts/vpx-standalone-scripts` | Agent-managed pinned `jsm174/vpx-standalone-scripts` corpus |
| `PINMAME_EXISTING_VPX_TABLES` | One or more existing VPX table collections as a comma-separated, ordered list; search them from first to last |
| `PINMAME_ROM_LIBRARY_ROOT` | Existing user-authorized VPinMAME ROM corpus |

For `PINMAME_EXISTING_VPX_TABLES`, split on commas, trim surrounding whitespace, discard empty entries, resolve each path, and preserve the supplied order. If it is unset and local discovery does not find the table collections, ask the human to provide one or more folders in preferred search order. Do not require separate primary/archive variables.

Do not ask the human to provide PinMAME, `vpxtable_scripts`, or `vpx-standalone-scripts` checkouts. Clone and pin them automatically under the working root as described below, then treat their contents as read-only curation inputs. Do not modify, reorganize, rename, or delete the user's other read-only inputs. A source that is irrelevant to the selected game need not block unrelated work. Before treating another applicable source as unavailable, ask the human for its path and allow them to provide it directly even if no environment variable is set. If the human cannot provide a source required to substantiate an authoring-critical claim, keep the game partial or stop only that line of work rather than guessing or refusing unrelated work.

### Writable working directories

The human must not have to declare environment variables for writable locations. Derive the repository root with `git rev-parse --show-toplevel`, take its parent, and use the fixed sibling `pinmame-game-defs-working-dir` as the only curation working root. At initial preflight, validate that exact sibling path and create it and every subfolder below when missing. Reuse existing directories without deleting or replacing their contents. If the path exists as a file or reparse point, stop and ask the contributor instead of choosing another location silently.

| Relative path under `pinmame-game-defs-working-dir` | Writable purpose |
| --- | --- |
| `worktrees` | Per-game Git worktrees |
| `vpx-sources` | Downloaded/retained VPX tables, sidecars, extractions, manifests, and provenance |
| `manuals` | Downloaded manuals, rendered pages, extracted text, and manual manifest |
| `review-artifacts` | Retained spatial-analysis and model-review artifacts that do not belong in Git |
| `roms` | Newly downloaded ROM archives used for authorized local research |
| `source-checkouts` | Agent-managed pinned upstream Git checkouts |
| `source-checkouts/.incoming-*` | Incomplete diagnostic clone directories only; enumerate and report them, but never reuse, promote, or search them as source evidence |
| `builds` | Out-of-source build trees, including the pinned PinMAME native library |

Resolve and create the layout automatically:

```powershell
$repoRootText = (& git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($repoRootText)) { throw 'Cannot resolve the repository root.' }
$repoRoot = [System.IO.Path]::GetFullPath($repoRootText)
$repoParent = [System.IO.DirectoryInfo]::new($repoRoot).Parent.FullName
$workingRoot = [System.IO.Path]::GetFullPath((Join-Path $repoParent 'pinmame-game-defs-working-dir'))
$expectedWorkingRoot = [System.IO.Path]::GetFullPath((Join-Path $repoParent 'pinmame-game-defs-working-dir'))
if ($workingRoot -ne $expectedWorkingRoot) { throw 'Unexpected working-root resolution.' }

$workingFolders = [ordered]@{
	Worktrees = Join-Path $workingRoot 'worktrees'
	VpxSources = Join-Path $workingRoot 'vpx-sources'
	Manuals = Join-Path $workingRoot 'manuals'
	ReviewArtifacts = Join-Path $workingRoot 'review-artifacts'
	Roms = Join-Path $workingRoot 'roms'
	SourceCheckouts = Join-Path $workingRoot 'source-checkouts'
	Builds = Join-Path $workingRoot 'builds'
}

foreach ($path in @($workingRoot) + $workingFolders.Values) {
	if (Test-Path -LiteralPath $path) {
		$item = Get-Item -LiteralPath $path -Force
		if (-not $item.PSIsContainer -or ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) { throw "Unsafe working directory: $path" }
	} else {
		[void][System.IO.Directory]::CreateDirectory($path)
	}
}
```

Clone the three public source repositories when missing and detach each checkout at its required pinned revision. Clone into a unique incoming sibling first, validate and pin it there, and move it to the final path only after success. At every preflight, enumerate existing `.incoming-*` directories under `source-checkouts`, report their count and exact paths to the human as abandoned diagnostic leftovers that are safe to delete after investigation, and exclude them from every source, evidence, and native-library search. Never reuse or promote one. If cloning or checkout is interrupted, leave that incoming directory for diagnosis; a later run uses a new incoming path and is not blocked by the incomplete clone. Existing final checkout directories must have the expected origin, be completely clean, and contain the pinned commit before reuse. Never reset, clean, overwrite, or delete an unexpected or dirty final checkout; stop and ask the human to inspect it. Configure all managed checkouts with `core.autocrlf=false` and `core.eol=lf` before materializing files so evidence hashes are independent of the contributor's global Git settings; the `vpx-standalone-scripts` repository's own `*.vbs text eol=crlf` attribute still takes precedence. Spot-check any reused checkout that supplies hashed evidence against a known recorded hash instead of trusting a clean Git status. A network failure is a tooling/network blocker, not a reason to ask the human to supply these repositories manually.

```powershell
$abandonedIncoming = @(Get-ChildItem -LiteralPath $workingFolders.SourceCheckouts -Directory -Force -ErrorAction Stop | Where-Object { $_.Name -like '.incoming-*' })
if ($abandonedIncoming.Count -gt 0) {
	Write-Warning "Found $($abandonedIncoming.Count) abandoned incoming checkout(s); never reuse or search these paths:"
	$abandonedIncoming.FullName | ForEach-Object { Write-Warning $_ }
}

$checkouts = @(
	@{ Name = 'pinmame'; Url = 'https://github.com/vpinball/pinmame.git'; Revision = '4ec52ff0ac133ac251681518aed2249e19fe26eb' },
	@{ Name = 'vpxtable_scripts'; Url = 'https://github.com/sverrewl/vpxtable_scripts.git'; Revision = '0c036bb61b4b4e8c778c37559f6795df8cd1521e' },
	@{ Name = 'vpx-standalone-scripts'; Url = 'https://github.com/jsm174/vpx-standalone-scripts.git'; Revision = '15d112648a1b94b9f59eb8b3c335d57283653c50' }
)

foreach ($checkout in $checkouts) {
	$path = Join-Path $workingFolders.SourceCheckouts $checkout.Name
	$newClone = -not (Test-Path -LiteralPath $path)
	if ($newClone) {
		$incomingName = ".incoming-$($checkout.Name)-$([System.Guid]::NewGuid().ToString('N'))"
		$candidatePath = Join-Path $workingFolders.SourceCheckouts $incomingName
		if (Test-Path -LiteralPath $candidatePath) { throw "Incoming checkout path already exists: $candidatePath" }
		git clone --filter=blob:none --no-checkout $checkout.Url $candidatePath
		if ($LASTEXITCODE -ne 0) { throw "Failed to clone $($checkout.Name)." }
	} else {
		$candidatePath = $path
	}

	$item = Get-Item -LiteralPath $candidatePath -Force
	if (-not $item.PSIsContainer -or ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) { throw "Unsafe checkout path: $candidatePath" }
	$origin = "$(git -C $candidatePath remote get-url origin)".Trim()
	if ($LASTEXITCODE -ne 0 -or $origin -ne $checkout.Url) { throw "Unexpected origin for $($checkout.Name): $origin" }
	if (-not $newClone -and (git -C $candidatePath status --porcelain)) { throw "Dirty agent-managed checkout: $candidatePath" }

	git -C $candidatePath config --local core.longpaths true
	if ($LASTEXITCODE -ne 0) { throw "Failed to enable long-path support for $($checkout.Name)." }
	git -C $candidatePath config --local core.autocrlf false
	if ($LASTEXITCODE -ne 0) { throw "Failed to disable automatic line-ending conversion for $($checkout.Name)." }
	git -C $candidatePath config --local core.eol lf
	if ($LASTEXITCODE -ne 0) { throw "Failed to pin checkout line endings for $($checkout.Name)." }
	git -C $candidatePath cat-file -e "$($checkout.Revision)^{commit}" 2>$null
	if ($LASTEXITCODE -ne 0) {
		git -C $candidatePath fetch --no-tags origin $checkout.Revision
		if ($LASTEXITCODE -ne 0) { throw "Failed to fetch pinned revision for $($checkout.Name)." }
	}
	git -C $candidatePath switch --detach $checkout.Revision
	$head = "$(git -C $candidatePath rev-parse HEAD)".Trim()
	if ($LASTEXITCODE -ne 0 -or $head -ne $checkout.Revision -or (git -C $candidatePath status --porcelain)) { throw "Failed to pin $($checkout.Name) cleanly." }
	if ($checkout.Name -eq 'vpxtable_scripts') {
		$knownEvidencePath = Join-Path $candidatePath 'Aaron Spinlling (Data East 1992) v1.02.vbs'
		$knownEvidenceSha256 = '92abfcb92e97fad7abf0658ac5168af54ee6d19be8a7fe58ffc76de420270f40'
		if (-not (Test-Path -LiteralPath $knownEvidencePath -PathType Leaf) -or (Get-FileHash -LiteralPath $knownEvidencePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $knownEvidenceSha256) { throw "The vpxtable_scripts working-tree bytes do not match the recorded LF-normalized evidence hash: $knownEvidencePath" }
	}

	if ($newClone) {
		if (Test-Path -LiteralPath $path) { throw "Final checkout path appeared while cloning: $path" }
		Move-Item -LiteralPath $candidatePath -Destination $path -ErrorAction Stop
	}
}
```

Build PinMAME under `<working-root>/builds/pinmame` when a compatible native library is not already present. The pinned revision keeps the libpinmame project at `cmake/libpinmame/CMakeLists.txt` and its official workflow copies that file to the checkout root before configuration because its source paths are root-relative. Make the same copy; `/CMakeLists.txt` is gitignored at the pinned revision, so this preparation keeps `git status --porcelain` clean while all generated build output remains outside the checkout. For Windows x64, use the following concrete invocation and adjust `PLATFORM`, `ARCH`, generator, and configuration for the contributor's target platform:

```powershell
$pinmameCheckout = Join-Path $workingFolders.SourceCheckouts 'pinmame'
$pinmameBuild = Join-Path $workingFolders.Builds 'pinmame'
$libPinmameProject = Join-Path $pinmameCheckout 'cmake\libpinmame\CMakeLists.txt'
$rootProject = Join-Path $pinmameCheckout 'CMakeLists.txt'
if (-not (Test-Path -LiteralPath $libPinmameProject -PathType Leaf)) { throw "Missing pinned libpinmame CMake project: $libPinmameProject" }
if (Test-Path -LiteralPath $rootProject) {
	if (-not (Test-Path -LiteralPath $rootProject -PathType Leaf) -or (Get-FileHash -LiteralPath $rootProject -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $libPinmameProject -Algorithm SHA256).Hash) { throw "Unexpected existing PinMAME root CMakeLists.txt: $rootProject" }
} else {
	Copy-Item -LiteralPath $libPinmameProject -Destination $rootProject -ErrorAction Stop
}
cmake -S $pinmameCheckout -B $pinmameBuild -DPLATFORM=win -DARCH=x64
if ($LASTEXITCODE -ne 0) { throw 'PinMAME CMake configuration failed.' }
cmake --build $pinmameBuild --config Release
if ($LASTEXITCODE -ne 0) { throw 'PinMAME native-library build failed.' }
if (git -C $pinmameCheckout status --porcelain) { throw 'PinMAME checkout became dirty during build preparation.' }
```

These local variables are the canonical writable paths for the task. Do not require the human to persist or export them. When an existing test or tool requires a legacy environment variable such as `PINMAME_VPX_SOURCES_ROOT`, set it from the derived path immediately before invoking that process. Never create replacement copies of the user's missing read-only inputs in the working directory.

Before beginning a game, confirm the current repository, applicable read-only inputs, writable evidence roots, model tiers, browser access, and the pinned native library needed by that game's gates. Report only genuine unresolved prerequisites; do not fail merely because a tool was installed outside a conventional path.

## Objective and completion standard

The objective is to cover every physical pinball machine supported by the pinned PinMAME catalog. A definition is `author_ready` only when a table author can use it to fully recreate the physical game: controller variants, switches, outputs, displays, mechanisms, physical behavior, recreation knowledge, evidence provenance, and normalized positions must all be complete and validated. A record that does not meet that standard must remain conspicuously `partial` or `stub`; never promote it for progress credit.

Only physical machines belong in scope. Exclude community rethemes, virtual-only tables, joke drivers, test drivers, non-pinball games and custom ROMs that do not run on the documented physical machine. A later firmware revision or a compatible FreeWPC/community ROM may remain a driver variant of the physical machine when it genuinely runs on that hardware; its release year does not create a new physical game. Do not group unrelated titles merely because they share a theme.

The coordinate convention follows VPX/player view in one normalized `playfield` space:

- `x = 0` is the left side and `x = 1` is the right side.
- `y = 0` is the rear/backglass end and `y = 1` is the front/apron end.
- Record playfield positions for switches, coils/controlled devices, lamps, flashers, and GI emitters. Cabinet/backbox/service devices use a controlled `not_applicable` spatial record rather than invented coordinates.
- Use one placement per physical emitter or device location. Disclose projections, shared emitters, quantities, uncertainty, and exact source roles. Never present a render helper, lightmap object, primitive origin, or script-only surrogate as an observed physical socket.

## Pinned baseline and current-state ledger

This runbook is generic policy and must stay free of individual game names, counts, claims, and
pinned revisions. All of that is mutable state and lives in `docs/CURRENT-STATE.md`: the pinned
upstream revisions and their baseline role, the reviewed scope exceptions, the current generated
coverage counts, per-game promotion notes worth carrying forward, and which games are already
claimed.

Read that file before selecting a game and update it after every material change, in the same
commit as the work it describes. When a curation lesson generalizes beyond one machine, write the
general rule here and leave the machine that produced it in the ledger. If an operational pinned
input changes, stop, produce a reviewed catalog/source diff, update every affected hash and count,
and include the scope change in the mandatory high-tier model review and maintainer PR review;
never let an upstream checkout drift silently.
## Canonical architecture and artifact ownership

The canonical product is independently versioned, VPE-neutral JSON data. Physical machine identity is primary; PinMAME driver/ROM variants attach to a physical machine, and `machine_family` groups genuine editions without erasing edition-specific hardware. A generated or flattened representation may be consumed elsewhere, but no consumer-specific implementation detail may alter canonical hashes.

Repository artifacts have distinct authority:

- `catalog/pinmame.json` is the generated driver-to-physical-machine catalog and current canonical index. It must map every in-scope driver exactly once and carry definition status and hashes.
- `controllers/pinmame/*.json` defines stable controller groups, common/platform devices, routing adapters, legal address ranges, and revision-scoped transport metadata.
- `machines/author-ready`, `machines/partial`, and `machines/stubs` contain physical-machine records honestly separated by coverage state. Moving a file between them is a validated promotion/demotion, not cosmetic organization.
- `knowledge/<manufacturer>/<machine-id>.md` contains source-linked recreation knowledge, especially mechanism behavior and edition differences that do not yet fit typed schema fields.
- `evidence/` contains portable manifests and compact derived evidence; `reports/` contains generated coverage, queue, conflict, and spatial-audit outputs. Large/source-owned artifacts remain in the configured external roots and are referenced by immutable hashes and locators.
- Root `index.json`, `games/`, and `platforms/` are legacy migration inputs and are not the canonical index or current source of truth. Do not update or consume root `index.json` as if its 22-game inventory represented coverage.
- Consumer-owned mappings such as VPE hints, Unity object names, input actions, regex match counts, DOF, B2S, and PUP metadata live outside the canonical catalog. Do not add `device_hint`, `device_item_hint`, `num_matches`, an open-ended consumer extension, or equivalent fields.

The legacy semantic definitions were in the managed integration's game classes, not `pinmame-dotnet`; `pinmame-dotnet` is the native interop wrapper. The legacy corpus is migration evidence, not unquestioned truth: it contains duplicate addresses, repeated RGB IDs, empty inventories, inherited definitions, label mistakes, and platform-specific merge behavior. Preserve anomalies as sourced candidates/conflicts until evidence resolves them; never silently normalize them during import.

## Identity, routing, inheritance, and mechanism invariants

- Keep `machine_id`, `machine_family`, `definition_version`, `controller_id`, exact `driver_id`, stable semantic `device_id`, controller `binding`, and legacy `alias` as distinct concepts. ROM hashes identify evidence/compatibility; ROM bytes never enter Git.
- Canonical semantic IDs are strings. Controller addresses remain signed numeric binding fields so negative diagnostic IDs are representable. A controller-number change may alter a variant binding without renaming the semantic device.
- Preserve required legacy numeric and zero-padded switch aliases such as `7`, `07`, and `007` while compatibility requires them. Alias cycles and ambiguous targets are errors.
- Controller groups have stable IDs scoped by provider authority and direction. Human display names are labels, not identity. Physical `kind` is separate from transport: a flasher routed through a solenoid callback remains a flasher.
- LibPinMAME and Controller Plugin routing are revisioned adapters. Any `ctrl://` URI is derived output, never canonical identity, and the experimental plugin API cannot become the sole representation.
- PinMAME's public switch state is already normalized. `controller.inversion_applied_by_emulator` is informational and must never be reapplied by consumers; `physical.normally_closed` records real hardware construction separately.
- Device kind, spatial applicability, and address availability answer separate questions. In particular, a virtual output has no physical playfield device, but it is `used` when PinMAME publishes meaningful runtime state and `unused` when the address is dead, reserved, or constant zero; never normalize availability solely from `kind` or `spatial.reason`.
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

Use a rendered crop only when the fact is a **drawing** - schematic wiring, a connector fan-out, an insert map. A printed table belongs in the transcription, where it is a kilobyte, diffable and greppable; as an image it is forty times the size and cannot be searched. Generate crops with `tools/make_excerpt.py`, which records the page, crop box, dpi and tool so the image can be re-derived, and which refuses anything over 100 kB. Do not threshold to 1-bit: printed shading is itself evidence on some machines, the shaded opto rows of a switch matrix being the obvious case. Grayscale is the default; a colour page whose colours carry meaning is a deliberate exception, and the excerpt should say why.

Embedding transcribed tables is a different act from redistributing a document. A connector-pin-to-lamp-name table is factual data, and the excerpt is what makes an assertion legible without shipping the manual. The existing prohibitions are unchanged: ROM bytes, whole manuals, and community VPX tables are never committed.

Keep assertion state fail-closed and distinguish `unknown`, `candidate`, `observed`, `validated`, `conflicted`, and `deprecated`. A toggling output is only an observation, not proof of its semantic identity; failure to observe an address is never proof that it is unused. Exact agreement between sources does not prove independence when they may share ancestry.

When a manual's wiring, parts list, or assembly drawing proves that a lamp, GI string, or flasher is physically on the playfield, backbox, or cabinet while a known-working script binds a visual proxy somewhere else, split the authorities: the manual controls physical and spatial classification, while the script controls runtime binding. Record the disagreement as a conflict and do not promote the proxy coordinate as the physical device's position.

Track coverage dimensions separately: identity, controller platform, input/output/display enumeration, semantic names, physical kind/wiring/polarity, emulator normalization, diagnostic enumeration, runtime observation, causal exercise, mechanism inventory/behavior, spatial placement, variant differences, recreation notes, provenance, and unresolved conflicts. `coverage.status` is exactly `stub`, `partial`, or `author_ready`, with a machine-readable `coverage.missing` list. Only the completeness validator may justify `author_ready`; no authoring-relevant unknown/conflict, unnamed required address, missing physical/controller variant, incomplete mechanism topology, missing spatial record, or missing recreation note may remain.

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

Search for VPX tables in this order:

1. Each folder in `PINMAME_EXISTING_VPX_TABLES`, in the supplied order
2. `vpuniverse.com`
3. `vpforums.org`

Do not spend time searching for a Pro recreation while a Premium or LE version exists; community authors usually recreate the higher tier because there is no extra virtual cost. Finish higher-tier and non-Pro work first. Never derive Pro geometry from a Premium/LE table without an explicit edition overlay and supporting evidence.

Organize retained table artifacts under `<working-root>/vpx-sources/<manufacturer>/<machine-slug>/`. Keep the downloaded `.vpx`, script sidecars, extracted `vpxtool` output, reports, and provenance metadata. Move downloads out of the user's Downloads folder promptly. After a downloaded archive has been safely extracted and its contents verified in the organized source directory, the archive itself may be deleted; do not delete the retained VPX or extraction.

Organize manuals under `<working-root>/manuals/by-machine/<machine-id>/` and keep `<working-root>/manuals/manifest.json` reconciled. Retain original PDFs, hashes, attribution, source page/download URLs, extracted text/tables, and useful rendered reference pages. Manuals are a reusable research archive and must not be discarded after a game is completed.

Use `PINMAME_ROM_LIBRARY_ROOT` as the user's authorized existing read-only ROM corpus. New ROM downloads belong only in `<working-root>/roms/`, never in Downloads or this Git repository. Pass that derived folder explicitly to the harness or analysis tool that needs it. Commit hashes, archive/member metadata, and analysis results only; never commit ROM bytes or modify, redistribute, or delete the user's existing ROMs.



## Model and tool allocation

Be conscious of model cost while matching capability to judgment. Use these current tier assignments; verify that the exact model or alias is available through its CLI before relying on it, and update this table when a provider supersedes a listed model.

| Tier | OpenAI through Codex CLI | Anthropic through Claude Code CLI | Default role |
| --- | --- | --- | --- |
| High | `gpt-5.6-sol` at `xhigh` | `opus` at `high` effort | difficult curation, escalation, promotion decisions, and independent final review |
| Mid | `gpt-5.6-terra` at `xhigh` | `sonnet` at `high` effort | structured research, implementation, spatial mapping, and test work with clear evidence |
| Low | `gpt-5.6-luna` at `xhigh` | `haiku` at `high` effort | bounded mechanical extraction, OCR cleanup, inventories, hashes, and report generation |

### Low tier: mechanical and low-judgment work

Delegate bounded, verifiable jobs such as file inventory, VPX object-candidate extraction, exact-name-to-coordinate mapping, device counts, evidence hashing, straightforward OCR cleanup, mechanical report generation, or drafting test fixtures from an already-decided mapping. Do not delegate source-authority decisions, semantic conflict resolution, physical-family identity, custom-mechanism conclusions, promotion decisions, or schema design to the lower-cost tier.

Every delegated prompt must include exact input paths, an exact output scope, the coordinate convention, evidence authority, non-negotiable fail-closed rules, and commands that prove success. Require the worker to report uncertainty rather than resolve it by assumption. The primary contributor must inspect the resulting artifacts and evidence rather than accepting the worker summary.

### Mid tier: structured curation and implementation

Use the mid tier for research synthesis when authoritative sources agree, deterministic curator and fixture implementation from settled requirements, spatial mapping with explicit VPX candidates, test-failure triage, and other work that requires context but not a novel authority decision. Escalate immediately when evidence conflicts, physical identity is ambiguous, a mechanism must be reconstructed, or author-ready promotion depends on the conclusion.

### High tier: curation and escalation

Use `gpt-5.6-sol` or `opus` for source-authority conflicts, variant/family identity, physical-versus-runtime disagreements, custom mechanism reconstruction, projection policy, incomplete evidence, reverse-engineering questions, schema changes, integration conflict resolution, and promotion decisions. Inspect the actual retained evidence whenever a decision changes author readiness.

### High-tier model: mandatory pre-submission review

Before opening or updating a PR for maintainer review, have an independent high-tier model perform a read-only review of the exact proposed contribution. Prefer a different provider from the model that performed the primary curation: work led by `gpt-5.6-sol` should be reviewed by `opus`, and work led by `opus` should be reviewed by `gpt-5.6-sol`. If the other provider's high-tier model is available, cross-provider review is mandatory because it reduces correlated blind spots. Only when the other provider is genuinely unavailable may a fresh, independent high-tier session from the same provider be used; disclose that limitation in the PR.

Give the reviewer the base branch/commit, contribution `HEAD`, `git write-tree` hash, complete base-to-head diff and path list, unstaged/untracked state, retained evidence paths and hashes, acceptance criteria, and fresh gate results. Ask it to find discrete accuracy, provenance, determinism, schema, test, scope, and maintainability problems rather than edit files.

Verify every finding independently, fix valid issues, rerun all affected gates, and repeat the high-tier review after any material change. Record the reviewed `HEAD` and tree hash in the PR description so maintainers can tell whether later pushes invalidated it. A model review is advisory quality control, not project approval, and it never authorizes merge.

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

Check the current-state ledger and open PRs/issues to avoid duplicating claimed work. Finish existing partial games before starting untouched games, ordered by physical release date newest first except for explicit maintainer priorities. Finish higher-tier and non-Pro work before opening any new Pro search; do not abandon an already-started Pro contribution merely because Pro searches are otherwise deferred.

Create one branch and one worktree per game under `<working-root>/worktrees/pinmame-game-defs-<slug>`, based on the latest reviewed `master` integration commit. Before creating it, verify that the exact target does not exist and the branch name is unused. Do not mix two games in one staged tree.

Record the worktree path, branch, base commit, active model tiers/sessions, evidence roots, and current coverage status in this file's current-state ledger.

### 2. Inventory the physical family and variants

Trace every PinMAME root/clone driver for the physical title. Confirm physical manufacture year, manufacturer, model, IPDB identity, editions, display/controller hardware, language revisions, prototypes, conversions, FreeWPC/community firmware, and whether any driver is virtual-only. Group only firmware compatible with the physical machine. Keep distinct physical editions separate when their playfields or hardware differ, even if they will later share a `machine_family` identifier.

Check that no obsolete stub still claims a driver moved into the curated definition. Regenerate the exact catalog after driver grouping changes and add regression tests for historically confusing identities.

### 3. Acquire and pin evidence

Search local VPX folders before VPU/VPF. Prefer the exact physical edition; a Premium/LE table is not geometry proof for a Pro. Verify that the table script actually runs the expected ROM family. Extract the VPX with `vpxtool`, retain the original and extracted files, and compare the embedded script with any sidecar.

Acquire the official manual/schematics from the manufacturer, IPDB, Archive.org, Arcade Archive, or another attributable source. Hash the original PDF and record exact page locators. Render pages containing switch, lamp, solenoid, GI, mechanism, connector, ball-path, and playfield diagrams. If text extraction is empty or poor, OCR the relevant pages; never treat OCR as more authoritative than the rendered page.

Index the authorized ROM archive and PinMAME sources when needed. A retained extraction-integrity assertion must be reproducible: define the canonical manifest algorithm, include every relative POSIX path with byte size and SHA-256 in sorted order, hash canonical JSON bytes, and test recomputation against the retained extraction. Never hard-code an unexplained manifest digest.

### 4. Build the semantic definition

Start from the existing partial or a deterministic seed. Enumerate all controller inputs, outputs, displays, mechanisms, and driver variants. Give every address a semantic disposition: used, unused, cabinet/service, duplicate/shared, or explicitly unresolved. Preserve matrix ranges and special/direct-switch namespaces exactly; do not silently drop an address because the VPX does not use it.

For each mechanism, document enough knowledge to recreate it: physical topology, moving parts, actuators, sensors and marks, switch/coil causality, ball paths, default/home state, startup behavior, timing clues, reset behavior, jams/failure modes, and edition differences. Keep this prose in `knowledge/<manufacturer>/<machine>.md` even if structured mechanism fields cannot yet express all useful details.

Relationships must express physical or proven causal behavior, not merely proximity or convenient script routing. Do not claim that an outhole coil actuates a trough switch or that a kicker directly actuates a gun mark unless the mechanism really does so.

### 5. Add normalized spatial evidence

Use the exact retained VPX table bounds and object coordinates. Normalize with the repository helper; do not hand-round inconsistently. Prefer exact physical object centers or meaningful wall/trigger centroids. Use a documented projection only when no direct physical object exists and the projection is defensible from manual/table geometry. Assign stable placement IDs and roles, enforce unique IDs, keep coordinates in range with at most six decimal places, and align quantity with placements.

Map lamps to physical bulbs, not primitives or lightmap helpers. Reconcile shared RGB channels and co-located emitters explicitly. For GI, distinguish playfield bulbs, rear-panel bulbs, and coin-door/cabinet bulbs; playfield/rear placements and cabinet quantity may need different treatment. Displays are cabinet/backbox devices and require controlled `not_applicable` spatial evidence with both PinMAME core and manual/human-review provenance.

Generate a machine-specific spatial audit report listing exact evidence artifacts, hashes, extraction manifest, transformation, every projection class, unresolved records, and promotion decision. When any authoring-critical placement or semantic conflict remains, keep `coverage.status = partial`, name the missing dimensions, and make the blocker concrete.

### 6. Make generation deterministic

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

Update the contribution branch against the latest `master` before final review. Resolve conflicts by preserving all newer upstream work and applying the game's delta. Common conflicts are generated catalog/coverage/queue files, pending spatial sets, hard-count regression tests, and this runbook's current-state ledger. Rebuild generated files and update combined counts from the actual repository; never choose one stale side wholesale.

Run the full gates on the exact clean PR candidate, then obtain the mandatory independent high-tier model review described above. Fix valid findings and repeat both testing and model review until the reviewed `HEAD` and tree hash match the proposed PR exactly. Push the contributor branch and open or update a PR targeting `master`, including evidence locations, coverage status, gate results, and the reviewed hashes. Maintainers perform the authoritative final review and decide whether to approve or merge; contributors and model reviewers must not represent their review as maintainer approval.

### 10. Remove the completed worktree after maintainer disposition

After maintainers merge or otherwise close the PR and all wanted work is preserved remotely, remove the per-game worktree. Resolve and inspect the exact absolute target under `<working-root>/worktrees/`; verify it is the expected directory, not a reparse point, on the expected branch/commit, and completely clean. Use `git worktree remove <exact-path>` without `--force`. Stop if any check or removal fails. Never recursively delete a worktree directory, broaden the target, or discard unexplained files. Prune only stale administrative entries after the directory is safely gone.

Keep evidence archives outside the Git worktree. Removing a completed code worktree must not remove manuals, VPX tables/extractions, review artifacts, or ROM indexes.

## Parallel work and status reporting

Do useful independent work while a worker or reviewer model runs. Separate games into separate worktrees so one review does not block another. Do not edit the same worktree concurrently, and do not let a reviewer mutate the exact tree it is reviewing. At most one contribution tree should be in conflict resolution at a time.

Report status at least hourly while work is ongoing. Include a percentage indicator, completed/in-review/blocked games, exact branches or commits when useful, current author-ready/partial/stub counts, active worker/reviewer state, concrete blockers, next actions, and whether completed worktrees were cleaned. The percentage is an implementation-progress indicator, not false machine-coverage credit; author-ready coverage must always be reported separately from partials and stubs.

Keep this runbook's current-state ledger, the live task plan, `catalog/pinmame.json`, `reports/coverage.*`, and `reports/curation-queue.*` synchronized after every material change. Record when a game stays partial and why. The user explicitly asked not to stop until all supported physical PinMAME games are covered or the user says to stop; when blocked on one game, continue safe work on another rather than ending the project.

## Harness and reverse-engineering escalation

Static source extraction can enumerate controller structure but cannot prove every semantic name or custom mechanism. Use the implemented LibPinMAME gameplay harness for unresolved runtime behavior: boot a legal user-supplied ROM, drive switches, capture lamps/solenoids/displays, preserve NVRAM/reset conditions, and produce content-addressed traces without ROM bytes. Define explicit scenarios and expected causal transitions instead of free-play logs.

Escalate to Ghidra only for authoring-critical facts still unresolved after manual, VPX script, PinMAME source, ROM strings/data tables, and harness traces. Follow the approach used in the `kiki` project, normally discovered as a sibling of this repository: identify the exact ROM, loader/CPU memory map, entry points, I/O tables, state variables, and mechanism routines; document addresses and confidence; confirm static conclusions with runtime traces when possible. Do not promote speculative decompilation labels to validated physical facts.

## Machine families and edition prose

After the spatial-update backlog, add a stable `machine_family` identifier that groups the editions of one physical title, for example a manufacturer's Pro, Premium, Limited Edition, and Vault builds of the same game. Keep unrelated games in different families even when they share a theme or a licensed name, including cases where two manufacturers released differently titled machines from the same licence. Research and cite concise prose explaining the physical and rules/hardware differences among editions. A family identifier enables navigation and shared evidence; it must not erase edition-specific devices, geometry, mechanisms, or driver compatibility.

## Project-wide curation completion gates

Per-game success is necessary but not sufficient. Keep working until every gate below is proved by current generated artifacts and tests, or until the user explicitly stops the run:

- The exact pinned `PinmameGetGames` result is captured from the resolved native PinMAME library; every in-scope driver appears exactly once, every retained clone parent resolves, every reviewed virtual-only exclusion remains absent, physical-family exceptions are explicit, and catalog regeneration is byte-for-byte deterministic. Environment-dependent ROM availability such as `PinmameGame.found` is local-report data and must not affect canonical hashes.
- PinMAME structural extraction records controller generation, active groups/counts, remaps, common inputs, emulator normalization, output types, displays, custom ranges, and simulation/mech hook presence with the exact PinMAME revision. Generic generated labels are scaffolding, never validated semantics.
- Both pinned VPX script corpora are inventoried deterministically, every eligible script is hashed, controller IDs and I/O/mechanism candidates are extracted with exact locators, table revisions are grouped without erasing provenance, conflicts remain first-class, and parser inference never rises above candidate status by itself.
- The legacy 11-class managed corpus and old JSON corpus remain covered by migration/compatibility fixtures, including numeric and zero-padded aliases, negative diagnostics, platform-specific merge behavior, duplicate/collision cases, direct flipper relationships, and authored mech reverse resolution. The hint migration report explicitly drops all authoring hints, and unresolved semantic device references hard-fail rather than silently becoming controller ID `0`.
- Schema and semantic validation reject invalid JSON, stale generated files, duplicate or illegal bindings, alias cycles, dangling imports/models, mixed ID types, unsupported transports, illegal re-inversion, ambiguous inheritance, spatial violations, and dishonest promotion. Representative valid artifacts and every known failing fixture are tested.
- Runtime evidence uses the pinned library and legally supplied ROMs in isolated per-run state. Run manifests pin ROM and emulator hashes, NVRAM initialization, service language, actions, timeouts, normalized observations, and output/display checkpoints. ROM bytes and NVRAM blobs remain external; host input readback is never treated as ROM evidence; wrong-switch, wrong-output, wrong-idle-state, and wrong-mechanism fixtures must fail clearly.
- Every one of the 785 physical-game records is `author_ready`, every supported physical/controller variant is accounted for, and the generated completion gate is true. Stubs contribute zero coverage; partials are not publishable as complete entries; the non-game diagnostic remains separately classified.
- Machine families and cited edition-difference prose are complete without conflating unrelated titles or collapsing edition-specific devices, geometry, mechanisms, or compatibility.
- All reviewed curation work is integrated on `master`, no required change remains only in a worktree, generated catalogs/reports match the integrated tree, and completed branches/worktrees are safely cleaned.

## Final curation handoff

External contributors submit a focused PR targeting `master` and wait for maintainer review; they do not merge their own contribution. Maintainers perform the final evidence/code review and own integration decisions.

The curation project is complete only when every in-scope physical PinMAME machine resolves to an exact definition and every record is honestly classified. The final handoff must include coverage totals, remaining partial/stub blockers if the user stops early, validation results, branch/commit locations, retained evidence locations, and confirmation that completed worktrees were cleaned.
