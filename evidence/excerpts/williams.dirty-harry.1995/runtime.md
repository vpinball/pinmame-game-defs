# Retained runtime evidence

All runs use authorized LX-2 bytes, newly isolated state, the pinned native library, keyboard off and HandleMechanics0. Host switch readback is stimulus. This ledger records actual transitions and frame hashes, not inferred physical quantities or socket positions.

## dh-switch-edges
- Raw trace SHA256: `293bef61b7017edad07f72aa2211a46295e0000215dfa85dc3b5f9b8be67a307`
- Scenario SHA256: `69c1d3aea0fb77547337dd69d2b022cd4828e2f3e669c063abca25cb113dfcee`; native library SHA256: `2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`
- Observed nonzero solenoids: [6, 9, 10, 11, 12, 13, 20, 29, 31, 33, 34, 45, 46, 47, 48]

## dh-solenoid-test
- Raw trace SHA256: `11477dc40e060f8f4595f3fba1ec71d3a135856cdddaa6ba3ac9488a7b59f0e0`
- Scenario SHA256: `bcb8ce72bfa969c597cfcc50ae2387808a3a393faff46f83cc8465824ba92e43`; native library SHA256: `2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`
- Observed nonzero solenoids: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 25, 26, 27, 28, 29, 31, 35, 36]

## dh-flasher-test
- Raw trace SHA256: `bbfd060913cbc16666b9ebd6f9758ed12c07cc743eab4c598b943eb1352b0929`
- Scenario SHA256: `40dae00f5b77b80c77c09363aa73126411f68ae6a172796b36880551613e801c`; native library SHA256: `2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`
- Observed nonzero solenoids: [6, 17, 18, 19, 20, 21, 22, 23, 24, 29, 31]

## dh-gun-explore
- Raw trace SHA256: `9acd9d4aa120680743eaea78622b2752cec46db71d7e1b0afb82a8b3f59baeea`
- Scenario SHA256: `304764edf1b0eacb0f0fa29b1c26a2c3d4a214c6382a66a6f64d07650926ce00`; native library SHA256: `2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`
- Observed nonzero solenoids: [3, 6, 20, 29, 31]

## dh-mechanisms
- Raw trace SHA256: `cc801bc4d25bb62771fe033d191067c1760098672cb526008710114efbd1231d`
- Scenario SHA256: `e85ca9bbf3d40772f1c0269b670f059b64218c712016456b3a0fcc03c703882b`; native library SHA256: `2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`
- Observed nonzero solenoids: [1, 2, 3, 5, 6, 8, 16, 20, 29, 31, 35]

## dh-lighting-flippers
- Raw trace SHA256: `a6281c28da0c8b6bbd415a28fb37529500242119a0fd89fac80787ae3bd93130`
- Scenario SHA256: `035864cdd41565bc9cc1ef05c3876f233181181703f1bf4e1d226a7d5cd980e6`; native library SHA256: `2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`
- Observed nonzero solenoids: [6, 20, 29, 31, 33, 34, 46, 47, 48]

## dh-gun-feedback
- Raw trace SHA256: `773fe18d3d1cb720e49430a0f66d281908901d4e038a563f28a2623632541d99`
- Scenario SHA256: `558405fb6e09815ffd79057d3350d50b0c7641ce6ae7e698f76f68018c28b30b`; native library SHA256: `2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`
- Observed nonzero solenoids: [6, 20, 29, 31]

## dh-gun-static
- Raw trace SHA256: `ae7a27ff35c42939a65d6537956c333690da22e220940953119e896c32b338a0`
- Scenario SHA256: `34366716f9fd0e84556db809000f3425c463998606f4a1d15a7f272bff094c6c`; native library SHA256: `2011243e8d2747cbeac5e42262c271bbdd6a467605acd5edf13dbeeefcbc3591`
- Observed nonzero solenoids: [6, 20, 29, 31]

## Primary visual readings and scope

- T.1 top line names fitted matrix contacts at public1 and clears at0;24 is named on release.111/113/115 are synthesized EOS,117 remains unnamed,112/114/116/118 fire lower-right/lower-left/upper-right/lower-left respectively. The whole92-address sweep is retained,including unpopulated PIC columns.
- T.4 step order includes1-16,20,25-28,35,36. It names6 DROP TARGET DOWN,25 DROP RESET and36 LEFT LOOP GATE while pulsing those outputs. Positive amendment evidence establishes their production non-fitment.
- T.5 names17 HEADQUARTERS,18 SAFEHOUSE,19 WAREHOUSE,21 GUN LOADED,22 RIGHT RAMP,23 RIGHT BACK,24 LEFT BACK,then wraps. Names were read from retained frames,not inferred from the callbacks.
- T.17 position box follows76; Up starts20,Down stops20; ball44 fires3. With76held0,20 remained active after22seconds and stopped onEscape. The manual's approximate20second stop is therefore retained as a physical-test instruction,not asserted as an unconditional LX-2 timer.
- T.16 host42closure fires35. T.18 trigger11fires1/8/16; shooter15closure fires2; popper45closure fires5; chamber44closure fires3. Host77was presented as mini-trough feedback; no motor-to77 causal assertion is made.
- T.12 separately exercises the six fitted power/hold circuit selections; public33/45/47 aggregate their paired bits. T.6 changes all five GI channels through intensity levels. T.8 walks the lamp matrix. Those tests establish callback behavior,not bulb fitment.

## Gun timeout feedback comparison

Two fresh runs each started from a different position-switch level. In the periodic run the host presented30candidate marks (0.25second closed/0.75second open); the static run held76closed45seconds. Both motor20on intervals were approximately24.600elapsed harnessseconds and stopped withoutEscape. The earlier22second static-open observation was below this measured limit. These synthetic patterns support a ROM elapsed timeout independent of the tested marker pattern; they do not measure the physical cam,gun speed or mains timing. The manual calls its stop about20seconds.

## Complete directory retention

The canonical manifests cover raw JSON, every retained frame and isolated emulator state, using `tools/build_external_evidence_manifest.py`. Only the two manifest files themselves are excluded. The header-source exploration is retained separately from the eight evidentiary runs. Directory names are relative to `review-artifacts/williams.dirty-harry.1995/runtime/`.

| Directory | Files | Bytes | Manifest SHA256 |
| --- | --- | --- | --- |
| dh-flasher-test | 28 | 1315405 | `2d1fc644b20b3e5bbe3077f8f29a34bf97eaac482cd2bfd5414f4b4b2e9ccb03` |
| dh-gun-explore | 25 | 1308788 | `455ec7c49011a9572d03538e8297651e547941316778345713aab4ad98500efe` |
| dh-gun-feedback | 74 | 1589378 | `784a755e705a8717467e3dd03426032ed1b1fc8825ba278a8ae074a49c6bc1b2` |
| dh-gun-static | 16 | 1239491 | `fd24be7c2c66b18b075527d8f8b4642afd75d7abd3f0f479499b1bce0f6dbbf9` |
| dh-lighting-flippers | 134 | 2136818 | `123f0862790f3d202aa83b5be01d1d5c68087bb9f07ca584eb19602ad5c39654` |
| dh-mechanisms | 44 | 1467763 | `bdd2efa9b9717b41ac27eb6c159e0039a946cffb4a7104cf3bfd38cd2fad1591` |
| dh-solenoid-test | 122 | 1863176 | `b4bdd0cd478ec7863711e9cda6787ca39d6953e2ee1b211c9c543015ddd3125e` |
| dh-switch-edges | 197 | 3532322 | `28e9cd9120bfa1d26765a80b14a8e11dc060a7dc7beddd36208534582fdbd951` |
| explore-tests | 33 | 1345423 | `c7c74b85e9b1de332fc6e7b2e84fcd731cbada53e2d6e138259720aa6179ce08` |

The raw event times give final test-motor intervals of **24.599782 s** (periodic feedback) and **24.599817 s** (static closed). These are elapsed harness times, not physical gun speed. The compact ledger retains both startup and service intervals for recomputation.
