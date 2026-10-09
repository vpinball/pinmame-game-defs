# Black Hole — Auxiliary lamp driver board, light box and four-digit display (printed pages 34, 35 and 38)

Source: the Scribd copy of the Gottlieb *Black Hole Instruction Manual* (document 223467608), viewer pages 36, 37 and
40 (printed pages 34, 35 and 38). Read from the page images. Page 35 is a fold-out scanned at letter width: only its
left part survives in this copy, so the light box's lamp list beyond "NAME AND SCENE LAMPS" and its title block are not
legible.

## Auxiliary lamp driver board (A11), page 34

Drawing E-21338 "AUX. LAMP DRIVER BOARD (1A11), SYSTEM 80, GAME #668", dated 7-22-81. A1P1 "FROM LIGHTBOX 1A11J1": pin
1 "(NOT USED)", pin 4 +5V DC, pin 2 ground. An LM555M timer (U5) clocks an SN7490N decade counter (U3) through an
SN7400N (U1); an SN7442N decoder (U4) drives ten MPS-U45 transistors Q1-Q10 through SN7405N inverters (U2, U6). The
outputs leave on A11P2 / A11J2 pins 1-10 and A10J9 / A10P9 pins 2-11 (wires 600, 611, 622, 633, 644, 655, 666, 677,
700, 711) to lamps numbered 1-28 drawn around a "LIGHTBOX LAMP IDENTIFICATION FRONT VIEW" frame (lamps 1-10 on the
first column of drivers, 11-19 and 20-28 in parallel rows); A10J8-1 (wire 322) brings "+6VDC". Notes: "1. ALL
TRANSISTORS ARE MPS-U45. 2. ALL RESISTORS ARE ±5%, 1/4W. 3. ALL STROBED LAMPS ARE #44."

## Light box, page 35 (left part only)

A1J2 (from A1 control board) carries segment lines a-h for three digit groups A, B, C (wires 300-377, 600-677,
800-877, group C through A10P5/A10J5), and A1J3 the digit strobes D1-D16 (wires 400-455, 466-733, and 744-777 through
A10P5/A10J5). They feed "1A4J1 TO A4 SCORE DISPLAY", "2A4J1 TO A4 SCORE DISPLAY" and "3A4..." (cut off), each with
segments a-h, digits D1-D6 or D7-D12, 5V AC, 5V AC RET., +60V DC and GND. A2J3 from the A2 power supply brings +60V DC
(044), +42V DC (055) and +5V DC (688). A12P4 from the transformer panel brings 5V AC (122), 5V AC RET. (144), 3V AC (155)
and 3V AC RET. (177) through A10J3/A10P3, "[077] 6.3V AC" and "[000] 6.3V AC RET." to "NAME AND SCENE LAMPS (50)",
"[322] +6V DC (SOURCE)" and "[555] SOUND 16". The lamp lines that page 26 sends to the light box on A3J2 are not legible
in this copy.

## Four-digit display (A5), page 38

Drawing E-20927 "4-DIGIT DISPLAY (A5), SYSTEM 80", dated 2-27-81. A5J1 pins 7-14 carry segments a-h to a UDN6118A
segment driver (Z2) and an SN7432N OR gate (Z1); pins 2, 3, 5 and 6 carry digit strobes D16, D15, D14 and D13 to a
second UDN6118A (Z3). The tube DS1 is a "4-LT-11 (FUTABA)" showing two pairs of digits ("88 88"); note "SIMILAR
SEGMENTS OF EACH DIGIT ARE INTERNALLY WIRED IN PARALLEL." Parts list: C1 1 mfd 100V; C2, C3 .01 mfd; DS1 4-Digit Display
Tube—FUTABA 4-LT-11; Z1 SN7432N; Z2, Z3 UDN6118A.
