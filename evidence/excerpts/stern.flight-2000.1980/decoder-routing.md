# Flight 2000 decoder and connector routing

Stern Electronics instruction manual, PDF pages 37–42. The unpaginated lamp sheet was also checked against the complete drawing (IPDB paginated schematics PDF page 11). Listed decoder outputs are in numeric order; U3 and U4 draw their last three outputs above output 0. For the momentary solenoid test, the printed I.D. is the Q number. The PinMAME coil address is the selected decoder output plus one.

| Decoder | Outputs 0 through 14, in order |
| --- | --- |
| Momentary coil U2 | Q2, Q1, Q5, Q6, Q7, Q3, Q4, Q8, Q13, Q14, Q9, Q10, Q12, Q11, Q16 |
| Lamp U1 | Q14, Q12, Q13, Q8, Q9, Q10, Q11, Q4, Q1, Q2, Q3, Q7, Q16, Q5, Q6 |
| Lamp U2 | Q29, Q27, Q28, Q35, Q34, Q22, Q26, Q25, Q24, Q17, Q23, Q21, Q15, Q18, Q19 |
| Lamp U3 | Q36, Q38, Q44, Q49, Q48, Q37, Q32, Q20, Q42, Q41, Q40, Q39, Q33, Q30, Q31 |
| Lamp U4 | Q57, Q50, Q51, Q54, Q55, Q60, Q59, Q58, Q56, Q46, Q52, Q53, Q47, Q43, Q45 |

Momentary output 15 has no load on U2 pin 17. On PDF pages 26 and 37–40, PIA PB4/PB5/PB6/PB7 run the right top kicker, coin lockout, flipper enable, and left top kicker respectively. PinMAME publishes these as 17–20. The bottom right sling's Q6 drive is printed G-P in the solenoid list and G-R in the two schematic views. Q18 follows the R-W left kicker circuit on A3J5-3.

The lamp drawing uses some crowded or conflicting connector labels. The following are reads of the artwork, in printed order, using pin:Q notation. The labels follow the drawn nets, separate from the game load list.

| Jack | Printed pin:Q pairs |
| --- | --- |
| J1 | 18:14, 19:12, 17:13, 23:8, 14:9, 15:10, 16:11, 28:4, 24:1, 25:2, 26:3, 27:7, 1:29, 9:27, 8:28, 3:35, 2:34, 0:22, 7:26, 6:25, 5:24, 11:17, 13:20, 4:23, 12:21 |
| J2 | 2:3, 3:7, 22:16, 6:5, 14:6, 8:23, 12:21, 23:15, 20:18, 15:19, 11:33, 6:30, 2:31, 9:40, 1:39, 5:52, 10:47, 7:43, 1:45, 8:53 |
| J3 | 26:36, 25:38, 19:44, 17:49, 16:48, 23:37, 27:32, 21:42, 20:41, 22:40, 24:39, 1:57, 12:50, 15:51, 11:54, 9:55, 3:60, 4:59, 2:58, 10:56, 18:46, 13:52, 16:53 |

Q3 also reaches the J2 Q3 line from J1-26. The load list and matching grey-red wire establish both Shoot Again effects. Q7 also reaches the J2 Q7 line from J1-27. Q40 also feeds J2-9 from J3-22 and Q39 feeds the J2 Q39 line from J3-24. Q52 and Q53 each reach both J2 and J3. The J1-10 load-table route and the drop of the leading 1 before 0 on the Q22 net are consistent with the table's A rollover lamp on public 22. Other disputed connector labels and missing physical sockets remain open where the table and drawings do not settle them.

The playfield schematic (PDF page 37) shows 6 VAC general illumination across A2J1-8 (W) and A2J1-2 (R), with a generic lamp symbol. Cabinet and backbox schematics show the same class of transformer-fed lighting. The schematic does not give per-socket locations or a complete playfield bulb count. The two flipper windings and their normally closed bypass switches are drawn on PDF pages 37–38, independently of the MPU matrix.
