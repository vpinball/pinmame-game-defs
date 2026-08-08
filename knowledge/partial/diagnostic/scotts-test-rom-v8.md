# Scott's Test ROM (version 8)

Coverage: **partial diagnostic-software classification; not a physical game definition**

## Classification

PinMAME declares `scotest8` under the explicit `Scott's Test ROM` section in `by35games.c`, and the public driver description is `Scott's Test ROM (version 8)`. It is diagnostic software targeting Bally AS-2518-17/35-era hardware, not a distinct playfield an author can recreate.

The catalog retains it because it is a supported PinMAME driver. It is excluded from the physical/virtual game completion denominator only because the definition positively classifies it as `diagnostic_software`; unknown records continue to count as games.

## Emulated hardware

PinMAME initializes it as generation `GEN_BY17`, with the `dispBy7` display layout, left-flipper switch handling, eight balls, and the Bally 50 sound board. It uses the generic `input_ports_by35` input ports and the `by35_mBY35_50S` machine configuration.

## Remaining diagnostic documentation

The software's complete test sequence, expected switch/output address coverage, display prompts, sound tests, and operator procedure have not yet been documented. Those omissions keep this record partial even though they do not affect physical-game coverage.

## Sources

- PinMAME `4ec52ff0ac133ac251681518aed2249e19fe26eb`, `src/wpc/by35games.c:1992-2002` and `src/wpc/driver.c:338`.
