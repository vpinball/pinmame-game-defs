# Contributing to the PinMAME machine catalog

This repository describes what PinMAME-supported pinball machines are made of: every switch, lamp,
coil, display and mechanism, the address the emulator reports for each one, and the evidence behind
every claim.

A good contribution names one fact and cites where it came from. That is worth more than a large
change nobody can verify.

## Two kinds of contribution

**Correcting something.** Every page of the [reference site](https://games.visualpinball.org/)
links the exact file it renders. Click *Edit the definition*, change the line, and GitHub forks the
repository and opens the pull request for you — no local checkout needed.

**Describing a machine nobody has covered yet.** Hundreds of machines are still generated stubs. If
you own one, have its manual, or have already built a working table for it, you can move it from
`stub` to `partial` and eventually to `author_ready`. If you have AI inference to spare, point your agent
to [`docs/INSTRUCTIONS.md`](docs/INSTRUCTIONS.md) and get it to work.

If you're using agents to do the work, there are a few prerequisites.

- VisualPinMAME should be installed, with an accessible `./roms` folder.
- The tooling needs [Python](https://www.python.org/downloads/) installed.

Tell the folder locations to the agent in your prompt, or set them as env variables as documented [here](docs/INSTRUCTIONS.md#existing-read-only-inputs). 
Also tell it your VPX table collection folders to avoid having to download the tables it's working on another time.   

## The rules that matter most

**Cite a source for everything.** Each non-trivial assertion references a record in the definition's
`sources` array. `license` and `attribution` are mandatory for `manual` and `vpx_script` records.
A claim without provenance cannot be validated and will not be merged.

**Never commit ROMs, manuals, or table files.** The repository stores extracted facts, locators and
SHA-256 hashes — not the documents themselves. `index-roms` deliberately hashes an authorized corpus
without extracting anything from it.

**Precedence is domain-specific.** When sources disagree:

| Question | Winner |
| --- | --- |
| Controller addresses, callbacks, ball routing, mechanism causality | A known-working VPX script |
| Wiring, connectors, wire colours, part numbers, switch construction, assembly geometry | The operator manual |
| Emulator group routing, display layout, output typing, normalisation | Pinned PinMAME source |

A lower-priority source may still open a conflict when the higher-priority one is ambiguous,
incomplete, or is clearly implementing a virtual simplification rather than the physical mechanism.
Record it in `conflicts` rather than quietly picking a side.

**Coverage is fail-closed.** Only the completeness validator may set `author_ready`. It refuses while
any address is unnamed, any mechanism lacks its actuators and sensors, a supported variant is
unaccounted for, or the recreation note is missing. Do not hand-edit `coverage.status`.

**Provenance is per assertion, and separate from coverage.** Use `unknown`, `candidate`, `observed`,
`validated`, `conflicted` or `deprecated` honestly. "Output 11 toggled" is `observed`; "output 11 is
the gun motor" needs more. Failing to observe an output is not evidence that it is unused.

**Keep consumer concerns out.** No Unity object-name regexes, no VPE input-map actions, no
device-matching hints. Portable roles such as `cabinet.start`, `service.up` and `flipper.lower.left`
are fine — the consuming engine owns the mapping.

**Polarity belongs to hardware.** Where a platform profile sets `inversion_applied_by_emulator`,
PinMAME already reports logical active state; never invert again. `normally_closed` describes the
real part and stays a physical fact.

## Making a small correction

1. Open the machine on the reference site and click **Edit the definition** (or **Edit the note**).
2. Change the one thing that is wrong.
3. In the pull request, say where the correct value came from: manual page, VPX script line, PinMAME
   source path, or a reading from the machine's own service menu.

If a source record for that evidence does not exist yet, add one — see `schemas/machine.schema.json`
for the required fields.

## Describing a machine

Work from a checkout:

```powershell
$env:PYTHONPATH = "src"
python -m pinmame_game_defs --help
```

A typical path from stub to partial:

1. **Gather evidence.** `extract-vpx` mines the pinned VPX script corpora for candidate addresses and
   mechanisms. `extract-pinmame-sims` does the same for PinMAME's own simulator data. Both write to
   `evidence/`, and both produce `candidate` facts — never `validated` ones.
2. **Acquire the manual** with `acquire-url-manual` or `acquire-archive-manual`, then `extract-manual`
   for deterministic text and tables. The PDF stays in the external cache; only facts and locators are
   committed.
3. **Curate.** Turn candidates into a definition under `machines/partial/<manufacturer>/`, naming every
   address — including the ones that are genuinely `unused`. An address nobody has looked at and an
   address confirmed empty are different facts.
4. **Write the note** at `knowledge/<manufacturer>/<machine-id>.md`: edition differences, mechanism
   behaviour, tuning values from a working table, and the pitfalls. Start it with a
   `Coverage: **…**` line — the reference site renders it as the note's summary.
5. **Validate and report:**

```powershell
python -m pinmame_game_defs validate
python -m pinmame_game_defs coverage
python -m unittest discover -s tests -v
```

`validate` checks catalog reachability, hashes, canonical fields, references and the author-ready
gates. It must pass before a pull request is ready.

## Editions of one title

Stern shipped most games as a Pro and a Premium/LE with genuinely different playfields, so each is
its own physical machine. Group them with `families/<slug>.json`:

```json
{
  "format": "pinmame-machine-family",
  "schema_version": 1,
  "family": { "id": "stern.ac-dc", "title": "AC/DC", "manufacturer": "Stern" },
  "members": [
    { "machine_id": "stern.ac-dc-pro.2012", "edition": "Pro",
      "differences": "What this edition has that its siblings do not." }
  ],
  "knowledge": { "path": "knowledge/families/ac-dc.md" }
}
```

Write `differences` for the reader who has to pick an edition to build. Device counts are already
compared automatically — prose should explain what the counts cannot: which physical toy, ramp or
playfield level accounts for them, and whether a table built against one edition binds correctly
against another.

## Identity conventions

| Identifier | Example | Meaning |
| --- | --- | --- |
| `machine.id` | `stern.metallica-pro.2013` | One physical product — one playfield, one wiring loom |
| driver id | `mtl_180h` | An exact PinMAME ROM set; many resolve to one machine |
| device id | `switch.fuel-lane-rollover` | A stable semantic name a table binds to |
| `binding` | `pinmame.input.switch` + `52` | The address group and signed device number |

Device IDs are the contract. A controller number may change in a variant patch; the device ID must
not, or every table mapping breaks.

## Pull request checklist

- [ ] Every changed or added assertion cites a source record.
- [ ] `license` and `attribution` set on any new `manual` or `vpx_script` source.
- [ ] No ROM, manual or table binaries committed.
- [ ] `python -m pinmame_game_defs validate` passes.
- [ ] `python -m unittest discover -s tests` passes.
- [ ] `coverage.status` left to the validator.
- [ ] Disagreements recorded in `conflicts` rather than silently resolved.

## Where to read more

- [`docs/INSTRUCTIONS.md`](docs/INSTRUCTIONS.md) — Instructions for agents.
- [`schemas/`](schemas/) — JSON Schema for machines, controllers, the catalog and evidence.
- [Reading a definition](https://games.visualpinball.org/guide) — the same vocabulary,
  explained for readers rather than authors.
- [Schema reference](https://games.visualpinball.org/schema) — every field of every
  type, generated from `schemas/` on every deploy. A schema change documents itself; you do not need
  to update the site. Plain-English notes for fields the schema does not describe live in
  `site/scripts/prepare-schema.ts`.
