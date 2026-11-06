"""Embryon's reviewed main lamp mapping and source-literal auxiliary mapping."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "tools/seeds/bally/embryon-1981-lamps.json"
SEED_SHA256 = "badc09fe0d8f83f150c03dcb512b4467b08eb693d0f02392fe20cffd6e854816"
A5 = "schematic.embryon.a5"
A9 = "schematic.embryon.a9"
WIRING = "schematic.embryon.w1255"


def build_lamps(item, na, provenance) -> list[dict]:
    payload = SEED.read_bytes()
    if hashlib.sha256(payload).hexdigest() != SEED_SHA256:
        raise ValueError("Embryon lamp seed changed")
    data = json.loads(payload)
    main = data["main"]
    expected = {n for base in (1, 17, 33, 49) for n in range(base, base + 15)}
    if {int(n) for n in main["labels"]} != expected:
        raise ValueError("Embryon main-lamp table is incomplete")
    aux = {row["public_lamp"]: row for row in data["aux"]}
    result = []
    for base in (1, 17, 33, 49, 65, 81, 97, 113):
        for n in range(base, base + 15):
            if n < 65:
                unused = n in main["unused"]
                kind = "virtual" if unused else "flasher" if n == 56 else "lamp"
                d = item("lamp", n, main["labels"][str(n)], kind,
                         "unknown" if unused else "used", (A5,))
                d["provenance"] = provenance(A5, "pinmame.embryon", "vpx.embryon.modern", status="validated")
                d["wiring"] = {"board": "A5", "driver_transistor": data["main_scr"][str(n)]}
                if unused:
                    d["spatial"] = na("no_physical_device", A5)
                    d["physical"] = {"notes": "The schematic marks this load N/U. Native traces nevertheless publish it outside diagnostics, and that firmware use is not established; public availability remains unknown."}
                    d["provenance"]["status"] = "observed"
                    d["provenance"]["source_refs"].append("runtime.embryon.solenoid")
                    d["provenance"]["source_refs"].append("runtime.embryon.flippers")
                elif n in main["backbox_only"]:
                    d["spatial"] = na("cabinet_or_service", A5)
                elif n == 56:
                    d["physical"] = {"quantity": 5, "notes": "A5J3-2 feeds A10J1-3 in W-1192-29c despite the A5 board's N/U label. Circuit 56 has four #921 flasher lamps and one #44 lamp in the A10 control circuit. The #44 lamp's purpose, visibility and socket location are unknown; emitter positions remain unverified."}
                    d["wiring"]["drive_connection"] = "A5J3-2 to A10J1-3"
                    d["provenance"] = provenance(A5, "manual.embryon.color", "pinmame.embryon", "vpx.embryon.modern", status="validated")
                elif n == 59:
                    d["physical"] = {"location": "Apron credit indicator"}
                result.append(d)
                continue
            row = aux.get(n)
            if row is None:
                d = item("lamp", n, f"Auxiliary selector {n} (emulator alias unresolved)",
                         "virtual", "unknown", (A9,))
                d["physical"] = {"notes": "A9 has no AD3 input, so hardware aliases this selector while PinMAME retains a distinct matrix bit; public semantics remain unresolved."}
                d["spatial"] = na("no_physical_device", A9)
            elif row["literal_load"] == "N/U":
                d = item("lamp", n, f"Auxiliary output {n} unfitted", "virtual", "unknown" if n == 117 else "unused", (A9, "pinmame.embryon", "runtime.embryon.solenoid", "runtime.embryon.flippers"))
                d["provenance"]["status"] = "validated"
                d["spatial"] = na("no_physical_device" if n == 117 else "unused", A9)
                d["physical"] = {"notes": "No fitted load. Selector 7 has no SCR on any A9 group; by35_lampStrobe suppresses only selector 15 and captures shared data writes on the physically blank selector 7, including startup and normal operation."}
                if n == 117:
                    d["provenance"]["status"] = "observed"
                    d["physical"]["notes"] = "Q26/J3-17 is N/U, but this public bit is active during boot and game start, not only diagnostics. Its firmware use remains unexplained, so availability is unknown."
            else:
                label = row["literal_load"]
                if n in (70, 86):
                    label = label.rsplit(" (", 1)[0]
                d = item("lamp", n, label, "lamp", "used", (A9, WIRING))
                d["provenance"] = provenance(A9, WIRING, "pinmame.embryon", status="validated")
                d["wiring"] = {"board": "A9", "driver_transistor": row["scr"],
                               "drive_connection": f"{row['connector']}-{row['pin']}"}
                if n in (70, 86):
                    d["physical"] = {"notes": "A9 labels right/left quantities 2/1; W-1255 labels them 1/2. The fitted counts are unresolved pending an owner circuit trace."}
                    d["provenance"] = provenance(A9, WIRING, status="conflicted")
                elif n in (87, 102):
                    d["physical"] = {"quantity": 2 if n == 87 else 1}
            result.append(d)
    return result
