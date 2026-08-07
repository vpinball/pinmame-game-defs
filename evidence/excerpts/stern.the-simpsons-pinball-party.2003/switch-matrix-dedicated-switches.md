# The Simpsons Pinball Party — Switch Matrix Grid & Dedicated Switches (wiring)

Transcribed from `The_Simpsons_Manual.pdf`, PDF page 30, printed page 16,
table "SWITCH MATRIX GRID & DEDICATED SWITCHES". Read from a 150 dpi
`pdftoppm` render (`method: mixed` — the manual's OCR text layer was used only
to confirm this is PDF page 30 via its printed-page-number footer; every cell
value below was read from the rendered image, not from `pdftotext`). The
whole 8x8 matrix and all eight dedicated switches are transcribed, not only
the addresses the definition names, so an unused or shaded cell is as visible
as a used one.

Column (drive) wiring: `1` GRN-BRN/CN5-P1/Q1, `2` GRN-RED/CN5-P3/Q2, `3`
GRN-ORG/CN5-P4/Q3, `4` GRN-YEL/CN5-P5/Q4, `5` GRN-BLK/CN5-P6/Q5, `6`
GRN-BLU/CN5-P7/Q6, `7` GRN-VIO/CN5-P8/Q7, `8` GRN-GRY/CN5-P9/Q8.

Row (return) wiring: `1` WHT-BRN/CN7-P9/U400, `2` WHT-RED/CN7-P8/U400, `3`
WHT-ORG/CN7-P7/U400, `4` WHT-YEL/CN7-P6/U400, `5` WHT-GRN/CN7-P5/U401, `6`
WHT-BLU/CN7-P3/U401, `7` WHT-VIO/CN7-P2/U401, `8` WHT-GRY/CN7-P1/U401.

`[DOTS]` marks a cell also marked "Diode On Terminal Strip" — a diode-location
note, not a distinct switch. Cells 27 and 28 are printed shaded gray "NOT
USED"; cells 1 and 8 are also shaded gray, matching the page-31 legend's
"mounted in the cabinet" shading (they are the optional UK-only cabinet-side
buttons), which is a *mounting-location* shade, not an opto shade — this
manual's switch-matrix page carries no opto-shading legend at all (see
`switch-locations-footnotes.md`).

| Row | Col1 (#/loc/name/part) | Col2 | Col3 | Col4 | Col5 | Col6 | Col7 | Col8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 Cabinet Side / LEFT BUTTON (UK ONLY) / 180-5160-00 | 9 Below P/F / COMIC BOOK GUY STANDUP / 515-6027-08 | 17 Below P/F / DROP TARGET #1 (TOP) [DOTS] / 180-5158-00 | 25 Abv. Upr. P/F / UPPER PLAYFIELD EXIT / 180-5190-28 | 33 Blw. Upr. P/F / UPF LIGHT STANDUP / 515-5966-04 | 41 Below P/F / BULLY 3-BANK (TOP) / 515-6027-08 | 49 Below P/F / LEFT BUMPER / 180-5015-03 | 57 Below P/F / LEFT OUTLANE / 500-6227-02 |
| 2 | 2 Coin Door / 4TH COIN SLOT / 180-5204-00 | 10 Below P/F / 5-BALL TROUGH #1 (LEFT) / 180-5119-02 | 18 Below P/F / DROP TARGET #2 (MID) [DOTS] / 180-5158-00 | 26 Blw. Upr. P/F / GARAGE RAMP ENTER / 180-5190-28 | 34 Blw. Upr. P/F / UPF LOCK STANDUP / 515-5966-04 | 42 Below P/F / BULLY 3-BANK (MID) / 515-6027-08 | 50 Below P/F / RIGHT BUMPER / 180-5015-03 | 58 Below P/F / LEFT RETURN LANE / 500-6227-02 |
| 3 | 3 Coin Door / 6TH COIN SLOT / Future Use | 11 Below P/F / 5-BALL TROUGH #2 / 180-5119-02 | 19 Below P/F / DROP TARGET #3 (BOT) [DOTS] / 180-5158-00 | 27 (gray) NOT USED | 35 Blw. Upr. P/F / UPF TOP STANDUP / 515-5966-02 | 43 Below P/F / BULLY 3-BANK (BOT) / 515-6027-08 | 51 Below P/F / BOTTOM BUMPER / 180-5015-03 | 59 Below P/F / LEFT SLINGSHOT / 180-5054-00 (x2) |
| 4 | 4 Coin Door / RIGHT COIN SLOT / 180-5204-00 | 12 Below P/F / 5-BALL TROUGH #3 / 180-5119-02 | 20 Below P/F / ITCHY & SCRATCHY SAUCER [DOTS] / 180-5116-01 | 28 (gray) NOT USED | 36 Abv. Upr. P/F / COUCH ENTER / 180-5190-28 | 44 Above P/F / UP RIGHT SAUCER BACKUP / 180-5119-02 | 52 Below P/F / POP SIDE STANDUP / 515-6027-08 | 60 Below P/F / RIGHT OUTLANE / 500-6227-02 |
| 5 | 5 Coin Door / CENTER COIN SLOT / DBA / 180-5204-00 | 13 Below P/F / 5-BALL TROUGH #4 / 180-5119-02 | 21 Above P/F / SPINNER / 180-5010-04 | 29 Below P/F / KWIK-E-MART LOOP / 500-6227-02 | 37 Blw. Upr. P/F / TV LOCKUP / 500-6227-02 | 45 Above P/F / RIGHT RAMP ENTER / 180-5190-28 | 53 In Cabinet / TOURNAMENT BUTTON / 180-5174-00 | 61 Below P/F / RIGHT RETURN LANE / 500-6227-02 |
| 6 | 6 Coin Door / LEFT COIN SLOT / 180-5204-00 | 14 Below P/F / 5-BALL TROUGH VUK OPTO / See Sw.14 Note | 22 Below P/F / BART SKATEBOARD TOP / 180-5190-48 | 30 Below P/F / KWIK-E-MART STANDUP / 500-6227-02 | 38 Abv. Upr P/F / COUCH LOCK (BOT) / 180-5119-02 | 46 Above P/F / RIGHT RAMP MADE / 180-5190-28 | 54 In Cabinet / START BUTTON / 180-5174-00 | 62 Below P/F / RIGHT SLINGSHOT / 180-5054-00 (x2) |
| 7 | 7 Coin Door / 5TH COIN SLOT / Future Use | 15 Below P/F / 5-BALL STACKING OPTO / See Sw.15 Note | 23 Below P/F / BART SKATEBOARD / 180-5190-48 | 31 Below P/F / ADV. POPS STANDUP / 500-6227-02 | 39 Abv. Upr. P/F / COUCH LOCK (MID) / 180-5119-02 | 47 Above P/F / LEFT RAMP ENTER / 180-5190-28 | 55 Below P/F / UPPER LEFT VUK / 180-5116-01 | 63 Below P/F / LEFT ORBIT / 500-6227-02 |
| 8 | 8 Cabinet Side / RIGHT BUTTON (UK ONLY) / 180-5160-00 | 16 Below P/F / SHOOTER LANE / 180-5157-00 | 24 Below P/F / UPPER RIGHT SAUCER / 180-5186-00 | 32 Below P/F / LIGHT OTTO STANDUP / 500-6227-02 | 40 Abv. Upr. P/F / COUCH LOCK (TOP) / 180-5119-02 | 48 Below P/F / GARAGE DOOR / 500-6138-01R | 56 In Cabinet / PLUMB BOB TILT / See Sw.56 Note | 64 Below P/F / RIGHT ORBIT / 500-6227-02 |

## Dedicated switches (`GROUND IC U206 INPUTS`, ground BLK CN6-P1/-P11)

| DS | Wire | Connector | Location | Description | Part |
| --- | --- | --- | --- | --- | --- |
| DS-1 | GRY-BRN | CN6-P2 | on Cabinet Side | #1 LEFT FLIPPER BUTTON | 180-5160-00 |
| DS-2 | GRY-RED | CN6-P3 | Below Playfield | #2 LEFT FLIPPER E.O.S (End-of-Stroke) | 180-5149-00 on Flipper |
| DS-3 | GRY-ORG | CN6-P4 | on Cabinet Side | #3 RIGHT FLIPPER BUTTON | 180-5164-00 Doubled |
| DS-4 | GRY-YEL | CN6-P6 | Below Playfield | #4 RIGHT FLIPPER E.O.S. (End-of-Stroke) | 180-5149-00 on Flipper |
| DS-5 | GRY-GRN | CN6-P7 | on Cabinet Side | #5 UPPER RT. FLIPPER BUTTON | 180-5164-00 Doubled |
| DS-6 | GRY-BLU | CN6-P8 | on Coin Door | #6 VOLUME (RED BUTTON) — In Test: LEFT | 180-5192-02 |
| DS-7 | GRY-VIO | CN6-P9 | on Coin Door | #7 SERV. CRED. (GREEN BUTTON) — In Test: RIGHT | 180-5192-04 |
| DS-8 | GRY-BLK | CN6-P10 | on Coin Door | #8 BEGIN TEST (BLACK BUTTON) — In Test: ENTER | 180-5192-00 |
