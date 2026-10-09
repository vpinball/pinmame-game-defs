# Jack*Bot — Service Bulletin 86

Text of `Williams_1995_Jack_Bot_Service_Bulletin_86.pdf` (SHA-256 `9fe7a8314e8de55585893743b80087b351c4cc80e62aa8431676d517512381e0`; a one-page Acrobat Web Capture of the bulletin, dated January 11, 1996, retrieved from the Wayback copy of the IPDB file), extracted by the curator from the PDF text layer with `pdftotext -layout` and reproduced as extracted, then checked against a render of the page. The drawing labels of Figures A and B are not part of the text layer and were read from the rendered page.

## Page 1

```
Service Bulletin: SB 86
DATE: January 11, 1996
GAMES: Jack*Bot and Congo sample games manufactured before 12-15-95
SUBJECT: Premature loss of battery voltage on the WPC-95 CPU Board
The CPU boards affected have the bare board part number of 5764-14533-08 (screened on back side of
board). The circuit boards should have been modified in house, but in case any were missed, follow the
modification procedure below.
* Cut trace on the component side of the PCB as shown in Figure A. Tack solder the cathode of a 1N5817
1.0A diode (D28 on drawing and later board revisions) to U21 pin 2 as shown. Solder a short piece of
insulated wire from the anode end of D28 to the feedthrough hole near U12 pin 20 as shown in Figure A.
* Solder a 22K ohm 5% 1/4W resistor (R129 on drawing and later board revisions) to the feedthrough holes
in the PCB near U18 as shown in Figure B.
* Verify that R91 is a 22M ohm 5% 1/4W resistor.

Thank you,
WMS GAMES Parts & Service INC.
```

In the rendered page the word `near` is set in italic in both places it appears.

Drawing labels as printed (the drawings are not reproduced):

```
Figure A: C63, D28, U21, R91, C54, U12; callouts "Cut Here" and "Wire Jumper"
Figure B: U18, R129, C64
```
