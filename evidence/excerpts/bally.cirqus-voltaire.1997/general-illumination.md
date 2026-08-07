# Cirqus Voltaire — General Illumination

This excerpt collects the General Illumination facts already transcribed in full in
`solenoid-flasher-table.md` (PDF page 156, printed 2-50, the primary wiring source with connector
numbers) and `solenoid-flashlamp-locations.md` (PDF page 152, printed 2-46, the locations list with
reversed Backbox 1/2 labels and no connector data). This file is the GI-scoped pointer the curator's
source record cites; see those two files for the full transcription and connector detail.

Summary: five public GI addresses 0-4 (printed 01-05). Addresses 0-2 (Playfield Right/Middle/Left)
are `#44` playfield strings on connectors J105-1/2/3, driven by Q5/Q4/Q3. Addresses 3-4 are `#555`
backbox strings (Backbox 2 / Backbox 1 per the wiring table's own connector order, J106-5/J106-6, Q2/
Q1) marked "**do not brighten and dim, they are always on**"; address 4 additionally reaches a
cabinet connector (J104-1/J104-3).

The retained VPW script's `UpdateGI(no, step)` (`extracted-vpxtool/script.vbs`) dispatches only
`Case 0`, `Case 1`, `Case 2` -- driving the `Gi_Pf_Right_01` / `Gi_Pf_Middle_02` / `Gi_Pf_Left_03`
emitter collections (11, 9, and 11 `Light` objects respectively, once each collection's own large
overlay-shape helper -- `GIRight`/`GiCenter`/`GILeft`, `Flasher`-type with no discrete center -- is
excluded) and toggling the `Ringmaster_on`/`Ringmaster_off` texture on GI address 1. No `Case 3`/`Case
4` exists, matching the manual's own "always on" / backbox-only classification for those two
addresses: they take a controlled `cabinet_or_service` spatial record rather than an invented
playfield coordinate.
