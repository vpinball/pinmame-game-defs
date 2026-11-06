"""Select portable facts from the retained, bounded WWF M6808 investigation.

The original archive stays immutable. This does not execute a ROM, claim complete
control-flow coverage, or export opcode bytes. Mnemonics, addresses, values and
digests are factual derived evidence; physical construction remains unknown.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = Path("data-east.wwf-royal-rumble.1994/session-20261106/parent-configuration-input")
OUTPUT = ROOT / "tools/wwf_static_evidence.json"
MEMBERS = {"wwfcpua.106": "wwfr_106", "wfcpuc5.512": "wwfr_103", "wwfcpuf.103": "wwfr_103f"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify_archive(base):
    manifest = read(base / "SHA256SUMS.json")
    paths = [row["path"] for row in manifest]
    actual = {p.relative_to(base).as_posix() for p in base.rglob("*")
              if p.is_file() and p.name != "SHA256SUMS.json"}
    if len(paths) != 23 or len(set(paths)) != 23 or set(paths) != actual:
        raise ValueError("Incomplete or duplicate WWF static-evidence manifest")
    for row in manifest:
        path = (base / row["path"]).resolve()
        if not path.is_relative_to(base.resolve()) or not path.is_file():
            raise ValueError("Missing WWF static artifact")
        if path.stat().st_size != row["size"] or sha(path) != row["sha256"]:
            raise ValueError(f"WWF static artifact drift: {row['path']}")
    return manifest


def instructions(record, low, high):
    """Select complete instruction records inside an explicitly reviewed region."""
    regions = [r for r in record["regions"] if int(r["start"], 16) <= low and int(r["end_exclusive"], 16) >= high]
    if len(regions) != 1:
        raise ValueError("Missing or ambiguous reviewed WWF instruction region")
    rows = [{k: d[k] for k in ("pc", "op", "mode", "size", "arg", "text")}
            for d in regions[0]["instructions"] if low <= d["pc"] < high]
    if not rows or rows[0]["pc"] != low or rows[-1]["pc"] + rows[-1]["size"] != high:
        raise ValueError("Incomplete WWF instruction boundary")
    return rows


def build(review_root):
    base = Path(review_root) / RELATIVE
    manifest = verify_archive(base)
    code = read(base / "focused-code-evidence.json")
    if set(code) != set(MEMBERS):
        raise ValueError("Incomplete WWF CPU family")
    shared = [code[m]["shared_region_digests"] for m in MEMBERS]
    if not all(rows == shared[0] for rows in shared):
        raise ValueError("WWF shared regions differ across variants")
    first = code["wwfcpua.106"]
    shared_rows = {
        "normal_pia_setup": instructions(first, 0x4585, 0x45A2),
        "irq_reads": instructions(first, 0x61A5, 0x61C1),
        "fatal_fault_setup_and_blink": instructions(first, 0x5EE7, 0x5F20),
    }
    printers = {}
    for member, game in MEMBERS.items():
        delta = 0 if member == "wwfcpua.106" else -0x85
        printers[game] = {"caller": instructions(code[member], 0xAEC5 + delta, 0xAED8 + delta),
                          "buffer_and_send": instructions(code[member], 0xB068 + delta, 0xB0CC + delta)}
    return {
        "machine_id": "data-east.wwf-royal-rumble.1994",
        "authority": "bounded static inference; no execution or physical jumper proof",
        "generator": "tools/build_wwf_static_evidence.py",
        "retained": {"relative_path": RELATIVE.as_posix(), "manifest_sha256": sha(base / "SHA256SUMS.json"),
                     "files": manifest},
        "inputs": [{"driver": MEMBERS[row["member"]], **row} for row in read(base / "rom-inputs.json")],
        "source_files": [{"path": row["relative_path"], "sha256": row["sha256"]}
                         for row in read(base / "source-evidence.json")["files"]],
        "shared_region_digests": shared[0], "shared_instructions": shared_rows,
        "printer_instructions": printers,
        "conclusions": [
            "Verified normal setup selects DDRA and writes 255, then selects PA; the 6821 direction mask removes external PA7.",
            "Reviewed IRQ PA read is overwritten; fatal blink setup uses DDRA 16 and only output bit4 survives the mask.",
            "The actual printer helper reads buffer 0A00 and writes PB only after CRA IRQ2 signals input CA2 readiness.",
            "Stock s11 PIA2 supplies CA1/CB1 service inputs but no CA2 ready transition. This explains timeout in the reviewed send path, not a whole-program unused-output claim.",
        ],
        "limitations": [
            "Direct-flow decoding assumes ordinary call returns; inline arguments, indexed transfers and the scheduler leave coverage gaps.",
            "No whole-program indexed-memory alias proof, printer protocol reconstruction, physical configuration identity or runtime printer transaction.",
            "REA verified ZIP inventory; raw M6808 was unsupported. The incompatible Ghidra 6809 alias was not used. Decoding uses the pinned M6808 opcode table.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-root", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(build(args.review_root), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != payload:
            raise ValueError("WWF static evidence drift")
    else:
        OUTPUT.write_bytes(payload)


if __name__ == "__main__":
    main()
