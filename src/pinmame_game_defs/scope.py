from __future__ import annotations


# PinMAME exposes these custom ROMs, but they exist only for community virtual
# tables and do not represent manufactured or buildable physical machines.
OUT_OF_SCOPE_DRIVER_REASONS = {
	"acd_170_ac": "American Country VPX-only AC/DC reskin",
	"beachbms": "Beach Bums VPX-only Hollywood Heat reskin",
	"beav_butt": "Beavis and Butt-Head VPX-only Class of 1812 reskin",
	"bubba": "Bubba the Redneck Werewolf VPX-only Hollywood Heat reskin",
	"che_cho": "Cheech & Chong Road-Trip'pin virtual original",
	"rambo": "Rambo VPX-only Raven reskin",
	"tomjerry": "Tom & Jerry VPX-only Hollywood Heat reskin",
}
OUT_OF_SCOPE_DRIVER_IDS = frozenset(OUT_OF_SCOPE_DRIVER_REASONS)
_OUT_OF_SCOPE_DRIVER_CASEFOLDS = frozenset(driver_id.casefold() for driver_id in OUT_OF_SCOPE_DRIVER_IDS)


def is_in_scope_driver(driver_id: str) -> bool:
	return driver_id.casefold() not in _OUT_OF_SCOPE_DRIVER_CASEFOLDS
