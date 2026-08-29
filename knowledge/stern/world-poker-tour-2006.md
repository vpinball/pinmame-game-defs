# World Poker Tour (Stern 2006)

Coverage: **partial - machine identity only. Nothing about playfield devices, wiring, mechanisms,
or behavior is evidenced yet.**

This record was promoted from the generated catalog stub `stub.pinmame.wpt_140a` by the
catalog-wide identity pass of 2026-08-29. The promotion resolves machine identity and carries the
catalog's residual driver grouping over unchanged, and it deliberately asserts nothing else. Every
requirement in the definition's `coverage.missing` is genuinely outstanding.

## Identity

- PinMAME catalog: root driver `wpt_140a`, description "World Poker Tour (V14.0)", manufacturer
  "Stern", catalog year "2008".
- OPDB record `G5poe-MQrb5` (IPDB 5134) names this machine "World Poker Tour"
  (Stern, manufacture date 2006-02-20); the resolved identity rests on the
  agreement of the PinMAME catalog and this reviewed mapping.
- The definition's driver list is exactly the clone tree PinMAME declares under `wpt_140a`;
  whether every listed driver really runs on this physical machine is unverified.

## Drivers this record holds

- `wpt_103a` (2006, Stern, clone of `wpt_140a`).
- `wpt_105a` (2006, Stern, clone of `wpt_140a`).
- `wpt_106a` (2006, Stern, clone of `wpt_140a`).
- `wpt_106f` (2006, Stern, clone of `wpt_140a`).
- `wpt_106g` (2006, Stern, clone of `wpt_140a`).
- `wpt_106i` (2006, Stern, clone of `wpt_140a`).
- `wpt_106l` (2006, Stern, clone of `wpt_140a`).
- `wpt_108a` (2006, Stern, clone of `wpt_140a`).
- `wpt_108f` (2006, Stern, clone of `wpt_140a`).
- `wpt_108g` (2006, Stern, clone of `wpt_140a`).
- `wpt_108i` (2006, Stern, clone of `wpt_140a`).
- `wpt_108l` (2006, Stern, clone of `wpt_140a`).
- `wpt_109a` (2006, Stern, clone of `wpt_140a`).
- `wpt_109f` (2006, Stern, clone of `wpt_140a`).
- `wpt_109f2` (2006, Stern, clone of `wpt_140a`).
- `wpt_109g` (2006, Stern, clone of `wpt_140a`).
- `wpt_109i` (2006, Stern, clone of `wpt_140a`).
- `wpt_109l` (2006, Stern, clone of `wpt_140a`).
- `wpt_111a` (2006, Stern, clone of `wpt_140a`).
- `wpt_111af` (2006, Stern, clone of `wpt_140a`).
- `wpt_111ai` (2006, Stern, clone of `wpt_140a`).
- `wpt_111al` (2006, Stern, clone of `wpt_140a`).
- `wpt_111f` (2006, Stern, clone of `wpt_140a`).
- `wpt_111g` (2006, Stern, clone of `wpt_140a`).
- `wpt_111gf` (2006, Stern, clone of `wpt_140a`).
- `wpt_111i` (2006, Stern, clone of `wpt_140a`).
- `wpt_111l` (2006, Stern, clone of `wpt_140a`).
- `wpt_1129af` (2006, Stern, clone of `wpt_140a`).
- `wpt_112a` (2006, Stern, clone of `wpt_140a`).
- `wpt_112af` (2006, Stern, clone of `wpt_140a`).
- `wpt_112ai` (2006, Stern, clone of `wpt_140a`).
- `wpt_112al` (2006, Stern, clone of `wpt_140a`).
- `wpt_112f` (2006, Stern, clone of `wpt_140a`).
- `wpt_112g` (2006, Stern, clone of `wpt_140a`).
- `wpt_112gf` (2006, Stern, clone of `wpt_140a`).
- `wpt_112i` (2006, Stern, clone of `wpt_140a`).
- `wpt_112l` (2006, Stern, clone of `wpt_140a`).
- `wpt_140a` (2008, Stern).
- `wpt_140af` (2008, Stern, clone of `wpt_140a`).
- `wpt_140ai` (2008, Stern, clone of `wpt_140a`).
- `wpt_140al` (2008, Stern, clone of `wpt_140a`).
- `wpt_140f` (2008, Stern, clone of `wpt_140a`).
- `wpt_140g` (2008, Stern, clone of `wpt_140a`).
- `wpt_140gf` (2008, Stern, clone of `wpt_140a`).
- `wpt_140i` (2008, Stern, clone of `wpt_140a`).
- `wpt_140l` (2008, Stern, clone of `wpt_140a`).

## PinMAME source contract (candidate)

- The pinned PinMAME source declares `wpt_140a` at `src/wpc/sam.c:2506` with machine module `sam1`; the definition declares controller platform `pinmame.sam` from it.
- The driver source's named switch/solenoid symbols are carried as 1 candidate devices in the definition.

## What a curator must establish next

Controller platform from the pinned PinMAME driver source; full input, output, and display
enumeration with semantic names; physical wiring and polarity; mechanism inventory and behavior;
variant differences across the clone tree; recreation knowledge from a manual, schematic, or
known-working table; runtime provenance; and a normalized spatial placement for every physical
device. No manual, table, ROM analysis, or harness evidence is retained for this machine yet.
