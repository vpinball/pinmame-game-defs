# Exact runtime provenance and external manifest

```json
{
  "command_template": "python -B tools/guns_n_roses_harness.py --library <pinned builds/pinmame-8371478/Release/pinmame64.dll> --game gnr_300 --rom-path <read-only user ROM root> --work-dir <new isolated state> --scenario <committed scenario> --boot-wait 8 --dmd-dir <new snapshot directory> --output <raw run.json>",
  "executed_harness": {
    "executed-checkpoint-adapter.py": "e353928fe5298afd9ff6f7f79d89fa051943c8453b6ec289e062ada470bcbb01",
    "executed-generic-harness.py": "18ae798e99a9803541095920e4b71dbf87f467c0d6008041ebef5229c1416c59"
  },
  "format": "pinmame-runtime-provenance",
  "game": "gnr_300",
  "language": "US English 3.00",
  "library_sha256": "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e",
  "machine_id": "data-east.guns-n-roses.1994",
  "manifest": {
    "algorithm": "build_external_evidence_manifest.py: every sorted relative POSIX path with size and SHA256; UTF8 compact JSON object sorted keys, final newline; exclude manifest.json and manifest.sha256 only.",
    "directory": "external:pinmame-review-artifacts/data-east.guns-n-roses.1994/session-20260930/runtime",
    "sha256": "c1e2229d918477a290320c07cca742d6ea64e710255339c790fbc7ac8d0ff725"
  },
  "pinmame_revision": "8371478a7640f1896dcdf565aed340dc5df989ba",
  "rom": {
    "access": "Read-only user-supplied ROM root; no bytes copied or committed",
    "archive": "gnr_300.zip",
    "sha256": "1ade04ee7299e422f14c832fe03c4196b46518b1f08bdb5aea6491e4d2eb78e6"
  },
  "runs": [
    {
      "display_checkpoints": [
        "MAGNET TEST",
        "LASER KICK TEST",
        "SWITCH TEST"
      ],
      "expectations": "Start cycles raw37=51,38=52,39=53; switch54->14,37->4,39->5,38->6; hostleft->47/48,right->45/46",
      "raw": "magnet-laser-v2-run.json",
      "readiness": "Output23 assertion after transient Laser/Switch title, before stimulus",
      "scenario": "executed-magnet-laser-scenario.json",
      "scenario_sha256": "796cf62b4f327ba351ffc9f40ef785f186ea18567a00b4f7e5760852144505cf",
      "sha256": "3580db58380b3921102cebca406e924cf2d9dc210dc4f5988ac1cf3394939d0f",
      "state": "magnet-laser-v2-state"
    },
    {
      "display_checkpoints": [
        "ACTIVE SWITCH TEST"
      ],
      "raw": "active-switch-run.json",
      "readiness": "Output23 assertion after transient title",
      "scenario": "executed-active-switch-scenario.json",
      "scenario_sha256": "bf9332e7c239beb103603ab3e8e73c8407e22239dbe3750bcd6086aa116c4199",
      "screenshots": "Every held PGM and raw pixel hash retained in tools/guns_n_roses_active_switches.json",
      "sha256": "1ebefdf46827518e10ae6d098c99c6184877aa336a3c3bb531cae4d7a03d7cd9",
      "state": "active-switch-state"
    }
  ],
  "setup": {
    "boot_wait_s": 8,
    "handle_mechanics": 0,
    "initial_switches": [],
    "keyboard": "Named service keys enable shared DE input handling; direct states only outside keyboard-owned cabinet matrix",
    "reset": "Fresh separately named state directory for each evidentiary run; no imported NVRAM or exploratory state",
    "witness": "Primary curator created distinct previously absent magnet-laser-v2-state and active-switch-state paths; each raw run records its concrete state path. Exploratory states remain separate and are not used as evidence."
  },
  "version": 1
}
```
