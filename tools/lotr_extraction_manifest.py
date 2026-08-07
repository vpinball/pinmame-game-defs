"""Write and verify reproducible manifests for the three retained LOTR extractions.

The manifest algorithm is defined here rather than assumed, so the recorded digest can be
recomputed by anyone holding the same extraction:

  1. Walk the extraction directory and take every regular file.
  2. Record its path relative to that directory as a POSIX string, its byte size, and its
     SHA-256, sorted by path.
  3. Serialise the resulting object as canonical JSON (sorted keys, no insignificant
     whitespace) and take the SHA-256 of those bytes.

Nothing here is hard-coded: the digest in the machine definition is whatever this produces.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

def _evidence_root() -> Path:
    """Resolve the retained VPX sources root: PINMAME_VPX_SOURCES_ROOT, else the runbook's
    sibling working directory. Nothing here writes into the repository."""
    override = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if override:
        return Path(override) / "stern" / "lord-of-the-rings-2003"
    # Walk up until the runbook's sibling working directory is found, so this resolves the same
    # way from the main checkout and from a per-game worktree.
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "pinmame-game-defs-working-dir" / "vpx-sources"
        if candidate.is_dir():
            return candidate / "stern" / "lord-of-the-rings-2003"
    raise SystemExit(
        "Cannot locate the retained VPX sources. Set PINMAME_VPX_SOURCES_ROOT to the vpx-sources root."
    )


# Resolved lazily, below, and only after the mode has been validated. Resolving it at import time
# made the tool report "Cannot locate the retained VPX sources" for an unknown mode when run
# outside the working-dir tree - so the fail-closed mode check was unreachable on exactly the
# checkout a maintainer would have, which is where it matters most.


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build(root: Path) -> dict:
    entries = []
    total = 0
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        size = path.stat().st_size
        total += size
        entries.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": size,
            "sha256": file_sha256(path),
        })
    return {
        "format": "pinmame-vpx-extraction-manifest",
        "version": 1,
        "algorithm": (
            "every regular file under the extraction root, path relative and POSIX, with byte size and SHA-256, "
            "sorted by path; the manifest digest is the SHA-256 of this object serialised as canonical JSON with "
            "sorted keys and compact separators"
        ),
        "file_count": len(entries),
        "total_bytes": total,
        "files": entries,
    }


def canonical(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


# Fail closed. This tool writes into the external, read-only evidence root, so verifying is the
# default and writing must be asked for explicitly by exact name. Anything else is an error
# rather than a silent overwrite of the pinned manifests.
mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
if mode not in {"--verify", "--write"}:
    raise SystemExit(f"unknown mode {mode!r}; expected --verify (default) or --write")

BASE = _evidence_root()
EXTRACTIONS = {
    "vpx-extraction.lotr-vpw-1-6": BASE / "vpxtool-extract",
    "vpx-extraction.lotr-jpsalas-600": BASE / "alt-jpsalas-600" / "vpxtool-extract",
    "vpx-extraction.lotr-hanibal-4k": BASE / "alt-hanibal-4k" / "vpxtool-extract",
}
failures = 0
for source_id, root in EXTRACTIONS.items():
    if not root.is_dir():
        print(f"{source_id}: extraction missing at {root}")
        failures += 1
        continue
    manifest = build(root)
    digest = hashlib.sha256(canonical(manifest)).hexdigest()
    out = root.parent / "extraction-manifest.json"
    if mode == "--verify":
        if not out.is_file():
            print(f"{source_id}: manifest missing at {out}")
            failures += 1
            continue
        recorded = json.loads(out.read_text(encoding="utf-8"))
        recomputed = hashlib.sha256(canonical({k: v for k, v in recorded.items() if k != "manifest_sha256"})).hexdigest()
        same = recorded.get("manifest_sha256") == recomputed == digest
        print(f"{source_id}: {'OK' if same else 'DRIFT'} files={manifest['file_count']} digest={digest}")
        failures += 0 if same else 1
    else:
        payload = dict(manifest)
        payload["manifest_sha256"] = digest
        out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
        print(f"{source_id}: files={manifest['file_count']:5d} bytes={manifest['total_bytes']:,} digest={digest}")
sys.exit(1 if failures else 0)
