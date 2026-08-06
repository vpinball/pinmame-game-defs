# Current state

This file is the mutable, game-specific companion to `docs/INSTRUCTIONS.md`. The runbook holds
generic policy that changes rarely; everything that goes stale as curation proceeds lives here:
the pinned upstream revisions, the reviewed scope exceptions, the generated counts, per-game
promotion notes, and who is working on what.

Keep it synchronized after every material change. Generated reports remain the numerical source of
truth; if regeneration disagrees with a count below, investigate the diff and update this file
rather than preserving a stale literal.

## Pinned baseline

These pins and generated counts are the reproducible handoff baseline. Verify operational inputs against the configured checkouts and generated artifacts before continuing. The `pinmame-dotnet` and legacy managed-integration revisions below are historical provenance for already-migrated compatibility fixtures and do not require local checkouts during routine game curation. Fetch either exact revision only when changing or revalidating that migration. If an operational pinned input changes, stop, produce a reviewed catalog/source diff, update every affected hash and count, update this ledger, and include the scope change in the mandatory high-tier model review and maintainer PR review; never let an upstream checkout drift silently.

| Input | Required revision | Baseline role |
| --- | --- | --- |
| `vpinball/pinmame` | `4ec52ff0ac133ac251681518aed2249e19fe26eb` | Authoritative LibPinMAME build and catalog: 2,873 reported drivers, seven reviewed virtual-only exclusions, 2,866 in-scope drivers, 772 clone-tree roots, 785 physical-game records, and one separately classified non-game diagnostic |
| `vpinball/pinmame-dotnet` | `e3e31eea6cd8eb046b4a8ea3110a31bb19c32b45` | Managed LibPinMAME interop reference; it does not own the legacy semantic game definitions |
| Legacy managed integration | `cf2030710f9a6ee19fdbeec9cc9fccaba2032a6f` | Migration evidence for the 11 hand-maintained game classes, shared platform data, aliases, direct wires, and the hint consumer being sunset |
| `sverrewl/vpxtable_scripts` | `0c036bb61b4b4e8c778c37559f6795df8cd1521e` | First pinned known-working VPX script corpus |
| `jsm174/vpx-standalone-scripts` | `15d112648a1b94b9f59eb8b3c335d57283653c50` | Second pinned known-working VPX script corpus |

The reviewed physical-only exclusion set is exactly `acd_170_ac`, `beachbms`, `beav_butt`, `bubba`, `che_cho`, `rambo`, and `tomjerry`. Do not regenerate stubs for them. Ordinary firmware modifications and physical conversions remain in scope when they run on documented hardware; examples include `clash` for a physical Rock Encore conversion and `mac_zois` for the physical machinaZOIS installation. Any addition to or removal from the exclusion set is a scope change requiring evidence, tests, a catalog diff, high-tier model review, and maintainer PR review.

At the 2026-08-05 handoff, `catalog/pinmame.json` contains 2,866 drivers mapped to 785 physical-game records plus one non-game diagnostic. `reports/coverage.json` reports 23 `author_ready` games, 79 `partial` games, 683 `stub` games, one separate partial diagnostic, 15 definitions missing spatial placement, and `completion_gate: false`; author-ready physical coverage is 23/785 (2.9299%). Generated reports are the numerical source of truth. If regeneration changes these values, investigate the diff and update this paragraph rather than preserving stale literals. Never report implementation-progress percentage as author-ready coverage.

Williams Medieval Madness (`williams.medieval-madness.1997`) was promoted on 2026-08-05 and is the first author-ready Williams WPC machine. It introduced the `pinmame.wpc-95` controller profile, which every later WPC-95 game should reuse instead of `pinmame.wpc-alpha`.

Bally Attack From Mars (`bally.attack-from-mars.1995`) was promoted on 2026-08-05 as the second WPC-95 machine, incorporating and superseding external PR #2. It is the first definition to enumerate PinMAME's two auxiliary lamp columns: `afmGameData` declares `lampCol = 2`, and the sixteen saucer-L.E.D. addresses 91-98 and 101-108 are shifted in serially by public solenoids 37 and 38. Reuse that pattern for any other game whose `core_tGameData` declares extra lamp columns, and note that WPC-95 auxiliary outputs 37-40 are mirrored at 41-44 while `custSol` duplicates appear from 51 upward. Its curation also recorded a genuine pinned-PinMAME defect worth remembering: `afm.c` names the two loop gates the opposite way round from the manual and from both retained known-working scripts, and is internally inconsistent because its `/* 33 */` and `/* 34 */` comments contradict its own `WPC_FLIPPERCOIL95` bit reads. Verify emulator-side left/right naming against the printed table before trusting it.

Bally Centaur (`bally.centaur.1981`) was promoted to `author_ready` on 2026-08-06 and is the project's first Bally MPU AS-2518-35 machine. It introduced `controllers/pinmame/by35.json`, which every later BY35-driver machine should reuse.

Its profile rules: public momentary solenoid = PIA1:B selector + 1, so 1-15 with no address 16 because selector 15 is the idle state; four continuous outputs at 17-20; a six-column switch matrix published as sequential positions 1-48, not column-times-ten notation, with the three diagnostic contacts at -7 to -5; and a lamp strobe that ignores decoder selector value 0x0f, so 16, 32, 48, 64, 80, 96, 112 and 128 are unreachable decoder slots rather than unused lamps. The public lamp address collapses to `16 * d + lampadr + 1` on the main board, plus 64 on the auxiliary board.

Five lessons from this machine generalise to every other BY35 game.

1. **A printed "Self Test #" column is a test order, not a public address.** The two are unrelated, and the ROM's own solenoid test publishes the mapping because it flashes each coil's number as it fires it - so run it rather than guessing. On Centaur that exposed printed 14 and 15 transposed against public 14 and 15, and public 7 being the outhole kicker rather than the ball release both retained scripts call it.
2. **On a six-column game one continuous solenoid address carries the sixth switch-column strobe, not a coil.** On Centaur that is public 17. It reads as permanently asserted because by35.c OR-accumulates solenoid state within each VBLANK window, so never read a held continuous output as an unused one.
3. **PinMAME reports lamp-matrix bits, not bulbs.** An unconnected matrix position still lights during a self-test lamp sequence. Distinguish them by what the ROM drives in normal play - the evidence schema now has `lamp_addresses_driven_outside_self_test` for exactly this.
4. **Check a community table for placeholder rows before trusting its geometry.** Centaur's retained table parks every auxiliary lamp its author could not place in a line along the bottom-left corner, and an earlier pass wrongly promoted those coordinates to validated placements.
5. **Board schematics are generic and may live in another game's manual.** The AS-2518-43 auxiliary lamp driver sheet appears in no Centaur manual; it was found in the Kings of Steel schematics. Vendors list the board as fitted to Black Pyramid, Future Spa, Spy Hunter, Centaur, Kings of Steel, X's and O's, Centaur II and Kiss. Centaur is the only one PinMAME models with `lampCol > 0`, which makes the board look Centaur-specific from the emulator side and it is not.

Two labels in the record are reasoned rather than printed and are documented as such in the knowledge note: public lamp 113, the twelfth auxiliary circuit, is labelled for its decoder group because no document names it; and option switches 17-20 come from the community option-switch documentation that all four retained tables carry, which agrees with the printed manual on every switch the manual does document.

The physical family is `centaur` (Bally, 1981) with `centaura` and `centaurb`, the 2004 and 2008 Bally/Oliver free-play ROMs, which are later firmware for the same physical machine rather than new games. Do not group `centauri`/`centaurj`, which are Inder's unrelated 1979 Spanish game and correctly remain a separate stub.

At the 2026-08-05 handoff, X-Men Pro, Transformers Pro, and TRON Pro are already claimed as maintainer-local pending work. External contributors must not duplicate them unless a maintainer explicitly reassigns one. Before selecting any game, check this ledger plus open PRs/issues for newer ownership information. Otherwise, prioritize existing partial games by physical release date newest first, with Pro-only searches deferred until higher-tier/non-Pro work is exhausted unless a maintainer gives a new priority.

Canonical machine data must remain free of consumer authoring hints. Sunset of the legacy hint patcher belongs to its owning consumer project and is outside this curation runbook; curators must never revive it by adding hints to definitions.
