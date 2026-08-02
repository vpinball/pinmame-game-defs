# The Avengers Pro (Stern, 2012)

Coverage: **author-ready - complete Pro I/O, wiring, mechanisms, initial state, and controller bindings validated**

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

## Sources

- `manual.avengers-pro`: official Stern `Avengers-Pro-Manual.pdf`, SHA-256 `fdabec154947bc814d1b172fe68e91ad440780282c759f71668cfe7754f50031`; switch chart PDF page 13, coil chart page 16, lamp chart page 19, location maps, and model-specific assembly drawings.
- `vpx.avengers-pro.vpw-1-3-1`: known-working Pro script at vpxtable_scripts revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`, SHA-256 `85ea928246dbdf4b59a73e5237b6d248970770d3146381b06a1620c92cba21e8`.
- `runtime.avengers-pro.boot-start`: isolated exact `avs_170.zip` run, raw SHA-256 `4fa936ed6307059ef69f17100390a96ef91b9a28a65346d6ca8f45e1823122d6`; ROM archive SHA-256 `5bf37fe0f4a7a101d941de3659dd29dd9913b01f020d3202d644a86ed8802cc3` remains external.
