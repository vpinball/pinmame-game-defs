# PinMAME Machine Reference

A static, browsable reference for the [`pinmame-game-defs`](https://github.com/vpinball/pinmame-game-defs)
catalog — the switches, lamps, coils, displays and mechanisms a table author needs to recreate a
PinMAME-supported machine, plus the evidence behind every claim.

The site renders the catalog and adds nothing to it. If a fact is not in the definitions, it is not
on the page.

## What it gives a table author

| Route | Purpose |
| --- | --- |
| `/` | Overview, coverage at a glance, entry points |
| `/machines` | Browse every physical machine, filter by coverage, manufacturer, platform and hardware (kicker, drop target bank, diverter, DMD size…) |
| `/machines/<slug>` | The reference page: wiring setup, switch/lamp maps, device tables, mechanisms, direct wiring, recreation notes, ROM sets, evidence |
| `/roms` | Look up any of the ~2 900 driver IDs and follow it to its machine |
| `/platforms` · `/platforms/<slug>` | Controller profiles: legal address ranges, transports, normalisation rules |
| `/families/<slug>` | One title, all its editions, with a side-by-side comparison of what differs |
| `/coverage` | Completion report and curation queue |
| `/guide` | How to read a definition — identity, bindings, polarity, roles, provenance, evidence precedence |
| `/schema` | Every field of every type, generated from the JSON Schemas themselves |

`⌘K` / `Ctrl K` (or `/`) opens a search across every machine **and** every ROM set.

## Stack

- **Nuxt 4** + TypeScript, prerendered to fully static HTML (`nitro.preset: 'github_pages'`)
- **Tailwind CSS v4** via `@tailwindcss/vite`, tokens defined in `app/assets/css/main.css`
- **`@nuxt/icon`** with a locally bundled Lucide collection — no network calls at runtime
- No server and no client-side API.

## Running it

```bash
npm install
npm run dev
```

`npm run dev` regenerates the data layer first, then starts Nuxt on `http://localhost:3000`.

### Where the catalog comes from

`scripts/prepare-data.ts` looks for a `pinmame-game-defs` checkout in this order:

1. `$PINMAME_DEFS_ROOT`
2. the parent directory — this is the case once the site lives inside the defs repo as `site/`
3. `../pinmame-game-defs`
4. `../.worktrees/pinmame-game-defs-machine-definitions`

Point it somewhere else with:

```bash
PINMAME_DEFS_ROOT=/path/to/pinmame-game-defs npm run dev
```

## Building

```bash
npm run generate
```

This runs the data pipeline, prerenders every route into `.output/public`, then runs
`scripts/verify-build.ts`, which fails the build if any expected machine, platform or static asset
is missing. Nitro is deliberately configured with `failOnError: false` so a single malformed
definition cannot block a deploy — the verifier is what turns a silently missing page into a loud
error naming the route.

Preview the output with `npx http-server .output/public`.

### Schema reference

`/schema` documents every type in the catalog's formats — one table per type, with field names,
types, enum values, constraints and which are required. It is **generated from the JSON Schemas**,
not written by hand: `scripts/prepare-schema.ts` walks `schemas/machine.schema.json` and
`schemas/controller.schema.json` and emits `data/schema.json`, which the page renders directly. A
field added upstream documents itself on the next build.

Inline objects get an entry of their own rather than being flattened into their parent's row, so
nothing in the schema goes undescribed. Two things are derived rather than transcribed: a reverse
index (`binding` says it is used by `input.binding`, `output.binding`, `device override.binding`),
and the constraints that are about a whole object rather than one field — an `allOf` conditional
becomes "When coverage.status is author_ready, schema_version is 2", and a `oneOf` of alternative
required sets becomes "Needs exactly one of minimum and maximum, or values".

Two things the schema genuinely cannot express are stated in the generator instead: which
`identifier` fields hold the id of something else (in JSON Schema they are all just strings), and a
sentence for the fields with no upstream `description` whose names do not carry the meaning. Both are
keyed by field path and **reported as a warning when the field they name disappears**, so they cannot
quietly rot. Anything the schema does describe is left alone — that text is the schema's to own.

### Manufacturer marks

`app/assets/icons/*.svg` holds the maker logos. They arrive as standalone drawing-tool documents,
which is not the same thing as a symbol you can drop into a page several times, so
`scripts/prepare-icons.ts` normalises them into `data/icons.json`:

- **Colour is baked in.** Some carry `fill: #231f20` and the rest default to black, so either way
  they vanish against the dark theme. Every mark is redrawn in `currentColor` and inherits the
  surrounding text colour, which is also what makes them work in both themes.
- **The class names collide.** Each file styles its shapes with `.cls-1` through an embedded
  `<style>`, and CSS inside inline SVG is *global* — with two marks on one page the last `.cls-1`
  wins for both. Since Midway's is the only one carrying `fill-rule: evenodd`, that is the
  difference between a logo and a filled-in blob. Declarations move onto the shapes as presentation
  attributes and the stylesheet is dropped.

`BrandMark` resolves a platform id or a manufacturer name to a mark via `app/utils/brand.ts` and
falls back to a neutral glyph, which is the common case — six marks against 19 platforms and 71
manufacturers. Platform ids are mapped explicitly rather than by substring, because `s11`, `s7` and
`wpc` are Williams hardware with the word "Williams" nowhere in them. `pinmame.whitestar` is
deliberately unmapped: the catalog calls it "Sega/Stern Whitestar", and stamping either logo on it
would assert something the name refuses to.

The mark replaced the platform's short id, which is what used to overflow its own tile —
`DATAEAST` did not fit, and `STERN-MPU200` would not have at any readable size. Nothing is lost,
because the tile always sits beside the name it stands for.

## Deploying to GitHub Pages

The site lives inside `pinmame-game-defs` and rebuilds on every catalog change. Its workflow is installed at the repository root as `.github/workflows/deploy.yml`, the contribution guide is at root because site actions link it there, and `site/public/CNAME` preserves the production custom domain in the generated artifact. In the repository settings, set **Pages → Source** to **GitHub Actions** and configure `games.visualpinball.org` as the custom domain.

The workflow sets `PINMAME_DEFS_ROOT` to the repo root, `NUXT_APP_BASE_URL` to `/`, and `NUXT_PUBLIC_SITE_URL` to `https://games.visualpinball.org`. Forks using a GitHub project-page subpath must override both URL values.

> Testing a subpath build locally on Windows: Git Bash rewrites a leading-slash value into a Windows
> path, so `NUXT_APP_BASE_URL=/pinmame-game-defs/` silently becomes `C:/Program Files/Git/…`. Prefix
> the command with `MSYS_NO_PATHCONV=1`, or use PowerShell.

`NUXT_PUBLIC_REPO_BRANCH` controls which branch the "Definition JSON" and "Notes source" links point at; it defaults to `master` for local development.

## Data layer

`scripts/prepare-data.ts` emits two kinds of artifact:

- **`data/`** — bundled and imported directly by the app.
  - `site.json` — repository-wide counters, coverage roll-ups, manufacturers, decades
  - `machines.json` — the browse index, stored as positional rows to stay small
  - `platforms.json`, `curation.json`
  - `detail-slugs.json` — which machines have a detail document
  - `schema.json` — the schema reference, one entry per type (see *Schema reference*)
  - `icons.json` — manufacturer marks, normalised for inlining (see *Manufacturer marks*)
- **`public/data/`** — static assets, never bundled into JS. See *Performance* for why.
  - `machines/<slug>.json` — one resolved definition per described machine, with its note
    rendered to HTML at build time
  - `index.json`, `drivers.json` (~2 900 ROM sets), `platforms.json`, `search.json`

Both directories are generated and git-ignored.

Controller-profile `notes` are escaped and rendered as literal text by default. A group with `notes_format: "markdown"` is parsed as GitHub Flavored Markdown at build time and emitted as `notesHtml`; raw HTML tokens are escaped, unsafe link/image URL schemes are reduced to text, and heading levels are constrained to H4 or deeper beneath the platform group's H3. This opt-in avoids reinterpreting legacy formulas such as `col*10`, while allowing reviewed long notes to use sections, lists, tables, emphasis, and inline code. The Vue app never parses Markdown at runtime.

Catalog stubs — machines PinMAME supports but nobody has described yet — still get a prerendered
page. A deep link from an authoring tool must always land somewhere that explains the state of the
definition rather than 404.

## Machine families

Stern shipped most titles as a Pro and a Premium/LE with genuinely different playfields, so the
catalog holds them as separate physical machines. That is correct, and it also means four AC/DC
entries sit side by side in search with nothing saying they are one game.

**The catalog has no family field**, so `prepare-data.ts` derives one: machines of the same
manufacturer whose PinMAME drivers share a name prefix. That prefix is how PinMAME itself groups a
title's ROM sets — `acd_170` and `acd_150h` are the same game by construction — which makes it
evidence rather than a guess. Across all 786 machines it yields **15 families covering 33 machines,
every one a real edition group** (12 Stern Pro/LE pairs, AC/DC's four editions, Firepower's
conversions, Volcano's sound-only variant) with no false positives.

The family page's real value is the comparison, not the list: AC/DC Premium has 156 lamps to the
Pro's 80, 28 coils to 21, and two drop-target banks the Pro never had. Rows where the editions agree
are hidden by default.

It stays labelled as derived on the page itself. **The moment the catalog authors families, they win
outright** — the derivation only fills gaps for titles no document covers.

### The authored shape

Drop `families/<slug>.json` into the defs repo and the site picks it up with no changes here:

```json
{
  "format": "pinmame-machine-family",
  "schema_version": 1,
  "family": { "id": "stern.ac-dc", "title": "AC/DC", "manufacturer": "Stern" },
  "members": [
    { "machine_id": "stern.ac-dc-pro.2012", "edition": "Pro",
      "differences": "Ordinary matrix lamps, one aggregate GI string, no upper playfield." },
    { "machine_id": "stern.ac-dc-premium-limited-edition-luci.2012", "edition": "Premium / LE / LUCI",
      "differences": "Adds the bell, the upper playfield and its drop-target banks, RGB GI." }
  ],
  "knowledge": { "path": "knowledge/families/ac-dc.md" },
  "sources": []
}
```

Only `family` and `members` are required. `edition` overrides the label the site would otherwise cut
from the machine name; `differences` is per-edition prose rendered on that edition's card and on the
machine page itself; `knowledge.path` is a markdown note rendered as the family overview, using the
same `Coverage: **…**` lead-in convention as machine notes.

A `machine_id` that resolves to nothing is reported as a build warning rather than silently dropped —
that is how a typo or a renamed machine surfaces.

Prose earns its place where the numbers cannot speak: the comparison table can say the Premium has
156 lamps to the Pro's 80, but only prose can say *why* — an upper playfield, a bell, and the LUCI
magnet. Keep it to what a table author must not get wrong.

## Discovery and machine-readable access

The browse page paginates on the client, so link-following alone reaches only the first screenful of
machines. `sitemap.xml` is what actually makes the catalog crawlable — it is generated from the same
index the routes come from, and deliberately **excludes the 683 stub pages**, which carry roughly
nine unique words each and are served `noindex, follow`.

`useSeo()` is the single place that sets a page's title, description, canonical URL and social card,
so the four cannot drift. `NUXT_PUBLIC_SITE_URL` (default `https://games.visualpinball.org`) is the absolute public root including any subpath; canonicals and sitemap entries are generated to match byte for byte.

`public/og.png` is drawn at build time by `scripts/make-og-image.ts` — the same 5×7 WPC font the hero
uses, rasterised into a pixel buffer and encoded as a PNG with nothing but `node:zlib`. Links to this
site get pasted into Discord and VPForums far more than they get found through search, so the card
earns its keep.

### Endpoints for tools and agents

| URL | Contents |
| --- | --- |
| `data/index.json` | Catalog v2: every machine with its kind, status, platform, root drivers, complete ROM-set list and detail URL |
| `data/machines/<slug>.json` | Full resolved definition — drivers joined, related machines, note as HTML |
| `data/drivers.json` | Every PinMAME ROM set mapped to its machine |
| `data/platforms.json` | Controller profiles and address ranges |
| `data/search.json` | Compact search index |
| `llms.txt` | Orientation for agents, including the coverage and provenance caveats |

`data/index.json` identifies its contract with `format: "pinmame-machine-reference-index"` and `version: 2`. Relative to v1, every machine carries the authoritative `machineKind` and complete `roms` list; consumers should reject unknown future versions.

These are the same documents the pages render, so an agent gets data already resolved rather than the
raw catalog. The canonical source remains the repository; this site is a rendering of it. An MCP
server belongs beside the catalog rather than inside this project, and can be backed by either.

## Performance

Two decisions matter more than everything else combined.

**Machine definitions are static assets, not JS modules.** A dynamic import per
machine creates 100+ chunks, and Nuxt's build manifest emits a
`<link rel="prefetch">` for every one of them on every page. Since each chunk embeds a full
definition, one page pulled ~10 MB of JSON nobody had asked for. Serving them from `public/data`
instead fixed it:

| Page | Before | After |
| --- | --- | --- |
| Home | 10.2 MB · 120 requests | **0.56 MB · 17 requests** |
| `/machines` | 10.9 MB · 122 requests | **1.2 MB · 19 requests** |
| Heaviest machine page | 11.3 MB · 124 requests | **1.7 MB · 21 requests** |

`loadMachineDetail()` reads the file from disk on the server, because the prerenderer does not serve
`public/` to `$fetch`. On the client it rarely runs at all — payload extraction means a client-side
navigation gets the data from the target route's `_payload.json`.

**NuxtLink prefetches on interaction, not on visibility** (`experimental.defaults.nuxtLink`), so a
grid of sixty cards costs nothing until a pointer lands on one.

`PlayfieldMap` splits rendering into a base layer and a highlight layer. Nothing in the base layer
depends on what is focused, so hovering patches a handful of nodes instead of every marker — about
7 ms per interaction with 148 clusters on screen, and scrolling holds 60 fps.

When measuring, beware `requestAnimationFrame` floors: a double-rAF "hover to paint" measurement
reports 33 ms on a 60 Hz display no matter how fast the work actually is.

## Contributing

Every page that renders a file offers a one-click route to changing it. `ContributeCard` and
`useRepoLink().edit()` build GitHub `/edit/<branch>/<path>` URLs, which fork the repository for the
visitor and land them on the pull-request form — no local checkout for a wrong switch label.

| Page | Action |
| --- | --- |
| Machine (described) | Edit the definition · Edit the note · Report a problem (prefilled issue) |
| Machine (stub) | Start this definition — edits the generated `machines/stubs/<driver>.json` |
| Platform (with profile) | Edit the profile |
| Platform (no profile) | Author this profile — GitHub's new-file form, prefilled path |
| Coverage | Browse machines needing work |
| Guide, footer | Persistent entry points |

Each card also links `schemas/machine.schema.json` and the plan document, and asks for a source with
any change — the catalog cannot validate a claim without provenance.

## Design notes

The palette is one dark surface set plus a fixed hue per device kind, so a colour means the same
thing on every page: cyan is a switch, amber-red a coil, yellow a lamp, magenta a magnet. Coverage
status has its own three colours and is never mixed with device colours.

Every external reference points at a file, not a project. A machine page links its own definition
JSON and note by path; a source record's `locator` is parsed for file paths, line ranges and PDF page
numbers, so a PinMAME citation becomes a permalink to `src/wpc/sam.c#L240-L268` at the pinned
revision, and a manual citation becomes `…#page=119`. See `app/utils/links.ts`.

Three components carry most of the weight:

- **`DotMatrix`** renders text through a hand-authored 5×7 bitmap font in the Bally/Williams WPC
  style (`app/utils/dmdfont.ts`), picking the largest integer scale each line fits at. Rasterising a
  vector typeface and thresholding it gives mushy glyphs; a real DMD font is drawn pixel by pixel.

- **`AddressMatrix`** lays the switch or lamp addresses out as the physical matrix. WPC-family
  platforms are detected by their column·row numbering (11–88, never a digit 9 or 0), everything
  else is chunked sequentially into columns of eight. Holes in the grid are real: an address marked
  *unused* was checked and found empty.
- **`DeviceTable`** renders wire codes as actual two-tone colour chips, hides columns that carry no
  information for the current group, and keeps every address searchable in-page.
