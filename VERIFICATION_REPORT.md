# Verification Report: Phase 1 C# to JSON Conversion

**Generated:** 2026-02-12
**Source:** `VisualPinball.Engine.PinMAME` C# game classes
**Target:** `pinmame-game-defs` JSON files

## Platform Files

| Platform | Switches | Coils | Aliases | Wires |
|----------|----------|-------|---------|-------|
| bally | 12 | 5 | 13 | 4 |
| sam | 13 | 4 | 14 | 4 |
| system80 | 11 | 5 | 12 | 4 |
| wpc | 12 | 5 | 13 | 4 |

## Game Files

| Game ID | C# Class | Platform | ROMs | Switches | Coils | Lamps | Aliases |
|---------|----------|----------|------|----------|-------|-------|---------|
| afm | AttackFromMars | wpc | 9 | 50 | 35 | 64 | 0 |
| centaur | Centaur | bally | 3 | 48 | 16 | 60 | 0 |
| cftbl | CreatureFromTheBlackLagoon | wpc | 8 | 41 | 28 | 64 | 0 |
| fg | FlashGordon | bally | 8 | 39 | 16 | 0 | 0 |
| mm | MedievalMadness | wpc | 6 | 50 | 33 | 64 | 0 |
| rock | Rock | system80 | 4 | 28 | 8 | 51 | 4 |
| rock_enc | RockEncore | system80 | 5 | 28 | 8 | 51 | 4 |
| star-trek-stern | StarTrekEnterprise | sam | 12 | 49 | 29 | 220 | 0 |
| t2 | Terminator2 | wpc | 11 | 49 | 32 | 68 | 4 |
| trn | TRONLegacy | sam | 14 | 44 | 30 | 64 | 0 |
| twd | TheWalkingDead | sam | 19 | 31 | 25 | 110 | 0 |
| **TOTAL** | | | **99** | **457** | **260** | **816** | **12** |

## Known Anomalies in C# Source

These are anomalies present in the C# source code that are faithfully reproduced in JSON:

1. **Centaur** has duplicate coil ID 5 -- two entries with `new(5)` mapping to different drop targets.
   Both entries are included in JSON. This is a known bug in the C# source.
2. **TheWalkingDead** has three lamp entries all with ID 81 (Fire Button Red/Green/Blue channels).
   All three are included. This likely represents three color channels sharing one PinMAME lamp number.
3. **FlashGordon** has an empty lamp array (`AvailableLamps = {}`). Lamps not yet mapped in C#.
4. **RockEncore** extends Rock without overriding any hardware definitions.
   JSON file contains the same switches/coils/lamps/aliases as Rock (inherited data).
5. **StarTrekEnterprise** lamps 281/283/282 all have description "(Beam) Me Up - B".
   This appears to be a copy-paste typo in the C# source (all three channels say " - B").
6. **AttackFromMars** has coils 10 and 11 both described as "Right Slingshot".
   This is in the C# source and is reproduced as-is.

## Conversion Rules Applied

### Game-Only Data
Game JSON files contain ONLY game-specific data from the game class's
`Switches`, `GameCoils`, `AvailableLamps`, `Roms`, and `Aliases` arrays.
Platform-level defaults (coin switches, flipper coils/switches, wires) are in platform files.

### Exception: Flipper Coil Overrides
When a game class defines coils using the named string constants
(`CoilFlipperLowerRight`, etc.), these ARE included in the game file because
they override the platform defaults. Examples:
- T2 overrides all 4 flipper coils (custom DeviceHint, marks upper flippers unused)
- Rock defines all 4 flipper coils with custom DeviceHints

### Field Omission Rules
- `normally_closed`: only included when `true`
- `is_lamp`: only included when `true`
- `is_unused`: only included when `true`
- `constant_hint`: only included when not `None`
- `type` (lamp): only included when not `SingleOnOff` (default)
- `source` (lamp): only included when not `Lamp` (default)
- `fading_steps`: only included when non-zero
- `channel`: only included when not `Alpha` (default)
- `num_matches`: only included when non-default
- `version` (ROM): only included when non-null
- `description` (ROM): only included when non-null

## Field Mapping Reference

| C# Source | JSON Field | Notes |
|-----------|------------|-------|
| `InputConstants.ActionStartGame` | `"Start Game"` | Resolved constant |
| `InputConstants.ActionPlunger` | `"Plunger"` | Resolved constant |
| `InputConstants.ActionSlamTilt` | `"Slam Tilt"` | Resolved constant |
| `InputConstants.ActionCoinDoorOpenClose` | `"Coin Door Open/Close"` | Resolved constant |
| `InputConstants.ActionInsertCoin1` | `"Insert Coin Slot 1"` | Resolved constant |
| `InputConstants.ActionInsertCoin2` | `"Insert Coin Slot 2"` | Resolved constant |
| `InputConstants.ActionInsertCoin3` | `"Insert Coin Slot 3"` | Resolved constant |
| `InputConstants.ActionInsertCoin4` | `"Insert Coin Slot 4"` | Resolved constant |
| `InputConstants.ActionCoinDoorCancel` | `"Coin Door Cancel (WPC)"` | Resolved constant |
| `InputConstants.ActionCoinDoorDown` | `"Coin Door Down (WPC)"` | Resolved constant |
| `InputConstants.ActionCoinDoorUp` | `"Coin Door Up (WPC)"` | Resolved constant |
| `InputConstants.ActionCoinDoorEnter` | `"Coin Door Enter (WPC)"` | Resolved constant |
| `InputConstants.ActionCoinDoorBack` | `"Coin Door Back (SAM)"` | Resolved constant |
| `InputConstants.ActionCoinDoorMinus` | `"Coin Door Minus (-) (SAM)"` | Resolved constant |
| `InputConstants.ActionCoinDoorPlus` | `"Coin Door Plus (+) (SAM)"` | Resolved constant |
| `InputConstants.ActionCoinDoorSelect` | `"Coin Door Select (SAM)"` | Resolved constant |
| `InputConstants.ActionRightFlipper` | `"Right Flipper"` | Resolved constant |
| `InputConstants.ActionLeftFlipper` | `"Left Flipper"` | Resolved constant |
| `InputConstants.ActionUpperRightFlipper` | `"Upper Right Flipper"` | Resolved constant |
| `InputConstants.ActionUpperLeftFlipper` | `"Upper Left Flipper"` | Resolved constant |
| `InputConstants.ActionSelfTest` | `"Self Test"` | Resolved constant |
| `InputConstants.ActionLeftAdvance` | `"Left Advance"` | Resolved constant |
| `InputConstants.ActionRightAdvance` | `"Right Advance"` | Resolved constant |
| `InputConstants.MapCabinetSwitches` | `"Cabinet Switches"` | Resolved constant |
| `SwitchConstantHint.AlwaysClosed` | `"always_closed"` | Enum to snake_case |
| `SwitchConstantHint.AlwaysOpen` | `"always_open"` | Enum to snake_case |
| `LampType.SingleFading` | `"single_fading"` | Enum to snake_case |
| `LampType.RgbMulti` | `"rgb_multi"` | Enum to snake_case |
| `LampSource.GI` | `"gi"` | Enum to lowercase |
| `ColorChannel.Red` | `"red"` | Enum to lowercase |
| `ColorChannel.Green` | `"green"` | Enum to lowercase |
| `ColorChannel.Blue` | `"blue"` | Enum to lowercase |
| `PinMameRomLanguage.English` | `"en"` | ISO 639-1 |
| `PinMameRomLanguage.French` | `"fr"` | ISO 639-1 |
| `PinMameRomLanguage.German` | `"de"` | ISO 639-1 |

## Files Produced

### Platform files (4)
- `platforms/bally.json`
- `platforms/sam.json`
- `platforms/system80.json`
- `platforms/wpc.json`

### Game files (11)
- `games/afm.json`
- `games/centaur.json`
- `games/cftbl.json`
- `games/fg.json`
- `games/mm.json`
- `games/rock.json`
- `games/rock_enc.json`
- `games/star-trek-stern.json`
- `games/t2.json`
- `games/trn.json`
- `games/twd.json`

