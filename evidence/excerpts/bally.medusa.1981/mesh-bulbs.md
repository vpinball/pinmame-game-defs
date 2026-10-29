# Medusa rear-bar modelled bulbs

Source: the exact retained VPX SHA256
`35598302510b003baf68b5f9a274010b7325e639206c33203ff802f758eb7c3f`.
Exported with `vpxtool git:v0.33.3 export obj --units vpu` on
2026-10-29T12:23:30Z. Retained outside Git as
`bally.medusa.1981/world-obj/Medusa (Bally 1981).obj`, 11,210,362 bytes,
SHA256 `aa38d3de5c283f8dbc02800c07c5817c201ca982aeaf1d58955eda5dfb36981e`.
Missing texture warnings affect appearance, not the exported vertex positions.

Primary inspection found 21 separate visible primitives with mesh filename
`Bulb-Wedge-Small.obj`, positioned along the rear Olympus bar. The rest of the
primitive inventory comprises posts, caps, screws, bumpers, kicker, scoop and
deflector models; it supplies no general insert/GI socket model. All Lights
have show_bulb_mesh=false. Thus the rear row is a defensible physical bulb
model even though its associated Light objects are forward glow helpers.

The complete bounds, nearest script-bound Light, public address and rounded
normalized coordinates are committed in
`tools/seeds/bally/medusa-1981-bulbs.json`. Each row has 67 world vertices.
The names in left-to-right order are:

```text
Primitive74 Primitive26 Primitive31 Primitive33 Primitive37 Primitive44
Primitive46 Primitive50 Primitive53 Primitive57 Primitive61 Primitive63
Primitive68 Primitive70 Primitive72 Primitive78 Primitive80 Primitive81
Primitive82 Primitive84 Primitive88
```

Their corresponding public channels, in the same order, are:

```text
65 81 97 113 66 82 98 114 67 83 99 115 68 84 100 116 69 85 101 117 60
```

OBJ x/y are table x/y and z is negative height. Use each body's world bounds
center, x/952 and y/1974, rounded to six decimals. This gives every body
y=0.007144, whereas its forward glow is about y=0.013791. Four bumper-cap
world bounds independently check orientation/scale against Bumper1-4's stored
centers: Primitive21/Bumper1, Primitive22/Bumper3, Primitive23/Bumper4 and
Primitive28/Bumper2 differ by less than one VPU on each axis. The seed and
evidence-enabled tests recompute these checks from the retained export.

The own-game harness labels a 21-position top panel, #1 at left and #21 at
right. The retained physical upper-playfield photograph shows the rear bar
in place. These support the assembly, count and order, not independent exact
socket measurements. Coordinates stay observed, and public100 stays candidate
because both physical sheets duplicate its printed #3 instead of identifying
position15. No wiring correction or bulb part number is inferred.

The remaining insert and target Lights are render candidates only. They are
retained in `evidence/spatial/bally.medusa.1981.json` but are not emitted as
canonical lamp/socket placements. This also excludes the doubled top-target
glows, 29 GI helpers and eight translucent-flipper lighting helpers.
