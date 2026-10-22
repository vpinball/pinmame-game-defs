# Lamp drawing and observed table positions

Curator visually checked the native production manual PDF 41 / printed 37, including the complete location drawing, frame and the six control symbols below. Source: Sega Pinball, Inc., `Baywatch_Manual.pdf`, SHA-256 `9545ae03f7ef1bcc41f3e5e08b6be996d581f9141b1f70228fe9969ba9ace400`. The retained full-page render is `verified-renders/page-41.webp`, 2550 by 3300 pixels, SHA-256 `ea78927d48519db54d36fa288e230380f70be5f6e7ef603a2917e3c18a7935ec`. The two small native-resolution diagram crops beside this excerpt retain the tower socket group and lamp 12, including their number labels. They are drawing regions, not images of the separate printed location table.

These are manual readings of depicted device centres, not factory measurements. Pixel origin is the full page's top-left; x increases right and y down. The tower points are the approximate centres of the three hatched socket bodies below the sloping rail, not the large 33/34/35 labels. The middle body's arrow identifies 34. Lamp 12 is the hatched body below the diagonal rail, with 12 printed above. The floor controls use the centres of the filled insert outlines containing their white numbers, not nearby black dots or the glyph centres.

The outer drawing frame centre-line corners are rear-left (334,141), rear-right (1591,140), front-left (337,3002) and front-right (1598,3001), each read to about +/-4 pixels. Average opposite corner coordinates to obtain left=335.5, right=1594.5, rear=140.5 and front=3001.5. The comparison uses `x=(px-335.5)/1259`, `y=(py-140.5)/2861`. It does not fit the table or any control points. The raw readings and source hashes are retained in `tools/baywatch_lamp_drawing.json`; `drawing_comparison()` in the curator recomputes the report.

All control readings used for this comparison are below; none was discarded to improve agreement. Differences are table minus drawing, normalized to each source's own frame. Table points are the exact retained insert objects, divided by 952 and 2162. Six decimals preserve calculation reproducibility, not measurement accuracy.

| Floor lamp | Drawing centre px | Drawing x,y | Table object | Table x,y | Difference x,y |
| --- | --- | --- | --- | --- | --- |
| 38 | 1094,211.5 | .602462,.024816 | l38 | .606092,.024399 | +.003630,-.000417 |
| 62 | 916,500 | .461080,.125655 | l62 | .460215,.125983 | -.000865,+.000328 |
| 30 | 916,622.5 | .461080,.168473 | l30 | .457852,.168854 | -.003228,+.000381 |
| 61 | 415,878 | .063145,.257777 | l61 | .064470,.258673 | +.001325,+.000896 |
| 36 | 526.5,1069.5 | .151708,.324712 | l36 | .151261,.327503 | -.000447,+.002791 |
| 9 | 888,2655 | .438840,.878889 | l9 | .434349,.884077 | -.004491,+.005188 |

| Elevated lamp | Drawing socket centre px | Drawing x,y | Table emitter | Table x,y | Difference x,y |
| --- | --- | --- | --- | --- | --- |
| 12 | 1245.5,1340 | .722796,.419259 | BulboF12 | .800330,.322505 | +.077534,-.096754 |
| 33 | 496,789 | .127482,.226669 | BulboF33 | .120437,.108845 | -.007045,-.117824 |
| 34 | 550,780 | .170373,.223523 | BulboF34 | .148651,.107626 | -.021722,-.115897 |
| 35 | 602,771 | .211676,.220377 | BulboF35 | .177002,.106530 | -.034674,-.113847 |

Read floor centres to about +/-5 pixels and elevated socket bodies to about +/-6 pixels. Together with the frame allowance this gives a conservative drawing-reading envelope of about +/-0.009 x and +/-0.004 y. This is not a statistical interval or an estimate of table accuracy. Scan skew, stroke width and rounded body extents limit the reading. Drawing stylization, the relation of symbol centre to emitter, the physical board frame and especially the projection of elevated sign/tower lamps remain unquantified. Floor controls differ by at most .005188 in either axis; this does not calibrate the elevated plane or establish factory coordinates. The much larger elevated differences are a measured source discrepancy, without proof that the table or physical machine is wrong.

The table positions are recomputed from the exact `BulboF12/33/34/35` world-mesh bounds, not their primitive origins. The retained script at 1111-1120 binds each address to its `BulboF` primitive through `FlashDLm`, plus the corresponding `f` sprite through `Flash`. An inspection of the exact extraction's Light/Flasher/Primitive objects within 65 VPX units of each drawing comparison point (raw approximately 688.102,906.438 for 12 and 121.363,490.058 / 162.195,483.257 / 201.515,476.456 for 33/34/35), and of every object bound to these addresses, found no defensible alternate emitter there:

- Near the tower, `GIBulb20/GIBulb20g` are at 102,500.75 and `GIBulb21/GIBulb21g` at 223,469.25. Script 980-983 drives these render pairs with local GI lamp 200. They cannot become tower indicators. Other nearby objects are lane wire, screws, brackets and a microswitch.
- Near 12, the `MetalGYR1` world-bounds centre is 693.49095,861.67817. It is hardware, with no lamp-12 script binding. No alternate Light or bulb primitive was found within that radius.
- `f12`, `f33`, `f34` and `f35` are Flasher opacity sprites. Their stored origins are respectively 743.375,966.5625; 110,249; 265.68915,822.94727; and 293.70667,819.1438. Their origins differ from their polygons and are not physical sockets. They remain excluded regardless of proximity.

The manual controls construction, identity and device presence. The script controls address-to-object binding, and the exact table/world OBJ supplies observed recreation positions. Perspective photographs corroborate the elevated construction and three tower lenses, without supplying a coordinate transform. Preserve the current observed table positions with an explicit warning on each device and a spatial blocker. This unresolved drawing/table comparison is a placement limitation, not an additional machine-design conflict or a basis for promotion.
