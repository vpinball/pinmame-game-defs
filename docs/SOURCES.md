# Sources and excerpts

On-demand companion to `docs/INSTRUCTIONS.md`. Read it before step 3 of the per-game workflow, before weighing disagreeing sources, and before writing a conflict or an excerpt; it is not loaded by default.
The runbook wins where the two disagree.

**Belongs here:** where to search for tables and manuals, how retained evidence is organized, how to read and weigh manuals, scripts and PinMAME source, and how to make excerpt crops.

**Does not belong here:** the evidence-authority order and the conflict rules themselves (`docs/INSTRUCTIONS.md`), or platform address arithmetic (`docs/PLATFORMS.md`).

## Rules

### Search order and retention

Search for VPX tables in this order:

1. Each folder in `PINMAME_EXISTING_VPX_TABLES`, in the supplied order
2. `vpuniverse.com`
3. `vpforums.org`

Do not spend time searching for a Pro recreation while a Premium or LE version exists; community authors usually recreate the higher tier because there is no extra virtual cost. Finish higher-tier and non-Pro work first. Never derive Pro geometry from a Premium/LE table without an explicit edition overlay and supporting evidence.

Organize retained table artifacts under `<working-root>/vpx-sources/<manufacturer>/<machine-slug>/`. Keep the downloaded `.vpx`, script sidecars, extracted `vpxtool` output, reports, and provenance metadata. Move downloads out of the user's Downloads folder promptly. After a downloaded archive has been safely extracted and its contents verified in the organized source directory, the archive itself may be deleted; do not delete the retained VPX or extraction.

Organize manuals under `<working-root>/manuals/by-machine/<machine-id>/` and keep `<working-root>/manuals/manifest.json` reconciled. Retain original PDFs, hashes, attribution, source page/download URLs, extracted text/tables, and useful rendered reference pages. Manuals are a reusable research archive and must not be discarded after a game is completed.

Use `PINMAME_ROM_LIBRARY_ROOT` as the user's authorized existing read-only ROM corpus. New ROM downloads belong only in `<working-root>/roms/`, never in Downloads or this Git repository. Pass that derived folder explicitly to the harness or analysis tool that needs it. Commit hashes, archive/member metadata, and analysis results only; never commit ROM bytes or modify, redistribute, or delete the user's existing ROMs.

### Excerpt crops

Use a rendered crop only when the fact is a **drawing** - schematic wiring, a connector fan-out, an insert map. A printed table belongs in the transcription, where it is a kilobyte, diffable and greppable; as an image it is forty times the size and cannot be searched. Generate crops with `tools/make_excerpt.py`, which records the page, crop box, dpi and tool so the image can be re-derived, accepts `--rotate 90`, `180`, or `270` for sideways scans, and refuses crops over its `--max-bytes` (100 kB by default); `tests/test_excerpts.py` allows up to 1.5 MB only for page-scale drawings listed in `PAGE_SCALE_DRAWINGS`. Do not threshold to 1-bit: printed shading is itself evidence on some machines, the shaded opto rows of a switch matrix being the obvious case. Grayscale is the default; a colour page whose colours carry meaning is a deliberate exception, and the excerpt should say why.

**Never render at a fixed dpi.** `tools/render_excerpt_image.py` derives the resolution instead, and should be preferred for any new crop. A scanned page is a single embedded raster at whatever the scanner produced - 150, 200, 400, 600, rarely a round number and essentially never 300 - so the tool reads that image's own pixel width against its placed width in points and renders at exactly that. Rendering higher invents pixels and inflates the repository; rendering lower discards the fine print in a connector table, which is usually the reason the crop exists. A born-digital page has no native resolution at all, so there the tool picks a dpi from the smallest type inside the crop and targets a readable glyph height. Record the tool's printed `image_derivation` verbatim: it names the page, the crop box, which case applied and why, and any width cap that reduced the result below native. Crop tightly to the table, block or drawing being cited - a tight crop is the evidence for one claim, where a whole page is a chunk of a copyrighted service manual.

## Lessons

Each lesson ends with the lines of `docs/archive/current-state-ledger-until-2026-10-01.md` that
record the case behind it, and with `verified:` where it was checked against the repository code or
pinned PinMAME source on 2026-10-01. A lesson added later names the commit or knowledge note that
produced it instead.

### Finding and reading sources

- **Fetch IPDB through Wayback first.** IPDB answers plain HTTP and headless Chrome with 403. `https://web.archive.org/web/2024id_/<IPDB URL>` serves the archived bytes unmodified; cite the resolved capture URL and hash the file. Live, a headful Puppeteer session with a persistent `userDataDir` clears the challenge (also VPU, VPF). (archive L446, L677; verified: tools/curate_johnny_mnemonic.py cites full-timestamp `id_` URLs)
- **Cite the untouched download.** When a PDF needs decrypting or an OCR layer, the original stays the cited copy; the processed copy sits beside it for search only. (archive L272, L306, L425)
- **OCR finds pages; renders decide cells.** Acrobat exposes no scriptable OCR; `Windows.Media.Ocr` over native-resolution renders gives a usable search layer. An existing text layer can still be wrong: one shifted a parts list by a row, others scramble multi-column tables. Read every cited cell from the render. (archive L431, L447, L728)
- **Confirm the document is the machine.** A same-titled Internet Archive item can be the arcade video game. Render a page and check manufacturer and board part numbers before citing it. (archive L633)
- **Prove a page is missing before saying so.** Check that consecutive renders' printed folios increment by one; a scan can silently lack every even page. Derive the PDF-to-printed offset per section: rebound scans change it, bind sheets in reverse and duplicate pages. (archive L666, L900)
- **Read addenda, amendments and bulletins first.** They correct printed figures, part numbers and device identity (a printed relay amended to a coil). Give the correction its own source record, apply it, and keep the printed original in the device note. (archive L662, L900, L940)
- **Use a secondary chart only where it reproduces the primary.** It may fill a gap the retained manual leaves only when its overlapping columns match the primary schematic exactly and runtime evidence groups the circuits the same way. Disclose it on every affected device. (archive L677)

- **A relabelled schematic is this game's only when its list is.** The IPDB Lamp Driver Schematic for Quicksilver was drafted for a sister game and relabelled by hand (the old title is struck through), and it carries a fuller lamp list than the manual's typed one plus a hand-corrected pin. Compare the two lists row by row, take pin corrections from the hand marks, and read the decoder and connector blocks yourself rather than reusing a sibling record's SCR table. (knowledge note `knowledge/stern/quicksilver-1980.md`)
### Weighing sources and writing conflicts

- **Check every table against its siblings.** Expect typos, transposed rows and reversed Left/Right inside one manual; settle a misspelling from its symmetric partner. Prefer the parts list, assembly page or schematic over matrix-page labels: a matrix "(EOS)" can name a part the assembly page identifies as something else. (archive L638, L693, L897)
- **Copies of one table are one source.** Front-matter, section and schematic-side reprints neither corroborate each other nor stay aligned; they can drift by a row or split two against two. Decide with a different kind of page, or with the script. (archive L554, L622, L835, L122)
- **A blank or "Not Used" row is rebuttable.** It is evidence of non-fitment that a label on another page or an unreferenced driver `#define` does not overcome; a wiring page, a drawn location balloon or a live script binding does. (archive L693, L763, L767)
- **Settled disagreements are notes.** Two higher-authority sources that are independent of each other against one printed row settle it: follow them in structured data, keep the literal cell in the excerpt, and state the misprint on the device. A connector list that merely lacks an entry proves nothing. (archive L622, L692, L835, L1001, L122)
- **A resolution path must name evidence that exists.** Check every ROM short name against the record's own `drivers`; if no manual is retained, say so rather than cite a page. Also say what would not settle it, e.g. no harness trace shows which bulb a lamp-matrix bit reaches or which string plugs which connector. (archive L1066)
- **PinMAME source is emulator evidence, not fitment.** Per-game `core_set_pwm_output_type` typing is a brightness model; it can contradict printed bulbs and addresses and may be copied from a VPX table. A `*** PRELIMINARY ***` banner or an author's "no access to this game" header weakens that driver's mechanism tables and flipper fields. `hw.custSol` can be synthetic. (archive L406, L751, L752, L780, L846, L847, L879, L974; verified: capcom.c:751, cv.c `cv_getSol`, ft.c:181-185)
- **Trace a symbol's uses before judging it.** `#define` names and comments can be swapped or stale. Before calling a symbol unused, follow every use, including struct initializers handed to `mech_add`. A swapped name that the code uses consistently with the machine is a naming defect: a device note, not a conflict. (archive L662, L667; verified: tz.c:210-211, 601-624, mech.c:143)
- **Semantics are what the script's code does.** Sub and routine names can say the opposite of the objects they move; the object manipulation decides. (archive L406, L835)
- **A binding outside the platform's published range is dead code.** Check the address against what `core_getSol` and the driver can publish first: a BY35 table's `SolCallback(25..38)` never fires. (archive L917; verified: core.c `core_getSol`, by35.c:322,328)
- **Record a substitution, not hardware.** A table may write an unfitted address as a stand-in for real mechanism feedback; record the address as substituted and keep the real sensors as candidates. (archive L491)
- **Verification, not size, decides a table's authority.** An author's "not verified" header, a table nobody has launched, and a re-theme whose `cGameName` matches the ROM rather than the machine are leads. A thin or pre-1.0 build that is known to work keeps its runtime authority, but read what it omits as a gap, never as evidence: an empty light collection is not a missing lamp. (archive L167, L406, L734, L1136)
- **Retain the VPinMAME library the table loads.** Keep a machine-neutral copy of `core.vbs` and the platform library (`s11.vbs`, `de.vbs`, `de2.vbs`, `wpc.vbs`, `sega2.vbs`) and cite it by excerpt. The library, not the table, decides which addresses key handlers write; libraries differ, and a table constant can suppress a write. (archive L462, L466, L474, L306; verified: tools/pinmame_flipper_column.py)
- **Identify the lamp idiom before counting lamps.** Tables use `Lampz.MassAssign`, `vpmMapLights`, `SetLamp`, custom `ChangedLamps`/`NFadeL` loops or the shared `Lights()` array; a resolver for one returns a false-clean zero on another. Strip whole-line and trailing comments, count the controller's addresses, then explain every extra object. (archive L167, L236, L944, L964, L975, L999, L1011; verified: vpx_source.py `LAMP_PATTERNS` lacks `vpmMapLights`)

### Excerpts

- **The size budget is a test.** `tests/test_excerpts.py` enforces it, and `make_excerpt.py --max-bytes` grants no exception. Only a page-scale drawing belongs in `PAGE_SCALE_DRAWINGS`; never list a table, crop it tighter. A listed ID that cites nothing, or now fits in 100 kB, fails too. (archive L1092; verified)
- **Fit, re-render, split.** `tools/fit_excerpt_images.py` shrinks over-budget table crops until they fit. `tools/rerender_excerpt_images.py` regenerates every crop from its recorded `image_derivation`. Split a dithered 1-bit matrix into quadrant crops. (archive L336, L1090; verified)
- **One image per excerpt.** When a transcription spans several pages, crop the one load-bearing page and name the others. Omit the image when no single page stands for the claim. (archive L1094; verified: schema)
- **A mixed-raster scan's resolution is its mask's.** Some IPDB scans store a low-resolution background image and draw the text and line art through a finer stencil `/Mask` (NBA Fastbreak: a 100 dpi background under a 300 dpi JBIG2 mask). `tools/render_excerpt_image.py` now takes the finer of an image and its `/Mask` or `/SMask`, and breaks a coverage tie toward the finer image, so such a crop renders at the line art's resolution; the derivation names the mask. (knowledge note `knowledge/bally/nba-fastbreak-1997.md`)
- **Disclose normalization.** If the transcription normalizes separators, punctuation or footnote marks, say so in the excerpt. (archive L1214)
