# Williams FunHouse (1990)

Physical machine ID: `williams.funhouse.1990`. FunHouse is a Williams WPC-Alpha machine with two sixteen-character alphanumeric displays. It predates Fliptronics: the physical flipper coils are direct-wired through a dedicated flipper driver board, while PinMAME publishes synthetic button-driven states for digital flipper animation.

## Identity and driver family

Pinned PinMAME's `fh_l9` clone tree has sixteen drivers: production parent `fh_l9` plus fifteen firmware revisions, LED ghost-fix variants, translation/rules modifications, FreeWPC firmware, and prototype `fh_pa1`. All use the same physical playfield and authoring-relevant address inventory.

`fh_pa1` uses a distinct `GEN_WPCALPHA_1` `core_tGameData` because the prototype had the earlier System 11 sound subsystem; production drivers use `GEN_WPCALPHA_2`. The two structs copy the same flipper-switch declaration, mechanisms, lamp-position data, and inverted-switch mask, so this is a controller/sound-generation variant of the same machine rather than another playfield.

The prototype struct also retains `gameSpecific1=1`, a stale value copied before production FunHouse was corrected to zero. In pinned `wpc.c`, that flag selects the unrelated `WPC_CFTBL` chase-light integrator and writes internal PWM lamp slots 65-72 from solenoids 20/24 and G.I. bits 0/3. `wpc_init` still publishes only 64 lamps because `fh_pa1` has `lampCol=0`, so those internal slots are not an eight-lamp FunHouse extension. They are a pinned-source defect and must not be recreated as physical lamps.

The retained known-working table binds `fh_905h` at active script line 64. The adjacent `fh_905` assignment is commented out. `fh_905h` is physically identical to the `fh_l9` parent.

## Controller and public addresses

The record reuses `controllers/pinmame/wpc-alpha.json` unchanged. It enumerates eight dedicated cabinet inputs, the complete 8×8 switch matrix, all eight public generic-flipper input positions 111-118, eight CPU DIP positions, 50 public solenoid/state positions, the complete 8×8 lamp matrix, five G.I. strings, and both displays. Generic inputs 112 and 114 are live right/left cabinet-button states; the other six positions are explicit unused addresses.

Public outputs 1-28 are the printed coils, motors, and flasher circuits. Addresses 29 and 30 mirror live J111/WPC_GILAMPS state bits. Address 31 is the real pre-Fliptronic Game-On relay whose documented chain runs from CPU board U4/J121 through power-driver J113, the relay, J110, the cabinet switch, and J109 to the flippers. Address 32 is constant zero; 33-44 are unused on this machine/generation; 49 is the live virtual `sShooterRel` channel consumed by the built-in PinMAME simulator's left- and right-shooter transitions; and 50 is the reserved gap before the custom-output range, which FunHouse does not declare. Address 49 has no physical driver-board circuit.

## Physical flippers versus synthetic outputs

`fhGameData` declares `FLIP_SWNO(12,11)` and no `FLIP_SOL()` bits. The handbook lists three fitted assemblies: lower right FL-11630, lower left FL-11630, and upper left FL-11753. The printed flipper-circuit page shows them wired through the dedicated flipper driver board and cabinet buttons, outside the CPU-addressable solenoid matrix; its generic upper-right position is unfitted on FunHouse. Public inputs 112 and 114 are the generic right/left cabinet-button states. `core_updateSw` copies them to ordinary matrix inputs 11 and 12 for the ROM, so 11/12 are neither playfield coordinates nor EOS contacts.

When the Game-On relay is active, `core_updateSw` fabricates public states 45-48 from the live flipper buttons because the physical coils are not CPU controlled. Addresses 45/46 represent the same right-side state in power and combined public views, and 47/48 do the same for the left side. The retained script consumes callbacks `sLRFlipper` (46) and `sLLFlipper` (48); `SolLFlipper` rotates both `LeftFlipper` and `LeftFlipper1`. A recreation should use 46 for the lower-right bat and 48 for both lower-left and upper-left bats, but must not model 45-48 as four additional physical coils.

## Switch matrix and trough

The manual marks exactly two switches `(opto)`: 51 Dummy Jaw and 55 Steps Superdog. Pinned `fhGameData`'s inverted-switch mask sets exactly those two positions (`0x11` in column 5), so PinMAME's public polarity is fully normalized with no disagreement.

Switch 63 is Right Trough. The November 1990 handbook places callout 63 at the rightmost trough position, while the retained script's `ballrelease_hit` asserts `Controller.Switch(63)` and `KickBallToLane` kicks the same `ballrelease` object before clearing it. That kicker supplies the validated position and makes the trough sequence explicit: drained ball at outhole 73, trough positions 72/74/63, then solenoid 15 releases the rightmost ball into a shooter lane.

## Rudy comprises separate mechanisms

Rudy's head assembly combines three independent systems:

1. The jaw uses solenoid 21, a continuously running A-13997 DC gearmotor, and solenoid 22, its direction relay. Pinned `fh_handleMech` closes the open jaw when 21 is active alone and opens the closed jaw when 21 and 22 are active together. Dummy Jaw opto 51 detects a ball in the mouth.
2. Solenoids 26 and 27 latch the eyelids open and closed.
3. Solenoids 25 and 28 move the eyes right and left; neither active means straight ahead.

No separate retained-table object identifies the jaw motor or four eye/eyelid drives apart from the head assembly, so outputs 21, 22, and 25-28 are explicitly projected onto the fixed Dummy Jaw position rather than assigned invented coordinates.

## Trap door, gates, locks, and kickouts

Solenoids 5 and 6 open and close the upper-right trap door. The retained script derives switch 76 directly from the door primitive's `RotX`, asserting it at the closed angle rather than reading a discrete contact object. Switch 75 senses the upper-right loop path next to the door.

Solenoid 2 controls the upper-ramp/Steps-track diverter and automatically returns after the window modeled by `fh_handleMech`. Solenoid 14 controls the left-outlane Steps gate, rerouting a ball to the left shooter lane as a save feature; it likewise has no separate position sensor.

The three lock sensors 25, 27, and 28 share one A-14138 three-switch assembly. Solenoid 8 releases the locked balls for multiball. Rudy's Hideout uses switch 46 and solenoid 3, while the separate Dummy Eject Hole uses switch 65 and solenoid 16.

The manual really uses `Kickbig` twice: solenoid 3 is `Kickbig` and solenoid 4 is `Tunnel Kickbig`. These are distinct devices, not OCR errors or misspellings to normalize without evidence.

## Lamps and flashers

The controlled lamp matrix is fully populated. Addresses 53, 61, and 82 are marked `(x 2)` and have two spatially distinct physical bulbs. Same-named co-located table objects for 51, 52, and 72 are brightness/render layers around one manual-documented bulb, so each remains quantity one.

Lamp 12 is `Gangway 100,000`. The original operations manual's lamp matrix, the supplied November 1990 handbook's lamp matrix, and the physical playfield photograph agree; the original manual's isolated `Gangway 10,000` lamp-location entry is therefore a resolved one-digit typo. The physical award ladder is 75,000 / 100,000 / 150,000 / 200,000 / 250,000 / Extra Ball.

The November handbook's lamp-location drawing shows Steps lamps 56, 55, and 54 as top, middle, and bottom sockets in one vertical stack. In the retained table, `Top_finger_1`, `Mid_finger_1`, and `Bot_finger_1` are the five-unit-radius physical hotspots. The `_2`, `_3`, and `_4` objects are larger rendering layers for the same three inserts and are excluded from quantity and placement counts.

Six printed flasher circuits carry explicit bulb quantities: 17 has three blue bulbs, 18 one Dummy flasher bulb, 19 two Clock bulbs, 20 two Superdog bulbs, 23 three red bulbs, and 24 three clear bulbs. The retained table provides three distinct emitter objects for each of 17, 23, and 24. It abstracts circuit 19's two Clock bulbs into one physical Light fixture, so that circuit preserves the manual's two-socket quantity as explicit co-located placements. Circuit 20 has distinct `F20` and `F20a` Light objects, and the pinned community script assigns both to output 20, so the Superdog bulbs retain separate measured positions.

## General illumination

The known-working script is authoritative for runtime semantics. All retained known-working FunHouse scripts examined use the same effective mapping: address 1 drives Rudy, address 2 drives the upper/rear playfield, address 4 drives the lower playfield, and addresses 0 and 3 have no distinct playfield handler. The handbook supplies the exact physical circuit mapping: public 0/printed 01 uses Brown/White-Brown Q18/F10, 1/02 Violet/White-Violet Q10/F6, 2/03 Yellow/White-Yellow Q14/F8, 3/04 Orange/White-Orange Q16/F9, and 4/05 Green/White-Green Q12/F7.

Address 1 has three Rudy sign/shade emitters. GI_Upper's 19 table objects collapse into 15 physical hotspots after co-located brightness layers are clustered; GI_Lower's 45 objects collapse into 14. Every stored coordinate comes from the smallest-radius named object in its cluster, never from an arithmetic centroid. Address 0 is genuinely backglass-only in playfield authoring space. Address 3 is not: the handbook proves printed circuit 04 serves both the center backglass and a right-rear playfield branch. No retained script identifies the individual playfield emitters, so address 3 deliberately has no spatial record rather than a false cabinet-only disposition.

## Spatial convention and remaining blocker

Coordinates use the retained table bounds `left=0 top=0 right=964 bottom=2162`, normalized as `x/964` and `y/2162`, with `x=0` left, `x=1` right, `y=0` rear/backglass, and `y=1` apron/player. Cabinet, DIP, constant, unused, and virtual positions carry explicit not-applicable records. Projections are limited to a mechanism's own known object and are enumerated in the spatial audit.

The record remains partial only for spatial placement. Catalog identity, address enumeration, semantic names, polarity/normalization, physical wiring, displays, mechanisms, variants, recreation notes, provenance, and conflicts are validated. Promotion requires a socket-level survey identifying the individual right-rear-playfield emitters on G.I. circuit 04/public address 3; until then, guessing their count or coordinates would make the definition less useful to an author.
