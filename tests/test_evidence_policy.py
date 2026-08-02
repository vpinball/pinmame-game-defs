from __future__ import annotations

import unittest

from pinmame_game_defs.evidence_policy import EvidenceAssertion, EvidenceConflict, decide_evidence


class EvidencePolicyTests(unittest.TestCase):
	def test_known_working_vpx_wins_runtime_disagreement(self) -> None:
		decision = decide_evidence(
			"controller_address",
			[
				EvidenceAssertion(22, "manual.page-18", "manual"),
				EvidenceAssertion(24, "vpx.known-table", "vpx_script", known_working=True),
				EvidenceAssertion(22, "pinmame.core", "pinmame_core"),
			],
		)
		self.assertEqual(24, decision.value)
		self.assertEqual(("vpx.known-table",), decision.selected_source_refs)

	def test_manual_wins_physical_wiring_disagreement(self) -> None:
		decision = decide_evidence(
			"physical_wiring",
			[
				EvidenceAssertion("J8-P8", "manual.page-18", "manual"),
				EvidenceAssertion("virtual-gate", "vpx.known-table", "vpx_script", known_working=True),
			],
		)
		self.assertEqual("J8-P8", decision.value)

	def test_human_review_can_support_mechanism_causality(self) -> None:
		decision = decide_evidence("mechanism_causality", [EvidenceAssertion("motor-drives-figure", "review.physical", "human_review")])
		self.assertEqual("motor-drives-figure", decision.value)
		self.assertGreater(decision.priority, 0)

	def test_pinmame_wins_display_topology_disagreement(self) -> None:
		decision = decide_evidence(
			"display_topology",
			[
				EvidenceAssertion((128, 32), "pinmame.sam", "pinmame_core"),
				EvidenceAssertion((256, 64), "vpx.color-upscale", "vpx_script", known_working=True),
			],
		)
		self.assertEqual((128, 32), decision.value)

	def test_unverified_vpx_cannot_claim_runtime_authority(self) -> None:
		decision = decide_evidence(
			"ball_routing",
			[
				EvidenceAssertion("manual-path", "manual.page-40", "manual"),
				EvidenceAssertion("script-path", "vpx.scraped", "vpx_script"),
			],
		)
		self.assertEqual("manual-path", decision.value)

	def test_equal_priority_disagreement_remains_a_conflict(self) -> None:
		with self.assertRaises(EvidenceConflict):
			decide_evidence(
				"controller_callback",
				[
					EvidenceAssertion(4, "vpx.table-a", "vpx_script", known_working=True),
					EvidenceAssertion(5, "vpx.table-b", "vpx_script", known_working=True),
				],
			)

	def test_equal_values_merge_source_references(self) -> None:
		decision = decide_evidence(
			"mechanism_causality",
			[
				EvidenceAssertion("switch-36-to-output-4", "vpx.table-a", "vpx_script", known_working=True),
				EvidenceAssertion("switch-36-to-output-4", "vpx.table-b", "vpx_script", known_working=True),
			],
		)
		self.assertEqual(("vpx.table-a", "vpx.table-b"), decision.selected_source_refs)


if __name__ == "__main__":
	unittest.main()
