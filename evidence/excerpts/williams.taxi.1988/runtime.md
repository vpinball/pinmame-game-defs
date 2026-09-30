# Taxi L4 service observations

Pinned PinMAME 8371478a7640f1896dcdf565aed340dc5df989ba; DLL SHA256 ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d. Legal taxi_l4.zip SHA256 30f21e3aa2ed62e93d38953e410b0c92679f264b7252d0408aad1d3eb991c03c. Compact derivative: evidence/runtime/system-11/taxi-l4-service.json, reproduced by tools/taxi_runtime_evidence.py. All raw segments, events, actions and snapshots remain in the retained raw runs.

Every evidentiary state directory was newly created. One fresh l4-init scenario initialized NVRAM; only its taxi_l4.nv was copied into each fresh diagnostic state. Each scenario deliberately waits8s after boot. COIL TEST was reached by a display checkpoint and captured public1..22 and25..32 (plus enable23); coil22's service pulse does not imply a fitted physical load. SINGLE LAMPS reached a display checkpoint and captured all64 matrix outputs and their service display frames. SWITCH EDGES reached its own checkpoint before host pulses; the six drop sensors27..32 show their passenger/bank name while public1 is held and clear on public0. On this unmasked System11 path, logical activation is not an electronic opto-component polarity claim.

Host82 held produced core switch57 and synthetic states45/46; host84 held produced core switch58 and synthetic states47/48. Host readback is separated from emulator-generated observations. Diagnostic enable23 is background activity, not a claimed flipper winding. Static stimuli do not measure physical movement, bulb quantity, sockets, or geometry. Asynchronous service display frames can contain mixed labels during scanning; the complete raw vectors are retained rather than silently treating a transient last frame as a physical label. Printed parts and independently extracted complete ROM tables control the settled semantic names.

Raw successful runs:

- taxi-1988/runtime/l4-init.json: SHA256 567cb5ee80421a1a5eead013909c001967c8c86e925e9c170fa0ae197f3a4321; scenario tools/harness-scenarios/system-11/taxi-nvram-init.json: SHA256 2638b812853df33bcf2d862bade36fcb93540f7534b81cbc6c1ea109c0d81a4a.
- taxi-1988/runtime/l4-coil.json: SHA256 2f51dfd9ab3ea4105124181b493a6fcf2867bf0db1f2f21e5a37a0dbd86e40d8; scenario tools/harness-scenarios/system-11/taxi-coil-test.json: SHA256 f443e809a7a29d073bd8fb040480f739a73a6d9f5201599ba6339a0165bef150.
- taxi-1988/runtime/l4-labels-v3.json: SHA256 a7041cb28975cc7759977b92c1566e11fc073cd22c0bdab4f4087ae718bdd4b2; scenario tools/harness-scenarios/system-11/taxi-service-labels.json: SHA256 43ee57c7b2ccb7b4e46fb677a6f332d24b35321fa2d78a24532c24927cfd5e6f.

Full runtime-directory manifest SHA256 834ea4eb748383df736f1a00bf0c749b75236adbed8b2626c16d874f109076b1. Earlier failed boot/label traces remain diagnostic only and are not successful runs in this derivative.
