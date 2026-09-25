"""PinMAME flipper-column inputs (public 81-88) for System 9/11 and Data East definitions.

These platforms run the flippers from the cabinet with no ``FLIP_SOL``, and ``core_updateSw``
(``src/wpc/core.c``) keeps the cabinet flipper buttons in PinMAME's own flipper switch column,
``CORE_FLIPPERSWCOL`` (internal column 11), which ``core_swSeq2m(n) = n + 7`` publishes at 81-88. With
keyboard handling off it reads the two lower button bits (82, 84) as the host wrote them, copies them
into the matrix switches named by ``FLIP_SWNO(l, r)`` on every update, and fabricates the synthetic
flipper outputs 45-48 from them. The end-of-stroke and upper-button bits join that copy only when
``hw.flippers`` sets ``FLIP_EOS`` or an upper ``FLIP_SW`` bit, which no driver on these platforms does,
and the ROM cannot read column 11 itself: ``s11.c``'s ``pia4a_r`` reads the matrix only through
``core_getSwCol`` with an eight-bit column strobe, which reaches columns 1-8.

The builder is a literal, side-effect-free helper shared by the deterministic curators, so the
contract reads identically on every machine. Each curator supplies what differs: its ``FLIP_SWNO``
pair, the evidence it cites, and what its own known-working script does with the addresses.
"""

from __future__ import annotations

from typing import Any


GROUP = "pinmame.input.switch"

# The VPinMAME script library that System 9/11 known-working tables load through LoadVPM "S11.VBS",
# retained once under a machine-neutral path (review-artifacts/vpm-script-libs/README.md).
VPM_LIBRARY_SOURCE = "vpm-script-library.s11-vbs"
VPM_LIBRARY_URI = "external:pinmame-review-artifacts/vpm-script-libs/s11.vbs"
VPM_S11_SHA256 = "5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"


def vpm_staged_flipper_notes(*, disabled_at: dict[int, str] | None = None) -> dict[int, str]:
	"""Sentences for 81/83, which S11.VBS names swURFlip/swULFlip and writes from staged flipper keys.

	``disabled_at`` maps 81/83 to the script locator where the table calls the matching
	``NoUpper*Flipper``, for a table that clears the solenoid number and so never writes the address.
	"""
	disabled_at = disabled_at or {}
	return {
		address: (
			f"S11.VBS names this address {constant}; its vpmKeyDown/vpmKeyUp write it from a staged {side}-flipper key "
			f"only while vpmFlips.FlipperSolNumber({index}) is non-zero, which core.vbs makes the default "
			+ (
				f"({default}). The retained script calls {opt_out} ({disabled_at[address]}), which sets it to 0, so this "
				"table never writes the address."
				if address in disabled_at else
				f"({default}) unless the table calls {opt_out}."
			)
			+ " The constant does not follow the PinMAME column, and the ROM cannot read the address on this "
			"machine, so any such write has no effect."
		)
		for address, constant, side, index, default, opt_out in (
			(81, "swURFlip", "right", 3, "sURFlipper = 34", "NoUpperRightFlipper"),
			(83, "swULFlip", "left", 2, "sULFlipper = 36", "NoUpperLeftFlipper"),
		)
	}

# (address, core.h bit constant, bit value, position, side, kind)
_COLUMN = (
	(81, "CORE_SWLRFLIPEOSBIT", 0x01, "Lower Right", "right", "eos"),
	(82, "CORE_SWLRFLIPBUTBIT", 0x02, "Lower Right", "right", "button"),
	(83, "CORE_SWLLFLIPEOSBIT", 0x04, "Lower Left", "left", "eos"),
	(84, "CORE_SWLLFLIPBUTBIT", 0x08, "Lower Left", "left", "button"),
	(85, "CORE_SWURFLIPEOSBIT", 0x10, "Upper Right", "right", "eos"),
	(86, "CORE_SWURFLIPBUTBIT", 0x20, "Upper Right", "right", "button"),
	(87, "CORE_SWULFLIPEOSBIT", 0x40, "Upper Left", "left", "eos"),
	(88, "CORE_SWULFLIPBUTBIT", 0x80, "Upper Left", "left", "button"),
)
FLIPPER_COLUMN_ADDRESSES = tuple(entry[0] for entry in _COLUMN)
LOWER_BUTTON_ADDRESSES = {"right": 82, "left": 84}


def flipper_column_id(address: int) -> str:
	return f"switch.flipper-column-{address}"


def _provenance(*refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(refs)}


def flipper_column_inputs(
	*,
	flip_swno: tuple[int, int],
	flip_swno_text: str,
	core_refs: tuple[str, ...],
	button_refs: tuple[str, ...],
	button_notes: dict[str, str],
	unused_notes: dict[int, str] | None = None,
	unused_note_refs: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
	"""Return the eight flipper-column inputs for a driver declaring ``FLIP_SWNO(left, right)``.

	``flip_swno`` is ``(left, right)`` in the driver's own macro order. ``core_refs`` cite the
	pinned PinMAME core and the controller profile; ``button_refs`` add whatever evidence shows a
	known-working consumer driving 82/84. ``button_notes`` maps ``"left"``/``"right"`` to the
	machine-specific closing sentence for that button, and ``unused_notes`` may add a sentence to an
	unused position, citing ``unused_note_refs`` in addition to ``core_refs``.
	"""
	left, right = flip_swno
	matrix = {"left": left, "right": right}
	unused_notes = unused_notes or {}
	items: list[dict[str, Any]] = []
	for address, constant, bit, position, side, kind in _COLUMN:
		base = (
			f"PinMAME flipper switch column (CORE_FLIPPERSWCOL, internal column 11), bit {constant} = 0x{bit:02X}, "
			f"published at {address} through core_swSeq2m(n) = n + 7."
		)
		if address in LOWER_BUTTON_ADDRESSES.values():
			notes = (
				f"{base} This is the {position.lower()} cabinet flipper button as the ROM receives it. The driver "
				f"declares {flip_swno_text} with no FLIP_SOL, so with keyboard handling off (the LibPinMAME default) "
				"core_updateSw reads this bit as the host wrote it and, on every update, copies it into matrix "
				f"switch {matrix[side]} through core_setSw and fabricates the synthetic "
				f"{'45/46' if side == 'right' else '47/48'} flipper outputs from it while the switched-solenoid "
				f"enable is on. Drive this address, not {matrix[side]}: a host write to {matrix[side]} is "
				f"overwritten on the next update. {button_notes[side]}"
			).rstrip()
			items.append({
				"id": flipper_column_id(address),
				"label": f"{position} Flipper Button (PinMAME Flipper Column)",
				"kind": "switch",
				"binding": {"group": GROUP, "device": address},
				"availability": "used",
				"provenance": _provenance(*core_refs, *button_refs),
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"roles": [f"flipper.lower.{side}.button"],
				"physical": {"location": "cabinet flipper button", "switch_type": "button", "notes": notes},
				"spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": _provenance(*core_refs)},
			})
			continue
		if kind == "eos":
			reason = (
				f"locals.flipMask carries this end-of-stroke bit only when hw.flippers sets FLIP_EOS (implied by "
				f"FLIP_SOL), and {flip_swno_text} sets neither, so core_updateSw neither synthesizes it nor copies it "
				"anywhere: PinMAME models no end-of-stroke switch on this machine."
			)
		else:
			reason = (
				"core_updateSw copies only the two lower button bits into the matrix and the synthetic outputs; this "
				f"upper-button bit would join locals.flipMask only if hw.flippers set the matching upper FLIP_SW bit, "
				f"and {flip_swno_text} sets FLIP_SW(FLIP_L) only."
			)
		reason += (
			" A host write survives in the column, but the ROM cannot read it there: s11.c's pia4a_r reads the "
			"switch matrix only through core_getSwCol with an eight-bit column strobe, which reaches columns 1-8."
		)
		notes = f"{base} {reason}"
		refs = core_refs
		if address in unused_notes:
			notes += f" {unused_notes[address]}"
			refs = (*core_refs, *unused_note_refs)
		items.append({
			"id": flipper_column_id(address),
			"label": f"Unused Flipper Column {position} {'End-of-Stroke' if kind == 'eos' else 'Button'} ({address})",
			"kind": "switch",
			"binding": {"group": GROUP, "device": address},
			"availability": "unused",
			"provenance": _provenance(*refs),
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"physical": {"location": "internal public address space", "switch_type": "other", "notes": notes},
			"spatial": {"status": "not_applicable", "reason": "unused", "provenance": _provenance(*core_refs)},
		})
	return items


def flipper_column_relationships(*, flip_swno: tuple[int, int], matrix_ids: dict[int, str], refs: tuple[str, ...]) -> list[dict[str, Any]]:
	"""Return the two proven copies core_updateSw makes from 82/84 into the FLIP_SWNO matrix switches."""
	left, right = flip_swno
	return [
		{
			"id": f"relationship.flipper-column-{button}-to-matrix-{target}",
			"kind": "direct",
			"source": flipper_column_id(button),
			"destination": matrix_ids[target],
			"provenance": _provenance(*refs),
		}
		for button, target in ((82, right), (84, left))
		if target
	]
