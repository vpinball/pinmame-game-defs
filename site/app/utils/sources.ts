/**
 * What each kind of source is, and how far to trust it.
 *
 * Shared between the evidence list and the conflict panel: when a conflict says
 * three sources disagree, it has to name them in the same words the evidence
 * section further down the page uses, or the reader is left matching ids by eye.
 */
export const SOURCE_META: Record<string, { label: string, icon: string, blurb: string }> = {
	manual: { label: 'Operator manual', icon: 'lucide:book-open', blurb: 'Authoritative for wiring, connectors, switch construction and assembly geometry.' },
	service_bulletin: { label: 'Service bulletin', icon: 'lucide:file-warning', blurb: 'Factory correction to the manual.' },
	service_diagnostic: { label: 'Service diagnostic', icon: 'lucide:activity', blurb: 'Names read out of the machine’s own test menus.' },
	vpx_script: { label: 'VPX script', icon: 'lucide:file-code-2', blurb: 'Known-working table script — ground truth for controller addresses and mechanism causality.' },
	vpx_table: { label: 'VPX table', icon: 'lucide:table-2', blurb: 'The table file the script came from, for physical-object evidence.' },
	pinmame_core: { label: 'PinMAME source', icon: 'lucide:cpu', blurb: 'Authoritative for emulator routing, display layout and output typing.' },
	pinmame_catalog: { label: 'PinMAME catalog', icon: 'lucide:list', blurb: 'Driver identity as reported by the pinned library build.' },
	pinmame_sim: { label: 'PinMAME simulator', icon: 'lucide:play', blurb: 'Names from PinMAME’s built-in table simulator.' },
	rom_static_analysis: { label: 'ROM analysis', icon: 'lucide:binary', blurb: 'Facts recovered from the game ROM itself.' },
	runtime_scenario: { label: 'Runtime run', icon: 'lucide:terminal', blurb: 'Observed by actually booting the ROM in a harness.' },
	human_review: { label: 'Human review', icon: 'lucide:user-check', blurb: 'A curator’s reviewed judgement.' },
	legacy_json: { label: 'Legacy definition', icon: 'lucide:archive', blurb: 'Imported from the previous VPE game definitions.' },
	vpe_csharp: { label: 'VPE C# definition', icon: 'lucide:file-type-2', blurb: 'Imported from the original C# game classes.' },
}

/** Controller profiles cite sources without a `kind`, so fall back gracefully. */
export const sourceMeta = (kind: string | null | undefined) =>
	(kind ? SOURCE_META[kind] : undefined) ?? { label: kind ? titleCase(kind) : 'Reference', icon: 'lucide:file', blurb: '' }
