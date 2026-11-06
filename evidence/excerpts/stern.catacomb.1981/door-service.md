# Catacomb cabinet service contacts

Source: Stern Electronics Catacomb schematics, PDF2, CABINET AND FRONT DOOR WIRING, original SHA-256 `45fd3691ca719eab243553b98967aef4fb7cbe6c1ce7340e3342ecf0a1d24294`. Method: curator visual tracing of the native drawing, preserving literal endpoints and wire order. Rights: NOASSERTION; Stern Electronics, Inc.; original retained locally.

The top service block draws three normally-open contacts returning to the common A3J2-7 (Y-R) line:

| Drawn contact | Other endpoint | Wire |
| --- | --- | --- |
| S33 MEMORY CLEAR | A4J3-5 | W- |
| TEST SWITCH | A4J3-1 | R |
| SLAM | A4J4-13 | B-O |

The drawing prints `W-` for the white wire; structured wiring normalizes this to `W`. This MEMORY CLEAR is the door contact, located separately from the MPU button by Catacomb's own [assembly drawing](service-locations.md). A4J3-5 belongs to this game's retained cabinet sheet; it is not copied from another game's harness. The MPU's on-board S33 has its own [NMI circuit](mpu-nmi.md).

Image derivation is recorded verbatim in the source record and can be reproduced with `tools/render_excerpt_image.py`.
