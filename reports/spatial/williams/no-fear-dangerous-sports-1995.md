# No Fear: Dangerous Sports (Williams, 1995) spatial blockers

Retained VPX SHA-256 `3523285c6829c44068f8d81c5d886af8ab89156ed0e5aac18fbcfbf7a918d14f`; script `580749d770efe2e887fd92f7d05b3afa7f848f64e9f2736204986353b00817c5`; 1703-file extraction manifest `a5595fa7a8200924cf77ff843d6f6c88d21b3d8acb5a53e4198b9c84544264a9`; manual `176d5c887bf89ca35c0a6d558a757a1939da7145814f477ce099a16d50e2752b`.

Bounds: `left=0 top=0 right=964 bottom=2162`. Every canonical coordinate is x/964 and y/2162 rounded to at most six places.

## Placement status

- `validated`: 0 devices
- `observed`: 106 devices
- `candidate`: 17 devices
- controlled `not_applicable` records: 85
- used devices with no placement record: 0

## Projection classes

- **switch:** The retained table's object for the switch (trigger, spinner, target, kicker or slingshot wall), chosen by what the script binds. One projection: the trough-stack (jam) opto 31, which the table does not model, sits on the trough kicker sw32 at the eject end, where the manual's trough boards put the jam position.
- **lamp:** The light the script maps through vpmMapLights AllLamps (TimerInterval = lamp number), at its own centre. An insert lamp's light sits on its insert, over the socket; the raised sign lights 38, 83 and 84 and the skull's eye lights 82 and 85 are invisible light-map sources with no bulb, so those placements are only candidates. 37 and 48 are two-bulb circuits with one table light each. 58 is not fitted and the cabinet button lamps 86-88 are not applicable.
- **solenoid:** The object the solenoid callback moves or lights: the popper, eject and trough kickers, the impulse-plunger triggers of the auto plunger and kickback, the magnet triggers, the drop target wall, the slingshot walls, the skull jaw primitive at its stored position, the flippers, and the flasher lights. The flasher lights are invisible light-map sources with no bulb, so their placements are only candidates, and the skull flasher 21's one light stands for its two playfield bulbs. The flasher circuits 20, 21 and 23 carry insert-panel bulbs as well; only their playfield bulbs are placed. The backbox flashers 22, 26 and 27 and the knocker are not applicable.
- **gi:** The lights of the table's GI_Top, GI_Right and GI_Left collections, which UpdateGI switches from public GI 0, 1 and 2 and whose split agrees with the ROM's PLAYFIELD TOP, RIGHT and LEFT names; they are invisible light-map sources with no bulb, so the placements are only candidates, and their number is not a bulb count. The insert-panel strings 3 and 4 are not applicable.

## Unresolved physical geometry

- No factory location drawing has been checked against the table: none of the placements is validated. The flasher, G.I. and raised lamp placements are candidates and every other placement is observed. The manual's lamp (2-35), switch (2-37) and solenoid/flashlamp (2-39) drawings carry numbered callouts that a drawing callout check could compare with these placements.
- The trough-stack opto 31 is projected onto the trough kicker sw32; the table models no jam position.
- The playfield G.I. strings 0-2 carry only candidate placements: the table's light-map sources model no bulb, and no drawing or other source locates or counts the playfield bulbs on each string.
- The flasher lights and the raised lamps 38, 82, 83, 84 and 85 carry only candidate placements: the table's lights are light-map sources with no bulb, set where the table throws the light, so they do not locate the sockets.
- Lamps 37 and 48 and the skull flasher 21's playfield pair light two bulbs each and the table models one light for each, so one bulb of each has no placement.
- Flasher 19's bulb count: the Solenoid/Flashlamp Table, its two copies and the flashlamp wiring drawing print one #906, the locations list prints two; the record follows the table and places the table's single light.

## Promotion decision

partial: every fitted playfield device has an observed placement or a controlled not-applicable record except the flashers, the raised lamps 38, 82, 83, 84 and 85 and the three playfield G.I. strings, which carry only candidate light-map positions; no placement has been validated against the manual's location drawings, the jam opto is projected, and lamps 37 and 48 and the skull flasher 21 lack a placement for their second playfield bulb.
