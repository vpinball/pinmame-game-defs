# Retained VPU 7733 / 2.0.3 VR comparison

Curator reviewed the exact embedded scripts, extracted object records, manual
pages 30–34 and 44–45, and the retained physical photographs. This is a factual
selection from the local artifacts, not a copy of either community script.

The public VPU release page names HauntFreaks and 32assassin as creators and
32assassin, HauntFreaks as scripting credits; Data East is the manufacturer. It
describes a makeover of the 2017 32assassin table, published March 2, 2022,
version 2.0.3. The page's reuse notice requires prior author permission. The
archive and scripts stay external. The page says ROM wwfr_103; the exact new
embedded script selects wwfr_106. This is stale page metadata, not a physical
machine conflict. No acquisition timestamp was captured: the retained inventory
records source-page and download completion modification times separately.

Both tables have bounds (0,0)–(1093,2162). Matching ancestry, callbacks and
coordinates supplement the older table; they do not independently validate it.

| Binding / region | Old retained table | New retained table | Disposition |
| --- | --- | --- | --- |
| Matrix 61 / Left Turbo Bumper | NFadeL 61,L61; own bulb mesh at (309.8645,422.34802) | Same binding, mesh and centre | One observed bulb at its named bumper; manual lamp/assembly records establish fitment |
| Matrix 62 / Bottom Turbo Bumper | NFadeL 62,L62; own bulb mesh at (506.5174,471.04306) | Same binding, mesh and centre | Candidate only: script binds rear/right body but manual lamp drawing puts 62 front/bottom |
| Matrix 63 / Right Turbo Bumper | NFadeL 63,L63; own bulb mesh at (386.65268,631.17474) | Same binding, mesh and centre | Candidate only: script binds front/bottom body but manual lamp drawing puts 63 rear/right |
| Matrix 15 / TAG cabinet button | Omitted from UpdateLamps | NFadeL 15,L15; L15.state also changes VR tag_button lighting | Cabinet applicability remains; no playfield socket inferred |
| Matrix 16,27,59 | Omitted from UpdateLamps | Still omitted | Manual fitment remains used |
| Local 125–132 | SolCallback(25–32) feeds lighting-array indices; 7 bulb meshes at 129/130/132 | Same callbacks; all flasher effect lights now lack their own bulb meshes | Local array indices are not matrix lamp addresses. No new physical flasher bulbs established |
| GI animation collection | 36 members, all 36 showing bulb meshes | 77 members, 38 showing bulb meshes | These are rendering groups, not an electrical socket census |
| GI_034 | Absent | Own bulb mesh centre (126.44533,998.76807) | Candidate only: no socket-specific factory construction/circuit reconciliation |
| GI_036 | Absent | Own bulb mesh centre (120.826675,1120.9738) | Candidate only, for the same reason |
| Right diverter / 22 | Enabled callbacks start an alternating timer; two collision walls swap | Same implementation | No independent physical home/held/toggle evidence |
| TAG switch / 62 | Plunger and MagnaSave paths assert 1 on down, 0 on up | Plunger path reverses these levels; MagnaSave paths retain them, after key-handler early-return guards | Consumed-script inconsistency; no physical polarity inference |

The 7 older flash mesh objects are f129a/f129, f130a/f130b/f130, and f132a/f132.
Several overlap or sit close to separate GI render bulbs. A physical No.89
socket cannot be identified from that duplication or matching circuit count
alone. The manual's location labels are not calibrated bulb centres. Neither
the new source nor the inspected photos establishes which duplicated render
body is the actual socket. They remain explicit candidates in the lighting audit.
The corrected 8R inventory is **two playfield plus two backbox bulbs**, four total;
the older chart's one-playfield printing and the earlier comparison's inherited
one-playfield assumption do not overrule the schematic/parts reconciliation.

The left bumper bulb61 is observed: manual lamp drawing and actual modeled bulb
agree. Lamp 62/63 physical coordinates are withheld despite actual bulb meshes.
Printed page 31 exchanges their positions versus the scripts. Printed page 29's switch map
does match sensor 50/51 at the table's bodies, but its names do not settle lamp
wiring. Compact lamp/switch drawing crops preserve the distinction. Production
lamp 62/63 test illumination or socket wire pairs must settle it. Other flat
matrix lights remain insert/glow geometry until their sockets are established.
