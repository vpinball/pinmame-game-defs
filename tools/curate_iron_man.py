"""Build reviewed, author-ready Iron Man and Iron Man Pro Vault Edition definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import SPATIAL_RETROFIT_PENDING_MACHINE_IDS, fail_closed_spatial_knowledge, fail_closed_spatial_partial, spatial_partial_path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
DRIVERS = {driver["id"]: driver for driver in CATALOG["drivers"] if driver["id"].startswith("im_")}

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
VPX_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
STANDALONE_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
ORIGINAL_MANUAL_SOURCE = "manual.iron-man-original-parts.2010"
VE_MANUAL_SOURCE = "manual.iron-man-vault-edition.2014"
VPX_SOURCE = "vpx.iron-man-vault-vpw-1.0.1"
STANDALONE_VPX_SOURCE = "vpx.iron-man-vault-vpw-1.0"
ROM_SOURCE = "rom.iron-man-vault.im-185ve"
RUNTIME_SOURCE = "runtime.iron-man-vault.boot-start"
ORIGINAL_IPDB_SOURCE = "ipdb.iron-man.5550"
VE_IPDB_SOURCE = "ipdb.iron-man-vault-edition.6154"
PRESS_SOURCE = "human-review.stern.iron-man-is-back.2014"
CODE_COMPAT_SOURCE = "human-review.stern.iron-man-code-1.86"
CANDIDATE_REGISTER_PATH = ROOT / "evidence/vpx/source-candidate-register/stern/iron-man-2010.json"

IRON_MAN_ORIGINAL_EXCERPTS = [
	{"id": "excerpt.iron-man-original.playfield-parts", "locator": "IronMan-Manual.pdf PDF page 25, crop box 0.03,0.12,0.50,0.46; MISC. PARTS (ABOVE) items 1–2 and instruction-card illustration.", "path": "evidence/excerpts/stern.iron-man.2010/playfield-parts.md", "sha256": "0be9991d363d9c5fb29b28802922662e5414bf909411c69d483422ba85031b66", "image": "evidence/excerpts/stern.iron-man.2010/playfield-parts.webp", "image_sha256": "09c42f527c4bc68aa19345e2be70f815c704bd1529b81e00c19bc71002ae9a16", "image_derivation": "IronMan-Manual.pdf page 25, crop box 0.03,0.12,0.5,0.46, scanned page rendered at its native resolution (embedded image xref 108, 2584px across 8.61in), rendered at 175 dpi, capped to 700px wide, grayscale, 701x654 WebP quality 40", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.iron-man-original.playfield-parts-upper", "locator": "IronMan-Manual.pdf PDF page 25, crop box 0.03,0.08,0.50,0.48; upper continuation of the parts table and instruction-card drawing.", "path": "evidence/excerpts/stern.iron-man.2010/playfield-parts-upper.md", "sha256": "e80617096a39b15076d24c5bbd889c779158d564dc80fc08761fa5aa3159bcf6", "image": "evidence/excerpts/stern.iron-man.2010/playfield-parts-upper.webp", "image_sha256": "a3c6258a877f8ac400e406b96165f7a083e157616b0d0b7096899d23c960a5bd", "image_derivation": "IronMan-Manual.pdf page 25, crop box 0.03,0.08,0.5,0.48, scanned page rendered at its native resolution (embedded image xref 108, 2584px across 8.61in), rendered at 137 dpi, capped to 550px wide, grayscale, 551x605 WebP quality 30", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.iron-man-original.playfield-parts-lower", "locator": "IronMan-Manual.pdf PDF page 25, crop box 0.03,0.44,0.50,0.78; lower playfield parts and bracket table.", "path": "evidence/excerpts/stern.iron-man.2010/playfield-parts-lower.md", "sha256": "8cf638630382594ccaa5b054b480e2e97056b76052e1815301d228e545e6645f", "image": "evidence/excerpts/stern.iron-man.2010/playfield-parts-lower.webp", "image_sha256": "812f1470df6c4d15759af1ede1e636666849df631b561c9616e010de602ff8a6", "image_derivation": "IronMan-Manual.pdf page 25, crop box 0.03,0.44,0.5,0.78, scanned page rendered at its native resolution (embedded image xref 108, 2584px across 8.61in), rendered at 137 dpi, capped to 550px wide, grayscale, 551x515 WebP quality 30", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
]

IRON_MAN_VAULT_EXCERPTS = [
	{"id": "excerpt.iron-man-vault.switch-matrix", "locator": "IronMan_Vault_web.pdf PDF page 16, crop box 0.48,0.10,0.97,0.52, rotated 90° counter-clockwise; switch matrix columns 1–14 and rows Q1–Q4.", "path": "evidence/excerpts/stern.iron-man-vault-edition.2014/switch-matrix.md", "sha256": "ac1d0c889fe956817bbf7c6dd3afaca7731a9dc46817098ed4cd4c5d5ba6b69a", "image": "evidence/excerpts/stern.iron-man-vault-edition.2014/switch-matrix.webp", "image_sha256": "df669449240fd612fec103999465f357556e363421e892830762a64dab6fb879", "image_derivation": "IronMan_Vault_web.pdf page 16, crop box 0.48,0.1,0.97,0.52, born-digital page rendered for legibility (smallest type in region 5.5pt, targeting 11px glyphs), rendered at 143 dpi, grayscale, rotated 90 degrees counter-clockwise, 663x598 WebP quality 35", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.iron-man-vault.switch-matrix-left", "locator": "IronMan_Vault_web.pdf PDF page 16, crop box 0.04,0.10,0.52,0.84, rotated 90° counter-clockwise; Q4 continuation, dedicated switches D-1–D-24, and DIP positions D-25–D-30.", "path": "evidence/excerpts/stern.iron-man-vault-edition.2014/switch-matrix-left.md", "sha256": "b087e0f8c9a79b3063829f16f9fe9c0e2264dbaa004f4ab064da7c265e21e4a9", "image": "evidence/excerpts/stern.iron-man-vault-edition.2014/switch-matrix-left.webp", "image_sha256": "9e20dbaa0e790cefe1871a7b6af694074121fe26276de4090d154a15fe48e372", "image_derivation": "IronMan_Vault_web.pdf page 16, crop box 0.04,0.1,0.52,0.84, born-digital page rendered for legibility (smallest type in region 1.8pt, targeting 11px glyphs), rendered at 147 dpi, capped to 600px wide, grayscale, rotated 90 degrees counter-clockwise, 1198x600 WebP quality 25", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.iron-man-vault.switch-matrix-right", "locator": "IronMan_Vault_web.pdf PDF page 16, crop box 0.48,0.10,0.97,0.84, rotated 90° counter-clockwise; switch matrix continuation columns 1–14 and rows Q1–Q4.", "path": "evidence/excerpts/stern.iron-man-vault-edition.2014/switch-matrix-right.md", "sha256": "ef17fd60c87e71a3223f158cb4f642937fe62146b7ed713890a80865ec318f6b", "image": "evidence/excerpts/stern.iron-man-vault-edition.2014/switch-matrix-right.webp", "image_sha256": "b9ddf3b6d64af10f603ddccbc7e1d8e4cd8e3c42c98468520ea80d5d345e5581", "image_derivation": "IronMan_Vault_web.pdf page 16, crop box 0.48,0.1,0.97,0.84, born-digital page rendered for legibility (smallest type in region 5.5pt, targeting 11px glyphs), rendered at 143 dpi, grayscale, rotated 90 degrees counter-clockwise, 1168x598 WebP quality 25", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
	{"id": "excerpt.iron-man-vault.coil-table", "locator": "IronMan_Vault_web.pdf PDF page 20, crop box 0.08,0.05,0.94,0.84; complete Q1–Q32 coil/flasher table.", "path": "evidence/excerpts/stern.iron-man-vault-edition.2014/coil-table.md", "sha256": "5ae4e63d50101aecae2d8c45750716c9d5ca44a114848d01e0cb8e35f5b738c0", "image": "evidence/excerpts/stern.iron-man-vault-edition.2014/coil-table.webp", "image_sha256": "7b7fd31e3d4ebc9b236d93ce5929c0e40b6d03e5ed90967789f8ed699de382fe", "image_derivation": "IronMan_Vault_web.pdf page 20, crop box 0.08,0.05,0.94,0.84, born-digital page rendered for legibility (smallest type in region 5.5pt, targeting 11px glyphs), rendered at 106 dpi, capped to 1000px wide, grayscale, rotated 90 degrees counter-clockwise, 711x1001 WebP quality 50", "method": "manual", "transcribed_by": "curator, read from the rendered source crop", "reviewed": True},
]

VPX_CANDIDATE_SOURCES = [
	{
		"id": "vpx.candidate.tier1-im2-160",
		"kind": "vpx_table",
		"uri": "external:local-vpx-search/Visual Pinball/Tables/_tmp/iron man 080215a.vpx",
		"sha256": "eaada74973ecb1c320420b287d5dca4970a39a25bb5c1ea2a10372786c6e2958",
		"locator": "Tier 1 search candidate; vpxtool romname reports im2_160, which is not an in-scope original Iron Man driver. Rejected as an unsupported/non-target variant. Readable script extraction is retained at evidence:vpx/source-scripts/stern/iron-man-2010/tier1-tmp-im2-160.vbs.",
		"license": "NOASSERTION",
		"attribution": "Local user-provided VPX table; credits remain in the retained extraction",
		"original_filename": "iron man 080215a.vpx",
	},
	{
		"id": "vpx.candidate.tier1-jpsalas-ironman2",
		"kind": "vpx_table",
		"uri": "external:local-vpx-search/Visual Pinball/Tables/JP's IronMan 2 v3.0.vpx",
		"sha256": "8bf4c377be4240b1de4842d2d3324da7d6683de9ff59f393b86c0373fbdb9ed5",
		"locator": "Tier 1 search candidate; vpxtool romname reports im_186ve, while info show names the community JP's IronMan Armored Adventures table. Its script defaults to the Vault ROM and only comments the original im_186 binding; the description says its playfield was made by the table author. Rejected as a community retheme/unsupported virtual variant. Readable script extraction is retained at evidence:vpx/source-scripts/stern/iron-man-2010/tier1-jpsalas-ironman2.vbs.",
		"license": "NOASSERTION",
		"attribution": "JP and table authors credited in the retained extraction",
		"original_filename": "JP's IronMan 2 v3.0.vpx",
	},
	{
		"id": "vpx.candidate.tier1-vault-vpw",
		"kind": "vpx_table",
		"uri": "external:local-vpx-search/Visual Pinball/Tables/Iron Man Vault Edition (Stern 2010) VPW v1.0.vpx",
		"sha256": "c0abc5d90d77a4cf7c3f0455cff91d4f0b9f7e750264742b987e9ddb30ab7a4b",
		"locator": "Tier 1 search candidate; vpxtool romname reports im_185ve and the embedded script identifies Iron Man Vault Edition (Stern 2014). This is the known-working Vault Edition geometry source and is not eligible for original 2010 placement. Readable script extraction is retained at evidence:vpx/source-scripts/stern/iron-man-2010/tier1-vault-vpw.vbs.",
		"license": "NOASSERTION",
		"attribution": "VPW and table authors credited in the retained extraction",
		"original_filename": "Iron Man Vault Edition (Stern 2010) VPW v1.0.vpx",
	},
	{
		"id": "vpx.candidate.tier2-archive-im183ve",
		"kind": "vpx_table",
		"uri": "external:local-vpx-search/Visual Pinball/Tables Archive/Iron Man (Stern 2010).vpx",
		"sha256": "dd4cc46c3002645c9f8cf9905699caf3d14231e069a98f8c47f25a0c35944cb1",
		"locator": "Tier 2 search candidate; despite its filename and generic IronMan (Stern 2010) splash, vpxtool romname and the embedded script report im_183ve, the Vault Edition driver. Rejected for original-edition geometry. Readable script extraction is retained at evidence:vpx/source-scripts/stern/iron-man-2010/tier2-archive-iron-man.vbs.",
		"license": "NOASSERTION",
		"attribution": "Local user-provided VPX table; credits remain in the retained extraction",
		"original_filename": "Iron Man (Stern 2010).vpx",
	},
	{
		"id": "vpx.candidate.tier2-archive-pro-vault",
		"kind": "vpx_table",
		"uri": "external:local-vpx-search/Visual Pinball/Tables Archive/Iron Man (Pro Vault Edition) (Stern 2010).vpx",
		"sha256": "dd4cc46c3002645c9f8cf9905699caf3d14231e069a98f8c47f25a0c35944cb1",
		"locator": "Tier 2 search candidate; byte-identical to the adjacent archive Iron Man file and reports im_183ve, the Vault Edition driver. Rejected for original-edition geometry. Reuses the retained readable extraction at evidence:vpx/source-scripts/stern/iron-man-2010/tier2-archive-iron-man.vbs.",
		"license": "NOASSERTION",
		"attribution": "Local user-provided VPX table; credits remain in the retained extraction",
		"original_filename": "Iron Man (Pro Vault Edition) (Stern 2010).vpx",
	},
	{
		"id": "vpx.candidate.tier3-vpuniverse-8679-siggis",
		"kind": "vpx_table",
		"uri": "https://vpuniverse.com/files/file/8679-ironman-siggis-mod/",
		"sha256": "8e3e175161b8f6671188762b831f843c168b854aa5bf79fadde7f2946e727c96",
		"locator": "Required-order VPU candidate for the physical Stern 2010 table, retained externally as Ironman (Stern 2010) Siggis MOD 2.0.vpx (67,338,240 bytes). Its im_183ve binding is compatible code, not product-identity proof. The 309-point candidate report and readable script are retained in repository evidence. Accepted only as 2D shared-layout corroboration after manual and exact-table reconciliation; no construction, Z, height, or Vault-specific hardware is imported.",
		"license": "NOASSERTION",
		"attribution": "Siggi and the table authors credited by the VPU distribution",
		"original_filename": "Ironman (Stern 2010) Siggis MOD 2.0.vpx",
	},
	{
		"id": "vpx.candidate.tier4-vpforums-16172-francisco",
		"kind": "vpx_table",
		"uri": "https://www.vpforums.org/index.php?app=downloads&showfile=16172",
		"sha256": "aafb93a1f4d7c65baf6f6458a6e10c51757db0bc48e5e2c89b40ab794ac37df4",
		"locator": "Required-order VPF candidate for Iron Man (Stern 2010) 1.0, retained externally as the extracted 179,437,568-byte VPX. The source page and table metadata identify the physical 2010 product; the script explicitly says positions were rearranged according to Iron Man Vault and binds compatible im_186ve code. Its 419-point candidate report and readable script are retained in repository evidence. Accepted only as 2D shared-layout corroboration; construction remains controlled by the 2010 parts book.",
		"license": "NOASSERTION",
		"attribution": "freneticamnesic, 32assassin, francisco666, and credited table contributors",
		"original_filename": "Iron Man (Stern 2010)_Francisco666MOD_1.vpx",
	},
	{
		"id": "vpx.candidate.tier4-vpforums-16778-bigus",
		"kind": "vpx_table",
		"uri": "https://www.vpforums.org/index.php?app=downloads&showfile=16778",
		"sha256": "5802d8a326366d67b48c6d477b4225121e0c4c17e1ac22651eb27406f99a79c5",
		"locator": "Required-order VPF candidate for Iron Man (Stern 2010)_Bigus(MOD) 2.1, retained externally as the extracted 185,057,280-byte VPX. It descends from the VPF 16172 reconstruction, retains the same physical identity and im_186ve-compatible script, and adds later layout/physics/lighting changes. Its 436-point candidate report and readable script are retained in repository evidence. Accepted as corroboration, never as independent evidence for construction or unsupported 3D measurements.",
		"license": "NOASSERTION",
		"attribution": "Bigus1, freneticamnesic, 32assassin, francisco666, and credited table contributors",
		"original_filename": "Iron Man (Stern 2010)_Bigus(MOD)2.1.vpx",
	},
]

VPX_CANDIDATE_REGISTER = {
	"format": "pinmame-vpx-candidate-register",
	"version": 1,
	"machine_id": "stern.iron-man.2010",
	"search_order": ["Visual Pinball/Tables", "Visual Pinball/Tables Archive", "vpuniverse.com", "vpforums.org"],
	"vpxtool": {"version": "git:v0.33.3", "operation": "script extract plus romname/info show"},
	"candidates": [
		{
			"search_rank": 1,
			"root": "Visual Pinball/Tables",
			"relative_path": "_tmp/iron man 080215a.vpx",
			"original_filename": "iron man 080215a.vpx",
			"bytes": 31019008,
			"sha256": "eaada74973ecb1c320420b287d5dca4970a39a25bb5c1ea2a10372786c6e2958",
			"vpxtool_romname": "im2_160",
			"vpxtool_table_name": "",
			"decision": "rejected",
			"reason": "Unsupported/non-target driver; not one of the in-scope original Iron Man drivers.",
			"extracted_script": {"path": "evidence/vpx/source-scripts/stern/iron-man-2010/tier1-tmp-im2-160.vbs", "bytes": 28510, "sha256": "e74ec59709a1a0c14e2cabf8173b35f040a1908bd62048dd7ba0e1aeacf11cc2"},
		},
		{
			"search_rank": 2,
			"root": "Visual Pinball/Tables",
			"relative_path": "JP's IronMan 2 v3.0.vpx",
			"original_filename": "JP's IronMan 2 v3.0.vpx",
			"bytes": 32436224,
			"sha256": "8bf4c377be4240b1de4842d2d3324da7d6683de9ff59f393b86c0373fbdb9ed5",
			"vpxtool_romname": "im_186ve",
			"vpxtool_table_name": "JP's IronMan Armored Adventures",
			"decision": "rejected",
			"reason": "Community retheme/unsupported virtual variant: the script defaults to im_186ve Vault Edition and only comments the original im_186 ROM binding.",
			"extracted_script": {"path": "evidence/vpx/source-scripts/stern/iron-man-2010/tier1-jpsalas-ironman2.vbs", "bytes": 29305, "sha256": "0645884ae539467cd2d54f531771054d26912c80596ccaec50431c1f4e5a63eb"},
		},
		{
			"search_rank": 3,
			"root": "Visual Pinball/Tables",
			"relative_path": "Iron Man Vault Edition (Stern 2010) VPW v1.0.vpx",
			"original_filename": "Iron Man Vault Edition (Stern 2010) VPW v1.0.vpx",
			"bytes": 245182464,
			"sha256": "c0abc5d90d77a4cf7c3f0455cff91d4f0b9f7e750264742b987e9ddb30ab7a4b",
			"vpxtool_romname": "im_185ve",
			"vpxtool_table_name": "Iron Man Vault Edition",
			"decision": "rejected",
			"reason": "Vault Edition driver and explicit 2014 product identity; not eligible for original 2010 geometry.",
			"extracted_script": {"path": "evidence/vpx/source-scripts/stern/iron-man-2010/tier1-vault-vpw.vbs", "bytes": 279163, "sha256": "d05c786a7a2e0384f47c6581ddfefd664573dda274be4da0b991fb23d9c0c5b6"},
		},
		{
			"search_rank": 4,
			"root": "Visual Pinball/Tables Archive",
			"relative_path": "Iron Man (Stern 2010).vpx",
			"original_filename": "Iron Man (Stern 2010).vpx",
			"bytes": 54112256,
			"sha256": "dd4cc46c3002645c9f8cf9905699caf3d14231e069a98f8c47f25a0c35944cb1",
			"vpxtool_romname": "im_183ve",
			"vpxtool_table_name": "",
			"decision": "rejected",
			"reason": "Vault Edition driver despite the filename and generic splash; not eligible for original 2010 geometry.",
			"extracted_script": {"path": "evidence/vpx/source-scripts/stern/iron-man-2010/tier2-archive-iron-man.vbs", "bytes": 29106, "sha256": "d913cc86286c9a42605e88823a1341425c44c4716042f5d66688e5335cc1be43"},
		},
		{
			"search_rank": 5,
			"root": "Visual Pinball/Tables Archive",
			"relative_path": "Iron Man (Pro Vault Edition) (Stern 2010).vpx",
			"original_filename": "Iron Man (Pro Vault Edition) (Stern 2010).vpx",
			"bytes": 54112256,
			"sha256": "dd4cc46c3002645c9f8cf9905699caf3d14231e069a98f8c47f25a0c35944cb1",
			"vpxtool_romname": "im_183ve",
			"vpxtool_table_name": "",
			"decision": "rejected",
			"reason": "Vault Edition driver; byte-identical to the adjacent archive candidate and not eligible for original 2010 geometry.",
			"same_source_as": "Iron Man (Stern 2010).vpx",
			"extracted_script": {"path": "evidence/vpx/source-scripts/stern/iron-man-2010/tier2-archive-iron-man.vbs", "bytes": 29106, "sha256": "d913cc86286c9a42605e88823a1341425c44c4716042f5d66688e5335cc1be43"},
		},
		{
			"search_rank": 6,
			"root": "vpuniverse.com",
			"source_uri": "https://vpuniverse.com/files/file/8679-ironman-siggis-mod/",
			"relative_path": "Ironman (Stern 2010) Siggis MOD 2.0.vpx",
			"original_filename": "Ironman (Stern 2010) Siggis MOD 2.0.vpx",
			"bytes": 67338240,
			"sha256": "8e3e175161b8f6671188762b831f843c168b854aa5bf79fadde7f2946e727c96",
			"vpxtool_romname": "im_183ve",
			"vpxtool_table_name": "",
			"decision": "accepted",
			"reason": "Physical Stern 2010 reconstruction accepted only as 2D shared-layout corroboration. The compatible VE ROM binding is not treated as product identity, and no construction or unsupported 3D measurement is imported.",
			"extracted_script": {"path": "evidence/vpx/source-scripts/stern/iron-man-2010/tier3-vpuniverse-8679-siggis-2.0.vbs", "bytes": 52170, "sha256": "3b4cc90353672bae686ad90c833c92fc33c8e347a394d8473aaeaabdcac7139d"},
		},
		{
			"search_rank": 7,
			"root": "vpforums.org",
			"source_uri": "https://www.vpforums.org/index.php?app=downloads&showfile=16172",
			"relative_path": "Iron Man (Stern 2010)_Francisco666MOD_1.vpx",
			"original_filename": "Iron Man (Stern 2010)_Francisco666MOD_1.vpx",
			"bytes": 179437568,
			"sha256": "aafb93a1f4d7c65baf6f6458a6e10c51757db0bc48e5e2c89b40ab794ac37df4",
			"vpxtool_romname": "im_186ve",
			"vpxtool_table_name": "Iron Man (Stern 2010)",
			"decision": "accepted",
			"reason": "Physical Stern 2010 reconstruction accepted as 2D shared-layout corroboration. Its script explicitly records rearrangement against Iron Man Vault; original construction remains controlled by the 2010 parts book.",
			"extracted_script": {"path": "evidence/vpx/source-scripts/stern/iron-man-2010/tier4-vpforums-16172-francisco.vbs", "bytes": 37787, "sha256": "9bfa427b1728b5f5fcc7302cdad51b91ba13f0a682ec1045f51bd2b25fa29a14"},
		},
		{
			"search_rank": 8,
			"root": "vpforums.org",
			"source_uri": "https://www.vpforums.org/index.php?app=downloads&showfile=16778",
			"relative_path": "Iron Man (Stern 2010)_Bigus(MOD)2.1.vpx",
			"original_filename": "Iron Man (Stern 2010)_Bigus(MOD)2.1.vpx",
			"bytes": 185057280,
			"sha256": "5802d8a326366d67b48c6d477b4225121e0c4c17e1ac22651eb27406f99a79c5",
			"vpxtool_romname": "im_186ve",
			"vpxtool_table_name": "Iron Man (Stern 2010)",
			"decision": "accepted",
			"reason": "Later physical Stern 2010 reconstruction in the same VPF lineage, accepted only as corroboration for the normalized 2D shared layout; later lighting, physics, and layout edits are not promoted automatically.",
			"extracted_script": {"path": "evidence/vpx/source-scripts/stern/iron-man-2010/tier4-vpforums-16778-bigus.vbs", "bytes": 36685, "sha256": "1e158fec5ee9f0b9818345483770c924d33a1cfb56421a201114a94d7021fca6"},
		},
	],
}


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(dict.fromkeys(source_refs))}


def aliases(namespace: str, value: int | str, manual_value: str | None = None) -> list[dict[str, str]]:
	result = [{"namespace": namespace, "value": str(value)}]
	if manual_value is not None:
		result.append({"namespace": "manual.address", "value": manual_value})
	return result


MATRIX_RETURN = [
	("WHT-BRN", "J6-P9"), ("WHT-RED", "J6-P8"), ("WHT-ORG", "J6-P7"), ("WHT-YEL", "J6-P6"),
	("WHT-GRN", "J6-P5"), ("WHT-BLU", "J6-P3"), ("WHT-VIO", "J6-P2"), ("WHT-GRY", "J6-P1"),
	("TAN-BLK", "J12-P9"), ("TAN-RED", "J12-P8"), ("TAN-ORG", "J12-P7"), ("TAN-YEL", "J12-P6"),
	("TAN-GRN", "J12-P4"), ("TAN-BLU", "J12-P3"), ("TAN-VIO", "J12-P2"), ("TAN-WHT", "J12-P1"),
]
MATRIX_DRIVE = [("GRN-BRN", "J1-P1"), ("GRN-RED", "J1-P3"), ("GRN-ORG", "J1-P4"), ("GRN-YEL", "J1-P5")]


# label, switch type, pulse, normally closed, roles
SWITCHES: dict[int, tuple[str, str, bool, bool, tuple[str, ...]]] = {
	1: ("Iron Monger motor down", "microswitch", False, False, ("position.down",)),
	3: ("Iron Monger motor up", "microswitch", False, False, ("position.up",)),
	4: ("Iron Monger left shoulder", "microswitch", True, False, ()),
	5: ("Iron Monger legs", "microswitch", True, False, ()),
	6: ("Iron Monger right shoulder", "microswitch", True, False, ()),
	7: ("Left orbit rollover", "leaf", False, False, ()),
	9: ("Right orbit rollover", "leaf", False, False, ()),
	10: ("War Machine opto", "opto", False, False, ("ball.position",)),
	11: ("Left orbit spinner", "other", True, False, ()),
	12: ("Left ramp entrance", "microswitch", False, False, ()),
	13: ("Center lane spinner", "other", True, False, ()),
	14: ("Right orbit spinner", "other", True, False, ()),
	15: ("Tournament start", "button", False, False, ("cabinet.tournament-start",)),
	16: ("Start button", "button", False, False, ("cabinet.start",)),
	18: ("Trough 4 left", "microswitch", False, False, ("ball.position",)),
	19: ("Trough 3", "microswitch", False, False, ("ball.position",)),
	20: ("Trough 2", "microswitch", False, False, ("ball.position",)),
	21: ("Trough 1 right", "opto", False, False, ("ball.position",)),
	22: ("Trough jam opto", "opto", False, False, ("ball.position",)),
	23: ("Shooter lane", "microswitch", False, False, ("ball.position",)),
	24: ("Left outlane", "leaf", False, False, ()),
	25: ("Left return lane", "leaf", False, False, ()),
	26: ("Left slingshot", "leaf", True, False, ()),
	27: ("Right slingshot", "leaf", True, False, ()),
	28: ("Right return lane", "leaf", False, False, ()),
	29: ("Right outlane", "leaf", False, False, ()),
	30: ("Top-left pop bumper", "leaf", True, False, ()),
	31: ("Top-right pop bumper", "leaf", True, False, ()),
	32: ("Bottom pop bumper", "leaf", True, False, ()),
	33: ("Iron Man target 4 top", "microswitch", True, False, ()),
	34: ("Iron Man target 3", "microswitch", True, False, ()),
	35: ("Iron Man target 2", "microswitch", True, False, ()),
	36: ("Iron Man target 1", "microswitch", True, False, ()),
	37: ("Right ramp exit", "microswitch", False, False, ()),
	38: ("Top lane left", "leaf", False, False, ()),
	39: ("Top lane right", "leaf", False, False, ()),
	40: ("Iron Man target 5 top", "microswitch", True, False, ()),
	41: ("Iron Man target 6", "microswitch", True, False, ()),
	42: ("Iron Man target 7", "microswitch", True, False, ()),
	43: ("Right ramp entrance", "microswitch", False, False, ()),
	44: ("Ground drone target", "microswitch", True, False, ()),
	45: ("Air drone target", "microswitch", True, False, ()),
	46: ("Tactical drone target", "microswitch", True, False, ()),
	47: ("Whiplash target left", "microswitch", True, False, ()),
	48: ("Whiplash target right", "microswitch", True, False, ()),
	49: ("Left ramp exit", "microswitch", False, False, ()),
	50: ("Sea drone target", "microswitch", True, False, ()),
}


def switch_id(number: int) -> str:
	label = SWITCHES[number][0] if number in SWITCHES else f"Unused matrix switch {number}"
	return f"switch.{number}-{slug(label)}"


def matrix_switch(number: int) -> dict[str, object]:
	spec = SWITCHES.get(number)
	label = spec[0] if spec else f"Unused matrix switch {number}"
	row, column = divmod(number - 1, 16)
	physical: dict[str, object] = {"switch_type": spec[1] if spec else "unknown"}
	if number in {1, 3}:
		physical["notes"] = "Physical Iron Monger endpoint contact. The proven VPX table changes endpoint state at motion start as an animation shortcut; a recreation must change it only when the moving assembly reaches the endpoint."
	result: dict[str, object] = {
		"id": switch_id(number), "label": label, "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": number}, "aliases": aliases("pinmame.switch", number, str(number)),
		"normally_closed": spec[3] if spec else False, "pulse": spec[2] if spec else False,
		"availability": "used" if spec else "unused", "physical": physical,
		"wiring": {"board": "CPU/Sound board", "drive_wire": MATRIX_DRIVE[row][0], "drive_connection": MATRIX_DRIVE[row][1], "return_wire": MATRIX_RETURN[column][0], "return_connection": MATRIX_RETURN[column][1]},
		"provenance": provenance(VE_MANUAL_SOURCE, ROM_SOURCE, VPX_SOURCE, CODE_COMPAT_SOURCE),
	}
	if spec and spec[4]:
		result["roles"] = list(spec[4])
	return result


DEDICATED_DEVICES = [65, 66, 67, 68, 69, 70, 71, 72, 84, 83, 82, 81, 88, 87, 86, 85, -7, -6, -5, -4, -3, -2, -1, 0]
DEDICATED_LABELS = [
	"Left coin chute", "Center coin chute", "Right coin chute", "Unused fourth coin chute", "Optional fifth coin chute", "Unused dedicated switch D6", "Unused Home switch", "Unused Away switch",
	"Left flipper button", "Left flipper end-of-stroke", "Right flipper button", "Right flipper end-of-stroke", "Unused dedicated switch D13", "Unused dedicated switch D14", "Unused dedicated switch D15", "Unused dedicated switch D16",
	"Pendulum tilt", "Slam tilt", "Optional ticket notch", "Unused dedicated switch D20", "Coin-door Back button", "Coin-door Minus button", "Coin-door Plus button", "Coin-door Select button",
]
DEDICATED_TYPES = ["button", "button", "button", "unknown", "button", "unknown", "unknown", "unknown", "button", "leaf", "button", "leaf", "unknown", "unknown", "unknown", "unknown", "tilt", "tilt", "microswitch", "unknown", "button", "button", "button", "button"]
DEDICATED_AVAILABILITY = ["used", "used", "used", "unused", "optional", "unused", "unused", "unused", "used", "used", "used", "used", "unused", "unused", "unused", "unused", "used", "used", "optional", "unused", "used", "used", "used", "used"]
DEDICATED_ROLES = {
	65: "cabinet.coin.left", 66: "cabinet.coin.center", 67: "cabinet.coin.right", 69: "cabinet.coin.fifth",
	84: "flipper.lower.left.button", 83: "flipper.lower.left.eos", 82: "flipper.lower.right.button", 81: "flipper.lower.right.eos",
	-7: "cabinet.tilt", -6: "cabinet.slam-tilt", -5: "cabinet.ticket-notch", -3: "service.back", -2: "service.down", -1: "service.up", 0: "service.enter",
}
DEDICATED_WIRES = [
	("PNK-BRN", "J2-P2"), ("PNK-RED", "J2-P3"), ("PNK-ORG", "J2-P4"), ("PNK-YEL", "J2-P6"), ("PNK-GRN", "J2-P7"), ("PNK-BLU", "J2-P8"), ("PNK-VIO", "J2-P9"), ("PNK-GRY", "J2-P10"),
	("GRY-BRN", "J3-P1"), ("GRY-RED", "J3-P2"), ("GRY-ORG", "J3-P4"), ("GRY-YEL", "J3-P5"), ("GRY-GRN", "J3-P6"), ("GRY-BLU", "J3-P7"), ("GRY-VIO", "J3-P8"), ("GRY-BLK", "J3-P9"),
	("LGN-BRN", "J13-P1"), ("LGN-RED", "J13-P3"), ("LGN-ORG", "J13-P4"), ("LGN-YEL", "J13-P5"), ("LGN-BLK", "J13-P6"), ("LGN-BLU", "J13-P7"), ("LGN-VIO", "J13-P8"), ("LGN-GRY", "J13-P9"),
]
DEDICATED_GROUNDS = [("BLK", "J2-P1/11")] * 8 + [("BLK", "J3-P10")] * 8 + [("BLK", "J13-P10")] * 8


def dedicated_id(number: int) -> str:
	return f"switch.d{number}-{slug(DEDICATED_LABELS[number - 1])}"


def dedicated_switch(number: int) -> dict[str, object]:
	index = number - 1
	device = DEDICATED_DEVICES[index]
	availability = DEDICATED_AVAILABILITY[index]
	result: dict[str, object] = {
		"id": dedicated_id(number), "label": DEDICATED_LABELS[index], "kind": "switch",
		"binding": {"group": "pinmame.input.switch", "device": device}, "aliases": aliases("pinmame.switch", device, f"D-{number}"),
		"normally_closed": number in {10, 12, 18}, "pulse": number in {1, 2, 3, 5}, "availability": availability,
		"physical": {"switch_type": DEDICATED_TYPES[index] if availability != "unused" else "unknown"},
		"wiring": {"board": "CPU/Sound board dedicated-switch input", "drive_wire": DEDICATED_WIRES[index][0], "drive_connection": DEDICATED_WIRES[index][1], "return_wire": DEDICATED_GROUNDS[index][0], "return_connection": DEDICATED_GROUNDS[index][1]},
		"provenance": provenance(VE_MANUAL_SOURCE, CORE_SOURCE),
	}
	if device in DEDICATED_ROLES and availability in {"used", "optional"}:
		result["roles"] = [DEDICATED_ROLES[device]]
	return result


def inputs() -> list[dict[str, object]]:
	items = [matrix_switch(number) for number in range(1, 65)]
	items.extend(dedicated_switch(number) for number in range(1, 25))
	for number in range(1, 9):
		items.append({"id": f"switch.dip-{number}", "label": f"CPU/Sound board DIP switch {number}", "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": number}, "aliases": aliases("pinmame.dip", number, f"D-{24 + number}"), "availability": "used", "physical": {"switch_type": "dip", "location": "CPU/Sound board"}, "provenance": provenance(VE_MANUAL_SOURCE, CORE_SOURCE)})
	return items


# label, kind, availability, manual part number
COILS: dict[int, tuple[str, str, str, str | None]] = {
	1: ("Trough up-kicker", "coil", "used", "090-5044-ND"), 2: ("Auto launch", "coil", "used", "090-5001-ND"),
	3: ("Iron Monger magnet", "magnet", "used", "090-5076-00"), 4: ("Whiplash magnet", "magnet", "used", "090-5076-00"),
	5: ("War Machine kick back", "coil", "used", "090-5001-ND"), 6: ("Orbit up-post", "coil", "used", "090-5044-ND"),
	7: ("Unused output Q7", "coil", "unused", None), 8: ("Optional shaker motor", "motor", "optional", "502-5027-00"),
	9: ("Top-left pop bumper", "coil", "used", "090-5044-ND"), 10: ("Top-right pop bumper", "coil", "used", "090-5044-ND"),
	11: ("Bottom pop bumper", "coil", "used", "090-5044-ND"), 12: ("Center-lane up-post", "coil", "used", "090-5044-ND"),
	13: ("Unused output Q13", "coil", "unused", None), 14: ("Unused output Q14", "coil", "unused", None),
	15: ("Left flipper", "coil", "used", "090-5020-20-ND"), 16: ("Right flipper", "coil", "used", "090-5030-ND"),
	17: ("Left slingshot", "coil", "used", "090-5001-ND"), 18: ("Right slingshot", "coil", "used", "090-5001-ND"),
	19: ("Iron Monger motor", "motor", "used", "041-5107-00"), 20: ("Pop-bumper-area flash", "flasher", "used", "113-5034-08"),
	21: ("Left-ramp top flash", "flasher", "used", "113-5034-08"), 22: ("War Machine front flash x2", "flasher", "used", "113-5034-08"),
	23: ("Iron Monger center-lane flash", "flasher", "used", "113-5034-08"), 24: ("Optional coin meter or 5 V device", "coil", "optional", None),
	25: ("Iron Monger flash x2", "flasher", "used", "113-5034-08"), 26: ("Right-ramp top flash", "flasher", "used", "113-5034-08"),
	27: ("War Machine flash x3", "flasher", "used", "113-5034-08"), 28: ("Iron Monger chest flash x3", "flasher", "used", "113-5034-08"),
	29: ("Whiplash flash x2", "flasher", "used", "113-5034-05"), 30: ("Mark VI flash x2", "flasher", "used", "113-5034-08"),
	31: ("Left-ramp bottom flash x2", "flasher", "used", "113-5034-08"), 32: ("Right-ramp bottom flash", "flasher", "used", "113-5034-08"),
}
FLASHER_QUANTITIES = {
	20: 1, 21: 1, 22: 2, 23: 1, 25: 2, 26: 1,
	27: 3, 28: 3, 29: 2, 30: 2, 31: 2, 32: 1,
}
CONTROL_WIRE = ["BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY", "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLK", "ORG-GRY", "ORG-VIO", "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY", "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY"]
CONTROL_CONNECTION = ["J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9", "J9-P1", "J9-P2", "J9-P4", "J9-P5", "J9-P6", "J9-P7", "J9-P8", "J9-P9", "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10", "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8"]


def output_id(address: int) -> str:
	return f"device.{address}-{slug(COILS[address][0])}"


def coil_wiring(address: int) -> dict[str, object]:
	wiring: dict[str, object] = {"board": "I/O Power Driver board", "driver_transistor": f"Q{address}", "control_wire": CONTROL_WIRE[address - 1], "control_connection": CONTROL_CONNECTION[address - 1]}
	if address in {7, 13, 14}:
		return wiring
	if address in {1, 2, 5, 6, 9, 10, 11, 12}:
		wiring.update({"power_wire": "YEL-VIO", "power_connection": "J10-P9/10", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address in {3, 4}:
		wiring.update({"power_wire": "VIO-YEL", "power_connection": "J10-P8", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 8:
		wiring.update({"power_wire": "RED-WHT", "power_connection": "J17-P7", "nominal_voltage_v": 16, "voltage_type": "ac"})
	elif address == 15:
		wiring.update({"power_wire": "GRY-YEL via 3 A fuse to RED-YEL", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address == 16:
		wiring.update({"power_wire": "BLU-YEL via 3 A fuse to RED-YEL", "power_connection": "J10-P6/7", "nominal_voltage_v": 50, "voltage_type": "dc"})
	elif address in {17, 18, 19}:
		wiring.update({"power_wire": "BRN", "power_connection": "J7-P1", "nominal_voltage_v": 20, "voltage_type": "dc"})
	elif address == 24:
		wiring.update({"power_wire": "RED", "power_connection": "J16-P4-8", "nominal_voltage_v": 5, "voltage_type": "dc"})
	else:
		wiring.update({"power_wire": "ORG", "power_connection": "J6-P10", "nominal_voltage_v": 20, "voltage_type": "dc"})
	return wiring


def make_output(address: int, label: str, kind: str, availability: str, sources: tuple[str, ...], group: str = "pinmame.output.solenoid", manual_address: str | None = None, physical: dict[str, object] | None = None, wiring: dict[str, object] | None = None, stable_id: str | None = None) -> dict[str, object]:
	namespace = "pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.gi" if group == "pinmame.output.gi" else "pinmame.solenoid"
	result: dict[str, object] = {"id": stable_id or f"device.{slug(label)}", "label": label, "kind": kind, "binding": {"group": group, "device": address}, "aliases": aliases(namespace, address, manual_address), "availability": availability, "provenance": provenance(*sources)}
	if physical:
		result["physical"] = physical
	if wiring:
		result["wiring"] = wiring
	return result


def main_outputs(vault_edition: bool) -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for address, (label, kind, availability, part_number) in COILS.items():
		physical: dict[str, object] = {}
		if part_number and (kind != "flasher" or vault_edition):
			physical["part_number"] = part_number
		if availability == "unused":
			physical["notes"] = "The driver transistor/control pin exists on the common SAM I/O board, but no physical device is installed."
		elif address == 8:
			physical["notes"] = "Optional factory shaker kit; do not assume it is installed on every cabinet. The manual's Q8 table prints 50 VDC, but its transformer/I/O schematics on PDF pages 49-50 and 56 place RED-WHT/J17-P7 on the 16 VAC secondary; the schematics and consistent SAM-board wiring govern this reconciled value."
		elif address == 24:
			physical["notes"] = "The physical service Q-table assigns this optional channel to a 5 V coin meter or similar device, so no stock playfield flasher is installed. The proven VPW table nevertheless declares output 24 inside its contiguous SetLampMod 120-132 flasher callback block; physical manual construction governs device identity, while that script callback is retained here as an explicit table-implementation conflict rather than promoted to hardware."
		elif kind == "flasher" and vault_edition:
			physical["notes"] = "Vault Edition LED flasher module as specified by the 2014 service manual."
		elif kind == "flasher":
			physical["notes"] = "The original 2010 construction uses incandescent flash lighting; preserve the logical Q address but do not substitute the Vault Edition LED-module part number."
		if kind == "flasher" and availability == "used":
			physical["quantity"] = FLASHER_QUANTITIES[address]
		if address == 31:
			if vault_edition:
				physical["notes"] += " The 2014 official coil-location map marks two separately located Q31 emitters and the exact Vault VPW script independently labels this callback x2, although the service Q-table omits the multiplier. Preserve both physical emitters."
			else:
				physical["notes"] += " Cross-edition evidence from the same logical/playfield layout fixes this quantity: the 2014 Vault coil-location map marks two Q31 emitters and the exact Vault VPW script labels the callback x2. The 2010 parts book does not number coil addresses, so preserve both original incandescent emitters as an explicit shared-layout inference rather than an original-manual callout."
		items.append(make_output(address, label, kind, availability, (VE_MANUAL_SOURCE, ORIGINAL_MANUAL_SOURCE, PRESS_SOURCE, VPX_SOURCE, CORE_SOURCE, CODE_COMPAT_SOURCE), manual_address=str(address), physical=physical, wiring=coil_wiring(address), stable_id=output_id(address)))
	items.append(make_output(33, "PinMAME SAM game-on state", "virtual", "used", (CORE_SOURCE, RUNTIME_SOURCE), physical={"notes": "Synthetic SAM fast-flip game-on output. It has no physical Q33 device; public addresses 34-36 are legacy query aliases rather than additional outputs."}, stable_id="virtual.game-on"))
	for address in range(51, 67):
		items.append(make_output(address, f"Unused SAM auxiliary compatibility address {address}", "virtual", "unused", (CORE_SOURCE, ROM_SOURCE), physical={"notes": "Iron Man is declared with SAM_GAME_AUXSOL12, but the physical service inventory and proven table contain no installed auxiliary controlled devices. This remains explicit emulator capacity."}, stable_id=f"virtual.aux-{address}"))
	return items


LAMPS = {
	1: "Start button", 2: "Tournament start button", 3: "Shoot Again", 4: "Left outlane", 5: "Left return lane", 6: "Right return lane", 7: "Right outlane", 8: "Extra Ball",
	9: "Center-lane arrow", 10: "Center-lane Iron Monger", 11: "Center-lane pop bumper", 12: "Tactical drone", 13: "Air drone", 14: "Left-ramp arrow", 15: "Left-orbit Iron Monger", 16: "Left-orbit pop bumper",
	17: "Iron Man target 4 top", 18: "Iron Man target 3", 19: "Iron Man target 2", 20: "Iron Man target 1 bottom", 21: "War Machine", 22: "Left ramp 400K", 23: "Left ramp 300K", 24: "Left ramp 200K",
	25: "Left ramp 100K", 26: "Right-ramp arrow", 27: "Shield", 28: "MONGER R", 29: "MONGER E", 30: "MONGER G", 31: "MONGER N", 32: "MONGER O",
	33: "MONGER M", 34: "Right-loop arrow", 35: "Right-orbit Iron Monger", 36: "Iron Man target 5 top", 37: "Iron Man target 6", 38: "Iron Man target 7", 39: "Right ramp 400K", 40: "Right ramp 300K",
	41: "Right ramp 200K", 42: "Right ramp 100K", 43: "Ground drone", 44: "Iron Man wizard mode", 45: "War Machine wizard mode", 46: "Iron Monger wizard mode", 47: "Whiplash wizard mode", 48: "Drones wizard mode",
	49: "Mark V", 50: "Mark IV", 51: "Mark III", 52: "Mark II", 53: "Mark I", 54: "Left-loop arrow", 55: "Mark VI", 56: "Special",
	57: "Top lane left", 58: "Top lane right", 59: "Sea drones", 60: "Top-left pop bumper", 61: "Top-right pop bumper", 62: "Bottom pop bumper", 63: "Right-orbit pop-bumper light",
	73: "Unlabeled clear matrix bulb 73", 79: "Unlabeled clear matrix bulb 79", 80: "Unlabeled clear matrix bulb 80",
}
LAMP_DRIVE = [("YEL-BRN", "J13-P9"), ("YEL-RED", "J13-P8"), ("YEL-ORG", "J13-P7"), ("YEL-BLK", "J13-P6"), ("YEL-GRN", "J13-P5"), ("YEL-BLU", "J13-P4"), ("YEL-VIO", "J13-P3"), ("YEL-GRY", "J13-P1")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
USED_LAMPS = set(range(1, 64)) | {73, 79, 80}
VE_555_LAMPS = {54, 56, 73, 79, 80}
RUNTIME_LAMPS_SEEN = {1} | set(range(3, 64))


def lamps(vault_edition: bool) -> list[dict[str, object]]:
	items: list[dict[str, object]] = []
	for address in range(1, 81):
		label = LAMPS.get(address, f"Unused lamp matrix address {address}")
		availability = "used" if address in USED_LAMPS else "unused"
		column = (address - 1) % 8
		row = (address - 1) // 8
		physical: dict[str, object] | None = None
		if availability == "used":
			if address in {73, 79, 80}:
				if vault_edition:
					physical = {"location": "Hidden row-10 matrix position; exact service location unlabeled", "notes": "The 2014 service matrix explicitly populates this address with a clear #555 bulb, but the playfield lamp-location drawing and proven VPX visual inventory omit it. Treat it as a hidden electrical matrix/load bulb, not as a visible playfield insert."}
				else:
					physical = {"location": "Hidden row-10 matrix position; exact service location unlabeled", "notes": "The original 2010 underside parts drawing visibly retains unnumbered twist-lock sockets, while shared Stern code compatibility and the later service grid identify row-10 addresses 73/79/80 as clear hidden bulbs. Their population on the original is a cross-edition construction inference rather than a numbered 2010 parts callout; do not turn them into visible playfield inserts."}
			elif vault_edition and address in VE_555_LAMPS:
				physical = {"location": label, "notes": "The Vault Edition service matrix specifies a clear #555-form-factor lamp here rather than LED module 112-5033-08."}
			elif vault_edition:
				physical = {"part_number": "112-5033-08", "location": label, "notes": "Vault Edition D.O.T.S. LED module."}
			else:
				physical = {"location": label, "notes": "Original 2010 incandescent matrix-lamp construction. The original parts book shows twist-lock sockets across the playfield underside; the later Vault Edition logical address remains compatible but its LED-module part number does not."}
		if address == 55 and physical is not None:
			physical["quantity"] = 2
			if vault_edition:
				physical["notes"] += " The 2014 official lamp-location map marks two physical Mark VI emitters controlled together at address 55; the exact Vault VPW collapses them into one central light pool."
			else:
				physical["notes"] += " Cross-edition evidence from the same logical/playfield layout fixes this quantity: the 2014 Vault lamp-location map marks two Mark VI emitters at address 55 and the exact Vault VPW collapses them into one light pool. The 2010 parts book does not number lamp addresses, so retain two original incandescent emitters as an explicit shared-layout inference rather than an original-manual callout."
		lamp = make_output(address, label, "lamp", availability, (VE_MANUAL_SOURCE, ORIGINAL_MANUAL_SOURCE, PRESS_SOURCE, ROM_SOURCE, VPX_SOURCE, CODE_COMPAT_SOURCE), group="pinmame.output.lamp", manual_address=str(address), physical=physical, wiring={"board": "I/O Power Driver board lamp matrix", "drive_wire": LAMP_DRIVE[column][0], "drive_connection": LAMP_DRIVE[column][1], "return_wire": LAMP_RETURN[row][0], "return_connection": LAMP_RETURN[row][1]}, stable_id=f"lamp.{address}-{slug(label)}")
		if address in {73, 79, 80}:
			lamp["roles"] = ["internal.load"]
		items.append(lamp)
	gi_notes = "Vault Edition shipped with LED playfield lighting while retaining the SAM aggregate GI callback." if vault_edition else "Original 2010 playfield uses incandescent GI; do not project the Vault Edition LED conversion backward."
	items.append(make_output(0, "General illumination master", "gi", "used", (VE_MANUAL_SOURCE, ORIGINAL_MANUAL_SOURCE, PRESS_SOURCE, VPX_SOURCE, RUNTIME_SOURCE, CODE_COMPAT_SOURCE), group="pinmame.output.gi", manual_address="GI-0", physical={"location": "Playfield general illumination", "notes": f"PinMAME exposes the machine's general illumination as aggregate channel 0. {gi_notes}"}, stable_id="gi.master"))
	return items


def mechanism(mechanism_id: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, sources: tuple[str, ...], positions: list[dict[str, object]] | None = None, assembly_part_number: str | None = None) -> dict[str, object]:
	result: dict[str, object] = {"id": mechanism_id, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*sources)}
	if positions is not None:
		result["positions"] = positions
	if assembly_part_number is not None:
		result["assembly_part_number"] = assembly_part_number
	return result


def mechanisms(vault_edition: bool) -> list[dict[str, object]]:
	common = (VE_MANUAL_SOURCE, ORIGINAL_MANUAL_SOURCE, VPX_SOURCE, STANDALONE_VPX_SOURCE)
	auto_launch_construction = "This 2014 product uses Stern's then-current one-piece molded auto-launcher." if vault_edition else "This 2010 product uses the original multi-piece auto-launch assembly rather than the later Vault one-piece molding."
	monger_construction = "The Vault product uses the strengthened one-piece molded Iron Monger toy announced by Stern." if vault_edition else "Retain the original 2010 multi-piece Iron Monger construction rather than the strengthened Vault molding."
	whiplash_construction = "The Vault product uses Stern's strengthened one-piece Whiplash molding." if vault_edition else "Retain the original 2010 Whiplash assembly rather than the strengthened Vault molding."
	war_machine_construction = "The Vault product uses Stern's strengthened one-piece War Machine molding." if vault_edition else "Retain the original 2010 War Machine assembly rather than the strengthened Vault molding."
	return [
		mechanism("mechanism.trough", "Four-ball trough", "kicker", [output_id(1)], [switch_id(number) for number in range(18, 23)], "Four balls rest on occupancy switches 18-21. Output 1 ejects the rightmost ball through jam opto 22 toward shooter switch 23. The proven table pulses switch 15 as a software-only release confirmation, but the service manual proves physical switch 15 is Tournament Start; never create a trough-release switch at 15.", common, assembly_part_number="500-6318-24-ND"),
		mechanism("mechanism.auto-launch", "Manual shooter with auto launch", "kicker", [output_id(2)], [switch_id(23)], f"A ball on shooter-lane switch 23 can be launched manually or by output 2. {auto_launch_construction} Controller behavior is shared.", common + (PRESS_SOURCE,)),
		mechanism("mechanism.iron-monger", "Motorized Iron Monger lift, targets, and magnet", "motorized", [output_id(19), output_id(3)], [switch_id(number) for number in (1, 3, 4, 5, 6)], f"Each motor pulse toggles commanded lift direction. Switch 1 is fully down and switch 3 fully up; target faces 4-6 move with the toy. The proven table uses a 240-unit travel range completed over 62 update steps, moves the collision/flash geometry with the toy, and disables the three target faces while down. Output 3 applies a strong non-centering magnet force to a nearby steel ball. Keep endpoint sensing tied to actual travel, not the VPX shortcut that changes endpoint switches when travel begins. {monger_construction}", common + (PRESS_SOURCE,), [{"id": "position.down", "label": "Lowered with targets unavailable", "sensors": [switch_id(1)]}, {"id": "position.up", "label": "Raised with targets hittable", "sensors": [switch_id(3)]}]),
		mechanism("mechanism.whiplash-magnet", "Whiplash magnet and target pair", "toy", [output_id(4)], [switch_id(47), switch_id(48)], f"Output 4 applies non-centering magnet force near the two fixed Whiplash targets. The magnet has no position sensor and must influence ball motion physically rather than teleporting the ball. {whiplash_construction}", common + (PRESS_SOURCE,)),
		mechanism("mechanism.war-machine", "War Machine captured-ball kick back", "kicker", [output_id(5)], [switch_id(10)], f"Switch 10 is an opto in the War Machine capture. Output 5 kicks the captured ball back into play; the proven table ejects approximately toward 165 degrees with strength 55, which is a starting point for tuning rather than a controller requirement. {war_machine_construction}", common + (PRESS_SOURCE,)),
		mechanism("mechanism.orbit-up-post", "Orbit up-post", "gate", [output_id(6)], [], "Output 6 raises the orbit post when enabled and lowers it when disabled. There is no public endpoint sensor; model the collision post itself and use the controller state as the commanded position.", common),
		mechanism("mechanism.center-lane-up-post", "Center-lane up-post", "gate", [output_id(12)], [], "Output 12 raises the center-lane post when enabled and lowers it when disabled. There is no public endpoint sensor.", common),
		mechanism("mechanism.flippers", "Lower flippers", "other", [output_id(15), output_id(16)], [dedicated_id(number) for number in (9, 10, 11, 12)], "Outputs 15/16 drive the left/right flippers. Public button/EOS pairs are 84/83 and 82/81; both EOS contacts are normally closed.", common),
		mechanism("mechanism.pop-bumpers", "Three pop bumpers", "other", [output_id(9), output_id(10), output_id(11)], [switch_id(number) for number in (30, 31, 32)], "Top-left, top-right, and bottom pop bumpers use output/switch pairs 9/30, 10/31, and 11/32.", common),
		mechanism("mechanism.slingshots", "Lower slingshots", "other", [output_id(17), output_id(18)], [switch_id(26), switch_id(27)], "Left and right slingshots use output/switch pairs 17/26 and 18/27.", common),
		mechanism("mechanism.shaker", "Optional shaker motor", "toy", [output_id(8)], [], "Output 8 drives the optional 16 VAC shaker kit from RED-WHT/J17-P7. The manual's Q8 table says 50 VDC, but its transformer/I/O schematics prove the 16 VAC feed. Treat absence as a valid factory configuration.", (VE_MANUAL_SOURCE, ORIGINAL_MANUAL_SOURCE)),
		mechanism("mechanism.routes", "Ramp, orbit, lane, and spinner network", "other", [], [switch_id(number) for number in (7, 9, 11, 12, 13, 14, 24, 25, 28, 29, 37, 38, 39, 43, 49)], "Left/right ramps have entrances 12/43 and exits 49/37. Orbit rollovers are 7/9, spinners 11/14, center-lane spinner 13, top lanes 38/39, and lower outlane/return pairs 24/25 and 29/28. The proven table uses Hit/UnHit handlers for every wire-form route contact and Spin handlers only for the spinners; preserve sustained lane/ramp/rollover state rather than pulsing those contacts.", common),
		mechanism("mechanism.fixed-targets", "Fixed Iron Man and drone target banks", "other", [], [switch_id(number) for number in (33, 34, 35, 36, 40, 41, 42, 44, 45, 46, 50)], "Seven fixed Iron Man targets occupy switches 33-36 and 40-42. Ground, Air, Tactical, and Sea drone targets are 44-46 and 50. These are static standups; the moving Iron Monger faces 4-6 and Whiplash pair 47/48 belong to their separate toy mechanisms.", common),
	]


VE_DRIVER_IDS = {driver_id for driver_id in DRIVERS if driver_id.endswith("ve")}
ORIGINAL_DRIVER_IDS = set(DRIVERS) - VE_DRIVER_IDS
if VE_DRIVER_IDS != {"im_183ve", "im_185ve", "im_186ve"}:
	raise ValueError("Iron Man Vault Edition drivers must classify exhaustively")
if ORIGINAL_DRIVER_IDS != {"im_100", "im_110", "im_120", "im_140", "im_160", "im_181", "im_182", "im_183", "im_185", "im_186"}:
	raise ValueError("Original Iron Man drivers must classify exhaustively")


def driver_records(vault_edition: bool) -> list[dict[str, object]]:
	selected: list[dict[str, object]] = []
	for driver_id in VE_DRIVER_IDS if vault_edition else ORIGINAL_DRIVER_IDS:
		source = DRIVERS[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = "Firmware revision for the 2014 Pro Vault Edition physical product." if vault_edition else "Firmware revision for the original 2010 physical product; the PinMAME Vault-rooted clone graph describes software lineage, not the later LED/backbox/toy construction."
		selected.append(record)
	return sorted(selected, key=lambda record: record["id"])


def sources(vault_edition: bool) -> list[dict[str, object]]:
	ipdb_source = VE_IPDB_SOURCE if vault_edition else ORIGINAL_IPDB_SOURCE
	ipdb_id = 6154 if vault_edition else 5550
	result = [
		{"id": ORIGINAL_MANUAL_SOURCE, "kind": "manual", "uri": "https://wp.sternpinball.com/wp-content/uploads/2018/11/IronMan-Manual.pdf", "sha256": "0948d154156860d351daa943ab3b5882ef4c86bb42cde630bcd04067ab85ed1a", "locator": "Official 32-page scanned 2010 parts/assembly book; major assemblies on PDF pages 2-16 and original playfield top/bottom construction on PDF pages 25-26. The underside drawing proves the original twist-lock lamp-socket construction.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "IronMan-Manual.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-03T03:02:34.177581Z"},
		{"id": VE_MANUAL_SOURCE, "kind": "manual", "uri": "https://wp.sternpinball.com/wp-content/uploads/2022/06/IronMan_Vault_web.pdf", "sha256": "20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990", "locator": "Official 88-page native-text service manual; switch matrix/dedicated/DIP table PDF page 16, switch locations 17, lamp matrix 18, lamp locations 19, Q1-Q32 table 20, coil locations 21, major assemblies 36-47, and schematics/wiring 48-58. The Q8 row on pages 20/48 prints 50 VDC, but transformer/I/O schematics on pages 49-50 and 56 place RED-WHT/J17-P7 on the 16 VAC secondary; the definition uses the schematic value.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "source_id": "stern", "original_filename": "IronMan_Vault_web.pdf", "rights": "NOASSERTION", "acquired_at": "2026-08-03T03:02:35.240041Z"},
		{"id": VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/sverrewl/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Iron%20Man%20Vault%20Edition%20%28Stern%202010%29%20VPW%20v1.0.1.vbs", "revision": VPX_REVISION, "sha256": "d0d37548468d67aa895121fd6ff82fdacc1d1a301a702c92325fb3ee9d7a89ea", "locator": "Known-working exact im_185ve VPW script: controller callbacks, switch contacts, two magnets, four-ball trough, War Machine kicker, both up-posts, Iron Monger lift/collision/endpoints, flippers, flashers, and GI.", "license": "NOASSERTION", "attribution": "VPW and table authors credited in the script; vpxtable_scripts contributors"},
		{"id": STANDALONE_VPX_SOURCE, "kind": "vpx_script", "uri": "https://github.com/jsm174/vpx-standalone-scripts/blob/15d112648a1b94b9f59eb8b3c335d57283653c50/Iron%20Man%20Vault%20Edition%20%28Stern%202010%29%20VPW%20v1.0/Iron%20Man%20Vault%20Edition%20%28Stern%202010%29%20VPW%20v1.0.vbs", "revision": STANDALONE_REVISION, "sha256": "756dadd23ad0dd8cadd3cb98d25553a27788230cc3f8fe04ee39c7a7effce37c", "locator": "Independent pinned mirror of the known-working im_185ve VPW script; exact callback and mechanism behavior agrees with the vpxtable_scripts copy. The retained SHA-256 is the repository checkout's CRLF materialization; the linked Git blob is the identical LF-normalized text (SHA-256 dd8697bcde0a980244163d044d60269f42f1c5f5e6d76fbc2c39a03c50ab4da2).", "license": "NOASSERTION", "attribution": "VPW and table authors credited in the script; vpx-standalone-scripts contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "src/wpc/sam.c Iron Man INITGAME/driver family, SAM_GAME_AUXSOL12 transport, 128x32 DMD, synthetic game-on state, public input translation, and prefix-wide LED output typing that must not erase the original physical incandescent boundary.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "PinmameGetGames im_ driver records and clone graph.", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/im_185ve.zip", "revision": PINMAME_REVISION, "sha256": "e04c56ca08cdd6b0aaa6fcacd601e183d338dae7a863a4486216f76b25d6738f", "locator": "Exact im_185ve archive from the user-authorized read-only corpus; im_185ve.bin SHA-256 c827da1c3f5305b27e9e504d7553bcd9c39547f357dd3827122adcc4c173c257, 29,699,292 bytes. ROM bytes remain external.", "license": "NOASSERTION", "attribution": "Analyzed locally from the user-authorized ROM corpus; ROM bytes remain external"},
		{"id": ipdb_source, "kind": "human_review", "uri": f"https://www.ipdb.org/machine.cgi?id={ipdb_id}", "locator": f"Physical identity, release year, and product inventory for IPDB {ipdb_id}; model {'PINBALL I-00B0' if vault_edition else 'I-00B3'} as printed by IPDB.", "license": "NOASSERTION", "attribution": "Internet Pinball Database", "acquired_at": "2026-08-03T00:00:00Z"},
		{"id": PRESS_SOURCE, "kind": "human_review", "uri": "https://sternpinball.com/2014/06/12/iron-man-is-back/", "locator": "Official 2014 product announcement: same game reissued with LED playfield lighting, modern metal/wood backbox, red T-molding, new cabinet/speaker-panel art, stronger one-piece molded Iron Monger/War Machine/Whiplash toys, and current one-piece auto launcher.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "acquired_at": "2026-08-03T00:00:00Z"},
		{"id": CODE_COMPAT_SOURCE, "kind": "human_review", "uri": "https://sternpinball.com/2020/05/04/stern-of-the-union-address-may-2020/", "locator": "Official Stern release note states Iron Man code 1.86 applies to both original and Vault editions.", "license": "NOASSERTION", "attribution": "Stern Pinball, Inc.", "acquired_at": "2026-08-03T00:00:00Z"},
		{"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "external:pinmame-game-code/iron-man-vault-edition/harness/boot-start-v3/run.json", "revision": PINMAME_REVISION, "sha256": "2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9", "locator": "Exact im_185ve boot/start with switches 1 and 18-21 initialized, six deliberately debounced coin pulses, start, 128x32x4 DMD artifacts, lamp 1 and 3-63 transitions, GI 0, and callback-tracked synthetic game-on 33; ROM archive SHA-256 e04c56ca08cdd6b0aaa6fcacd601e183d338dae7a863a4486216f76b25d6738f.", "license": "NOASSERTION", "attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external"},
	]
	result[0]["excerpts"] = IRON_MAN_ORIGINAL_EXCERPTS
	result[1]["excerpts"] = IRON_MAN_VAULT_EXCERPTS
	if not vault_edition:
		result.extend(VPX_CANDIDATE_SOURCES)
	return result


def build(vault_edition: bool) -> dict[str, object]:
	machine_id = "stern.iron-man-vault-edition.2014" if vault_edition else "stern.iron-man.2010"
	return {
		"format": "pinmame-machine-definition", "schema_version": 1,
		"machine": {"id": machine_id, "name": "Iron Man Pro Vault Edition" if vault_edition else "Iron Man", "manufacturer": "Stern", "year": 2014 if vault_edition else 2010, "kind": "physical_pinball", "model_number": "I-00B0" if vault_edition else "I-00B3", "ipdb_id": 6154 if vault_edition else 5550, "opdb_id": "GRVq4-M4oNp" if vault_edition else "GRVq4-MLyxq"},
		"coverage": {"status": "author_ready", "missing": [], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated"}},
		"controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
		"drivers": driver_records(vault_edition), "inputs": inputs(), "outputs": main_outputs(vault_edition) + lamps(vault_edition),
		"displays": [{"id": "display.dmd", "label": "Dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": {"status": "validated", "source_refs": [CORE_SOURCE, VE_MANUAL_SOURCE if vault_edition else ORIGINAL_MANUAL_SOURCE]}}, "provenance": provenance(CORE_SOURCE, RUNTIME_SOURCE, CODE_COMPAT_SOURCE)}],
		"mechanisms": mechanisms(vault_edition), "relationships": [], "sources": sources(vault_edition),
		"knowledge": {"path": f"knowledge/stern/iron-man-{'vault-edition-2014' if vault_edition else '2010'}.md", "status": "complete"}, "conflicts": [],
	}


ORIGINAL_KNOWLEDGE = """# Iron Man (Stern, 2010)

Coverage: **author-ready - complete physical I/O inventory, PinMAME bindings, wiring, mechanism causality, original-versus-Vault boundary, and recreation behavior validated**

## Identity and evidence precedence

This is the original 2010 Iron Man physical product, IPDB 5550, model I-00B3. It covers `im_100`, `im_110`, `im_120`, `im_140`, `im_160`, `im_181`, `im_182`, `im_183`, `im_185`, and `im_186`; firmware catalog years through 2020 do not change the playfield's 2010 construction. PinMAME roots the family under the Vault driver for software lineage, but that does not turn these ROMs into the 2014 reissue. The proven VPW script is runtime ground truth, the official service/parts manuals control physical construction and wiring, and PinMAME controls transport/display metadata.

## Original versus 2014 Pro Vault Edition

Both products use the same logical switch, Q-output, lamp, GI, DMD, and custom-mechanism map, and Stern states code 1.86 applies to both. The original uses its 2010 wood/cabinet/backbox treatment, incandescent insert/GI/flasher construction, earlier multi-piece auto-launch and toy assemblies, and original cabinet/speaker art. Do not project the Vault Edition's LED modules, strengthened one-piece Iron Monger/War Machine/Whiplash toys, brushed-aluminum cabinet art, red T-molding, modern metal/wood backbox, or current one-piece auto launcher backward. PinMAME's prefix-wide LED output typing is emulator metadata and is not evidence that the 2010 machine shipped with LEDs.

## Ball path, trough, and shooter

Four balls initialize on trough switches 18-21. Jam opto 22 sees an ejecting ball and output 1 serves it toward shooter-lane switch 23. The shooter supports the manual plunger and output 2 auto launch. Switch 10 is the War Machine capture opto; output 5 kicks that ball back into play. Main route sensors are orbit rollovers 7/9, spinners 11/13/14, ramp entrance/exits 12/43/37/49, top lanes 38/39, returns/outlanes 24/25/28/29, and the seven fixed Iron Man targets 33-36 and 40-42. The VPX trough routine's pulse of switch 15 is only a table workaround: physical switch 15 is Tournament Start.

## Iron Monger and magnets

Iron Monger is a moving collision assembly, not a cosmetic animation. Output 19 toggles travel between switch 1 down and switch 3 up; shoulder/legs targets 4-6 move with it and become unavailable below the playfield. The proven table uses a 240-unit range over 62 update steps, which is useful initial tuning. Output 3 is the strong non-centering Iron Monger magnet. Output 4 is the separate Whiplash magnet by targets 47/48. Apply real force to a steel ball and retain moving target/collision geometry; do not teleport the ball or set endpoint switches before travel completes.

## Posts and standard devices

Output 6 commands the orbit up-post and output 12 the center-lane up-post; both are unsensed and must change physical collision state. Flippers use outputs 15/16 with public button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops pair 9/30, 10/31, and 11/32. Slings pair 17/26 and 18/27. Output 8 is an optional 16 VAC shaker on RED-WHT/J17-P7: the manual's Q8 table prints 50 VDC, but its transformer/I/O schematics prove the 16 VAC secondary. Q7, Q13, and Q14 are unpopulated. Q24 is the manual's optional 5 V device/coin-meter channel even though the proven VPW table includes address 24 in its SetLampMod flasher block; physical service construction governs, so do not add a stock Q24 playfield flasher.

## Lamps, flashers, and controller capacity

Lamp addresses 1-63 are populated, 64-72 are unused, 73/79/80 are hidden clear #555 row-10 bulbs, and 74-78 are unused. Address 55 has quantity two and Q20-23/Q25-32 carry explicit physical quantities, including the two Q31 lower-left-ramp emitters. Those multiplicities are documented cross-edition inferences from the same logical/playfield layout: the numbered callouts are in the 2014 Vault location maps and the exact working table is the Vault VPW, while the 2010 parts book does not number lamp or coil addresses. The original parts drawing shows unnumbered twist-lock sockets over the playfield underside; population of 73/79/80 is likewise a documented cross-edition inference from that construction, Stern's shared-code compatibility, and the later service grid rather than a numbered 2010 callout. Preserve original incandescent construction for every shared emitter, and bind lamp matrix 1-80, GI 0, synthetic game-on 33, explicit unused auxiliary compatibility addresses 51-66, and the 128x32 four-bit DMD. Public solenoids 34-36 are legacy aliases of game-on 33 and are not physical outputs.

## Author construction checklist

- Build the four-ball trough, manual/auto shooter, War Machine capture/kickback, motorized Iron Monger with moving collision targets and both endpoints, both non-centering magnets, two unsensed up-posts, two ramps, orbit/spinner network, fixed target banks, flippers, pops, slings, and optional shaker.
- Initialize trough switches 18-21 and Iron Monger down switch 1. Preserve EOS polarity, actual motor endpoint timing, ball occupancy, and collision gating.
- Bind every explicit matrix/dedicated/DIP input, Q1-Q32, game-on 33, unused auxiliary capacity 51-66, lamp 1-80, GI 0, and DMD. Keep unused and optional channels explicit.
- Use the proven VPX script when runtime behavior is ambiguous, but use the 2010 parts book for original construction and the 2014 manual only for the shared logical/wiring map.

## Ordered VPX search and shared-layout reconciliation

Search was performed in the required order: `Visual Pinball/Tables`, `Visual Pinball/Tables Archive`, VPinball Universe, then VPForums. Every retained candidate was inspected with `vpxtool git:v0.33.3` using `romname`, `info show`, readable script extraction, and normalized candidate extraction. The complete portable register is `evidence/vpx/source-candidate-register/stern/iron-man-2010.json`; scripts and candidate reports are retained under `evidence/vpx/`.

The local temporary `im2_160` table and JP's community Armored Adventures retheme remain rejected. The local VPW and archive files are explicit Vault products and remain ineligible as standalone proof of original construction. The VPU Siggi table and both authenticated VPF downloads identify the physical Stern 2010 product. The VPF lineage explicitly says its positions were rearranged according to Iron Man Vault and binds `im_186ve`; Stern separately confirms that 1.86 code applies to both products. A VE suffix therefore proves firmware selection, not physical edition identity.

The official 2010 parts-book assembly drawings on PDF pages 25-26 and the official 2014 numbered switch/lamp/coil maps on PDF pages 17, 19, and 21 show the same two-dimensional playfield device layout. The three original-product VPX candidates independently retain that topology, while their raw render-object centers differ where authors rebuilt lights, moved cosmetic helpers, or collapsed physical emitter clusters. Switch 37 is the clearest conflict: the three raw centers are `(0.970588, 0.256501)`, `(0.912831, 0.059858)`, and `(0.932986, 0.078329)`, while the reviewed manual-reconciled anchor is `(0.915480, 0.092892)`. Canonical positions therefore use the reviewed shared-layout frame, never an average of raw table centers. The content-locked candidate register and retained 309/419/436-point reports make the decision reproducible.

This promotion is deliberately two-dimensional and edition-safe. It reuses only x/y locations for devices whose physical region and controller semantics are shared. Original incandescent lighting, multi-piece toys and launcher, cabinet/backbox construction, and every other 2010-specific physical fact remain sourced from the original parts book. Vault LED modules, one-piece toys, exact edition parts, Z coordinates, heights, and renderer helpers are never projected backward.

## Sources

- `manual.iron-man-original-parts.2010`: official scanned 2010 parts book SHA-256 `0948d154156860d351daa943ab3b5882ef4c86bb42cde630bcd04067ab85ed1a`; organized under the external manual cache.
- `manual.iron-man-vault-edition.2014`: official native-text service manual SHA-256 `20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990`; shared logical tables and wiring are on PDF pages 16-21 and 48-58.
- `vpx.iron-man-vault-vpw-1.0.1`: exact known-working `im_185ve` script SHA-256 `d0d37548468d67aa895121fd6ff82fdacc1d1a301a702c92325fb3ee9d7a89ea` at pinned revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e`.
- `runtime.iron-man-vault.boot-start`: exact-ROM compatible-code trace SHA-256 `2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9`; ROM bytes remain external.
- `evidence/vpx/source-candidate-register/stern/iron-man-2010.json`: deterministic four-tier VPX candidate register with full-table hashes, page identities, decisions, and retained extraction hashes.
- `human-review.iron-man-original-shared-layout.2026-08-04`: fail-closed reconciliation of both manuals, the reviewed Vault geometry, and three original-product candidate reports; licenses no inference beyond normalized 2D shared layout.
"""


VE_KNOWLEDGE = """# Iron Man Pro Vault Edition (Stern, 2014)

Coverage: **author-ready - complete physical I/O inventory, PinMAME bindings, wiring, custom mechanisms, edition construction, and recreation behavior validated**

## Identity and evidence precedence

This is the June/July 2014 Iron Man Pro Vault Edition reissue, IPDB 6154, model I-00B0 and Stern product 500-55B0-01. It covers only `im_183ve`, `im_185ve`, and `im_186ve`; the non-`ve` drivers belong to the original 2010 physical product even though PinMAME's clone graph shares one root. The exact `im_185ve` VPW script is runtime ground truth, the 2014 native-text service manual governs physical inventory/wiring, the original parts book documents inherited geometry, and PinMAME governs transport/display metadata.

## Vault Edition construction boundary

The logical game and mechanism map is shared with the original. The reissue adds LED playfield lighting, a modern metal/wood backbox with red T-molding, brushed-aluminum cabinet decals and new speaker-panel art, strengthened one-piece molded Iron Monger/War Machine/Whiplash toys, and Stern's then-current one-piece auto launcher. Preserve those physical differences when recreating this product. The service matrix uses LED module 112-5033-08 for most inserts but explicitly calls for clear #555-form-factor lamps at 54, 56, 73, 79, and 80; the three row-10 lamps are unlabeled load/test positions absent from the playfield location map.

## Ball path and custom devices

Four balls occupy switches 18-21; jam opto 22 and trough up-kicker 1 serve shooter switch 23, which supports manual and automatic launch through output 2. War Machine opto 10 holds a ball until kick-back output 5 ejects it. Orbit and center-lane posts are outputs 6 and 12 and have no sensors. Whiplash magnet 4 acts near targets 47/48. Spinners are 11/13/14, ramp entrance/exits 12/43/37/49, orbit rollovers 7/9, and the four drone targets 44-46/50. Never create a physical trough-release switch at address 15; the manual proves it is Tournament Start despite an old VPX bookkeeping pulse.

## Motorized Iron Monger

Output 19 toggles the Iron Monger lift between endpoint switch 1 down and switch 3 up. Target faces 4-6 and the toy's collision/flash geometry move with it; targets must become unavailable below the playfield. Output 3 is the strong non-centering magnet in the assembly. The proven table's 240-unit travel over 62 update steps is useful initial tuning, but its early endpoint-switch mutation is an animation shortcut. A recreation must report endpoints when physical travel reaches them and must apply magnetic force without teleporting the ball.

## Standard devices, lamps, and capacity

Flippers are outputs 15/16 with button/EOS pairs 84/83 and 82/81; EOS contacts are normally closed. Pops pair 9/30, 10/31, 11/32, and slings 17/26, 18/27. Output 8 is an optional 16 VAC shaker on RED-WHT/J17-P7; the manual's Q8 table says 50 VDC but its transformer/I/O schematics prove the 16 VAC feed. Q7/Q13/Q14 are unused. Q24 is the manual's optional 5 V coin-meter/device channel even though the proven VPW table includes it in the SetLampMod flasher block; the physical service table wins and no stock Q24 playfield flasher should be created. Q20-23/Q25-32 are LED flashers with exact module parts in the JSON; Q31 drives the two lower-left-ramp emitters shown in the location map and called x2 by the exact script. Lamp 1-63 and 73/79/80 are populated; address 55 drives two physical Mark VI emitters, 64-72 and 74-78 are unused, and the hidden row-10 bulbs are non-playfield electrical loads. Bind GI 0, synthetic game-on 33, explicit unused SAM auxiliary capacity 51-66, and the 128x32 four-bit DMD; never turn legacy aliases 34-36 or auxiliary capacity into playfield hardware.

## Spatial construction and multiplicity

Player-view positions use x=0 left, x=1 right, y=0 rear/backglass, and y=1 apron. Exact coordinates come from the organized 245,182,464-byte VPW table after semantic reconciliation against the official switch, lamp, coil, and GI maps. The controller script is runtime ground truth, but VLM light-map callbacks, reflections, transmission layers, and room/VR effects are renderer helpers rather than physical devices. Jam opto 22 has no table object; its disclosed approximate anchor is a least-squares continuation of the exact consecutive sw18-sw21 centers, with about plus or minus 0.02 normalized x/y uncertainty.

The official GI schematic fixes 27 playfield emitters on circuits B/Y/V (10/7/10), ten rear-panel emitters on circuit G, and two US or three European coin-door bulbs. Playfield construction is 25 under-playfield #44 bulbs plus one above-playfield #555 bulb on circuit Y and one on circuit V. The latter use exact `Lspot1`/`Lspot2` source centers: the VPW changelog says spotlight bulbs were separated and its ball-shadow code treats those objects as sources. Nearby `gi004`/`gi014` are the separated halo/render passes, not two more sockets; the other 25 physical playfield positions use exact `giNNN` centers. Objects `gi024`, `gi027`, `gi030`, and `gi031` are four rear-wall render pools introduced for backwall illumination, not physical sockets. The ten physical rear #44 sockets are represented by an explicit evenly spaced y=0 projection across the manual's single rear-panel row because the perspective sketch proves row and count but not ten independently measurable centers. The US coin-door branch has two #555 bulbs and the European branch three; cabinet bulbs intentionally have no playfield coordinate. The JSON uses US quantity 39 and documents European quantity 40.

Physical multiplicity follows the service maps even when VPW combines light output: Q22 has two modules at one War Machine-front cluster, Q27 has three War Machine modules, Q28 has three moving Iron Monger chest modules at one toy anchor, Q30 has two separately located Mark VI flashers around one combined table pool, and Q31 has two separately located lower-left-ramp emitters around one combined table pool. Lamp 55 likewise drives two separately mapped physical Mark VI emitters through one address while VPW exposes one central pool. Hidden row-10 lamps 73/79/80 are explicit internal nonvisual electrical loads with no invented playfield position; they are not cabinet devices. Cluster anchors preserve the correct construction region and quantity without misclassifying visual fanout as additional hardware.

Where the exact table collapses distinct modules, the individual Q27/Q30/Q31/lamp-55 construction anchors are calibrated from multiple official-map callouts against exact shared table points. Those manual projections have practical uncertainty of about plus or minus 0.01 normalized x and 0.02-0.04 normalized y; they preserve proven physical region and separation without claiming unrecoverable table precision.

## Author construction checklist

- Build the typed four-ball trough, one-piece manual/auto launch, War Machine capture/kickback, strengthened moving Iron Monger with endpoints/targets/magnet, Whiplash target/magnet, both unsensed up-posts, ramps/orbits/spinners, fixed target banks, flippers, pops, slings, and optional shaker.
- Initialize switches 18-21 and Iron Monger down switch 1. Preserve ball occupancy, normally-closed EOS contacts, moving collision geometry, and real endpoint timing.
- Bind every matrix/dedicated/DIP input, Q1-Q32, game-on 33, unused auxiliary 51-66, lamp 1-80, GI 0, and DMD, including the three unlabeled clear matrix bulbs.
- Recreate all documented emitter multiplicities, ten rear-panel GI sockets, the applicable two- or three-bulb coin-door GI branch, and both address-55 Mark VI emitters; do not use the number of VPX render helpers as a parts count.
- Use the exact VPW behavior as the runtime tie-breaker and the official 2014 service manual for construction, wiring, parts, and lamp technology.

## Sources

- `manual.iron-man-vault-edition.2014`: official manual SHA-256 `20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990`; organized under the external manual cache.
- `vpx.iron-man-vault-vpw-1.0.1`: pinned known-working exact-ROM script SHA-256 `d0d37548468d67aa895121fd6ff82fdacc1d1a301a702c92325fb3ee9d7a89ea`.
- `vpx-table.iron-man-vault-vpw-1.0-geometry`: organized exact table SHA-256 `c0abc5d90d77a4cf7c3f0455cff91d4f0b9f7e750264742b987e9ddb30ab7a4b`; table bounds are 0..952 by 0..2215 and only semantically reconciled geometry is used.
- `rom.iron-man-vault.im-185ve`: exact external archive SHA-256 `e04c56ca08cdd6b0aaa6fcacd601e183d338dae7a863a4486216f76b25d6738f`; contained binary SHA-256 `c827da1c3f5305b27e9e504d7553bcd9c39547f357dd3827122adcc4c173c257`.
- `runtime.iron-man-vault.boot-start`: exact boot/start trace SHA-256 `2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9` with game-on 33, DMD, lamps, and GI observed.
"""


def runtime_evidence() -> dict[str, object]:
	return {
		"format": "pinmame-machine-evidence", "version": 1,
		"machine_ids": ["stern.iron-man.2010", "stern.iron-man-vault-edition.2014"], "driver_ids": ["im_185ve"],
		"extractor": {"id": "libpinmame-gameplay-harness", "version": 1},
		"switches": [], "outputs": [], "mechanisms": [], "states": [],
		"recreation_notes": [],
		"runtime": {
			"game": "im_185ve",
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game im_185ve --rom-path <vpinmame-roms> --work-dir <isolated-state> --initial-switch 1 --initial-switch 18 --initial-switch 19 --initial-switch 20 --initial-switch 21 --pulse 65:300:0.7 --pulse 65:300:0.7 --pulse 65:300:0.7 --pulse 65:300:0.7 --pulse 65:300:0.7 --pulse 65:300:1.0 --pulse 16:500:3 --observe 3 --dmd-dir <external-dmd-dir> --output <external-json>",
			"rom_archive_sha256": "e04c56ca08cdd6b0aaa6fcacd601e183d338dae7a863a4486216f76b25d6738f",
			"raw_runs": [{"name": "boot-start-v3", "sha256": "2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9", "self_test_pulses": 0}],
			"observations": {"display_layouts_seen": [{"type": 14, "width": 128, "height": 32, "depth": 4}], "lamp_addresses_seen": sorted(RUNTIME_LAMPS_SEEN), "solenoid_addresses_seen": [33], "gi_addresses_seen": [0]},
		},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "path": "external:pinmame-game-code/iron-man-vault-edition/harness/boot-start-v3/run.json", "sha256": "2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9", "license": "NOASSERTION", "quality": "validated", "attribution": "Generated locally from PinMAME and the user-authorized ROM corpus; Stern's official 1.86 release note establishes compatibility with both physical editions while ROM bytes remain external"},
	}


def main() -> None:
	if "stern.iron-man.2010" in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		write_json(spatial_partial_path(ROOT / "machines/partial/stern/iron-man-2010.json"), fail_closed_spatial_partial(build(False)))
	if "stern.iron-man-vault-edition.2014" in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		write_json(spatial_partial_path(ROOT / "machines/partial/stern/iron-man-vault-edition-2014.json"), fail_closed_spatial_partial(build(True)))
	write_json(ROOT / "evidence/runtime/sam/iron-man-vault-edition-boot-start.json", runtime_evidence())
	write_json(CANDIDATE_REGISTER_PATH, VPX_CANDIDATE_REGISTER)
	write_text(ROOT / "knowledge/stern/iron-man-2010.md", fail_closed_spatial_knowledge("stern.iron-man.2010", ORIGINAL_KNOWLEDGE))
	write_text(ROOT / "knowledge/stern/iron-man-vault-edition-2014.md", fail_closed_spatial_knowledge("stern.iron-man-vault-edition.2014", VE_KNOWLEDGE))


if __name__ == "__main__":
	main()
