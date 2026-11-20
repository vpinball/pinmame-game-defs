# Starship Troopers — 3-Flipper Circuit Wiring Diagram

Read from `Sega_1997_Starship_Troopers_Manual.pdf` (IPDB 4341), PDF page 106, printed Section 5 page 92, from a 300 dpi
render checked against a Windows OCR pass. The crop `flipper-circuit.webp` renders the page.

Drawing:

- CPU/SOUND BOARD (PARTIAL VIEW), CN6 "DEDICATED SWITCH IN" (pins 1-12): GRY/GRN, GRY/YEL, GRY/ORG, GRY/RED and GRY/BRN.
- GRY/GRN to the N.O. MINI FLIPPER CABINET SWITCH; GRY/ORG to the N.O. RIGHT FLIPPER CABINET SWITCH; GRY/BRN to the
  N.O. LEFT FLIPPER CABINET SWITCH.
- GRY/YEL to the N.C. RIGHT EOS SWITCH; GRY/RED to the N.C. LEFT EOS SWITCH. The page draws no EOS switch for the mini
  flipper.
- All five return on BLK (GROUND) to J16 "POWER OUT" on the I/O POWER DRIVER BOARD (PARTIAL VIEW).
- MOS FET STP20N10L: Q14, Q15 and Q16 to J9 "HIGH CURRENT SOLENOIDS" pins 7, 8 and 9, on BLU/BLK, ORG/GRY and ORG/VIO.
- J10 "VOLTAGE OUTPUTS" pins 1 and 2: RED/YEL, then three branches, each through a "3A SLO-BLO (Located under Playfield)"
  fuse: BLU/YEL to the RIGHT FLIPPER COIL (23-1100) returning on ORG/VIO; GRY/YEL to the LEFT FLIPPER COIL (23-1100)
  returning on ORG/GRY; BLU/YEL to the MINI FLIPPER COIL (22-1080) returning on BLU/BLK. Each coil carries a diode.
- "NOTE: N.C. = Normally Closed, N.O. = Normally Open".

Heading text: "The White Star Board System™ has allowed us to simplify the flipper circuit to the point where we have
eliminated the flipper board all together. The flipper circuit is now configured the same as any other solenoid drive
circuit."

Technical Overview, verbatim: "Our New Flipper System uses one supply voltage (50v DC) for both kick and hold. Once the
Game CPU detects a flipper cabinet switch closure (during game play) it applies a 40 msec pulse to the gate of the
flipper drive transistor (STP20N10L). If it continues to detect a flipper cabinet switch closure (the player holding
the button in) it will continue to pulse the flipper drive transistor 1 msec every 12 msecs for the duration of the
hold cycle. The E.O.S. (End-Of-Stroke) Switch serves the same function as before as it prevents foldback when the
player has the flipper energized to capture balls. The E.O.S. Switch is a normally closed switch which opens
approximately a 1/16" when the flipper is energized. The Game CPU will detect a switch closure if the flipper bat is
forced back by a high velocity shot or rebound on the playfield and will apply another 40 msec pulse of 50v DC to the
coil."
