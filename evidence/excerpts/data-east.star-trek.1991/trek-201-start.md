# Production 2.01 start and ball serve

Pinned LibPinMAME build 46e1a01a, library SHA-256 `8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5`, authorized local `trek_201.zip` SHA-256 `1da4b5e8f9136b8ee03c780429808cb364bd054c0e3ba0fd6a60304ffd24cc67`. One successful run from a fresh state directory, binary outputs, keyboard and driver mechanics disabled. The committed scenario drives the sensor transitions (11–13 initially closed and 31 set to the crew-visible endpoint). It does not observe a physical ball or motor.

| Scenario step | Stimulus | Selected public solenoid transitions in that step |
| --- | --- | --- |
| 4 | Start with trough occupied | 2 rises and falls twice, 11/16/23 rise |
| 7 | Launch button 30 with shooter switch 14 closed | 3 rises and falls |
| 9 | Close outhole switch 10 after leaving the shooter | 1 rises, falls and rises again before the observation window ends |

Across steps 4–9, the observed state sequences on 37/38/39 match 51/52/53 respectively whenever those lines change. This corroborates the chase-output mirrors in PinMAME's `trek_getSol`. The display callback for index 0 reports 128 × 16. These are selections from the retained raw trace and do not establish that unobserved outputs were unused.
