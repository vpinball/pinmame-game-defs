# Transcription: VPinMAME script-library flipper constants (core.vbs as installed with Visual Pinball)

Source: the VPinMAME Visual Basic script library the retained known-working table
loads at runtime (`script.vbs` line 130 `ExecuteGlobal GetTextFile("controller.vbs")`,
line 134 `LoadVPM "01560000", "Capcom.VBS", 3.10`; `Capcom.VBS` in turn executes
`core.vbs` and `VPMKeys.vbs`). This copy was read from the contributor's working
Visual Pinball installation at `L:\Visual Pinball\Scripts\core.vbs`
(SHA-256 `d380c476c555cdcc4c13e160841211a6aefb5bcb271d807fc04ec42a6945bd72`);
an older retained copy in the same installation's `_setup-backups` tree carries
the same values.

The table script binds its two flipper handlers with:

```vbs
SolCallback(sLRFlipper) = "SolRFlipper"
SolCallback(sLLFlipper) = "SolLFlipper"
```

and the library defines (core.vbs, "-- Flipper solenoids (all games)" block):

```vbs
'-- Flipper solenoids (all games)
Const sLRFlipper = 46
Const sLLFlipper = 48
Const sURFlipper = 34
Const sULFlipper = 36
```

Capcom's own switch constants in `Capcom.VBS` ("Last Updated in VBS v3.61") for
reference:

```vbs
Const swLRFlip      = 82
Const swLLFlip      = 84
Const swURFlip      = 81
Const swULFlip      = 83

Const GameOnSolenoid = 51
```

Consequence recorded by this definition: the symbolic flipper-solenoid numbers
are environment-owned `core.vbs` constants naming the **hold**-side synthetic
addresses (46/48/34/36), while `src/wpc/capcom.c`'s `io_w` mirror writes only the
**power**-side addresses (45/47/33/35, from physical solenoids 9/10/11/12) and
never writes 46/48/34/36. Under this library revision the retained table's two
`SolCallback(sLRFlipper/sLLFlipper)` bindings therefore receive no emulator data
at all - a consumed-table/environment defect, not a machine fact - and the
lower flippers animate from the table's own key handlers while the ROM drives
its physical coils 9/10 directly. The 45/47 mirror addresses remain the only
script-facing carriers of ROM flipper drive on this platform.
