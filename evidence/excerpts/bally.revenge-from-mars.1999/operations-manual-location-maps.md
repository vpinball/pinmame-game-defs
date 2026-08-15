# Revenge From Mars stock location-map review

Source: *Revenge From Mars Operations Manual*, February 1999, model 50070. Visually reviewed from PDF pages 78, 80, 82, and 84 (printed pages 2-38, 2-40, 2-42, and 2-44). The four committed crops are the authoritative drawing excerpts; OCR was used only as a navigation aid because most callout text is part of the scanned line art.

## Coordinate projection

Each printed drawing uses the same player-view orientation. Callout endpoints and the centers of directly labelled inserts/devices were manually projected into one normalized playfield plane: `x=0` left, `x=1` right, `y=0` rear/backglass, and `y=1` front/apron. These are validated authoring projections, not surveyed measurements: the diagrams are service line art rather than surveyed CAD, their perspective and leader routing differ, and the curator records three-decimal coordinates only to make regeneration deterministic. Cabinet controls, coin-door lamps, and service hardware remain spatially not applicable.

The retained review crops and approximate outer-table pixel bounds used during visual review are: Matrix A `1584x2988`, bounds `(308, 291)-(1354, 2876)`; Matrix B `1534x2917`, bounds `(176, 289)-(1294, 2890)`; switches `1635x2988`, bounds `(336, 465)-(1296, 2874)`; and solenoids/flashers `1635x2988`, bounds `(361, 477)-(1356, 2860)`. The bounds are review anchors for orientation and relative depth, not an asserted affine calibration; individual points follow the drawn device center or callout endpoint and are validated as authoring projections rather than surveyed coordinates.

## Lamp Locations (Matrix A), printed page 2-38

The drawing locates these fitted Matrix A positions: `13A`, `15A`, `16A`, `17A`, `18A`, `23A`, `25A`, `26A`, `27A`, `28A`, `35A`, `36A`, `37A`, `38A`, `41A`, `42A`, `43A`, `44A`, `45A`, `46A`, `47A`, `48A`, `51A`, `52A`, `53A`, `54A`, `55A`, `56A`, `57A`, `61A`, `62A`, `63A`, `64A`, `65A`, `66A`, `67A`, `68A`, `71A`, `72A`, `73A`, `74A`, `75A`, `76A`, `77A`, `78A`, `81A`, `82A`, `83A`, `84A`, `85A`, `86A`, `87A`, and `88A`. `13A` Start and `23A` Launch are drawn outside the playfield as cabinet buttons. `21A` Tickets Low is a cabinet/service indicator present in the lamp table but has no playfield callout on this drawing. The printed note says `24A` Coin Door Illumination is not shown; it is likewise cabinet/service rather than assigned a playfield point.

## Lamp Locations (Matrix B), printed page 2-40

The drawing locates these fitted Matrix B positions: `11B`, `12B`, `13B`, `14B`, `15B`, `16B`, `17B`, `18B`, `21B`, `22B`, `23B`, `24B`, `25B`, `26B`, `27B`, `28B`, `31B`, `32B`, `33B`, `34B`, `35B`, `36B`, `37B`, `41B`, `42B`, `43B`, `44B`, `45B`, `46B`, `47B`, `51B`, `52B`, `53B`, `54B`, `55B`, `56B`, `57B`, `58B`, `61B`, `62B`, `63B`, `64B`, `65B`, `66B`, `67B`, `68B`, `71B`, `73B`, `74B`, `75B`, `76B`, `77B`, `78B`, `81B`, `82B`, `83B`, `84B`, `85B`, `86B`, `87B`, and `88B`. The lower-center cluster is read rear-to-front as the nine saucer-rim circles, the `25B`/`24B`/`23B` Fuel-Saucer-Weapons row, the five beam wedges `43B`/`26B`/`27B`/`22B`/`32B`, the eight-value arc `42B`/`41B`/`11B`/`13B`/`15B`/`17B`/`21B`/`31B`, and the front trio `12B`/`14B`/`16B`. The drawing places `18B` at the left slingshot and `28B` at the right slingshot; runtime names remain opposite, so spatial coordinates follow the printed physical addresses while semantic labels follow the machine lamp test.

## Playfield Switch Locations, printed page 2-42

The stock drawing locates playfield switches `11`, `12`, `15`, `16`, `17`, `18`, `25`, `26`, `27`, `28`, `31`, `32`, `33`, `34`, `35`, `36`, `37`, `38`, `41`, `42`, `43`, `44`, `45`, `46`, `47`, `51`, `52`, `61`, `62`, `63`, `64`, `65`, `67`, `68`, `71`, `72`, `73`, `74`, `75`, `76`, `77`, `78`, `85`, `86`, and `87`. Address `31` is printed twice: once in the top callout row and once beside `32` on the right margin. The spatial map treats the right-margin `31`/`32` pair as one center-loop assembly point because the drawing does not provide surveyable separation between the two reeds; the standalone top `31` is retained as a duplicate cross-reference, not a second physical switch. The drawing places `13` Start and `23` Launch outside the playfield as cabinet buttons. It contains no fitted devices for later community-firmware expansion positions `53`-`56`; those addresses are explicitly absent from the stock model 50070 rather than assigned guessed coordinates.

## Solenoid/Flasher Locations, printed page 2-44

The drawing locates printed drivers `1`-`17`, `22`, `23`, `25`-`28`, and paired-winding assemblies `33`-`40`. Paired power/hold callouts share one physical effect point: `33`/`34` lower-right flipper, `35`/`36` lower-left flipper, `37`/`38` lock diverter, and `39`/`40` up/down ramp. Factory-unused drivers `18` and `19` and optional ticket driver `48` have no stock playfield device.
