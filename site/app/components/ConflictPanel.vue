<script setup lang="ts">
import type { RichConflict } from '~/types/defs'

/**
 * The disagreements nobody has settled.
 *
 * This is the most consequential block on a machine page — it tells an author
 * which numbers not to trust — and it used to be the least readable: one
 * unbroken paragraph per conflict, up to 2 000 characters, with the address,
 * the disagreeing parties, the evidence and the way out all run together.
 *
 * Each conflict now leads with the three things a reader actually wants:
 * **which address**, **who disagrees**, and **what would settle it**. The prose
 * follows for anyone who needs the argument. Nothing is summarised away — the
 * text is the record's own, only marked up (see scripts/conflicts.ts).
 */
defineProps<{ conflicts: RichConflict[] }>()

/** Bare numbers need their group to mean anything; device ids read alone. */
const address = (target: { label: string, group: string | null }) => {
	if (!/^-?\d+$/.test(target.label)) return target.label
	const kind = target.group?.replace(/^pinmame\.(input|output)\./, '') ?? ''
	return kind ? `${kind} ${target.label}` : target.label
}
</script>

<template>
	<section class="rounded-panel border border-alert/35 bg-panel">
		<header class="flex flex-wrap items-baseline gap-x-3 gap-y-1 border-b border-alert/25 px-4 py-3">
			<h2 class="flex items-center gap-2 text-sm font-semibold text-alert">
				<Icon name="lucide:triangle-alert" class="size-4" />
				{{ conflicts.length }} unresolved conflict{{ conflicts.length === 1 ? '' : 's' }}
			</h2>
			<p class="text-[13px] text-ink-3">
				Sources disagree here and nobody has settled it. Treat these addresses as unproven.
			</p>
		</header>

		<article
			v-for="conflict in conflicts"
			:key="conflict.id"
			class="border-b border-line-soft px-4 py-4 last:border-0"
		>
			<h3 v-if="conflict.title" class="text-[14px] font-semibold text-ink">
				{{ conflict.title }}
			</h3>

			<!-- what is in dispute, and who is disputing it -->
			<dl class="mt-2 flex flex-col gap-1.5 text-[12px] sm:flex-row sm:flex-wrap sm:gap-x-6">
				<div v-if="conflict.targets.length" class="flex flex-wrap items-baseline gap-x-2 gap-y-1">
					<dt class="text-ink-4">
						Affects
					</dt>
					<dd
						v-for="target in conflict.targets"
						:key="`${target.group}-${target.label}`"
						class="num rounded border border-line bg-raised px-1.5 py-0.5 text-ink-2"
					>
						{{ address(target) }}
					</dd>
				</div>

				<div v-if="conflict.sources.length" class="flex flex-wrap items-baseline gap-x-2 gap-y-1">
					<dt class="text-ink-4">
						Disagreeing sources
					</dt>
					<dd
						v-for="source in conflict.sources"
						:key="source.id"
						class="inline-flex items-center gap-1.5 rounded border border-line px-1.5 py-0.5 text-ink-2"
						:title="source.locator ?? source.id"
					>
						<Icon :name="sourceMeta(source.kind).icon" class="size-3 text-ink-4" />
						{{ sourceMeta(source.kind).label }}
					</dd>
				</div>
			</dl>

			<!-- eslint-disable-next-line vue/no-v-html -- built by scripts/conflicts.ts from the record's own text -->
			<div class="conflict-body mt-3 max-w-3xl" v-html="conflict.bodyHtml" />

			<!--
				The single most actionable line in the record, and in the raw JSON it
				is the tail of a paragraph nobody finishes.
			-->
			<div
				v-if="conflict.resolutionHtml"
				class="mt-3 flex max-w-3xl gap-2.5 rounded-lg border border-line bg-raised/60 px-3 py-2.5"
			>
				<Icon name="lucide:wrench" class="mt-0.5 size-3.5 shrink-0 text-amber" />
				<div class="min-w-0">
					<p class="eyebrow mb-1">
						What would settle it
					</p>
					<!-- eslint-disable-next-line vue/no-v-html -- same build-time source -->
					<p class="conflict-body text-[13px] text-ink-2" v-html="conflict.resolutionHtml" />
				</div>
			</div>
			<p v-else class="mt-3 flex items-center gap-2 text-[12px] text-ink-4">
				<Icon name="lucide:help-circle" class="size-3.5 shrink-0" />
				No resolution path recorded — someone has to work out what evidence would settle this.
			</p>

			<p v-if="conflict.path" class="num mt-2.5 text-[11px] break-all text-ink-4">
				{{ conflict.path }}
			</p>
		</article>
	</section>
</template>

<style scoped>
.conflict-body {
	font-size: 13px;
	line-height: 1.7;
	color: var(--color-ink-2);
	/* Conflict prose quotes connector pins and long identifiers inline; without
	   this the longest of them sets the panel's min-content width and scrolls
	   the whole page sideways on a phone. */
	overflow-wrap: anywhere;
}

.conflict-body :deep(p + p) {
	margin-top: 0.65rem;
}

.conflict-body :deep(code) {
	font-family: var(--font-mono);
	font-size: 0.85em;
	background: var(--color-raised);
	border: 1px solid var(--color-line-soft);
	border-radius: 4px;
	padding: 0.05em 0.3em;
	color: var(--color-amber-soft);
}

.conflict-body :deep(a) {
	color: var(--color-amber);
	text-decoration: underline;
	text-underline-offset: 3px;
	text-decoration-color: color-mix(in srgb, var(--color-amber) 40%, transparent);
}

.conflict-body :deep(a:hover) {
	text-decoration-color: currentColor;
}

/* A link wrapping a code span should read as one object, not two. */
.conflict-body :deep(a code) {
	color: inherit;
	border-color: color-mix(in srgb, var(--color-amber) 30%, transparent);
}
</style>
