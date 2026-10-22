# Standard mechanism assemblies

Primary curator visually checked native renders of PDF88/90/91/92 (printed2-16/2-18/2-19/2-20) against the service manual SHA256 `689326bb09debe0984264e76080620f58f0c15e4780e5803bcc5dee0b9637239`. Factual part-table transcription. Repeated part numbers are preserved rather than corrected from a presumed left/right pattern.

## A-17811 Kicker Arm (Slingshot) Assembly, 2-16

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | 02-2364 | Coil Plunger |
| 2 | A-17810 | Mounting Bracket Assembly |
| 3 | A-12664 | Kicker Crank Assembly |
| 4 | 12-6227 | Hairpin Clip |
| 5 | 4700-00030-00 | Flatwasher, 17/64 x 1/2 x 15ga. |
| 6 | 03-8085 | Armature Link |
| 7 | 20-8716-5 | Roll Pin, 1/8 x 7/16" |

Associated Parts for Right & Left Kickers:

| Item | Part Number | Description |
| --- | --- | --- |
| 8 | B-9362-R-3 | Coil & Bracket Assy., Left |
| [blank] | B-9362-R-3 | Coil & Bracket Assy., Right |
| a) | A-17808 | Bracket & Stop Assembly |
| b) | 01-8-508-S | Coil Retaining Bracket |
| c) | 4006-01017-06 | Mach. Screw, 6-32 x 3/8" |
| d) | 4406-01119-00 | Nut, 6-32 ESN |
| e) | AE-26-1200 | Coil Assembly |
| f) | 03-7066 | Coil Tubing |
| 9 | 10-128 | Spring |

## B-9414-3 Jet Bumper Assembly, 2-18

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | A-4754 | Bumper Ring Assembly |
| 2 | 03-6009-A5 | Bumper Base, White |
| 3 | 03-6035-4 | Bumper Wafer, Red |
| 4 | 03-7443-5 | Bumper Body, White |
| 5 | 10-7 | Spring |
| 6 | 24-8776 | Socket-Wedge Base |
| 7 | 24-8768 | Bulb #555 (6.3v., 0.25A.) |
| 8 [Associated Part] | 03-8254-9 | Jet Bumper Cap, Tr. Red (1 Used) |

The drawing shows the skirt/wafer, ring and return spring. Its socket specification establishes a physical emitter in the assembly, but does not identify an electrical GI string or make the two separate jet-area dome lamps84/85 into bumper-body lamps. The printed cap quantity is retained without multiplying it by the jet count.

## A-9415-2 Jet Bumper Coil Assembly, 2-19

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | B-7417 | Bracket & Stop Assembly |
| 2 | 01-1747 | Coil Retaining Bracket |
| 3 | 01-5492 | Armature Link, Steel |
| 4 | 01-5493 | Armature Link, Bakelite |
| 5 | 02-3406-1 | Coil Plunger |
| 6 | 10-326 | Armature Spring |
| 7 | AE-26-1200 | Coil Assembly |
| 8 | 4006-01017-04 | Mach. Screw, 6-32 x 1/4" |
| 9 | 03-7066 | Coil Tubing |

Associated Parts (Not Shown):

| Item | Part Number | Description |
| --- | --- | --- |
| 10 | B-12030-2 | Leaf Switch Assembly |
| a) | A-16443 | Switch & Diode Assembly |
| b) | 01-1168 | Switch Mounting Bracket |
| c) | 01-3670 | Switch Plate |
| d) | 03-7395 | Switch Actuator |

## A-15361 Tilt Mechanism Assembly, 2-20

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | A-15360 | Mount Plate, Tilt Mech. |
| 2 | 01-3444 | Bracket, Tilt Upper |
| 3 | 01-3445 | Bracket, Tilt Lower |
| 4 | 03-8668 | Pendulum, Tilt Mech. |
| 5 | 12-6231 | Wire, Plum Bob |
| 6 | 4006-01113-06 | Mach. Screw, 6-32 x 3/8" |
| 7 [Associated Parts] | 20-6502-A | Plum Bob |
| 8 [Associated Parts] | 4406-01120-00 | Wing Nut (2) |

The pendulum moves inside the lower contact bracket. This is the plumb-bob tilt14, distinct from cabinet slam tilt21; it has no coil or reset output.

## B-10686-1 Knocker Assembly, 2-20

| Item | Part Number | Description |
| --- | --- | --- |
| 1 | A-5387 | Coil Plunger Assembly |
| 2 | 01-11273 | Mounting Bracket Assy. |
| 3 | AE-23-800 | Coil Sub-Assembly |
| 4 | 01-8-508-T | Coil Retaining Bracket |
| 5 | 23-6420 | Rubber Grommet |
| 6 | 4008-01017-04 | Mach. Screw, 8/32 x 1/4" |
| 7 | H-11835 | Knocker Cable |
| 8 | 03-7067-5 | Coil Tubing |

## Runtime cross-check

Successful clean-state T.1 sweep `dh-switch-edges`, trace SHA256 `293bef61b7017edad07f72aa2211a46295e0000215dfa85dc3b5f9b8be67a307`: steps98/100/102/104/106 present switch61/62/63/64/65 at1, respectively, and observe a1→0 pulse at coil9/10/11/12/13. The release is host stimulus, not mechanical feedback. T.4 independently names and pulses knocker7. These service observations do not claim a gameplay pulse width or a measured ring/arm travel time.
