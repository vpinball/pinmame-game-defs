# Embryon retained script and core timer

The local v1.4 embedded script initializes `bsTrough` with switches 8 and 5 and two balls,
and the saucer at switch 4. Public solenoids 1, 2 and 3 reset respectively the single,
left-three and top-three drop targets; 4 ejects the saucer, 5 serves the trough, 6 is
the knocker and 20 operates the right outlane flipper. The right flipper handler moves
the lower and upper flippers together. Five captive/messenger balls are created at
`k28`, `k17`, `k33`, `k34` and `k3433`.

At the back target, `t17x_Hit` calls `HitStandup 17` and then `ManualRightTargetUp`;
`HitStandup` queues `vpmTimer.PulseSw`. In the supplied `core.vbs` (SHA-256
`a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69`),
`PulseSw` queues a timer that writes the switch TRUE then FALSE. `SolDropUp` raises
the drop and clears its switch. This is a table workaround, not a faithful simulation
of the physical normally-closed back-contact break and restoration. Two fresh-state
native runs each exercised two such breaks: output 1 pulsed after every restoration,
and the host then modeled the target returning up by clearing switch 17. The drop is
down during the break; its subsequent home state follows the reset coil. This avoids
assuming that the physical target remains down after the ROM resets it.

The newer retained v2.0.2 script's `UpdateDTLamps` and `UpdateVRLamps` distinguish
the backbox and playfield letter bits. Its solenoid 18/19 GI effects are table visual
conveniences; the machine uses those outputs for lockout and flipper-enable relays.

Pinned `by35.c:134-166` calculates lamp data from the inverted high nibble of PIA0:A
and strobes both the main and auxiliary matrices on each data write. It suppresses
only address `0x0f`; each other selector produces public bits in all four data groups.
The address latches are updated separately at `by35.c:261` and `277`. A9's physical
selector 7 has no SCR on any group, so public 72/88/104/120 are transport captures on
a physically blank decoder row. Their startup and normal-operation activity is not
a diagnostic-only lamp sweep. The retained non-service traces also activate N/U
outputs 52/63/117; their firmware use has not been established, so they remain unknown.
