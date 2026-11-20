# Stern motor specification table

Stern Pinball, *CSI* manual, PDF page 69, Appendix F: 1, [original PDF](https://www.sternpinball.com/wp-content/uploads/2018/11/CSIManual.pdf), SHA-256 `bf918873d582f4fbd152db777b8ecef66c77692a88e6ddaf3ce99409e396055e`. Acquired 2026-11-20T10:27:59Z; retained as `review-artifacts/data-east-star-trek-1991/followup/stern-csi-motor-specs.pdf`. Complete page table transcribed from the PDF text and visually checked against the rendered page. Line breaks are flattened and merged game-name cells repeated; fractional values are rendered with `½`.

The printed introduction says the table lists games that used motors, and part numbers beginning `515-` include wiring harness and connector.

| Game Name | Function | Specifications | Part Nº |
|---|---|---|---|
| ABC Monday Night Football | Goal Post Up/Down Movement | Motor 24v A.C. 60 RPM CW | 515-5222-00 |
| Phantom of the Opera | Organ Up/Down Movement | Bowman Motor 24v 60Hz 3W 11 RPM CCW | 515-5256-00 |
| Checkpoint | Mag Wheel (in Backbox) | Motor D.C. (KEN) | 041-5005-00 |
| Checkpoint | Shaker | Johnson Motor (Vibrator) | 041-5002-00 |
| Teenage Mutant Ninja Turtles | Spinning Pizza Ball Deflector | Gear Motor 24v A.C. 325 RPM CW | 515-5397-00 |
| Batman | Bar Target Up/Down Movement | Bowman Motor 24v 60Hz 3W 11 RPM CCW | 515-5256-00 |
| Star Trek 25th Anniversary | Swinging Target | Bowman Motor 24v 22½ RPM | 515-5534-00 |
| Star Trek 25th Anniversary | Transporter F/X | Gear Motor 24v A.C. 3½ RPM | 500-5421-00 |
| Star Trek 25th Anniversary | Cooling Fan (for Transporter F/X) | 4½" Motor 12v | 041-5014-00 |
| Lethal Weapon 3 | Spinning Light | Motor 2½ v A.C. 4000 RPM CCW | 041-5017-00 |
| Star Wars | Bar Target Up/Down Movement | Bowman Motor 24v 60hz 3W 11 RPM CCW | 515-5256-00 |
| Star Wars | R2D2 Robot Left/Right Movement | Bowman Motor 24v A.C. 22½ RPM CW | 515-5571-00 |
| Star Wars | Death Star Rotation | Bowman "G" Motor 24v A.C. 60Hz 6 RPM CW | 515-5570-00 |
| Rocky & Bullwinkle & Friends | Nell Log "Cutting Blade" Forward/Back Movement | Autotrol Model E Motor 24v 60hz 4W 3 RPM CCW | 041-5023-00 |
| Jurassic Park | T-Rex Left/Right Movement | Multi Motor 5v D.C. | 041-5025-00 |
| Jurassic Park | T-Rex Up/Down Movement | Bowman Motor 24v 11 RPM CW | 041-5026-00 |
| Jurassic Park | Shaker | Johnson Motor (Vibrator) | 041-5002-00 |
| Last Action Hero | Crane Left/Right Movement | Multi Products Motor 12v D.C. #3312 OSC | 041-5027-00 |
| Last Action Hero | Shaker | Johnson Motor (Vibrator) 10.5v D.C. 10 AMP 2950 RPM CW | 041-5029-00 |
| Tales from the Crypt | Tombstone Up/Down Movement | Bowman Motor 24v A.C. 6 RPM CCW | 515-5900-00 |
| Tales from the Crypt | Shaker | Johnson Motor (Vibrator) 10.5v D.C. 10 AMP 2950 RPM CW | 041-5029-00 |
| The Who’s Tommy | Mirror Up/Down Movement | Bowman Motor 24v A.C. 6 RPM CCW | 515-5900-00 |
| The Who’s Tommy | Flipper Blinders | Servo Motor (94102) | 041-5032-00 |
| The Who’s Tommy | Spinning Airplane Propellers | Motor D.C. | 041-5033-00 |
| WWF Royal Rumble | Shaker | Johnson Motor (Vibrator) 10.5v D.C. 10 AMP 2950 RPM CW | 041-5029-00 |
| Maverick, The Movie | Turning Paddle Wheel | Motor 24v A.C. 10 RPM | 041-5036-00 |
| Mary Shelley’s Frankenstein | Creature Head Left/Right Movement | Servo Motor (94102) | 041-5032-00 |
| Batman Forever | Cannon Left/Right Movement | Bowman Motor 24v A.C. 60Hz 3W 6 RPM CCW | 515-6383-00 |

The Swinging Target row matches part `515-5534-00` in the Data East wiring schematic. The listed 22½ RPM corresponds to about 2.67 seconds per shaft revolution at that nominal rate. The physical target sweep and timing under load remain unmeasured.

The Transporter F/X row lists the 24 VAC, 3½ RPM specification under `500-5421-00`. Data East's Star Trek wiring schematic (printed p. 29) identifies the Special Effects Motor as `515-5532-00-14` and shows its 28 VAC supply. The documents give no cross-reference between these part numbers. The speed of the motor drawn in the Star Trek schematic remains unverified. [Data East wiring excerpt](solenoid-wiring.md)
