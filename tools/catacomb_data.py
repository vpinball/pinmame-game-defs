"""Pinned Catacomb raw evidence helpers, not a canonical definition curator.

The fixture preserves candidate manual transcriptions, source coordinates, and
script lines.  In particular, a light name alone does not establish a binding;
``mapped_lights`` uses the pinned AllLamps membership and timer interval.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

RAW_PATH = Path(__file__).resolve().parent / 'seeds/stern/catacomb-1981-raw.json'
RAW_SHA256 = 'a491af7965f303a4f850acd1ba1157a6ac2b8152fd4f66dbbb7ee597a217825c'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def load_raw(path: Path = RAW_PATH) -> dict:
    if sha256(path) != RAW_SHA256:
        raise ValueError(f'raw fixture hash mismatch: {path}')
    data = json.loads(path.read_text(encoding='utf-8'))
    validate_raw(data)
    return data


def validate_raw(data: dict) -> None:
    """Reject incomplete evidence; this does not validate a transcription."""
    expected = {str(n) for n in range(1, 64) if n % 16}
    if set(data['lamp_rows']) != expected:
        raise ValueError('lamp decoder rows are incomplete')
    rows = data['lamp_rows']
    if {int(k) for k, v in rows.items() if v['printed_table_row'] is None} != {2, 29}:
        raise ValueError('unexpected unnamed decoder rows')
    if len(data['manual']['pdf_18_switch_identification']) != 40:
        raise ValueError('manual switch table incomplete')
    members = data['collections']['AllLamps']
    lights = data['lights']
    if len(members) != len(set(name.casefold() for name in members)):
        raise ValueError('duplicate AllLamps member')
    if {x.casefold() for x in members} != {x['object'].casefold() for x in lights} or len(lights) != len(members):
        raise ValueError('light rows do not match mapped collection')
    if not any('vpmmaplights alllamps' in x['text'].casefold() for x in data['script_lines']):
        raise ValueError('script does not establish AllLamps mapping')
    gi = data['collections']['GIBulbPrims']
    mesh_names = {x['object'].casefold() for x in data['meshes']}
    if len(gi) != 21 or not all(n.casefold() in mesh_names for n in gi):
        raise ValueError('GI mesh collection incomplete')


def mapped_lights(data: dict, address: int) -> list[dict]:
    """Return the actual AllLamps members driven by the given timer value."""
    return [row for row in data['lights'] if row['timer_interval'] == address]


def mesh_center(row: dict) -> tuple[float, float]:
    """Center of the exported world bounds, in VPX units, before normalization."""
    return tuple((row['minimum'][i] + row['maximum'][i]) / 2 for i in (0, 1))


def normalize(data: dict, x: float, y: float) -> tuple[float, float]:
    bounds = data['table_bounds']
    result = (round((x - bounds['left']) / (bounds['right'] - bounds['left']), 6),
              round((y - bounds['top']) / (bounds['bottom'] - bounds['top']), 6))
    if not all(0 <= value <= 1 for value in result):
        raise ValueError(f'outside playfield: {x}, {y}')
    return result


def verify_sources(data: dict, *, vpx_root: Path | None = None, review_root: Path | None = None) -> None:
    """Verify every named source, item file, and stored OBJ mesh bound.

    A caller explicitly providing a root must see missing files or mismatches as
    errors. This intentionally does not inspect ROM bytes or write any files.
    """
    roots = {'vpx-sources': vpx_root, 'review-artifacts': review_root}
    if not any(roots.values()):
        raise ValueError('no evidence root supplied')
    for root in roots.values():
        if root is not None and not root.is_dir():
            raise ValueError(f'evidence root is not a directory: {root}')
    def source_path(source: dict) -> Path | None:
        path = Path(source['path'])
        root = roots[path.parts[0]]
        return root.joinpath(*path.parts[1:]) if root is not None else None
    for source in data['sources'].values():
        path = source_path(source)
        if path is not None and sha256(path) != source['sha256']:
            raise ValueError(f'source digest mismatch: {path}')
    if vpx_root is None:
        return
    gameitems = vpx_root / 'stern/catacomb-1981/vpu-2.0.1/extracted/gameitems'
    for row in data['lights'] + data['objects']:
        path = gameitems / row['file']
        if sha256(path) != row['file_sha256']:
            raise ValueError(f'game item digest mismatch: {path}')
    for source, rows in (('script', 'script_lines'), ('archive_script', 'archive_script_lines')):
        script = source_path(data['sources'][source]).read_text(encoding='utf-8-sig').splitlines()
        for row in data[rows]:
            if script[row['line'] - 1].strip() != row['text']:
                raise ValueError(f"{source} line changed: {row['line']}")
    obj_path = source_path(data['sources']['world_obj'])
    expected = {row['object']: row for row in data['meshes']}
    seen = {}
    current = None
    with obj_path.open(encoding='utf-8') as stream:
        for line in stream:
            if line.startswith('o '):
                current = line[2:].strip()
            elif line.startswith('v ') and current in expected:
                xyz = tuple(map(float, line.split()[1:4]))
                if current not in seen:
                    seen[current] = [list(xyz), list(xyz), 0]
                entry = seen[current]
                for i, value in enumerate(xyz):
                    entry[0][i] = min(entry[0][i], value)
                    entry[1][i] = max(entry[1][i], value)
                entry[2] += 1
    if set(seen) != set(expected):
        raise ValueError('OBJ mesh objects are missing')
    for name, row in expected.items():
        low, high, count = seen[name]
        if count != row['vertex_count'] or any(
            not math.isclose(a, b, rel_tol=0, abs_tol=1e-7)
            for a, b in zip(low + high, row['minimum'] + row['maximum'])
        ):
            raise ValueError(f'OBJ mesh bounds mismatch: {name}')
