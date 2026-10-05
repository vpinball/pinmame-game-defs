# Environment setup

On-demand companion to `docs/INSTRUCTIONS.md`. Read it when preflight finds a tool, input, checkout or native library missing or unverified, and before delegating to or reviewing with a model CLI; it is not loaded by default.
The runbook wins where the two disagree.

**Belongs here:** discovering and smoke-checking tools and agent CLIs, the CLI calls for workers and reviewers, resolving read-only inputs, and creating the working root, the pinned source checkouts and the native library.

**Does not belong here:** the pinned revisions themselves (`docs/CURRENT-STATE.md`), harness runs (`docs/HARNESS.md`), or where evidence of a particular kind is searched for and retained (`docs/SOURCES.md`).

## Mandatory prerequisites and discovery

Required capabilities are a hard gate, but a command missing from `PATH` or an unset convenience variable is not itself proof that the capability is unavailable. Start in this repository, derive its root with `git rev-parse --show-toplevel`, and inspect `PATH`, common installed-tool locations, workspace-provided runtimes, sibling repositories, and existing project folders. Record the resolved commands, versions, and external roots. If an applicable human-owned tool or read-only input still cannot be resolved, ask the human to provide its executable or folder before declaring that line of work blocked. The three public source repositories managed below are the exception: clone them automatically and report clone/network failures instead of asking the human for checkout paths. Abort only after reasonable discovery plus any applicable human request shows that a required capability or source is genuinely unavailable; do not silently omit the affected evidence or replace it with a weaker source/model. Do not install software or create substitute read-only source folders without contributor approval.

### Tool capabilities and download sources

| Capability | Used for | Installation or download source |
| --- | --- | --- |
| Git 2.23 or newer (`git`) | branches, worktrees, pinned filtered clones, exact-state review, commits, and PR preparation | [Git downloads](https://git-scm.com/downloads) |
| Python 3.13 or newer plus this package's dependencies | deterministic curators, catalog generation, validation, the PinMAME harness, PDF parsing, and tests | [Python downloads](https://www.python.org/downloads/); install this repository with `python -m pip install -e ".[tools]"` in an isolated environment when dependencies are not already available |
| ripgrep (`rg`) | first-choice source and file discovery | [ripgrep releases](https://github.com/BurntSushi/ripgrep/releases) |
| `vpxtool` | VPX identity inspection, script/object extraction, and spatial evidence | [vpxtool releases](https://github.com/francisdb/vpxtool/releases); record the exact version in evidence, and use v0.33.3 only when reproducing artifacts explicitly pinned to `vpxtool git:v0.33.3` |
| An archive extractor capable of RAR and ZIP, normally 7-Zip | inspecting and extracting retained VPX, ROM, and manual archives | [7-Zip downloads](https://www.7-zip.org/download.html) |
| A working PDF extraction/rendering toolchain, normally Poppler's `pdfinfo`, `pdftotext`, and `pdftoppm` plus the Python dependencies | PDF identity checks, text extraction, and rendered manual pages | [Poppler Windows builds](https://github.com/oschwartz10612/poppler-windows/releases) |
| OpenAI Codex CLI (`codex`), installed, authenticated, and working non-interactively when OpenAI models are used | running latest gpt sol, gpt terra, or gpt luna workers and reviewers | [Codex CLI documentation](https://developers.openai.com/codex/cli) |
| Claude Code CLI (`claude`), installed, authenticated, and working non-interactively when Anthropic models are used | running `opus`, `sonnet`, or `haiku` workers and reviewers | [Claude Code setup](https://docs.anthropic.com/en/docs/claude-code/getting-started) and [CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage) |
| Working CLI access to the model tiers required by the allocation policy in `docs/INSTRUCTIONS.md` | high-judgment curation, economical delegated extraction, and mandatory pre-submission review | At least one high-tier CLI is mandatory; when another provider's high-tier model is available, its CLI must also work so the final review can be cross-provider |
| An authenticated interactive browser or working browser automation | Cloudflare-gated IPDB/VPU/VPF research and downloads | [Google Chrome](https://www.google.com/chrome/) or [Puppeteer](https://pptr.dev/guides/installation) |
| Pinned PinMAME source and a compatible built native library | authoritative driver inventory and runtime-harness traces | [vpinball/pinmame](https://github.com/vpinball/pinmame); if no compatible library can be found, use the concrete CMake preparation and out-of-source build recipe below with a suitable C/C++ toolchain |

Tool names above are conventional, not mandatory installation paths. Locate an existing executable first, run a small version/smoke check, and use its fully qualified path when it is not on `PATH`. For the native library, search the final agent-managed PinMAME checkout and `<working-root>/builds/pinmame` for `pinmame64.dll`, `libpinmame.dll`, `libpinmame.so`, or `libpinmame.dylib`, explicitly excluding every `.incoming-*` tree; use `PINMAME_LIBRARY_PATH` only as an optional disambiguation override. If multiple plausible libraries exist, identify the one built from the pinned revision instead of choosing by filename alone.

### Agent CLI operation

Do not treat an installed executable as proof that an agent CLI works. For every provider intended for the contribution, run its version and doctor commands, verify authentication, and make a small non-interactive call using each required model alias. Run `codex --version` and `codex doctor` for Codex; run `claude --version` and `claude doctor` for Claude Code. If an applicable CLI cannot authenticate, select the named model, read the required files, or return output, fix it before delegating work or starting review. Record genuine provider unavailability rather than pretending that an inaccessible model performed a review.

Use PowerShell here-strings or prompt files for substantial prompts so shell expansion and quoting do not alter the instructions. Resolve and validate `$worktree` first. Resolve the latest available model in each required family from current provider model metadata and verify it through the CLI before use; never copy a version from an earlier run. Set `$latestTerraModel` and `$latestSolModel` below to those resolved model identifiers, not the literal string `latest`. Codex models use `xhigh` reasoning for this project; Claude models use `high` effort. Typical non-interactive worker calls are:

```powershell
$prompt = @'
Read docs/INSTRUCTIONS.md, then perform only the bounded task described below.
Report uncertainty and do not guess.
'@

$prompt | codex exec -C $worktree -m $latestTerraModel -c 'model_reasoning_effort="xhigh"' -s workspace-write -

Push-Location -LiteralPath $worktree
try {
	claude -p --model sonnet --effort high --permission-mode acceptEdits $prompt
} finally {
	Pop-Location
}
```

Select the latest GPT Sol, GPT Terra, or GPT Luna with Codex's `-m` option using the resolved identifier. Use the unversioned `opus`, `sonnet`, or `haiku` alias with Claude Code's `--model` option and verify that it resolves to the latest available model in that family. Do not substitute another family when the required tier is unavailable. Run a reviewer without edit permission: use `codex exec` in a read-only sandbox, because `codex review --base` accepts no custom prompt, and use Claude Code with `--permission-mode plan`. Name the base commit in the prompt. Typical review calls are:

```powershell
$reviewPrompt = @'
Perform an independent read-only review of the exact contribution tree: git diff <base>..HEAD.
Report only discrete, actionable findings; do not edit files.
'@

$reviewPrompt | codex exec -C $worktree -m $latestSolModel -c 'model_reasoning_effort="xhigh"' -s read-only -o $reviewFindingsPath -

Push-Location -LiteralPath $worktree
try {
	claude -p --model opus --effort high --permission-mode plan $reviewPrompt
} finally {
	Pop-Location
}
```

Start each CLI in the exact game worktree and explicitly grant access only to required external evidence roots. Capture the final response under the sibling working directory's `review-artifacts` folder together with the reviewed commit and tree hashes.

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
	@{ Name = 'pinmame'; Url = 'https://github.com/vpinball/pinmame.git'; Revision = '97aa922bf8e4b6970126192ec1ac1fb0305a4f62' },
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
