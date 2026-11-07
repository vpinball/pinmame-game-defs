# Whirlwind flashlamp placement evidence

The Williams manual, PDF 83 / printed 73, identifies thirteen C-bank bulbs.
Its round flashlamp symbols are usable measurements. The two leaders for
Million and Million+ terminate on insert features; they do not identify
socket centers and are deliberately excluded. The five sound-overlay bulbs
belong to the rear playfield panel D-13356 (PDF 52/62), not the backbox.
The complete Red Parts Catalog elevation, actual LMP1-LMP10 PCB photograph,
and operator's handbook establish two left, one middle and two right
flashlamps. The operations table's left quantity of three is an erratum;
the rear-panel-lamp-assembly and handbook-solenoids excerpts preserve it.

## Native factory drawing measurements

Source PDF SHA-256:
`365421ffdc059180ef5457fec2aa7567981954c383ab26d6b1e92223b790c649`.
Native render `hi-083.png`, 2473x3273, SHA-256
`74d2e9fd5823471dc42a45efca2cc83aa1ff9306b7de1e1465940c8fb2cec70a`.
Retained native drawing crop: `whirlwind-20261106/manual83-drawing.png`,
box (1384,327,2299,2291). Coordinates below are crop pixels, origin top left.
The committed image is a smaller, unmarked crop of this drawing.

The six bumper centers, two flipper pivots and spinner-bar center were read
independently on the drawing. Exact original-table object centers use
x/964 and y/2162; the seed retains their raw-file hashes and normalized
values. It also retains the equivalent full-render pixels.

| Control | Crop pixel |
| --- | --- |
| Bumper1 | 319,282 |
| Bumper2 | 477,255 |
| Bumper3 | 444,408 |
| Bumper4 | 94,736 |
| Bumper5 | 268,772 |
| Bumper6 | 202,627 |
| LeftFlipper pivot | 285,1535 |
| RightFlipper pivot | 590,1535 |
| sw41 spinner-bar center | 752,547 |

Least-squares affine mapping from crop pixels (u,v) to player coordinates:

    x = .0012246135663693367*u - .00001182511786664532*v - .012243619630393977
    y = .000014432178870973248*u + .0005773826714006729*v - .04858408563252357

Worst control leave-one-out offset is .037416 normalized. These are
independent mechanism reads, not points calculated backward from the fit.
Each measured point lies inside the nine-control convex hull. The scan
supports three decimal places for measured coordinates, not six.

| Public output | Physical symbol | Crop pixel | Normalized x,y |
| --- | --- | --- | --- |
| 26 / 2C | Spinner flashlamp circle | 732,583 | .877,.299 |
| 27 / 3C | Upper-jets flashlamp circle | 399,321 | .473,.143 |
| 29 / 5C | Lower-jets flashlamp circle | 180,715 | .200,.367 |
| 31 / 7C | Rear round flashlamp symbol | 444,530 | .525,.264 |
| 31 / 7C | Front round flashlamp symbol | 435,788 | .511,.413 |
| 32 / 8C | Compass flashlamp circle | 436,1300 | .506,.708 |

`tools/seeds/williams/whirlwind-1990-flasher-callouts.json` makes all reads
and transformations reproducible with `drawing_callouts.measured`.
The two excluded feature leaders are near crop (393,607) and (527,690).

## Five raised modeled domes

Supplemental table: Whirlwind 4K1.113, table SHA-256
`4ef5614e92109aa8c9362957e0b8390c56bcf04b098aaacad7cabb8482ffbd54`;
embedded script SHA-256
`704319827005cfaa196b4415cd9e42db3ff8b4d55192b711d08884456d7f2501`.
Its bounds are 0..952 by 0..2164. This supplies physical dome geometry;
the original known-working script remains runtime authority. Credits name
Flupper, Rothbauerw, Fleep and physical-owner reference contributor
Blackmoor, among others. The retained table and extraction are external.

| Public output | Bound dome base | Raw x,y,z | Normalized x,y |
| --- | --- | --- | --- |
| 25 | Flasherbase9 | 839.0108,1339.6975,85 | .881314,.619084 |
| 27 | Flasherbase4 | 605.4738,264.13303,143 | .636002,.122058 |
| 28 | Flasherbase3 | 283.548,385.0219,143 | .297845,.177921 |
| 29 | Flasherbase2 | 98.80734,696.13293,143 | .103789,.321688 |
| 30 | Flasherbase1 | 150.80733,1222.7997,115 | .158411,.565065 |

Script lines 376-385 register outputs 25-32. `FlasherSet` case 25 sets
ObjLevel(9); case 27 sets ObjLevel(4); case 29 sets ObjLevel(2).
`SetLamp` case 128 sets ObjLevel(3), and case 130 sets ObjLevel(1).
`InitFlasher` binds each numbered `objbase` to `Flasherbase` + nr.
Thus the numeric matches above are actual code paths. They do not come
from matching object names alone. The exact base centers locate the domes,
rather than displaced Flasherlight sprites or baked illumination maps.

The five separate factory reads used as checks are (721,1135), (516,288),
(250,417), (123,644), (133,1035), respectively. A nine-control fit plus
leave-one-out callout fit checks side, order and location with the
repository's .07 normalized limit. The callout fit includes the six printed
bumper numbers, using the same independently read centers as their control
features; this reuse is explicit. All eleven callout pairs agree, with
maximum leave-one-out offset .0538. This keeps the table coordinates;
it does not replace them with a drawing fit or claim independent layout
ancestry. Mesh inspection of the world-space OBJ supports these dome
bases; mounting feet are not extra bulbs. The table's Primitive115 and
Primitive056 are round windows and its remaining Light objects have
`show_bulb_mesh=false`; those helpers do not establish additional sockets.

The two excluded Million/Million Plus feature leaders remain excluded from
the factory callout check. Their actual separate glass bodies are now
placed from bounded paired physical photographs; see
`hidden-flasher-placement.md` and its pinned projection seed. Cellar matrix
bulbs use their own separate glass meshes, documented in `matrix-bulbs.md`.
