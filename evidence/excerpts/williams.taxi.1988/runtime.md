# Taxi L4 service observations

Pinned PinMAME 8371478a7640f1896dcdf565aed340dc5df989ba; DLL SHA256 ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e. All 1842 staged build-source blobs were independently compared to the pinned Git tree, with zero differences; runtime-pinned-8371478/verified-build-source.json retains that check. Legal taxi_l4.zip SHA256 30f21e3aa2ed62e93d38953e410b0c92679f264b7252d0408aad1d3eb991c03c. Compact derivative: evidence/runtime/system-11/taxi-l4-service.json, reproduced by tools/taxi_runtime_evidence.py. All raw segments, events, actions and snapshots remain in the retained raw runs.

The original ca33d8fd DLL was incorrectly attributed to this pin: the existing Centaur runtime record identifies that exact binary as built from 4ec52ff0ac133ac251681518aed2249e19fe26eb. Its original Taxi traces and 2,873-driver capture remain preserved under taxi-1988/runtime and the original native reconciliation, as historical diagnostics only. The new pinned DLL's existing retained catalog reports 2,895 drivers and matches all seven Taxi descriptors; native-catalog-pinned-reconciliation.json records the comparison. Neither the catalog baseline nor source pins changed. Only the fresh pinned runs below support the final runtime proof.

Every evidentiary state directory was newly created. One fresh l4-init scenario initialized NVRAM; only its taxi_l4.nv was copied into each fresh diagnostic state. Each scenario deliberately waits 8 s after boot. COIL TEST was reached by a display checkpoint and captured public 1..22 and 25..32 (plus enable 23); coil 22's service pulse does not imply a fitted physical load. SINGLE LAMPS reached a display checkpoint and captured all 64 matrix outputs and their service display frames. SWITCH EDGES reached its own checkpoint before host pulses; the six drop sensors 27..32 show their passenger/bank name while public 1 is held and clear on public 0. On this unmasked System 11 path, logical activation is not an electronic opto-component polarity claim.

The drop proof compares both the actual ROM label and its displayed numeric diagnostic address. Pinned src/wpc/s11games.c:644..649 gives display 0 CORE_SEG16/start 0/length 16 and display 1 CORE_SEG8/start 20/length 16. src/wpc/s11.c:412..439 applies S11_DISPINV before publishing segments and writes the lower row's low and high bytes separately under S11_LOWALPHA. Do not invert the published segments again. The decimal glyph map in src/wpc/core.c:137..140 is 0..9 = 0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f. Zero segments are blank. Alpha bit 15 and numeric low-byte bit 7 are preserved as decimal points; unknown glyphs/high bits in the decoded region fail closed, and a decimal-marked diagnostic number is rejected.

In these stable SWITCH EDGES snapshots, display 1 cells 4/5 (zero-based, segment-memory 24/25) hold the diagnostic switch number. This position comes from the retained snapshots, not from the host input address or from a generic display-layout assumption. All sixteen raw cells of both displays remain in each compact response. Only the explicitly listed numeric cells 4/5 are decoded; unrelated lower-row cells, including high-byte digits, remain raw and are not assigned guessed meanings. The upper label permits whitespace normalization only. Active and release response vectors are retained separately from the host stimulus/readback.

| Stimulus | Actual normalized display0 label | Actual display1 cells4/5 (decimal segment values) | Decoded diagnostic address | Release display0 / cells4/5 |
| --- | --- | --- | --- | --- |
| 27 | LOLA LEFT | 91,7 | 27 | blank / 0,0 |
| 28 | LOLA MIDDLE | 91,127 | 28 | blank / 0,0 |
| 29 | LOLA RIGHT | 91,111 | 29 | blank / 0,0 |
| 30 | PINBOT TOP | 79,63 | 30 | blank / 0,0 |
| 31 | PINBOT MIDDLE | 79,6 | 31 | blank / 0,0 |
| 32 | PINBOT BOTTOM | 79,91 | 32 | blank / 0,0 |

The helper's extractor version 3 rejects the stale binary, a recognized wrong name, a wrong numeric diagnostic address, unknown patterns and stale releases. Independent literal snapshot fixtures exercise those failures; host-injected switches do not appear in observed_switch_addresses.

Host 82 held produced core switch 57 and synthetic states 45/46; host 84 held produced core switch 58 and synthetic states 47/48. Host readback is separated from emulator-generated observations. Diagnostic enable 23 is background activity, not a claimed flipper winding. Static stimuli do not measure physical movement, bulb quantity, sockets, or geometry. Asynchronous service display frames can contain mixed labels during scanning; the complete raw vectors are retained rather than silently treating a transient last frame as a physical label. Printed parts and independently extracted complete ROM tables control the settled semantic names.

Raw successful runs:

- taxi-1988/runtime-pinned-8371478/l4-init.json: SHA256 434c55be2c2faeccd730ef8378c50a75788a882870e9a1d4b7a11dc0901e7ac5; scenario tools/harness-scenarios/system-11/taxi-nvram-init.json: SHA256 2638b812853df33bcf2d862bade36fcb93540f7534b81cbc6c1ea109c0d81a4a.
- taxi-1988/runtime-pinned-8371478/l4-coil.json: SHA256 b5c2d29c92914af3f5b0d6cc3545d86e73ddab0f3ca1da6cd090c9c4038a83b6; scenario tools/harness-scenarios/system-11/taxi-coil-test.json: SHA256 f443e809a7a29d073bd8fb040480f739a73a6d9f5201599ba6339a0165bef150.
- taxi-1988/runtime-pinned-8371478/l4-labels-v3.json: SHA256 665752ff7d6f93eb04ffafa6761c0ca7176a13e71e8382bd909ce9a866cfdc02; scenario tools/harness-scenarios/system-11/taxi-service-labels.json: SHA256 43ee57c7b2ccb7b4e46fb677a6f332d24b35321fa2d78a24532c24927cfd5e6f.

Full pinned runtime-directory manifest SHA256 5816d5b32b05f3de3ecb757e8becbf8d62dec80deb02d9fb99dcaf021f073c2e. Earlier failed boot/label traces and stale-DLL runs remain diagnostic only and are excluded from this derivative.
