<script setup lang="ts">
useSeo({
	title: 'Reading a definition',
	description: 'How to read a PinMAME machine definition: identity, address bindings, device kinds, polarity, portable roles, coverage states and evidence precedence.',
})

const repoLink = useRepoLink()

const PLAN = 'docs/MACHINE_DEFINITIONS_PLAN.md'

/** Each concept below is specified in a named section of the plan document. */
const spec = (anchor: string) => `${repoLink.file(PLAN)}#${anchor}`

const specLinks = [
	{ label: 'Identity hierarchy', anchor: 'proposed-identity-hierarchy' },
	{ label: 'Group and routing model', anchor: 'proposed-group-and-routing-model' },
	{ label: 'Device and mechanism model', anchor: 'device-and-mechanism-model' },
	{ label: 'Provenance and validation states', anchor: 'provenance-and-validation-states' },
	{ label: 'Inheritance and merge rules', anchor: 'inheritance-and-merge-rules' },
]

const sections = [
	{ id: 'identity', label: 'Identity' },
	{ id: 'addresses', label: 'Addresses & bindings' },
	{ id: 'kinds', label: 'Device kinds' },
	{ id: 'polarity', label: 'Polarity' },
	{ id: 'roles', label: 'Portable roles' },
	{ id: 'mechanisms', label: 'Mechanisms & wiring' },
	{ id: 'coverage', label: 'Coverage & confidence' },
	{ id: 'precedence', label: 'Evidence precedence' },
	{ id: 'workflow', label: 'A working order' },
	{ id: 'spec', label: 'The specification' },
]

const kinds = [
	{ kind: 'switch', body: 'A matrix or dedicated input the ROM polls. The address is the public PinMAME switch number, not a hardware pin.' },
	{ kind: 'dip_switch', body: 'Configuration bits on the CPU board. Not playfield hardware — they set replay levels, country and options.' },
	{ kind: 'coil', body: 'A driver output that moves something: kickers, ejects, posts, drop-target resets, flippers.' },
	{ kind: 'flasher', body: 'A driver output whose only job is light. Same address space as coils on most platforms.' },
	{ kind: 'lamp', body: 'A lamp-matrix channel. Insert lighting, controlled per address.' },
	{ kind: 'rgb_lamp', body: 'A colour-addressable lamp, modelled as a parent with explicit channel bindings.' },
	{ kind: 'gi', body: 'General illumination string. Often a single aggregate channel switching the whole string at once.' },
	{ kind: 'magnet', body: 'A holding or steering electromagnet. Strength and timing come from the recreation notes.' },
	{ kind: 'motor', body: 'A continuously driven mechanism — spinning toys, moving targets, gun turrets.' },
	{ kind: 'relay', body: 'Switches a circuit rather than driving a device directly.' },
	{ kind: 'virtual', body: 'Not physical hardware. A state the emulator exposes on an output address, such as SAM’s game-on flag.' },
]
</script>

<template>
	<div class="mx-auto max-w-[100rem] px-4 py-8 sm:px-6">
		<header class="mb-10 max-w-3xl">
			<h1 class="text-2xl font-semibold tracking-tight sm:text-3xl">
				Reading a machine definition
			</h1>
			<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
				Everything on this site comes from one JSON document per physical machine plus a markdown note beside it. This
				page explains the vocabulary those documents use, so the numbers on a machine page mean exactly one thing.
			</p>
		</header>

		<div class="grid gap-10 xl:grid-cols-[13rem_minmax(0,1fr)]">
			<aside class="hidden xl:block">
				<nav class="sticky top-20 space-y-0.5">
					<a
						v-for="section in sections"
						:key="section.id"
						:href="`#${section.id}`"
						class="block rounded-lg px-2.5 py-1.5 text-[13px] text-ink-3 transition-colors hover:bg-raised hover:text-ink"
					>{{ section.label }}</a>
				</nav>
			</aside>

			<div class="min-w-0 max-w-3xl space-y-12">
				<section id="identity" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						Identity: machine, driver, device
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Three identifiers do three different jobs, and keeping them apart is what lets a table survive a catalog
						update.
					</p>
					<dl class="mt-5 space-y-3">
						<div v-for="item in [
							{ term: 'machine.id', example: 'stern.metallica-pro.2013', body: 'The physical product. One playfield, one wiring loom, one definition — however many ROM revisions exist.' },
							{ term: 'driver id', example: 'mtl_180h', body: 'An exact PinMAME ROM set. Many drivers resolve to one machine; clones share its definition unless a hardware difference is recorded.' },
							{ term: 'device id', example: 'switch.fuel-lane-rollover', body: 'A stable semantic name for one input or output. This is what a table should bind to. If a controller number ever changes, the device id does not.' },
						]" :key="item.term" class="panel p-4"
						>
							<dt class="flex flex-wrap items-baseline gap-3">
								<span class="num text-sm text-amber">{{ item.term }}</span>
								<span class="num text-xs text-ink-4">{{ item.example }}</span>
							</dt>
							<dd class="mt-2 text-[13px] leading-relaxed text-ink-3">
								{{ item.body }}
							</dd>
						</div>
					</dl>
				</section>

				<section id="addresses" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						Addresses and bindings
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Every device carries a <span class="num text-amber">binding</span>: a group plus a signed device number.
						The group names the address space — <span class="num">pinmame.input.switch</span>,
						<span class="num">pinmame.output.solenoid</span>, <span class="num">pinmame.output.lamp</span> — and the
						platform profile says which numbers are legal in it.
					</p>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Numbers are the values PinMAME's public API reports, not hardware pins. WPC-family machines address the
						matrix as column·row, so 52 is column 5 row 2. SAM and later platforms number sequentially. Negative
						numbers are real: they carry diagnostic and dedicated inputs that sit outside the matrix.
					</p>
					<div class="panel mt-5 flex gap-3 p-4">
						<Icon name="lucide:lightbulb" class="mt-0.5 size-4 shrink-0 text-amber" />
						<p class="text-[13px] leading-relaxed text-ink-3">
							The switch and lamp maps on a machine page lay these out visually. Holes in the grid are meaningful —
							an address marked <em>unused</em> was checked and found to have nothing wired to it, which is different
							from an address nobody has looked at.
						</p>
					</div>
				</section>

				<section id="kinds" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						Device kinds
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						A small taxonomy, used consistently. The colour of a chip means the same thing on every page.
					</p>
					<ul class="mt-5 space-y-2">
						<li v-for="item in kinds" :key="item.kind" class="panel flex flex-wrap items-baseline gap-x-4 gap-y-1 p-3">
							<KindChip :kind="item.kind" />
							<span class="min-w-0 flex-1 text-[13px] leading-relaxed text-ink-3">{{ item.body }}</span>
						</li>
					</ul>
				</section>

				<section id="polarity" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						Polarity belongs to hardware, not to your table
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Platform profiles declare
						<span class="num text-amber">inversion_applied_by_emulator</span>. Where it is true, PinMAME has already
						normalised the signal and reports logical active state. Inverting again in a table produces a machine that
						boots with every optical switch backwards.
					</p>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Separately, a switch may be marked <span class="num text-amber">normally_closed</span>. That is a physical
						fact about the real part — an opto that conducts at rest, a drop target closed while raised. Build the right
						hardware behaviour; do not convert it into a runtime flip.
					</p>
				</section>

				<section id="roles" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						Portable roles
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Cabinet and service inputs carry roles like
						<span class="num text-amber">cabinet.start</span>,
						<span class="num text-amber">flipper.lower.left</span> and
						<span class="num text-amber">service.up</span>. They are deliberately engine-neutral: the catalog says
						which address is the start button, and the consuming engine decides which key or input action that maps to.
					</p>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						<span class="num text-amber">ball.position</span> marks the switches a ball rests on at boot — build balls
						there and the ROM finds a full trough. <span class="num text-amber">position.*</span> marks mechanism
						home, up, down and index sensors.
					</p>
				</section>

				<section id="mechanisms" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						Mechanisms and direct wiring
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						A mechanism ties actuators and sensors together and describes how the assembly behaves — which output ejects,
						which switch confirms, what state it starts in. Where a known-working table exists, the note carries its
						tested strengths, angles and timings as a starting point rather than a guess.
					</p>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Relationships are the connections that exist in copper. A
						<span class="num text-amber">pulse</span> relationship means closing that switch fires the coil in hardware
						— pop bumpers and slingshots do this — so it must fire whether or not a game is running. Do not wait for
						the ROM.
					</p>
				</section>

				<section id="coverage" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						Coverage and confidence are two different things
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						<strong class="text-ink">Coverage</strong> is the lifecycle of the whole definition: stub, partial, or
						author-ready. It is fail-closed — only the completeness validator can grant author-ready, and it refuses
						while any address is unnamed, any mechanism lacks its topology, or the recreation note is missing.
					</p>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						<strong class="text-ink">Provenance</strong> is per assertion: unknown, candidate, observed, validated,
						conflicted, deprecated. Observing that output 11 toggled is not the same as knowing it is the gun motor,
						and failing to observe an output is not evidence that it is unused.
					</p>
					<div class="mt-5 grid gap-3 sm:grid-cols-3">
						<div v-for="status in (['author_ready', 'partial', 'stub'] as const)" :key="status" class="panel p-4">
							<StatusChip :status="status" />
							<p class="mt-3 text-[13px] leading-relaxed text-ink-3">
								{{ STATUS_META[status].blurb }}
							</p>
						</div>
					</div>
				</section>

				<section id="precedence" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						When sources disagree
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Precedence is domain-specific, not a single ranking:
					</p>
					<ul class="mt-5 space-y-3">
						<li v-for="rule in [
							{ icon: 'lucide:file-code-2', title: 'A known-working VPX script', body: 'wins on controller addresses, callbacks, ball routing and mechanism causality. It is proof that a real ROM accepts those bindings.' },
							{ icon: 'lucide:book-open', title: 'The operator manual', body: 'wins on wiring, connectors and wire colours, part numbers, switch construction and polarity, and assembly geometry.' },
							{ icon: 'lucide:cpu', title: 'Pinned PinMAME source', body: 'wins on emulator group routing, display layout, output typing, and whatever the public API normalises before you see it.' },
						]" :key="rule.title" class="panel flex gap-3 p-4"
						>
							<span class="mt-0.5 grid size-7 shrink-0 place-items-center rounded-md border border-line bg-raised text-amber">
								<Icon :name="rule.icon" class="size-3.5" />
							</span>
							<p class="text-[13px] leading-relaxed text-ink-3">
								<strong class="text-ink">{{ rule.title }}</strong> {{ rule.body }}
							</p>
						</li>
					</ul>
					<p class="mt-4 text-[13px] leading-relaxed text-ink-3">
						A lower-priority source can still open a conflict when the higher-priority one is ambiguous, incomplete, or
						is clearly implementing a virtual simplification rather than the physical mechanism. Unresolved conflicts
						stay visible at the top of a machine page rather than being quietly decided.
					</p>
				</section>

				<section id="workflow" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						A working order
					</h2>
					<ol class="mt-5 space-y-3">
						<li v-for="(step, index) in [
							'Look up your ROM set to find the physical machine it resolves to, and check the coverage badge before you rely on anything.',
							'Read the “Wire it up” panel: platform, display geometry, address ranges, ball positions at boot, cabinet and flipper roles.',
							'Build the switches from the switch map, keeping unused addresses genuinely empty so the ROM sees the real machine.',
							'Wire the coils, flashers, lamps and GI, then add the direct-wired pulse relationships so pops and slings fire in hardware.',
							'Implement each mechanism using its actuators, sensors and behaviour text — and the tuning values from the recreation note.',
							'Read the recreation note end to end before shipping. It is where edition differences and the “do not copy this” warnings live.',
						]" :key="index" class="panel flex gap-4 p-4"
						>
							<span class="num grid size-7 shrink-0 place-items-center rounded-lg border border-line text-xs text-amber">{{ index + 1 }}</span>
							<p class="text-[13px] leading-relaxed text-ink-2">
								{{ step }}
							</p>
						</li>
					</ol>
				</section>

				<section id="spec" class="scroll-mt-20">
					<h2 class="text-lg font-semibold tracking-tight">
						The specification
					</h2>
					<p class="mt-3 text-[15px] leading-relaxed text-ink-2">
						Everything above is a reading of one document. These link to the section that defines it.
					</p>
					<ul class="mt-5 grid gap-2 sm:grid-cols-2">
						<li v-for="link in specLinks" :key="link.anchor">
							<a
								:href="spec(link.anchor)"
								target="_blank"
								rel="noopener noreferrer"
								class="panel group flex items-center gap-3 px-3 py-2.5 transition-colors hover:border-amber/35"
							>
								<Icon name="lucide:file-text" class="size-3.5 shrink-0 text-ink-4" />
								<span class="min-w-0 flex-1 truncate text-[13px] transition-colors group-hover:text-amber">{{ link.label }}</span>
								<Icon name="lucide:arrow-up-right" class="size-3.5 shrink-0 text-ink-4" />
							</a>
						</li>
					</ul>
				</section>

				<ContributeCard
					hint="Every machine page has an edit link to its own definition file, and every platform page to its profile. Editing on GitHub forks the repository for you and opens the pull request — the fastest useful contribution is correcting one wrong label with a source for the right one."
					primary-to="/machines?status=author_ready"
					primary-label="Find a definition to check"
				/>
			</div>
		</div>
	</div>
</template>
