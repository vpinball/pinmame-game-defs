# The Shadow (Bally, 1994) spatial review

Status: observed. Every switch, coil, motor, magnet and lamp and every flasher except 17 and 18 is placed from the retained VPW table or carries a controlled `not_applicable` record, but every placement stays `observed`, which keeps the record at `machines/partial/bally/the-shadow-1994.json`.

The geometry source is `The Shadow (Bally 1994) VPW Mod v1.0.vpx` (SHA-256 `f256caa5f7af3f17c5da3fa62b23ae49a6f4e9f80ab24acaac953db8d2cfe13e`); its embedded script (SHA-256 `973a9ad5b2ccbc31334dc3752e065f7a94265c69f9a89f3bcf58e2f3eec51f77`) is the runtime binding authority. Exact playfield bounds are `left=0 top=0 right=975 bottom=1974`; every coordinate is x/975 and y/1974 rounded to six places.

## Evidence decisions

- The VPW script is the runtime authority; the November 1994 operations manual is the physical inventory, construction and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.
- The trough optos, the lock positions and the Battlefield kicker opto are documented projections onto the mechanism that carries them; the diverter, kicker-head, slide-motor and mini drop-target reset coils are projections derived from the geometry of the parts they move.
- The ramp-ring lamps 81-84 use the table's ring primitives; the printed 2-39 drawing is consistent with 81 and only roughly checks 82-84.
- G.I. strings 3 and 4 (the insert strings) and the backbox bulbs of flashers 17, 18 and 26-28 are backbox devices and are not placed.

## Blockers

- Every coordinate comes from one table lineage (the VPW Mod 1.0 build and its Skitso ancestor, which agree almost everywhere because they share geometry). The main lamp drawing (printed 2-39) has been fitted to 29 table lamps with every residual within 0.015 (see manual_reconciliation), but no validation rule has been applied yet, and the switch (2-41) and solenoid/flasher (2-43) drawings have not been fitted.
- Flashers 21, 22 and 23 each print two playfield sockets; the VPW table models one Flupper dome per output, so the second socket of each is not placed.
- Flashers 17 (Mini Playfield) and 18 (Left Side) are not placed: the VPW table models no bulb or dome for them and drives only off-playfield helper lights, and the older table's F117/F118 are glow images, not sockets. Their sockets have to be measured on the printed 2-43 location drawing.
- The ramp-ring lamps 81-84 come from the table's ring primitives, not bulbs. Callout 81 on the 2-39 drawing points to a bracket about 0.02 from the ring, and the drawing's ramp inset, which alone shows 82-84, is only consistent with them to within 0.04-0.06, so the ring positions are not independently confirmed.
- Playfield general illumination (G.I. strings 1, 2 and 5, public 0, 1 and 4) has no factory socket list; every coordinate comes from the table's G.I. collections.

## Explicit projections

- pinmame.input.switch 36: Projected onto the Battlefield kicker head (Primitive SlingMiniPF, a mesh baked at world coordinates whose vertex bounding-box center is used, at the head's middle position): the Mini Kicker opto rides on the moving A-19070 coil/slide assembly, and the retained script pulses 36 from the Slingshot events of the nineteen position walls bf_k01-bf_k19 that it switches with Controller.GetMech(0).
- pinmame.input.switch 41: Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmBallStack holds the balls virtually on 41-45 (InitSw 0, 41, 42, 43, 44, 45) and the table has no object for the individual trough opto positions or for Top Trough 46; the manual draws the A-18753 outhole ball trough at the lower right.
- pinmame.input.switch 42: Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmBallStack holds the balls virtually on 41-45 (InitSw 0, 41, 42, 43, 44, 45) and the table has no object for the individual trough opto positions or for Top Trough 46; the manual draws the A-18753 outhole ball trough at the lower right.
- pinmame.input.switch 43: Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmBallStack holds the balls virtually on 41-45 (InitSw 0, 41, 42, 43, 44, 45) and the table has no object for the individual trough opto positions or for Top Trough 46; the manual draws the A-18753 outhole ball trough at the lower right.
- pinmame.input.switch 44: Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmBallStack holds the balls virtually on 41-45 (InitSw 0, 41, 42, 43, 44, 45) and the table has no object for the individual trough opto positions or for Top Trough 46; the manual draws the A-18753 outhole ball trough at the lower right.
- pinmame.input.switch 45: Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmBallStack holds the balls virtually on 41-45 (InitSw 0, 41, 42, 43, 44, 45) and the table has no object for the individual trough opto positions or for Top Trough 46; the manual draws the A-18753 outhole ball trough at the lower right.
- pinmame.input.switch 46: Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmBallStack holds the balls virtually on 41-45 (InitSw 0, 41, 42, 43, 44, 45) and the table has no object for the individual trough opto positions or for Top Trough 46; the manual draws the A-18753 outhole ball trough at the lower right.
- pinmame.input.switch 63: Projected onto the lockup kicker (Kicker Lockup): the retained script's cvpmBallStack bsLock holds the locked balls virtually on 63-65 (InitSw 0, 63, 64, 65) and the table has no object per lock position.
- pinmame.input.switch 64: Projected onto the lockup kicker (Kicker Lockup); see switch 63.
- pinmame.input.switch 65: Projected onto the lockup kicker (Kicker Lockup); see switch 63.
- pinmame.output.solenoid 3: Projection: the midpoint of the left diverter's two baked blade meshes Div_Bot_Left and Div_Bot_Right, each taken as the center of its vertex bounding box in the retained extraction's .obj (world x = obj x, world y = obj y); the coil sits under the blades, and the table models no coil object.
- pinmame.output.solenoid 4: Projection: the midpoint of the left diverter's two baked blade meshes Div_Bot_Left and Div_Bot_Right, each taken as the center of its vertex bounding box in the retained extraction's .obj (world x = obj x, world y = obj y); the coil sits under the blades, and the table models no coil object.
- pinmame.output.solenoid 5: Projection: the midpoint of the right diverter's two baked blade meshes Div_Top_Left and Div_Top_Right, each taken as the center of its vertex bounding box in the retained extraction's .obj (world x = obj x, world y = obj y); the coil sits under the blades, and the table models no coil object.
- pinmame.output.solenoid 6: Projection: the midpoint of the right diverter's two baked blade meshes Div_Top_Left and Div_Top_Right, each taken as the center of its vertex bounding box in the retained extraction's .obj (world x = obj x, world y = obj y); the coil sits under the blades, and the table models no coil object.
- pinmame.output.solenoid 15: Projection: the vertex bounding-box center of the baked kicker-head mesh SlingMiniPF (world x = obj x, world y = obj y); the head travels along the bf_k01-bf_k19 rail, so this is its modelled resting position, not a fixed socket.
- pinmame.output.solenoid 19: Projection: the vertex bounding-box center of the baked kicker-head mesh SlingMiniPF (world x = obj x, world y = obj y); the head travels along the bf_k01-bf_k19 rail, so this is its modelled resting position, not a fixed socket.
- pinmame.output.solenoid 20: Projection: the vertex bounding-box center of the baked kicker-head mesh SlingMiniPF (world x = obj x, world y = obj y); the head travels along the bf_k01-bf_k19 rail, so this is its modelled resting position, not a fixed socket.
- pinmame.output.solenoid 24: Projection: the midpoint of the drag-point bounding-box centers of the two middle Battlefield drop-target walls sw86 and sw87; the reset coil sits under the bank, and the table models no coil object.

## Manual drawing reconciliation

- Drawing: printed 2-39 LAMP LOCATIONS (continued), PDF page 134, rendered at its native 300 dpi as 2550x3300 px. Method: least-squares affine map from drawing pixels to normalized playfield coordinates, fitted to VPW lamp positions; control points are the pixel centers of numbered circular inserts (Hough-detected circles whose printed number sits inside the insert); leader endpoints are read by eye on a zoomed render to +/-2 px.
- Main playfield drawing: 29 control lamps, residual RMS 0.0053, largest 0.0148 (render SHA-256 `e6467d4155f5e37e4b19ce9d882cd5da9e1cadc6cd8b910c26aa8b66cd80429e`). Callout 81's leader endpoint at pixel (1420, 799) maps to (0.118, 0.347), on a bracket at the left ramp entrance, 0.041 from lamp 81's ring primitive.
- Ramp inset cross-check: The inset's control lamps span only the Battlefield (about 124x164 px), its x and y scales differ by about 21 percent, and the ring leader endpoints lie about 210-380 px outside that cluster, so these estimates are extrapolations: consistent with the ring primitives to within 0.04-0.06, but unable to confirm them.
  - Lamp 82: pixel (931, 781) -> (0.431, 0.362), 0.059 from its ring primitive.
  - Lamp 83: pixel (1061, 455) -> (0.636, 0.142), 0.038 from its ring primitive.
  - Lamp 84: pixel (1235, 549) -> (0.928, 0.206), 0.063 from its ring primitive.

## Counts

- Placements: 176
- Validated input addresses: 0
- Observed-only input addresses: 54
- Validated output bindings: 0
- Observed-only output bindings: 98
- Unplaced output bindings: 2
- Inputs with a controlled `cabinet_or_service` record: 19
- Inputs with a controlled `constant` record: 1
- Inputs with a controlled `dip_switch` record: 8
- Inputs with a controlled `internal_nonvisual` record: 3
- Inputs with a controlled `unused` record: 3
- Outputs with a controlled `cabinet_or_service` record: 5
- Outputs with a controlled `virtual` record: 15

## Promotion decision

Refused. `coverage.missing` is `["spatial_placement"]`: the placements come from one table lineage and only the lamp drawing has been fitted against them, three flashers have an unplaced second socket, flashers 17 and 18 are not placed, the ramp-ring positions are not independently confirmed, and the playfield G.I. sockets come only from the table's G.I. collections.

## Retained evidence

- Extraction manifest `external:pinmame-vpx-sources/bally/the-shadow-1994/vpw-mod-1.0/extracted-vpxtool.manifest.json`, SHA-256 `0ffe2c6f22c92bae205ece4dcc8d2d904009c1ed80dbc3d9693d0bfccedc1b59`, 1608 files, 203264122 bytes.
- Operations manual SHA-256 `900c94825a940a34abaae5d14284098b44dda1e6c7f79d47a92e60f7bd0c4b9e`.
