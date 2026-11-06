# Skateball — upper lamp-driver conductor paths

Source: game #1210 schematic W-1182-28C, PDF 3. The crop retains U1/U2 decoder branches and the connector junctions; inspect the companion full table transcription for all literal output names. Manually checked against the native render by the primary curator. Public numbers below are derived from PinMAME's decoder arithmetic, not printed test numbers.

U1 outputs 0–9/public 1–10 reach J1 pins18,19,17,23,14,15,16,28,24,25. Output10/Q3/public 11 branches to unused playfield J1-26 and fitted backbox J2-21 SHOOT AGAIN. Output11/Q7/public 12 branches to J1-27 RIGHT OUT SPECIAL and unused J2-13. Output12/Q16/public 13 reaches J2-22 BALL IN PLAY;13/Q5/public 14 reaches J2-16 LEFT OUT SPECIAL;14/Q6/public 15 reaches J2-14 BONUS SPECIAL.

U2 outputs 0–9/public 17–26 reach J1 pins1,9,8,3,2,10,7,6,5,11. Output10/Q23/public 27 branches to unused playfield J1-4 and fitted backbox J2-8 MATCH. Output11/Q21/public 28 branches to fitted J1-12 LOWER ROLLOVER BUTTON and unused J2-12. Output12/Q15/public 29 reaches J2-23 HIGH SCORE TO DATE;13/Q18/public 30 reaches J2-20 10K CENTER;14/Q19/public 31 reaches J2-15 20K RIGHT ARROW.

The diagram's solid dots distinguish those shared nets from crossing-only conductors. N/U describes a connector branch, not the entire SCR net. The backbox designation on J2 is the board's harness destination; eight named J2 loads continue to the playfield through the Table B plug.
