Source: `Stern_1979_Meteor_Manual.pdf` (IPDB machine 1580, 40 pages, 300 dpi one-bit scans without a text layer), PDF pages 30-31: the MPU 200 schematic. Transcribed from 250-600 dpi renders; only the title block and the S33 circuit at the MPU's NMI input were read.

# Meteor (Stern 1979) - MPU 200 schematic (PDF pages 30-31)

Title block (PDF page 31): "STERN ELECTRONICS INC. 1725 DIVERSEY BLVD. CHICAGO 60614", "MPU 200 SCHEMATIC", "FOR SOLID STATE", "DRN." (initials), "DATE 8-21-79"; drawing number "NO. 12B-602-S" (top right of page 31 and bottom left of page 30). A standard board drawing, not lettered for this game.

## S33 and the NMI input (PDF page 30, upper centre, left of the MPU)

| Item | As drawn |
| --- | --- |
| S33 | A pushbutton symbol (a bar over two open terminals) labelled "S33". Its left terminal goes to a ground symbol; its right terminal goes to the node below. |
| Node | Joins S33, R11 and C87, and runs right to the MPU's NMI input. |
| R11 | "R11 1.2KΩ" from the node up to "+5V". |
| C87 | "C87 .01MFD 100V" from the node down to a ground symbol. |
| U9 | "U9 6800 MPU"; the line from the node enters pin "6", labelled "NMI" with an overbar and an inversion bubble. Neighbouring pins: "8" VCC above, "7" "BA" below. |
| Junction | A junction dot on the line between C87 and pin 6 joins a vertical line that leaves the region upwards; where it ends was not traced. |

## Uncertain readings

- The label "S33" is faint ("S3?" on the coarser renders); the 600 dpi render reads "S33", and Figure 1 (PDF page 3) labels the MPU pushbutton "S33".
- R11's value reads "1.2KΩ" with the decimal point printed as a comma-like mark.
- The pin number at NMI reads "6"; the pin numbers at VCC and BA read "8" and "7".
