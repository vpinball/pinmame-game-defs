# Skateball - pinned PinMAME source licensing

Source revision: `46e1a01a0f73dc5ce163d98db1ae435883ecc450`. The primary curator read the pinned root `LICENSE` introduction, the first lines of the files below, and the relevant parent directories. No overriding license file is present in `src`, `src/wpc`, `src/libpinmame` or `src/lisy`.

Root `LICENSE` lines 12-15 distinguish files whose first line explicitly marks BSD-3-Clause from unmarked files, which retain the inherited old MAME terms. The aggregate CORE record cites files from both categories and therefore uses **PinMAME license**, with the per-file notices retained. The catalog record also uses this aggregate label; its directly cited game definitions and API files are BSD-marked. This records source licensing, without changing the machine facts derived from it.

| Retained file | First-line BSD-3-Clause marker | SHA-256 |
|---|---|---|
| `LICENSE` | Root per-file licensing policy | `21cde7ac6cffe0fa9e3a66beb89e0db1b78caa7bb8b8041d1b483f36460e026e` |
| `src/wpc/by35.c` | Present | `91df5b0c8a8ba19c017fec5ea45b7a4e2b911f2a56b9a793de7ad1caddd6f6e2` |
| `src/wpc/by35.h` | Present | `aa6cfe3df9d7e51bc4087c634e0ebaaed1f15cf3ccfc018aa2e46ae370aeef5a` |
| `src/wpc/by35games.c` | Present | `1c00fca170c7549a399a89fb0f76d4318fce08a6620becd4558fe8cb803bf00d` |
| `src/wpc/core.c` | Absent; inherited old MAME terms | `38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00` |
| `src/wpc/core.h` | Absent; inherited old MAME terms | `b6c03b20a09fbadff1ce16f9f1cfc9e5bace08857cb998b92d8f304695ec97c0` |
| `src/lisy/lisy35.c` | Present | `0c53afe597028f982d0a98532631dae6e395798a741db4ea486154eb30183653` |
| `src/libpinmame/libpinmame.cpp` | Present | `956ea00d6b1f5b3b8533534ca2319fb931618f8fac3aa3792340a106a15ad76e` |
| `src/libpinmame/libpinmame.h` | Present | `f9d22bf93a8a3716ac24904c70290d7696671b2937444e45cab3f5b4b1b93a59` |

The CORE locator names `core.c` and `core.h` for the synthetic flipper and switch contract. The catalog locator names `by35games.c` for the three driver declarations and `libpinmame.cpp:1110` for `PinmameGetGames`. The BSD-marked driver files do not establish a blanket BSD license for the other cited files or the complete emulator.
