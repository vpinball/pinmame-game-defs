# Cirqus Voltaire — Lamp Matrix

Transcribed from `Bally_1997_Cirqus_Voltaire_Manual.pdf`, PDF page 154, printed page 2-48, the LAMP
MATRIX table. Read directly from a 300 dpi `pdftoppm` render; the table is a clean unshaded 8x8 grid
with no drawing-only content, so no crop was made (a crop would cost roughly forty times the bytes of
this transcription for a fact this table already carries as text).

Column wiring: 1 Yellow-Brown J121-1 Q96, 2 Yellow-Red J121-2 Q100, 3 Yellow-Orange J121-3 Q95, 4
Yellow-Black J121-4 Q99, 5 Yellow-Green J121-5 Q94, 6 Yellow-Blue J121-6 Q98, 7 Yellow-Violet
J121-7 Q93, 8 Yellow-Gray J121-9 Q97. Row wiring: 1 Red-Brown J125-1 Q104, 2 Red-Black J125-2 Q108,
3 Red-Orange J125-4 Q103, 4 Red-Yellow J125-5 Q107, 5 Red-Green J125-6 Q102, 6 Red-Blue J125-7 Q106,
7 Red-Violet J125-8 Q101, 8 Red-Gray J125-9 Q105. This is the identical J121/J125/Q93-Q108 power
driver board wiring already documented for Williams Monster Bash (`monster-bash-1998` evidence),
confirming it is a shared WPC-95 board layout rather than a game-specific harness.

| Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label | Addr | Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | Cirqus "R" | 21 | Cirqus "I" | 31 | Side Show | 41 | Ringmaster Left | 51 | Crank Top | 61 | Middle Jackpot | 71 | Wow Right "W" Target | 81 | Extra Ball |
| 12 | Grid Top | 22 | Cirqus "C" | 32 | Left Loop Top | 42 | Ringmaster 2 | 52 | Crank 2 | 62 | Right Jackpot | 72 | Wow "O" Target | 82 | Top Jet Bumper |
| 13 | Cirqus "Q" | 23 | Grid Middle/Left | 33 | Left Loop 3 | 43 | Ringmaster 3 | 53 | Crank 3 | 63 | Light Standup Target | 73 | Wow Left "W" Target | 83 | Middle Jet Bumper |
| 14 | Cirqus "U" | 24 | Grid Bottom/Left | 34 | Left Loop 2 | 44 | Ringmaster 4 | 54 | Crank Bottom | 64 | Lock Standup Target | 74 | Ring "N" | 84 | Lower Jet Bumper |
| 15 | Grid Top/Right | 25 | Grid Bottom | 35 | Left Loop 1 | 45 | Ringmaster Right | 55 | Right Loop Top | 65 | Ring "R" | 75 | Ring "G" | 85 | Right In-Lane |
| 16 | Cirqus "S" | 26 | Grid Middle | 36 | Multiball | 46 | Special | 56 | Right Loop 3 | 66 | Ring "I" | 76 | Right Outlane | 86 | Volt Left |
| 17 | Grid Middle/Right | 27 | Grid Bottom/Right | 37 | Lock | 47 | Razz | 57 | Right Loop 2 | 67 | Shoot Again | 77 | Left In-Lane | 87 | Volt Right |
| 18 | Left Jackpot | 28 | Grid Top/Left | 38 | Spot Marvel | 48 | Frenzy | 58 | Right Loop 1 | 68 | Left Outlane | 78 | Skill Ring | 88 | Start Button |

`J1XX = Power Driver Board`. Lamp 88 (Start Button) is a real printed insert with a driver address,
but the retained VPX table's `UpdateLamps` routine has both of its `Lampm 88, l88` / `Lampm 88, l88b`
calls commented out (`extracted-vpxtool/script.vbs` lines ~1693-1694), so no `Light` object renders
it; it is still recorded `used` with a controlled `cabinet_or_service` spatial record like the other
cabinet-button lamps, and the table gap is disclosed in `physical.notes`.

Every other address (11-87) has a matching `Light` pair (`l##`/`l##b`, a co-located brightness double)
in the retained extraction; see `vpx-geometry.txt`. Lamps 85/86/87 (Right In-Lane, Volt Left, Volt
Right) and switches 17/26/75/76 (Right Inlane, Left Inlane, "Volt" Right, "Volt" Left; see
`switch-matrix.md`) independently corroborate each other: the retained script's `UpdateLamps` ties
lamp 85 to table object `volt3` (`imgswapm 85, volt3, ...`), lamp 86 to `volt1`, and lamp 87 to
`volt2`, while `sw17_Hit` sets `Volt3.Z`, `sw26_Hit` sets `Volt4.Z`, `sw75_Hit` sets `Volt2.Z`, and
`sw76_Hit` sets `Volt1.Z` -- so lamp 85/switch 17 (`volt3`), lamp 87/switch 75 (`volt2`), and lamp
86/switch 76 (`volt1`) each share one physical "Volt" insert, and lamp 77 (Left In-Lane) shares
`volt4` with switch 26.
