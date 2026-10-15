# Pinned PinMAME source-license scope

Revision 97aa922bf8e4b6970126192ec1ac1fb0305a4f62, root LICENSE lines 4–18 and section VI lines 73–84. LICENSE SHA-256: 21cde7ac6cffe0fa9e3a66beb89e0db1b78caa7bb8b8041d1b483f36460e026e. Scope checked against the retained checkout; this is a compact licensing summary, not a replacement license grant.

The project is transitioning from its inherited old-MAME license to BSD-3-Clause. Lines 12–15 limit the BSD designation to files whose first line is `// license:BSD-3-Clause`; files without that marker remain under the inherited terms. Lines 17–18 allow subdirectory overrides. Neither src/ nor src/wpc/ contains a LICENSE/COPYING override.

The following files supply this definition's transport and title evidence. None has the required first-line BSD marker:

| File | First line | SHA-256 |
| --- | --- | --- |
| src/wpc/alvg.c | /************************************************************************************************ | f076d3ecaa8a027430b7b551699caf466d12758bad3566f10789e40529d607af |
| src/wpc/alvggames.c | #include "driver.h" | 3e8b6f6efe724b85b12143fda2b1b1be5d82eb7698d61c2b957c70b8de553aa8 |
| src/wpc/alvg.h | #pragma once | a7843991f3b9eeb547f8f538b9c6e3798b5fa84fb52bc445c4b5f120afd1b885 |
| src/wpc/core.c | /***********************************************/ | ae94d4ae8078f684b3ba58fd35cac84bf58e181de1e6f25ecb95f03c66966dcc |
| src/wpc/gen.h | #pragma once | 87fb2634fbbdc4faf15920df4e959d06524bc09a66b78dcb5976c0b5e94ec64b |

Section VI separately governs source-code reuse, including commercial authorization and source availability conditions, and expressly permits reuse of information contained in the source for any use. The metadata label `LicenseRef-PinMAME-legacy` identifies these inherited terms; it does not claim BSD licensing. Attribution: PinMAME development team and contributors; the Alvin G driver credits Steve Ellenoff and Gerrit.
