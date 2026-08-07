# Bram Stoker's Dracula — General Illumination

Transcribed from `Dracula_Bram_Stoker_OPS.pdf`, PDF page 120 (printed 3-8, Solenoid/
Flasher Table's GI rows — see `solenoid-flasher-wiring.md` for the full table) and PDF
page 128 (printed 3-16, General Illumination Circuit, theory only, no additional wiring
facts). Cross-checked against the retained known-working script's `GIUpdate2` handler.

| GI addr (public, 0-based) | Manual item | Function | Playfield conn. | Backbox conn. | Cabinet conn. | Bulb |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 01 | Lower Playfield / Insert | J121-1 | J120-1 | — | #555 |
| 1 | 02 | Upper Playfield / Insert | J121-2 | J120-2 | — | #555 |
| 2 | 03 | Center Playfield / Insert | J121-3 | J120-3 | — | #555 |
| 3 | 04 | Insert | — | J120-5 | — | #555 |
| 4 | 05 | Insert | — | J120-6 | J119-3 | #555 |

GI addresses 0-2 are the only strings with a printed Playfield connector. GI addresses 3
and 4 are backbox-only (4 additionally reaches the cabinet), matching the "Cabinet,
Insert" description on the Solenoid/Flasher Location page (`solenoid-flasher-locations.md`).

## Script cross-check (`script.vbs`, `Sub GIUpdate2(no, pwm)`)

```
Case 0 : For each bulb in GIBOT: bulb.State = pwm: Next
Case 1 : For each bulb in GITOP: bulb.State = pwm: Next
Case 2 : For each bulb in GIMID: bulb.State = pwm: Next
Case 3 : gibg4.state = pwm
Case 4 : gibg5.state = pwm
```

This is a clean, zero-conflict match: GI 0/1/2 drive real playfield `Light` collections
(GIBOT 8 members, GITOP 20 members, GIMID 10 members — see `vpx-geometry.txt` for every
member's normalized coordinate), and GI 3/4 drive single non-playfield bulbs, exactly as
the manual's connector columns show. Unlike Williams Tales of the Arabian Nights or Bally
Theatre of Magic, there is no script-vs-manual disagreement over which GI strings are
playfield-wired.
