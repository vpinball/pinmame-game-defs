# Reconciled lamp functions

The complete factory lamp list prints the named function and harness connection. The board diagram determines which SCR PinMAME addresses. The exact VPX artwork and script establish the placement and binding of the observed insert effects. The stock gameplay trace independently exercises several of the disputed addresses.

| Public address and SCR | Function | Evidence and wiring limit |
| --- | --- | --- |
| 29, Q15 | Special at Spot BLAST | The board routes Q15 to the branch labeled J2-23. The load list's Special Lane Top uses J2-30. The playfield artwork and `Lights(29)` place the effect next to Spot BLAST. Exact harness wire and pin remain open. |
| 37, Q48 | O outer return insert | VPX `Lights(37)` is in the right outer lane and the ROM extinguishes 37 on O switch 22. The load list labels it a top rollover at J3-16. The board prints a second J3-16. |
| 44, Q39 and 46, Q30 | Upper and center Second Stage Go | VPX `Lights(44)` and `Lights(46)` drive the two separate inserts. In the stock probe, 46 lights on the second capture at step 16 and 44 lights on countdown qualification at step 40. The list repeats J2-5 on both rows. |
| 53, Q55 and 55, Q59 | Upper T rollover and corner T | VPX `Lights(53)` and `Lights(55)` are separate. Step 28 hits upper T switch 21 and turns 53 off and 55 on. The chart repeats J3-4. |
| 59, Q52 | Right spinner 1,500 | `Lights(59)` is at the labeled spinner insert. J3-13 has its own named black-wire load in the factory chart and the same SCR on the schematic. The schematic's J2-5 branch remains uncertain. |
| 60, Q53 and 62, Q43 | Upper and center First Stage Go | VPX `Lights(60)` and `Lights(62)` drive separate inserts. In the stock probe, 62 lights on the first capture at step 8 and 60 lights on countdown qualification at step 40. The list repeats J2-7 on both rows. |
| 63, Q45 | Match | The factory chart identifies a backbox Match at J2-1 and the script comments agree. A second stray J2-1 designation appears on Q39's branch. |

## Unfitted lamp output Q31

U3 output S14 drives the physical SCR Q31, so PinMAME publishes it at `2 × 16 + 14 + 1 = 47`. The board drawing appears to print J2-2 on both Q31 and Q3. The factory load list puts Q3's backbox Shoot Again at J2-21, alongside its playfield counterpart at J1-26. Inkochnito's chart gives Q31 as A5J2-2 with blank load and wire-color cells. The exact Q31 pin remains a wiring-detail uncertainty.

The 60 named factory load rows can be matched to functions on the other outputs by combining the load roster, decoder routes, insert artwork, exact VPX bindings and the stock observations above. This crosswalk includes duplicated or uncertain printed pins, including those for the stage and T effects and Q15. The factory roster leaves Q31 without a named load, the chart leaves its load cells blank, and the exact VPX leaves its public 47 binding commented out. Together these support the unfitted disposition. [Factory lamp list](lamp-wiring.md) · [Decoder and board routes](decoder-routing.md) · [VPX contract](vpx-contract.md) · [Inkochnito controlled-lamp chart](https://www.pinballrebel.com/pinball/cards/Tech_Charts/Stern_Flight-2000_Tech_Chart.pdf)

The wire-side specimen photos corroborate the general J2 harness population. Listing 223109 shows the plug on a Stern LDA-100 with the upper pin 23 marked. The lower-end enlargement leaves the individual cavities indistinct. Listing 194559 shows the harness on a replacement board, with insufficient legible markings to number the cavities independently. Pin 2 remains unverified by photography. [Original-board specimen, photo 7](https://pinside.com/pinball/market/classifieds/ad/223109) · [Second specimen, photo 23](https://pinside.com/pinball/market/classifieds/archive/194559)

The retained `flight2k` trace shows repeated rising edges on public 47 during service edges 1 and 2, the burn-in and lamp test. These tests explain the observed pulses at the unfitted output, whose canonical availability is `unused`. [Service trace summary](../../runtime/stern/flight-2000-service.json)

The wiring uncertainties above do not make the listed lamp effects unknown. The remaining positions are tracked separately. A rendered `Light` center is an insert aperture candidate unless a suitable photograph, drawing or modeled bulb establishes the actual socket center. [Factory lamp list](lamp-wiring.md) · [Decoder and board routes](decoder-routing.md) · [Exact VPX contract](vpx-contract.md)
