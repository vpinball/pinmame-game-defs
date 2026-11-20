# Data East Star Trek: service bulletins 31–35

Factual extracts from the five separately retained factory bulletins. PDF and
printed page numbers coincide. Windows.Media.Ocr en-US was run on all 17
rendered pages; the statements and troubleshooting table below were checked
against the page images. This is a selective paraphrase, not a transcription
of the full bulletins. The spelling of headings and table cells in the SB33
table is normalized for case and obvious typographic errors.

## SB31, 6 December 1991, PDF 1

The enclosed game program is version 1.17 and the display program is 1.09;
the bulletin says to use the ROMs as a pair. It describes fixes for tech-alert
bugs and an intermittent failure to launch the ball, periodic display resets
to recover synchronization with the CPU, and a RESTART GAME adjustment to
prevent accidental restarts before the last ball. It recommends updating all
Star Trek games; that recommendation is not evidence a particular game was
updated.

## SB32, 17 December 1991, PDF 1

For an up/down ramp that does not always return down, check that the Ramp Up
switch is closed when the ramp is up. If that switch works, check the coil
bobbin screw on the latching mechanism. A limited number of games lacked
Loctite on this screw; the bulletin recommends tightening and applying it at
the next service. Its drawing points to the bobbin screw. It does not identify
which individual machines were corrected.

## SB33, 18 December 1991, PDF 1–13 (reprint)

### Optical principle and assembly

PDF 2: the fixed artwork interleaves vertical slices of two pictures: the
transport team in the room and the empty room. A grid sheet over the artwork
has black stripes separated by clear areas. Moving the grid side to side hides
one picture and reveals the other; total side-to-side travel is approximately
0.040 inch. The diagram shows the transition between the two images.

PDF 3–9: a motor assembly attaches to the rear of the insert. A limit switch
assembly has two switch actuators with the cam pin between them. Fixed artwork
and grid sheets are mounted on separate plates; the grid assembly sits over
the fixed artwork and slides in top and bottom guide brackets. Two springs
connect grid-sheet holes to fixed screws to the right of the assembly; the cam
surface is lubricated. Top-guide spacing uses 0.020-inch shims at both grid
corners, removed after the guide is secured. Shipping blocks hold the grid for
shipping; these are not operational components. These views are assembly
views, not playfield coordinates.

### Complete troubleshooting table, PDF 10

| Problem | Cause | Solution |
| --- | --- | --- |
| Picture does not change | Motor not running | Check electrical connections and power. |
| Picture does not change | Grid plate does not move side to side | Slightly loosen the three top guide plate screws; ensure the grid plate moves friction-free. Clean both plates, apply talc, reassemble and adjust. |
| Picture very faint at rest but improves during change | Switch actuation is either too late or too early | Reset actuation points of switches. |
| Black lines run diagonally through picture | Fixed artwork misaligned to grid plate | Loosen the three fixed artwork screws and realign fixed artwork to grid sheet. |
| Black lines run diagonally through picture | Grid plate too loose up and down | Loosen the three top guide plate screws, move guide plate down slightly, retighten and check smooth side-to-side operation; realignment of fixed artwork may be necessary. |

### Adjustment and limit behavior, PDF 11–13

With springs unhooked, the grid plate should slide side to side without
apparent friction. In transporter motor pulse diagnostics, pulse the motor
until the cam pin actuates the top switch; actuation should occur within the
top 15 degrees of rotation. Adjust fixed artwork so the entire transport team
is sharply visible, viewing the unit straight on. Cycle the motor half a turn:
the team disappears; adjust the bottom switch to just make at that point.
Cycling to the top switch stops the motor with the team visible; cycling to
the bottom switch stops it with the team completely absent. Repeat cycles to
check switch settings. This describes the physical adjustment, not a proven
PinMAME switch address or startup state.

## SB34, 6 February 1992, PDF 1

The chase light assembly is secured to the ramp by tie wraps and contains
individual bulbs inside tubes. On some assemblies excessive bulb-lead length,
vibration, and overly snug tie wraps can twist leads and short the 12 V DC
supply to the chase-light PCB. A failed PCB driver can load the 12 V line,
causing momentary blackout and/or power-supply F1 and F2 7 A slow-blow fuse
failure. The vendor added plastic insulation to internal enamel-coated magnet
wires. Data East says this modification was implemented on the last several
hundred Star Trek games and that replacement boards and assemblies would be
distributed. This neither establishes the count of bulbs nor proves earlier
games were retrofitted.

## SB35, 16 April 1992, PDF 1

The bulletin describes intermittent freeze-ups caused either by the CPU waiting
for a lost/busy display or by certain switch timing during ball search. It
also describes knocker or shooter-lane Turbo Boost kicker activation instead
of flash lamps when normally closed 50 V contacts of the PPB left/right relay
become pitted and stick. Its prescribed update replaces CPU ROM C5 with 2.00;
display 1.09 is enclosed for recipients who missed the December mailing. The
new CPU program resets a display busy too long, continues even when resets do
not wake it, improves switch timing in ball search, and modifies left/right
relay control to reduce arcing. The bulletin does not establish which machines
received the update or the specific behavior of untested ROM variants.
