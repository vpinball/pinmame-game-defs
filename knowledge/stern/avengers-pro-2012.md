# The Avengers Pro (Stern, 2012)

Coverage: **author-ready - complete Pro I/O, wiring, mechanisms, initial state, controller bindings, and spatial placements validated**

## Identity and evidence precedence

This definition covers `avs_110`, `avs_140`, `avs_170`, and `avs_170c`; the colored ROM changes display presentation only. The known-working VPW-derived Pro table uses `avs_170c` and its callbacks match the model-specific Pro manual: it is ground truth for PinMAME addresses, initial state, ball routing, and mechanism causality. The Pro manual governs physical inventory, service numbering, wiring, assemblies, and edition differences. The exact-ROM harness separately confirms the 128x32 four-bit DMD, GI 0, and conventional lamp activity.

## Four-ball trough and launcher

The Pro has four balls at switches 18-21 plus jam switch 22. The working table initializes 21, 20, 19, and 18 and output 1 ejects from the right end. Unlike LE, the shooter lane is matrix switch 23; dedicated D15/public 86 is unused. Output 2 drives the auto launcher with a proven 0.6-second impulse, power 55, and 0.5 randomness.

## Pro-specific output topology

The Pro has no LE eight-transistor auxiliary board. Its center HULK reset is main output 6, left ramp gate is 12, Hulk arms are 17 through a step-up board, Loki lock is 22 through a step-up board, and Hulk magnet is 23 through a step-up board. The pinned PinMAME root configures eight custom callback slots for the whole Avengers clone family, so a Pro ROM can emit public 51-58 transitions even though those drivers are physically absent. The model-specific manual and working Pro script resolve that emulator-family artifact: do not instantiate 51-58 on the Pro playfield.

## Targets and routes

The Pro THOR switches 1-4 are passive targets with no reset output; do not copy the LE THOR drop bank. The center HULK drop bank uses switches 52-55 and resets through main output 6. Left orbit is switch 47, right ramp exit is 48, and the Pro right orbit is switch 61 rather than LE switch 58. Output 7 opens the left orbit gate and output 12 raises the left ramp gate.

## Hulk, Loki, and Tesseract

Outputs 3/4 rotate Hulk in opposite directions with wheel optos 41/42. Output 17 lifts the arms. Switch 57 detects the Hulk plate and output 23 energizes its radius-16 centering magnet. Switch 62 holds the eject ball until output 5 kicks it at the proven angle 25 and force 20. The active-low Loki optos 49-51 initialize high when empty and output 22 drops the retaining post. The Tesseract is passive and inertial: ball impact drives rotation, optos 45/46 report it, and there is no motor output.

## Lamps and standard devices

All 80 matrix addresses are present, with unused 40, 56, 59, 64, 72, 74, 76, 77, 79, and 80 explicit. This matrix is substantially different from LE and must not be shared by number. GI is address 0. Three pops use switches 30-32/outputs 9-11, slings use 26/27 and 13/14, and the lower flippers use outputs 15/16 with dedicated buttons and normally-closed EOS contacts.

## Recreation checklist

- Build the four-ball trough, matrix shooter lane, passive THOR target bank, resettable center HULK bank, active-low three-ball Loki lock, Hulk rotation/arms/magnet/eject assembly, left orbit and ramp gates, and free-spinning Tesseract.
- Do not add the LE bridge, second resettable bank, right-orbit/ramp auxiliary gates, RGB GI relay bank, six-ball trough, or physical outputs 41-48.
- Treat exact Pro manual addresses as authoritative over clone-root callback capacity; observed public 53/54 activity during boot is not proof of physical Pro coils.
- Preserve sustained/PWM semantics for motors, magnet, lock, gates, and flippers, and use the proven script motion/force values as authoring baselines.

## Spatial coordinate model

All located records use the exact plain Pro table's 952 by 2115 player-view frame: x=0 is left, x=1 is right, y=0 is the rear/backglass end, and y=1 is the apron. The working Pro script establishes causality and semantic addresses; the official Pro manual establishes physical inventory and multiplicity; the exact table is used only for reconciled geometry. Cabinet, service, backpanel, virtual, unused, DIP, and other off-playfield records are explicit N/A dispositions with no fabricated XY. Paired GI render layers and unrelated VPX bloom/render helpers are collapsed or excluded; lock lamps 71/73/75 retain the three dedicated on-playfield L71/L73/L75 bulb-cover primitive centers rather than the unrelated Q18 S118a helper or off-playfield glow planes.

The official maps override two explicitly recorded VPX anomalies. First, the physical switch/coil maps put 30/Q9 left, 31/Q10 right, and 32/Q11 bottom; the exact table's Bumper1 at x=.678933 is scripted to sw31 and Bumper2 at x=.880455 to sw30. The controller bindings stay as scripted, but the physical XY assignments follow the manual. Second, the official coil-test map puts Q18 left flasher at y≈.43, Q12 left ramp gate at y≈.47, and Q19 right flasher at y≈.49. The archive's named S118p/S118a, RampControlGate, and S119a/S119b objects instead land at y=.182622/.264379/.355755. Adjacent mapped assemblies reconcile, so these three isolated vertical VPX placements are rejected; the manual-map approximate anchors are retained without inventing sub-map precision.

The Pro topology remains four trough balls on 18-21 plus jam 22, matrix shooter 23, center HULK reset 6, ramp gate 12, Hulk arms 17, Loki 22, magnet 23, and right orbit 61. No LE bridge, auxiliary board, six-ball trough, or LE-only mechanism is introduced.

Q21 is a manual-map assembly projection at about (0.374,0.252) on Hulk, between the Q17/Q3-Q4 and Q23/Q6 callouts on manual page 15. The VPX S121/S121a centroid at (0.663449,0.238199) is a conflicting render proxy, so it is rejected rather than silently retained; Q21's placement provenance is manual-only.

The four trough sensors and jam sensor are disclosed assembly projections. The exact table's Kicker.Drain and Kicker.BallRelease provide the trough endpoints, Primitive.Apron identifies the apron boundary, and the working script supplies the 18-to-21 physical order and four-ball inventory. Q1 uses the BallRelease assembly anchor. Switches 41/42 use the Hulk assembly anchor and 45/46 use the Tesseract base anchor; these points describe assemblies, not hidden contact leaves.

## Sources

- `manual.avengers-pro`: official Stern `Avengers-Pro-Manual.pdf`, SHA-256 `fdabec154947bc814d1b172fe68e91ad440780282c759f71668cfe7754f50031`; switch chart PDF page 13, coil chart page 16, lamp chart page 19, location maps, and model-specific assembly drawings.
- `vpx-table.avengers-pro-archive-45de3964`: exact plain Pro table `Avengers (Pro), The (Stern 2012).vpx` for ROM `avs_170`, SHA-256 `45de396493ddf562f06baa6950a5b3b46d7803f4aca1ed1df4ad7f45a6a4c5df`; bounds 0,0 through 952,2115; read-only extraction and candidate report `03-archive-pro`.
- `vpx.avengers-pro.vpw-1-3-1`: known-working Pro script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `85ea928246dbdf4b59a73e5237b6d248970770d3146381b06a1620c92cba21e8`.
- `runtime.avengers-pro.boot-start`: isolated exact `avs_170.zip` run, raw SHA-256 `4fa936ed6307059ef69f17100390a96ef91b9a28a65346d6ca8f45e1823122d6`; ROM archive SHA-256 `5bf37fe0f4a7a101d941de3659dd29dd9913b01f020d3202d644a86ed8802cc3` remains external.
