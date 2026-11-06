# Phantom of the Opera 1.25 runtime bindings

Source: retained embedded script.vbs, SHA-256 e373bf66dab343166e954fb2a7ed9c1ee0d8627ae5e125b13e4339b46757d5f6. TastyWasps, based on 32assassin, DCrosby and Cirque; other credits in the source. Method: direct code reading, project curator, reviewed.

The script declares poto_a32 and loads de.vbs (lines 58-68); HandleMechanics=0 and HandleKeyboard=0 (316-326). Lines 133-157 bind solenoids 1-7 to SetLamp 101-107; 8 to FlashRed4; 9 to FlashRed5; 10 to SolRelayB; 11 to PFGI; 12 to FlashRed3; 13 to FlashRed1; 14 to SolRamp; 15 to FlashRed2; 16 to SolKickback; 25 to bsTrough.SolIn; 26 initially to bsTrough.SolOut then to ballreleasehack; 27 to bsSaucer.SolOut; 28 to VukTopPop; 29 to BotPop; 30/31 to empty callbacks; 32 to a Knocker sound. The callback overwrite at 26 is intentional executable code, so the later handler wins.

Lines 342-351 initialize bsTrough.InitSw 0,13,12,11,10,0,0,0 with three balls and exit BallRelease; bsSaucer.InitSw 0,28,29,0,0,0,0,0 exits sw28 and kicks one ball per command. Drain_Hit adds to the trough; sw28_Hit adds to the two-ball saucer. ballreleasehack suppresses the last trough ball unless the left saucer holds two. It is a table workaround, not a machine's physical interlock.

TopVUK asserts 36 while occupied and output 28 clears it and raises/kicks its ball; BottomVUK does the same for switch 44/output 29 (516-583). The raise timers, DestroyBall/CreateBall transfers, Kick angles/velocities and subway helper Kicker2→Kicker3 are VPX geometry/tuning, not physical device counts.

Direct switch objects are sw14,17-20,25-27,37,45; pulse objects are sw23 spinner, sw30/31 ramp gates, sw33-35/41-43/49-51 targets. Left/right sling events pulse 21/22. Bumper1 pulses 46, Bumper2 pulses 48, Bumper3 pulses 47 (663-670). This nonsequential bumper order agrees with the manual's spatial identities.

The organ initializes its counter at 0, drives switch 53 true and 52 false, and sets rampdown=1/collidable. Output 14 alternates the animation direction on rising calls. At counter >60 it asserts 52, clears 53 and makes RampOrgan noncollidable; below 0 it asserts 53, clears 52 and restores collision (707-746). Thus the comments beside initialization call the endpoints backwards, while executable state agrees with manual 52 Open / 53 Closed. There is no public direction output. A physical reconstruction uses the motor's crank/limit switches, not the script's counter as measured cam geometry.

LampTimer reads ChangedLamps into LampState/FadingLevel, then UpdateLamps uses NfadeL for 1-48 and 57-64, Flash on f49-f55, and no binding for 56. Solenoid pseudolamps 101-107 drive S101a; S102a/b/c; S103a; S104a/b; S105a; S106a/b; S107a/b. NfadeL 53,S108b1 also drives an organ glow from a rear-panel letter lamp address, while the organ animation writes it directly. This is a table-lighting defect; it is not a second physical lamp 53. The active NfadeLm115,S115a has no SetLamp115 callback.

SolRelayB(10) and PFGI(11) both invert the same GI collection (287-304). The manual identifies 10 as the PPB's A/C mux relay and 11 as the GI relay. The extra GI handler at 10 is table behavior, not a second GI control or changed physical wiring.

The five Flupper anchors are Flasherbase1-5; callbacks13/15/12/8/9 drive those anchors respectively. They do not enumerate the physical four-bulb circuits, and their library flare/bloom sprites add no bulbs. The matrix Light objects are insert overlays without shown bulb meshes; off-table L39/L40/L47/L48 and S101a are invisible backbox helpers. Rear-panel f49-f55 are render sprites. They never establish physical bulb coordinates.
