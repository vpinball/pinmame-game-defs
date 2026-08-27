# Stern Big Buck Hunter Pro (2010) — recreation knowledge

Status: observed. This note records what a table author needs to recreate the machine and
where the evidence stops. The one-paragraph version: a Stern S.A.M. machine whose retained
factory documentation is a 41-page mechanical partial with **no electrical tables** — no
switch matrix, no lamp matrix, no coil table, no schematics — a gap PinMAME's own driver
source acknowledges (`sam.c`'s bbh block: "Did not find a complete manual anywhere (even
Stern's downloads do not have the schematics/solenoids) so this is from the VPX table,
completed with the backglass flasher map"). Everything below is therefore anchored to one
of exactly three authorities: the retained known-working table's script (runtime), the
partial manual's assembly drawings (construction), and pinned PinMAME source (topology).

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
The definition makes no assertion that depends on which 1.7 dump a runtime carries.

## The evidence hierarchy on this machine

1. **Runtime semantics** — the retained 37.6 kB script (32assassin's VPX rebuild of an
   85vette VP9 table, June 2017). It binds: trough solenoid 1 (pulsing the exit opto 22),
   auto-launch 2, Buck drive 3/4/5 (bodies commented away), post 7 and 23, kickback 12
   (body commented away), Elk diverter 14 off switch 85, flippers 15/16, flasher channels
   19-22 and 25-27/29/31/32 as `Setlamp 119…132` pseudo-lamps, plus maintained rollover
   handlers and the trough ball stack (21, 20, 19, 18).
2. **Construction** — the partial manual's assembly pages. The decisive one is PDF page 3:
   the trough cut-away labels its own switches SW. 18/SW. 19 (roller microswitches,
   180-5119-02) and SW. 21/SW. 22 (dual opto boards, 515-0173-00/515-0174-00), which is the
   only place in the retained evidence where printed labels meet public addresses.
3. **Topology** — pinned `sam.c`: `INITGAME(bbh, GEN_SAM, sam_dmd128x32, SAM_2COL,
   SAM_NO_AUX)`, sequential switch numbering, 80 lamps, 66 enumerated solenoids, one GI
   channel, the dedicated-switch comment map, and the EOS mirror that copies each flipper
   button bit to its EOS bit.

## Mechanisms a recreation needs

- **Four-ball trough** — the clean case, fully cross-derived (manual labels + script
  ball stack). Three roller microswitches and a dual-opto pair at the kicker end; coil
  26-1200 NO DIODE on solenoid 1; the served ball crosses opto 22 on the way out.
- **Buck target** — the headline mechanism and the least-documented. A deer target
  traverses a track across the upper playfield, driven by a motor plus two direction
  circuits (script names: 3 = "right or backwards", 4 = "left or forwards", 5 = motor).
  Position feedback: drive-track optos the script's *commented-out* code names as
  "opto switch 37" and "opto switch 45". Hit detection: switch 1, physically wherever the
  target currently is. **The retained table drives none of this**: it animates the Buck
  itself by following the flashing Buck path lamps (16-20, super jackpot 57), detects hits
  through a 31-segment wall ladder under the animated target, and writes its endpoints to
  the unfitted UK post-save addresses 71/72. That substitution is a property of the
  recreation, not the machine. A faithful recreation that wants the ROM's own Buck logic
  must drive 37/45 and the drive coils the way the ROM expects — which needs a harness
  trace, because no electrical table exists to confirm the sensor count or addresses.
- **Elk diverter** — a mini-flipper gate feeding the Elk ramp, driven on solenoid 14 by
  the cabinet control wired to public switch 85 (the hardware D-13 upper-left-flipper
  position). The gate swaps between two ball-guide walls (`sw85`/`sw85a`). Which physical
  cabinet control feeds D-13 on a machine that fits no upper flipper is the second
  unresolved conflict — the cabinet parts tables list only the two red flipper buttons,
  start, and tournament.
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

## Lamp and flasher shape

The script's `UpdateLamps` binds 57 of the 80 lamp addresses. Distinctive facts: lamps
16-20 are the Buck path inserts (the table's substitute Buck driver consumes them as
inputs); lamp 57 is the Buck Super Jackpot; lamps 27-30 render as four colored bulb
primitives stacked at one position (no honest per-address placement exists); lamps 65-70
are the auxiliary lamp columns (SAM `lampCol = 2`, rows 9-10 of the transport) the script
binds to named playfield lights. The ten solenoid-driven flasher strings use script-internal
`Setlamp 119…132` channels above the real 80-address transport — those numbers are table
render channels, not controller addresses.

## What blocks promotion

See `coverage.missing` and the two conflicts in the definition. The concrete path forward:

1. Harness-trace a legal `bbh_160` ROM (exact pinned bytes): boot diagnostics, switch-status
   page, solenoid/lamp tests — this is the only route to semantic names for the ~40
   unbound addresses and to settle the opto-polarity conflict.
2. Resolve the Elk button question with cabinet wiring evidence from a real machine.
3. A complete factory manual, if one ever surfaces, supersedes the inference above.
