from __future__ import annotations

import json
import unittest
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
VPXTABLE_REPOSITORY = "https://github.com/sverrewl/vpxtable_scripts"
VPXTABLE_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
STANDALONE_REPOSITORY = "https://github.com/jsm174/vpx-standalone-scripts"
STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"


# Every retained script whose exact bytes are in one of the curated GitHub
# corpora. Keep this table intentionally explicit: changing a source hash,
# revision, repository, or path requires an evidence review rather than a
# silent link rewrite.
PINNED_SCRIPTS = {
	"092611fc754374d11d032b81b63638b5a2dc2f43464ee6c7c3cd27874c77e5c3": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "special_audiopan_and_audiofade_patched/Mustang (Stern 2014) v1.27.vbs"),
	"1bbcc5873a1db87fe59d1daefbb69b68872cf58f029320a9d7d9410db7c59d97": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Terminator 2 (Williams 1991).vbs"),
	"1c6bc48c74e7bb8e48293152ee226318a9a8dce230bd6b63554f9c92075dbff0": (STANDALONE_REPOSITORY, STANDALONE_REVISION, "Batman [The Dark Knight] (Stern 2008) 1.16/Batman [The Dark Knight] (Stern 2008) 1.16.vbs"),
	"2441d88ab8aef581fcdef3dd5c0b9523a36feb3ce4afb6133811f1f01b381afb": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "X-Men(ICPjuggla)6-27c.vbs"),
	"245b996baedb9e0ebb9fb6f986c17feb0d5ede66e214896b08621205d37015bb": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Kiss (Bally 1979) v2.0.0.vbs"),
	"3337481b28144a67f1df3c3650355be91699104930d8b3cc8503e14225a9d4ff": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "special_audiopan_and_audiofade_patched/Star Trek LE (Stern 2013) v1.10.vbs"),
	"37cf4e41a6dc9772968cc8a1b13797e7ffb6f504d7e43cd15a6bb12926e9ae3d": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Funhouse (Williams 1990).vbs"),
	"3ba739ba81a3f1cad3b1a2b3a7cf7ea8db76eaf1baf4998c920f5a3d361c5ef7": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Ripley's Believe It or Not! (Stern 2004) VPWmod v1.3.vbs"),
	"3be5af3f6b05c4f1445c391aab42713bf9e76af87d563bfb061e7bc5daedfd64": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Metallica Premium Monsters (Stern 2013) VPW 2.0.2.vbs"),
	"3d885c099bb54fe2bf67405bb35562b68d775748d7d76192b01f30c133e0ff36": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Spider-Man_VE_2.2.vbs"),
	"6d0de2bcea486250133d52ba042e8eda168756d9061f5c9abd1ca0326736a440": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Kiss (Bally 1979)2.1.vbs"),
	"6d445e52398640bd35a498553bb0ba32f1b9ce23e2964d0694c18ff2e9225650": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "X-Men LE (Stern 2012) VPW v1.0.6.vbs"),
	"6dbde0131a367c643ae87fe511052d28d83ed0cb6b74b87ba731a900678f1849": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Ali-v1.0.1.vbs"),
	"756dadd23ad0dd8cadd3cb98d25553a27788230cc3f8fe04ee39c7a7effce37c": (STANDALONE_REPOSITORY, STANDALONE_REVISION, "Iron Man Vault Edition (Stern 2010) VPW v1.0/Iron Man Vault Edition (Stern 2010) VPW v1.0.vbs"),
	"7bf550806bd87c17417a974ed75b1700885da883e0dce5ce31d7dc7ba6cc094f": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "24 (Stern 2009) v.2.3.1.vbs"),
	"85ea928246dbdf4b59a73e5237b6d248970770d3146381b06a1620c92cba21e8": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Avengers (Stern 2012)4k1.3.1.vbs"),
	"88101e2184729f952d196fdfe5885f9d7e81ec211b7b1b675d724419fcb6a7f1": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "AC-DC Pro Vault-1.0 Lighting Bug Fix.vbs"),
	"8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Avatar (Stern 2012) v1.12 LW_VPUMod.vbs"),
	"969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "The Rolling Stones LE (Stern 2011) v1.0.6i.vbs"),
	"987b8cae80fbe6cb00c652507fba2eaf422afef8a57852a7e4c59d5b3f9e157b": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Transformers Pro (Stern 2011) v.2.3.1.vbs"),
	"b478b21272befd41908aa3ef4daf3a90d4838334346718cb4d5fde7f23bb2fc0": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "AC-DC LUCI Premium VR (Stern 2013) v1.1.4.vbs"),
	"bd6868c93f180c58f6835cccd869c0fa1e28832fea6afc5bb4f9660505908e47": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "The Walking Dead LE Premium (Stern 2014) day 1.1.vbs"),
	"c6da231a360a0f062fa5b434d08faca3c1b7b6a5436cc51b5b54dac924e1a3b4": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "JPs Avengers Classic LE (Stern - 2012) v600.vbs"),
	"cf34b7ccad9aa3bac58b0338914315fa97f74479d52914037b42921e113bb237": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Spider-Man_3.0.vbs"),
	"d0d37548468d67aa895121fd6ff82fdacc1d1a301a702c92325fb3ee9d7a89ea": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Iron Man Vault Edition (Stern 2010) VPW v1.0.1.vbs"),
	"d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Tron Legacy LE (Stern 2011) VPMmod v1.1.4.vbs"),
	"e0fdef84892ea8bce6eae179509ac8262f103bac0173c2e822a4fe10aafcf7fa": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "AC-DC Pro-1.0 Lighting Bug Fix.vbs"),
	"f6c3d5ec0aa95bb6c3ac3160b35adff9a6b1c6d282e64e15a3709f426f08949a": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Terminator 2 (Williams 1991) g5k v1.1a.vbs"),
	"fe7d56aa0c8336f16181fdaf8a2ca51aa9da4f0d7956af288e42145565d16275": (VPXTABLE_REPOSITORY, VPXTABLE_REVISION, "Flash Gordon (Bally 1981) VPW Mod v3.1.3.vbs"),
}

LINE_ENDING_VARIANTS = {
	"756dadd23ad0dd8cadd3cb98d25553a27788230cc3f8fe04ee39c7a7effce37c": "dd8697bcde0a980244163d044d60269f42f1c5f5e6d76fbc2c39a03c50ab4da2",
	"1c6bc48c74e7bb8e48293152ee226318a9a8dce230bd6b63554f9c92075dbff0": "b98e2ffa70c947438c441ca708743e7409f240ecb30c8c29ab364c72f12467f3",
}


def pinned_records() -> list[dict[str, object]]:
	records: list[dict[str, object]] = []
	for path in (ROOT / "machines").rglob("*.json"):
		definition = json.loads(path.read_text(encoding="utf-8"))
		if definition["coverage"]["status"] == "stub":
			continue
		for source in definition.get("sources", []):
			if source.get("kind") == "vpx_script" and "/blob/" in source.get("uri", "") and source["uri"].startswith((VPXTABLE_REPOSITORY, STANDALONE_REPOSITORY)):
				records.append(source)
	return records


class PinnedVpxScriptLinkTests(unittest.TestCase):
	def test_all_github_vpx_script_records_are_exact_pinned_blobs(self) -> None:
		records = pinned_records()
		self.assertTrue(records)
		self.assertEqual(set(PINNED_SCRIPTS), {record["sha256"] for record in records})
		for record in records:
			repository, revision, relative_path = PINNED_SCRIPTS[record["sha256"]]
			self.assertEqual(revision, record["revision"], record["id"])
			self.assertEqual(f"{repository}/blob/{revision}/{quote(relative_path, safe='/')}", record["uri"], record["id"])

	def test_checkout_line_ending_variants_are_explicit(self) -> None:
		for record in pinned_records():
			expected_blob_sha256 = LINE_ENDING_VARIANTS.get(record["sha256"])
			if expected_blob_sha256 is None:
				continue
			locator = record["locator"]
			self.assertIn("CRLF materialization", locator, record["id"])
			self.assertIn("LF-normalized text", locator, record["id"])
			self.assertIn(expected_blob_sha256, locator, record["id"])


if __name__ == "__main__":
	unittest.main()
