from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .errors import DefinitionError


RUNTIME_DOMAINS = {
	"controller_address",
	"controller_callback",
	"ball_routing",
	"mechanism_causality",
	"runtime_initial_state",
}
PHYSICAL_DOMAINS = {
	"assembly",
	"geometry",
	"part_number",
	"physical_polarity",
	"physical_wiring",
	"voltage",
}
EMULATOR_DOMAINS = {
	"controller_transport",
	"display_topology",
	"emulator_routing",
	"output_type",
}
SUPPORTED_DOMAINS = RUNTIME_DOMAINS | PHYSICAL_DOMAINS | EMULATOR_DOMAINS


class EvidenceConflict(DefinitionError):
	pass


@dataclass(frozen=True, slots=True)
class EvidenceAssertion:
	value: Any
	source_ref: str
	source_kind: str
	known_working: bool = False


@dataclass(frozen=True, slots=True)
class EvidenceDecision:
	value: Any
	selected_source_refs: tuple[str, ...]
	discarded_source_refs: tuple[str, ...]
	priority: int


def evidence_priority(domain: str, assertion: EvidenceAssertion) -> int:
	"""Return a domain-specific precedence score; larger values win.

	A VPX script receives runtime authority only when it is identified as a known-working
	table. This prevents an arbitrary scraped script from silently overruling stronger
	evidence while preserving the project rule that proven VPX behavior is the runtime
	tie-breaker when sources disagree.
	"""
	if domain not in SUPPORTED_DOMAINS:
		raise ValueError(f"Unsupported evidence domain: {domain!r}")
	if domain in RUNTIME_DOMAINS:
		if assertion.source_kind == "vpx_script" and assertion.known_working:
			return 400
		return {"runtime_scenario": 350, "human_review": 325, "manual": 300, "pinmame_core": 250, "vpx_script": 200, "legacy_json": 100}.get(assertion.source_kind, 0)
	if domain in PHYSICAL_DOMAINS:
		return {"service_bulletin": 450, "manual": 400, "human_review": 350, "vpx_script": 200, "pinmame_core": 150, "legacy_json": 100}.get(assertion.source_kind, 0)
	return {"pinmame_core": 400, "service_diagnostic": 350, "runtime_scenario": 300, "vpx_script": 200, "manual": 150, "legacy_json": 100}.get(assertion.source_kind, 0)


def decide_evidence(domain: str, assertions: Iterable[EvidenceAssertion]) -> EvidenceDecision:
	items = list(assertions)
	if not items:
		raise ValueError("At least one evidence assertion is required")
	priorities = [(evidence_priority(domain, assertion), assertion) for assertion in items]
	winning_priority = max(priority for priority, _ in priorities)
	winners = [assertion for priority, assertion in priorities if priority == winning_priority]
	first_value = winners[0].value
	if any(assertion.value != first_value for assertion in winners[1:]):
		sources = ", ".join(assertion.source_ref for assertion in winners)
		raise EvidenceConflict(f"Equal-priority evidence disagrees for {domain}: {sources}")
	selected = tuple(dict.fromkeys(assertion.source_ref for assertion in winners))
	discarded = tuple(dict.fromkeys(assertion.source_ref for priority, assertion in priorities if priority < winning_priority))
	return EvidenceDecision(first_value, selected, discarded, winning_priority)
