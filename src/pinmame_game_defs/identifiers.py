from __future__ import annotations

import re
import unicodedata


def slug(value: object, fallback: str = "unnamed") -> str:
	text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii").casefold()
	text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
	return text or fallback


def unique_identifier(prefix: str, label: object, occupied: set[str], suffix: object | None = None) -> str:
	base = f"{prefix}.{slug(label)}"
	candidate = base
	if candidate in occupied and suffix is not None:
		candidate = f"{base}.{slug(suffix)}"
	index = 2
	while candidate in occupied:
		candidate = f"{base}.{index}"
		index += 1
	occupied.add(candidate)
	return candidate
