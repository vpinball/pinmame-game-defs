# Star Trek: The Next Generation — Ship Mode lamps 13 and 14, resolved 2026-10-21

The retained evidence bundle is
`external:pinmame-review-artifacts/star-trek-the-next-generation-1993/completion-2026-10-21/ship-mode/findings.json`,
SHA-256 `8e6c79507d979cb564172661ebd593466d907b81903691829c10b96cd8e11c40`.
Its canonical external manifest (177 files, 9,314,979 bytes) has SHA-256
`d1f182d214f8282d2b44ec1e8320a4105ea2a0a0f65603f935a8bf4888f97dc2`.

- Fresh-state harness run `explore-03-run.json`, SHA-256
  `e0e0db32561ec2ab00859fe3471d7d7355330a1952c8d28e81e73d4e14479eeb`, ties public
  lamp 13 to the visually read DMD title `TIME RIFT`: its selected-title frame is
  `031-first-mission-title-1-display-0.pgm`, whose pixel SHA-256 is
  `3438daa248df2194a515c94e859fc358a4584f82d0e9e946c67dd975a1e8b894`.
- The same run ties public lamp 14 to the visually read DMD title `WORM HOLE`: its selected-title
  frame is `059-second-mission-title-0-display-0.pgm`, whose pixel SHA-256 is
  `fbd57c89bac25d2020d07a3768d049c4d75b72d6bdb693555726d02104b89f5a`. Lamp 14 blinks,
  so this individual title frame may catch it off; the retained selection transition contains both
  public states.
- Pinball Fuzz's [STTNG restoration page](https://www.pinballfuzz.com/restorations/sttng) and its
  [original-playfield photograph](https://images.squarespace-cdn.com/content/v1/603bcc9f9959d83fcdc097b0/a3b2f213-bf9f-4f3d-bc20-2894bbaba5e8/3.jpg),
  raw SHA-256 `9fd4f4e41faed3ed102602bba46d906bfc078b5469ba4c0380682084ffbb3a14`, visibly label
  TIME RIFT at the lower-left ring insert and WORM HOLE at the left ring insert. It establishes
  physical insert side/order, not numeric coordinates.
- The known-working VPW script binds the two public addresses to `l13` and `l14`; retained VPX
  geometry supplies their coordinates: lamp 13 / TIME RIFT is `(0.396539, 0.6691)` and lamp 14 /
  WORM HOLE is `(0.338957, 0.621082)` in player view (x=0 left, x=1 right, y=0 rear, y=1 front).

Printed 2-41 literally labels the left insert 13 and the lower-left insert 14. The independent
runtime title evidence and physical playfield photograph settle that printed callout transposition;
the literal manual reading remains recorded in `lamp-locations-drawing.md`. The harness proves
public-lamp mission identity only, the photograph proves the named physical insert, and VPX supplies
the existing normalized coordinate.

The photograph is attributed to Pinball Fuzz; the playfield artwork is attributed to Williams
Electronics Games, Inc. and Paramount Pictures. Its rights and license are `NOASSERTION`. The
photograph remains external; this excerpt records only the factual reading and raw hash.
