# Retained runtime bindings

Source: JPSalas Alien Poker 1.0.1, metadata 29.12.2017; extracted script.vbs SHA256
808b4cd61e0d836a593cf733ae47c09a180e739954314cb55910db2ba4f6e9f7. Read and checked by the curator.
The script loads s6.vbs, declares alpok_l6 (French alternative commented), HandleKeyboard 0,
HandleMechanics 0 and one ball. Source/table bytes and exact extraction manifest are retained.

| Public switch | Bound object or initialization |
|---|---|
|9|bsTrough.InitSw; Drain_Hit adds the ball; BallRelease is the shooter-lane serve proxy|
|10,18,26,34,42|dtbank.InitDrop sw10,sw18,sw26,sw34,sw42; targets A,K,Q,J,10|
|13|LeftSlingshot_Slingshot|
|15,22,29|InitSaucer sw15,sw22,sw29|
|17|Spinner_Spin|
|35,36,37,38|Bumper2,Bumper1,Bumper3,Bumper4 Hit|
|11,12,23,24,25,27,32|same-number Trigger Hit/UnHit|
|14,16,20,30|same-number HitTarget Hit|
|19,21,28,33,39,40,41|same-number Wall Hit; audio anchors can name other objects|

| Output | Runtime operation |
|---|---|
|1|bsTrough.SolOut, final serve at BallRelease|
|2,3,15|left Spade, right Heart, top Club saucer ExitSol_On|
|4,5,6,7,8|dtbank.SolUnHit5,4,3,2,1 (10,J,Q,K,A individually raised)|
|14|knocker sound callback|
|21|dtbank.SolDropDown (all targets dropped)|
|23|vpmNudge.SolGameOn|
|sLRFlipper,sLLFlipper|right two flippers together, left one flipper|

UpdateLamps maps 1–48,50–53,56 to same-number Lights. 18 additionally drives l18a (spinner);
37 additionally drives l37a (upper extra-ball arrow). Bumper lamps 29–32 each drive lN and lNa,
two render layers on one bumper, not two sockets. Flash objects l2a,l3a,l13a–l16a,l37b are
glow helpers. 54,55,57–64 drive backdrop indicators/text. 50–53 are playfield-positioned
backbox proxies. l56 lies on bare wood outside the painted playfield and does not locate a
physical credit socket. GI is locally animated by GiOn/GiEffect; no public GI channel is bound.

The table writes 43 on right key edges, then calls vpmKeyDown/Up. Retained s6.vbs SHA256
51540940fc31d7afccbee636815c40369fa852b86116339c641073845a6ad24a defines swLRFlip 82,
swLLFlip 84 and writes those bits in its key handlers. PinMAME copies 82 into 43 each update,
so the table's direct 43 write is redundant. core.vbs SHA256
a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69 supplies the ball-stack
and target helpers. Script kick strengths, animation timers and GI shows are table tuning.
