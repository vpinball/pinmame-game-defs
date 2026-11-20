# Gamatron (Pinstar, 1985)

**Coverage is partial.** This record identifies the conversion and assigns its single PinMAME driver. Full curation of the conversion's wiring, geometry and mechanisms remains open.

Pinstar released Gamatron in December 1985 as a kit for standard-size four-player machines. IPDB 984 describes a replacement playfield, a Bally/Stern boardset with a Pinstar CPU-socket daughterboard, and a revised ball walker. In particular it shows one pop bumper and two slingshots where the stock Flight 2000 playfield has two pop bumpers and four slingshots. The Pinstar conversion has no VSU-100 speech board. Its standard-width playfield, artwork, bumper/sling topology and backglass make it a distinct physical machine. The 1986 Sonic Gamatron is a separate existing record. [Pinstar Gamatron, IPDB 984](https://www.ipdb.org/machine.cgi?id=984)

PinMAME's `gamatron` is defined as an emulator clone of `flight2k` but loads the separate 8 KiB `gamatron.764` image and uses `by35_mST200` with ST300 sound. Keep the emulator parent relationship while attaching the driver to the Pinstar conversion. [Pinned Gamatron driver](https://github.com/vpinball/pinmame/blob/46e1a01a0f73dc5ce163d98db1ae435883ecc450/src/wpc/stgames.c#L35-L41)
