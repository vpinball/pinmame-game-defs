# Elvira and the Party Monsters (Bally, 1989) spatial review

Status: observed. The machine record stays `partial` at `machines/partial/bally/elvira-and-the-party-monsters-1989.json`; see the promotion decision.

The geometry source is the retained `Elvira and the Party Monsters (Bally 1989) nude.vpx` at SHA-256 `b9f54017274ccb4f3bddb08f6a999723502745527cdd8e237d639c1222552330`, an artwork variant of the 32assassin table. Its embedded script, SHA-256 `aaa5bc0f1893d27dc4e49c2d3829a03ad79769f6328e6e4a8138fc4308d0bc4b`, is the runtime binding authority. Playfield bounds are `left=0 top=0 right=952 bottom=1974`; every coordinate is x/952 and y/1974 rounded to six places.

## Evidence decisions

- Positions come only from objects the retained script binds to an address. Each was compared with the manual's switch, lamp and solenoid location drawings (printed 2-37, 2-39, 2-15); where the drawing prints no callout or ends its leader visibly elsewhere, the placement is `observed`.
- The manual owns physical construction and location; the known-working script owns runtime binding; pinned PinMAME owns the System 11B address space. The table's objects agree with the manual's drawings on every bumper, slingshot, lane, target, saucer and lock callout checked.
- Trough, lock, slingshot, drop-bank, popper, eject and flip-up addresses without an object of their own are documented projections onto the object of their own mechanism.
- Cabinet and backbox devices get controlled `not_applicable` records: the cabinet switches, the two flipper-button optos, the diagnostic inputs, the Country jumper, the knocker, the ELVIRA insert flashers, the insert GI relay, the A/C relay, the backboard Dead Head lamps 57-59, the backglass Barbeque lamps 60-64 and both displays.

## Explicit projections

- Switch 9: Projected onto the Drain kicker (Kicker.Drain, object centre): the retained script manages the outhole inside its bsTrough cvpmBallStack and has no object of the switch's own. The manual draws callout 9 at the outhole end of the trough.
- Switch 11: Projected onto the BallRelease kicker (Kicker.BallRelease, object centre): the three trough positions have no individual objects, bsTrough.InitSw 9, 11, 12, 13 managing them against the single exit kicker. The manual draws 11 nearest the shooter lane, then 12, then 13.
- Switch 12: Projected onto the BallRelease kicker; see switch 11.
- Switch 13: Projected onto the BallRelease kicker; see switch 11.
- Switch 31: Taken from Trigger.sw31, the invisible trigger the script's sw31_Hit handler pulses, which sits at the rear edge where the left (Monster Slide) ramp ends. The manual's switch drawing prints no callout 31, so the position is observed rather than validated.
- Switch 33: Projected onto the drag-point centroid of Wall.LeftSlingShot, whose _Slingshot event the script uses to pulse this address; the switch is part of the slingshot assembly (manual note ***, paired kicker actuating switch B-12459/B-12715).
- Switch 34: Projected onto the drag-point centroid of Wall.RightSlingShot; see switch 33.
- Switch 49: Projected onto the BallLock kicker (Kicker.BallLock, object centre): bsLock.InitSw 0, 49, 50, 51 manages the three lock positions against that single kicker. The manual's leaders for 49, 50, 51 and 52 all end in the upper-left lock lane.
- Switch 50: Projected onto the BallLock kicker; see switch 49.
- Switch 51: Projected onto the BallLock kicker; see switch 49.
- Switch 52: Taken from Trigger.sw52, the invisible trigger the script's sw52_Hit handler pulses. It sits about 0.1 right of where the manual's leader for 52 ends in the lock lane, so the position is observed.
- Switch 55: Projected onto Primitive.Coffin_Elvira, the open-state visual the script shows when target 53 is hit. The retained table has no object for the flip-up position switch; the manual's leader for 55 ends at the first flip-up. Observed, not validated; see conflict.flip-up-switch-roles.
- Switch 56: Projected onto Primitive.Coffin_Drac, the open-state visual shown for target 54; see switch 55.
- Solenoid 1: Projected onto the Drain kicker (Kicker.Drain), the object bsTrough.SolIn kicks from; the manual draws 01A at the outhole.
- Solenoid 2: Projected onto the BallRelease kicker (Kicker.BallRelease), the object bsTrough.SolOut ejects from; the manual draws 02A at the shooter-lane feed.
- Solenoid 3: Projected onto the centre target of the bank (HitTarget.sw42): one reset coil lifts all three targets, and the manual draws 03A at the bank.
- Solenoid 5: Projected onto the eject-hole saucer (Kicker.sw48) that bsTP.SolOut ejects; the manual draws 05A there.
- Solenoid 6: Projected onto the popper's saucer (Kicker.sw32). SolPopper lifts the ball from sw32 to the raised kicker sw32a before bsBP ejects it; the manual draws 06A at the popper.
- Solenoid 8: Projected onto the lock kicker (Kicker.BallLock) that bsLock.SolOut ejects; the manual draws 08A at the lock release.
- Solenoid 14: Two effect placements at the two rubber boogie men (Primitive.boogie1 and Primitive.boogie2) that SolBoogie moves. The Boogie Monsters Assembly C-12920 has one coil driving a rocker link between two shafts, so the placements mark where the one coil's effect is seen, not two coils.
- Solenoid 15: Placed at Light.f15, the one object the script flashes for this address. The location drawing's single leader for callout 15 ends on the left side rail, which agrees with this position, but the solenoid table prints two playfield bulbs; observed pending conflict.flasher-bulb-quantities.
- Solenoid 16: Three placements at Light.f16, f16a and f16b, the array the script flashes for this address. The manual's location drawing gives callout 16 three leaders in the upper-left quadrant, but the solenoid table prints "#906 flashlamp 2p". Observed pending conflict.flasher-bulb-quantities.
- Solenoid 17: Projected onto the upper-left bumper (Bumper.Bumper1) whose hit pulses switch 35; the manual draws 17 inside the upper-left bumper.
- Solenoid 18: Projected onto the drag-point centroid of Wall.LeftSlingShot; the manual draws 18 inside the left slingshot.
- Solenoid 19: Projected onto the upper-right bumper (Bumper.Bumper2) whose hit pulses switch 36; the manual draws 19 inside the upper-right bumper.
- Solenoid 20: Projected onto the drag-point centroid of Wall.RightSlingShot; the manual draws 20 inside the right slingshot.
- Solenoid 21: Projected onto the lower bumper (Bumper.Bumper3) whose hit pulses switch 37; the manual draws 21 at the lower bumper.
- Solenoid 22: Two effect placements at the two flip-up targets (HitTarget.sw53 and sw54) that SolFlipReset resets. One reset coil (B-12916) serves the Flip Up Targets Assembly; the manual draws 22 at the flip-up targets.
- Solenoid 32: Placed at Light.f32, the object the script flashes for this address. The manual's leader for 08C runs toward the skull passage roughly 0.1 lower and further right than this object, so the position is observed rather than validated.

## Counts

- Placements: 124
- Located input addresses: 42
- Located output bindings: 78
- Observed (not validated) bindings: 8
- Outputs with an intentionally omitted spatial key: 3
- Inputs with a controlled `cabinet_or_service` record: 13
- Inputs with a controlled `dip_switch` record: 1
- Inputs with a controlled `internal_nonvisual` record: 1
- Inputs with a controlled `unused` record: 12
- Outputs with a controlled `cabinet_or_service` record: 11
- Outputs with a controlled `internal_nonvisual` record: 1
- Outputs with a controlled `unused` record: 1
- Outputs with a controlled `virtual` record: 20

## Blockers

- Lamps 11 and 20 (slingshot inserts) carry no spatial record: the manual's lamp matrix and its location drawing put them on opposite slingshots (conflict.slingshot-lamp-sides).
- Solenoid 11 (Playfield GI Relay) switches playfield general illumination, but the manual enumerates no GI bulb count or position; the retained table's 29-member GI collection is not adopted.
- Solenoid 16 (Boogie Monsters flashers) carries three observed placements against a printed two-bulb count, and solenoid 15 one placement against two printed playfield bulbs (conflict.flasher-bulb-quantities).
- Solenoid 29 (Moon / Wolfman) has one retained object for two printed playfield bulbs; its placement is observed.
- Flashers 13, 25, 27, 28, 29, 30, 31 and 32 also light Insert Board bulbs in the backbox (1 to 3 each, included in physical.quantity); only their playfield bulbs are placed.
- Switches 31, 52, 55 and 56 and solenoids 15, 16, 29 and 32 have observed rather than validated placements: the manual's drawings print no callout, end the leader visibly away from the retained object, or print more bulbs than the table models.

## Promotion decision

Every controller address is enumerated with a semantic disposition and its printed wiring, and polarity is settled: `eatpmGameData` leaves `wpc.invSw` all zero, the drop-target optos reach the matrix through the C-12559 comparator board as ordinary closures, and the flipper-button optos carry button state. Promotion is refused because the slingshot lamps and the playfield GI have no placement, two flasher counts disagree inside the manual, and the flip-up switch roles are disputed. `coverage.missing` is `["input_semantics", "output_semantics", "mechanism_behavior", "spatial_placement", "unresolved_conflicts"]`; the addresses the three conflicts name (switches 53-56, lamps 11 and 20, flashers 15 and 16) carry `conflicted` provenance.

## Retained evidence

- Retained vpxtool extraction, 1263 files, 58249735 bytes, manifest SHA-256 `fa3ddac51285909c3763a87c017e2bfddac9ec422082bfae1fcedce4b3623fa5`.
- Object-by-object geometry dump `external:pinmame-review-artifacts/elvira-and-the-party-monsters/vpx-geometry-raw.tsv`.
- Eleven transcribed manual excerpts with rendered crops under `evidence/excerpts/bally.elvira-and-the-party-monsters.1989/`.
