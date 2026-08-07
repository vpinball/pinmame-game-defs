# Whirlwind — Special/Controlled Solenoid Circuit Theory and A/C Select Relay

Transcribed from `Whirlwind_OPS.pdf`, PDF page 43 (printed page 33, "TEST/
DIAGNOSTIC PROCEDURES (Continued)", Figure 4) and PDF page 105 (printed page
95, "CONTROLLED, SPECIAL, & SWITCHED SOLENOIDS" schematic, Section 3). Read
from the 300 dpi rendered pages.

## Printed page 33 — Figure 4 theory (verbatim)

"'On' State Logic - Special Solenoid": driver stage 7407 -> 7402 (NOR) ->
2N4401 -> TIP122 -> Special Solenoid coil at Sol. B+ (+25V), triggered from
"Spl Sol Trigger 1J18" and gated "Low, with flippers enabled".

"'Off' State - Special Solenoid": "The Special Switch Trigger Input goes low.
Meanwhile, the PIA line remains high. The remaining signals reverse their
states."

"'On' State Logic - Controlled Solenoid": driver stage 7408 (AND) -> 2N4401
-> TIP122 -> Controlled Solenoid coil at Sol. B+ (+25V), gated by a PIA
enable input and a BLANKING signal.

"'Off' State - Controlled Solenoid": "The Enable Input (from the PIA) goes
low. Meanwhile, the BLANKING signal remains high. The rest of the signals
reverse their states."

"NOTE: As directed by the game program, the Solenoid A/C Select Relay
(solenoid 12) switches the solenoid B+ power between two power busses to
permit actuating two groups of solenoids at the proper times. In its
de-energized state, the Relay connects the 'circuit A power' to 16
'controlled' and 'switched' solenoids (identified in the table with no suffix
letter or the letter A, after the solenoid number). Individual solenoid
operation then depends on the game program enabling the ground path for
solenoid actuation via the driver transistor associated with each solenoid
circuit. For example, the game program can actuate the Outhole Kicker
solenoid (sol. 01A), via the driver transistor Q33.

When the game program determines that the Solenoid A/C Select Relay (sol. 12)
must be energized, the relay connects 'circuit C power' to eight group C
solenoids (01C through 08C). Now, driver transistor Q33 can actuate the
Bottom Right Flasher circuit (sol. 01C), which has two lamp circuits, one to
the Insert Board and one to the playfield. Using this 'multiplexing'
technique, the same driver transistor can control actuation of two separate
(A side and C side) solenoid circuits."

Figure 4 traces the exact circuit for solenoid 01A/01C (Outhole Kicker /
Bottom Right Flasher): System 11B CPU Board (D-11883) driver transistor Q33
(1J11-1) feeds, through the Aux Power Driver Board (D-12247) and Master
Interconnect Board (D-12313-574) with the A/C select relay (K1, driven by
solenoid 12's own Q8 driver via 5J2-5/Vio-Brn), either the Outhole Kicker
coil (Sol. 01A, Brn wire, de-energized/"A" path) or the Bottom Right Flasher
#906 bulb (Sol. 01C, Orn wire, energized/"C" path via 5J11-1).

## Printed page 95 — Controlled, Special, & Switched Solenoids schematic

Confirms every function/driver-transistor pairing already in the Solenoid
Table (solenoid-flasher-locations.md): "CONTROLLED SOLENOIDS (25V)" block
(Sol. 9 Q17, Sol. 10 Q9, Sol. 11 Q16, Sol. 12 "A/C SELECT RELAY (AUX PWR
DRVR) Q8", Sol. 15 Q14, Sol. 16 Q6); "SPECIAL SOLENOIDS (25V)" block (Sol. 17
Q75, Sol. 19 Q73, Sol. 21 Q77, Sol. 22 Q79); "SPECIAL SOLENOIDS (50V)" block
(Sol. 13 "RAMP DIVERTER" Q15, Sol. 14 "CELLAR KICKBACK" Q7, Sol. 18 "LEFT
KICKER (sling)" Q71, Sol. 20 "RIGHT KICKER (sling)" Q69); "SOUND OVERLAY
SOLENOIDS (25V)" block (Sol. 23 "L LIGHTNING FLASHERS (SOL Q1)", Sol. 24
"BLOWER/Triac Bd (SOL Q4)", Sol. 25 "Mdl THUNDER FLASHER (SOL Q7)", Sol. 26
"R THUNDER FLASHERS (SOL Q10)", Sol. 27 "WHEELS Spinner Motor (SOL Q13)");
and "SWITCHED SOLENOIDS" block (01A-08A/01C-08C with driver transistors
Q33/Q25/Q32/Q24/Q31/Q23/Q30/Q22 and diode-steered A/C pairs D45/D46 through
D41/D42, all routed through the "Aux Pwr Driver Board A/C Select Relay 25V
Circuits" "A" Side / "C" Side busses). Printed page 95 explicitly labels
solenoid 14 "CELLAR KICKBACK" (the Solenoid Table's own compressed
abbreviation is "Under P'fld Kickback"), confirming the two are the same
device.

No additional public-address information beyond the Solenoid Table itself;
this page is transcribed because it is a drawing (schematic), and the
A/C-relay multiplexing theory it and page 33 document is load-bearing for
`controllers/pinmame/system-11.json`'s solenoid-group notes.
