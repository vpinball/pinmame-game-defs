# Indianapolis 500 (Bally, 1995) spatial review

Status: observed. Every switch, coil, flasher, motor and lamp is placed from the retained table or carries a controlled `not_applicable` record. The playfield general-illumination strings are placed but only `observed`, switches 54 and 75 are `observed`, and the race track's G.I. reflector bulbs are not placed, which keeps the record at `machines/partial/bally/indianapolis-500-1995.json`.

The geometry source is the retained known-working `Indianapolis_500_VPX_1.1_RTM.vpx` (SHA-256 `a009c201fa4956ee086243486465e08917540c9a5044f5f14b88e24e704e2aeb`); its embedded script (SHA-256 `bbb957330598291fbd8be3d89e6de2c6f4c541f417f66d443809ff2fe8302f72`) is the runtime binding authority. Exact playfield bounds are `left=0 top=0 right=952 bottom=2162`; every coordinate is x/952 and y/2162 rounded to six places.

## Evidence decisions

- The embedded script is the runtime authority; the July 1995 Operators Handbook and the 152-page operations manual are the physical inventory, construction and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- Manual reconciliation (`external:pinmame-review-artifacts/indianapolis-500/manual-reconciliation.md`): All 28 callouts on the handbook's solenoid/flasher location drawing (printed 7) were measured through a least-squares refit; every one reaches its table object within 0.07 normalized (largest 18 at 0.064 and the lower 27 socket at 0.065) except 01, the documented auto-plunger projection. Every placed switch was overlaid on the handbook's switch-location drawing (printed 5) through a seven-point fit and ends on or within about a marker width of its marker; the four closest calls (25, 35, 54, 75) were re-measured through a ten-point least-squares refit, which keeps 54 (0.075) and 75 (0.064-0.078) observed. The other switches were not re-measured through the refit. The documented projections (trough optos 41-45, turbo optos 63/66) are exempt from the distance rule; their callouts reach the trough and the turbo.
- Sensors inside a mechanism (the trough optos, the turbo's ball-sense and index optos) and the Lightup LEDs are documented projections onto the mechanism or target that carries them.
- Left Side Flasher 27 has two sockets and two placements; every other flasher has one.
- G.I. strings 4 and 5 and the backbox bulbs of strings 1 and 3 are backbox devices and are not placed.

## Blockers

- Playfield general illumination (G.I. strings 1-3, public 0-2) has no factory socket list: the manuals print only the string names, connectors and bulb types. Every playfield G.I. coordinate therefore comes from the retained table's GITL/GITR/GIB collections that its UpdateGI dispatches per string, reduced to distinct bulb-mesh lights, and stays observed. Promotion needs a socket-level G.I. survey of a real machine, or a factory drawing that assigns each playfield G.I. socket to its string.
- The race track's two reflector fixtures belong to G.I. string 2 by their factory wire colours, but the drawing prints no bulb count and the retained table models no bulb there, so they are neither counted nor placed.
- Switches 54 (Ten Point) and 75 (Right Ramp Enter) stay observed: through the refitted handbook switch drawing, callout 54 ends 0.075 from its wall and callout 75 0.064-0.078 from its trigger, above the 0.07 limit.

## Explicit projections

- pinmame.input.switch 41: Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmTrough keeps the balls virtually and pulses Top Trough on each Trough (solenoid 13) eject, so no table object represents the individual trough opto positions; the manual draws 41-45 along the A-19963 outhole ball trough at the lower right.
- pinmame.input.switch 42: Projected onto the trough eject kicker (Kicker BallRelease); the retained script's cvpmTrough.InitSwitches Array(42, 43, 44, 45) models the four ball positions virtually.
- pinmame.input.switch 43: Projected onto the trough eject kicker (Kicker BallRelease); see switch 42.
- pinmame.input.switch 44: Projected onto the trough eject kicker (Kicker BallRelease); see switch 42.
- pinmame.input.switch 45: Projected onto the trough eject kicker (Kicker BallRelease); see switch 42.
- pinmame.input.switch 63: Projected onto the turbo housing (Primitive Turbo_Bottom, table object center): the sensor is the A-14231/A-14232 LED/phototransistor pair mounted through the A-20065 turbo housing wall, and the retained script sets public 63 from its own turbo simulator (CloseBallSense/OpenBallSense) rather than from a playfield object.
- pinmame.input.switch 66: Projected onto the turbo housing (Primitive Turbo_Bottom, table object center): the sensor is the A-20047 Turbo Opto PCB mounted under the impeller inside the A-20038 Turbo Motor Assembly, and the retained script sets public 66 from its own turbo simulator (CloseTurboIndex/OpenTurboIndex).
- pinmame.output.lamp 71: Lightup LED projected onto its target face, Wall sw56.
- pinmame.output.lamp 72: Lightup LED projected onto its target face, Wall sw56.
- pinmame.output.lamp 73: Lightup LED projected onto its target face, Wall sw56.
- pinmame.output.lamp 74: Lightup LED projected onto its target face, Wall sw56.
- pinmame.output.lamp 75: Lightup LED projected onto its target face, Wall sw57.
- pinmame.output.lamp 76: Lightup LED projected onto its target face, Wall sw57.
- pinmame.output.lamp 77: Lightup LED projected onto its target face, Wall sw57.
- pinmame.output.lamp 78: Lightup LED projected onto its target face, Wall sw57.
- pinmame.output.lamp 81: Lightup LED projected onto its target face, Wall sw58.
- pinmame.output.lamp 82: Lightup LED projected onto its target face, Wall sw58.
- pinmame.output.lamp 83: Lightup LED projected onto its target face, Wall sw58.
- pinmame.output.lamp 84: Lightup LED projected onto its target face, Wall sw58.
- pinmame.output.solenoid 1: Auto plunger projected onto shooter-lane switch SW25; the Plunger1 object lies below the playfield bounds.

## Counts

- Placements: 178
- Validated input addresses: 40
- Observed-only input addresses: 2
- Validated output bindings: 92
- Observed-only output bindings: 3
- Inputs with a controlled `cabinet_or_service` record: 17
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 3
- Inputs with a controlled `unused` record: 17
- Outputs with a controlled `cabinet_or_service` record: 6
- Outputs with a controlled `unused` record: 4
- Outputs with a controlled `virtual` record: 14

## Promotion decision

Refused. `coverage.missing` is `["spatial_placement"]`: the playfield G.I. sockets are known only from one community table's light collections, the race-track reflector bulbs are neither counted nor placed, and switches 54 and 75 fail the factory switch-drawing check.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/indianapolis-500-1995/extracted-vpxtool.manifest.json`, SHA-256 `1febbab77b92e2cd5d2f0ad4cfedb2d8eb6768e38aeefb3bf1f087af8b44dba1`, 1031 files, 152451195 bytes.
- Handbook SHA-256 `537bf77824588e57e34b58a995611b850b25a0445ea2d8b9401a2fd9c50ffdda`; operations manual SHA-256 `89d0cb19701e21b6136d073a270d774c2304775655fe29e70e6b802f657df808`.
