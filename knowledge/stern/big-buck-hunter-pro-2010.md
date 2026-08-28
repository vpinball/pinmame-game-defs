# Stern Big Buck Hunter Pro (2010) — recreation knowledge

Status: observed. This note records what a table author needs to recreate the machine and
where the evidence stops. The one-paragraph version: a Stern S.A.M. machine whose retained
factory documentation is a 41-page mechanical partial with **no electrical tables** — no
switch matrix, no lamp matrix, no coil table, no schematics — a gap PinMAME's own driver
source acknowledges (`sam.c`'s bbh block: "Did not find a complete manual anywhere (even
Stern's downloads do not have the schematics/solenoids) so this is from the VPX table,
completed with the backglass flasher map"). Everything below is therefore anchored to one
of exactly four authorities: the two retained known-working tables' scripts (runtime), the
partial manual's assembly drawings (construction), pinned PinMAME source (topology), and a
hash-pinned attract-mode harness run (availability observation).

## Identity and family

Stern Big Buck Hunter Pro, manufactured January 2010 (IPDB 5513; project date 2009),
S.A.M. hardware, designed by John Borg, sound by Ken Hale, software by Lonnie D. Ropp and
Lyman F. Sheats Jr. The PinMAME family is four firmware revisions — `bbh_140` (1.4,
02/10), `bbh_150` (1.5, 02/10), `bbh_160` (1.6, 05/10) and the clone-tree parent `bbh_170`
(1.7, 11/10) — all sharing the one static `bbhGameData`, all physically identical. There is
one physical edition; no Premium/LE split exists in the pinned catalog, and no other Big
Buck Hunter title appears in PinMAME at this revision (the later Open Season machine is not
in the catalog). `bbh_170` alone carries a FastFlips watch address, so PinMAME's synthetic
game-on output (public solenoid 33) is only expected to toggle on 1.7.

ROM evidence note: the contributor's library matches the pinned SHA-1s exactly for 1.4,
1.5 and 1.6; the 1.7 zip carries a differently-built dump (29,069,268 bytes,
SHA-1 `5c292f80…`) that matches neither the pinned byte range nor any simple offset of it.
The definition makes no assertion that depends on which 1.7 dump a runtime carries. Two
runtime facts for future harness work: this libpinmame build loads ROMs from **zip
archives** (loose `.bin` staging never reaches a running state), and `bbh_160` boots
cleanly from the exact-bytes staging copy under `roms/stern/big-buck-hunter-pro/zips/`.

## The evidence hierarchy on this machine

1. **Runtime semantics** — the two retained table scripts. The retained v1.11 table
   (37.6 kB, 32assassin's VPX rebuild of an 85vette VP9) binds: trough solenoid 1 (pulsing
   the exit opto 22), auto-launch 2, Buck drive 3/4/5 (bodies commented away), posts 7 and
   23, kickback 12 (body commented away), Elk diverter 14 off switch 85, flippers 15/16,
   flasher channels 19-22 and 25-27/29/31/32 as `Setlamp 119…132` pseudo-lamps, maintained
   rollover handlers, and the trough ball stack (21, 20, 19, 18). The retained v1.10
   "Modern Upgrade" (144 kB, TastyWasps, December 2023) binds the **same set** — every
   `SolCallback` line matches — which independently corroborates those runtime bindings,
   and adds three writes the v1.11 table never makes (see the 73-80 block below).
2. **Construction** — the partial manual's assembly pages. The decisive one is PDF page 3:
   the trough cut-away labels its own switches SW. 18/SW. 19 (roller microswitches,
   180-5119-02) and SW. 21/SW. 22 (dual opto boards, 515-0173-00/515-0174-00), which is the
   only place in the retained evidence where printed labels meet public addresses.
3. **Topology** — pinned `sam.c`: `INITGAME(bbh, GEN_SAM, sam_dmd128x32, SAM_2COL,
   SAM_NO_AUX)`, sequential switch numbering, 80 lamps, 66 enumerated solenoids, one GI
   channel, the dedicated-switch comment map, and the EOS mirror that copies each flipper
   button bit to its EOS bit.
4. **Runtime observation** — the hash-pinned attract-mode harness run of `bbh_160`
   (source `runtime-scenario.bbh-attract-observe`): the ROM's attract lamp chase drives
   **78 of 80 lamp addresses** (everything except 1 and 2), the single GI channel is
   active, no solenoid fires, and the watched switch candidates idle low. A driven matrix
   bit proves the ROM uses the address, never that a bulb is fitted.

## Mechanisms a recreation needs

- **Four-ball trough** — the clean case, fully cross-derived (manual labels + script
  ball stack). Three roller microswitches and a dual-opto pair at the kicker end; coil
  26-1200 NO DIODE on solenoid 1; the served ball crosses opto 22 on the way out.
- **Buck target** — the headline mechanism and the least-documented. A deer target
  traverses a track across the upper playfield, driven by a motor plus two direction
  circuits (script names: 3 = "right or backwards", 4 = "left or forwards", 5 = motor).
  Position feedback: drive-track optos the commented-out code names as "opto switch 37"
  and "opto switch 45". Hit detection: switch 1, physically wherever the target currently
  is. **Both retained tables drive none of this**: they animate the Buck by following the
  flashing Buck path lamps (16-20, super jackpot 57), detect hits through a 31-segment
  wall ladder, and write endpoints to the unfitted UK post-save addresses 71/72 (v1.11)
  while v1.10 additionally comments out the magna-save 37/6 advances. A recreation that
  wants the ROM's own Buck logic must drive 37/45 and the drive coils the way the ROM
  expects — which needs a harness trace of the ROM's own feedback path. The service-menu
  diagnostics include a dedicated **BUCK** test item (see below), which is the natural
  harness entry point for the drive coils.
- **Elk diverter** — a mini-flipper gate feeding the Elk ramp, driven on solenoid 14 by
  the cabinet control wired to public switch 85 (the hardware D-13 upper-left-flipper
  position). The gate swaps between two ball-guide walls (`sw85`/`sw85a`); the v1.10
  table pulses 85 from both walls' hit handlers, corroborating the binding. Which
  physical cabinet control feeds D-13 on a machine that fits no upper flipper is the
  second unresolved conflict — the cabinet parts tables list only the two red flipper
  buttons, start, and tournament.
- **Kickback ram** — coil 23-800 NO DIODE (solenoid 12) behind the ball-sense switch 34;
  the ram toy is a separate assembly (860-5110-04-ASY) riding above the kicker.
- **Up/down posts** — solenoids 7 and 23 raise/lower the two orbit posts; assembly family
  500-7153-04 (coil 26-1200 NO DIODE drawn Q12). No position sensor anywhere.
- **Spinner/spinning disk** — switch 44 pulses per rotation; the manual's assembly is a
  *motorized* spinning disk with an opto disk and opto board (511-5224-00 family), and the
  ball-guide assemblies carry additional opto transceivers (500-6775-01) whose switch
  addresses no retained source states. Treat the switch-44-to-assembly mapping as
  unproven.
- **Cabinet** — start button (3S, public 16) and tournament button (4T, public 15), both
  switch+lamp assemblies (500-6388-44-TL / 500-6587-06-TL); two red flipper buttons on
  single-stack switches (500-6889-01; the double-stack 500-6890-01 is qty 0, so **no EOS
  contacts are fitted anywhere** — all EOS states are PinMAME's synthesized mirrors); a
  two-chute coin door whose two chutes map to two of D-1..D-4 by an unknown choice.

## The 73-80 extended switch block (new question raised by the v1.10 table)

The shared S.A.M. profile's declared input ranges are -7..72 plus 81-88. But `sam.c`'s
matrix read returns `MAKE16BIT(swMatrix[2+sw_stb*2], swMatrix[1+sw_stb*2])`, so strobe bit
4 reads swMatrix[9] (the coin block, 65-72) **and swMatrix[10] (public 73-80)** as one
16-bit word — the block is reachable hardware the profile never had to name because no
prior retained source used it. The v1.10 table maintains `Controller.Switch(73)` from the
**left flipper key** and `Controller.Switch(75)` from the **right flipper key**, and pulses
switch 79 from its front key — while core.vbs simultaneously drives the real flipper
column (81/83). Whether this machine's ROM reads its flipper buttons from the flipper
column, from the 73-80 block, or from both is an open question; the definition enumerates
all eight block addresses as availability unknown. The switch test (below) settles it.

## Service-menu navigation (mapped by harness exploration)

Back (coin-door green, harness key `service_green`) → "SERVICE MENU / PRESS 'SELECT' TO
CONTINUE" splash → Select (`service_select`) → icon menu **DIAG | AUD | ADJ | UTIL | TOUR |
QUIT** → Select on DIAG → diagnostics submenu **SW | COIL | FLASH | LAMP | BUCK | MORE**
(captions "GO TO SWITCH MENU" etc.; Plus/Minus move the highlight). Entering a test from
the submenu resisted short, medium, double-tap, and 2.5 s Select presses in the explored
runs — the exact entry key (or hold) is still unmapped, and is the only remaining step
before a coil-test run can name the unknown solenoids and a switch-test run can settle the
73/75-vs-81/83 flipper question and the opto addresses. Committed scenarios:
`tools/harness-scenarios/stern/bbh-attract-observe.json` (the completed availability run)
and `bbh-switch-test.json` (the ready-to-run switch sweep, pending the entry key).

## Lamp and flasher shape

The script's `UpdateLamps` binds 57 of the 80 lamp addresses, and the attract-mode harness
run observed the ROM driving all but lamps 1-2 — so twenty lamp addresses the tables never
render are nonetheless live ROM outputs. Distinctive facts: lamps 16-20 are the Buck path
inserts (the tables' substitute Buck driver consumes them as inputs); lamp 57 is the Buck
Super Jackpot; lamps 27-30 render as four colored bulb primitives stacked at one position
(no honest per-address placement exists); lamps 65-70 are the auxiliary lamp columns (SAM
`lampCol = 2`, rows 9-10 of the transport) the script binds to named playfield lights.
The ten solenoid-driven flasher strings use script-internal `Setlamp 119…132` channels
above the real 80-address transport — those numbers are table render channels, not
controller addresses.

## What blocks promotion

See `coverage.missing` and the two conflicts in the definition. The concrete path forward:

1. Finish the service-menu entry (the one unmapped key) and run the **coil test** — names
   the eleven unknown solenoid addresses by observation — and the **switch test** while
   holding 73/75/79/81/83/85/37/45 — settles the flipper-block question, the Elk button's
   readable address, and the Buck optos in one run. The committed `bbh-switch-test.json`
   scenario is ready once entry works.
2. Resolve the Elk button question with cabinet wiring evidence from a real machine.
3. A complete factory manual, if one ever surfaces, supersedes the inference above.
