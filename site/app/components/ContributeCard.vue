<script setup lang="ts">
/**
 * The contribution call-to-action.
 *
 * Corrections belong in the definitions, not in this site, so every action here
 * lands on a specific file in the catalog rather than on the repository's front
 * page. GitHub's `/edit/` route forks and opens the pull-request form directly,
 * which makes "the label on switch 19 is wrong" a two-minute fix with no local
 * checkout.
 */
const props = withDefaults(defineProps<{
	/** Repo-relative path of the definition this page renders. */
	definitionPath?: string | null
	/** Repo-relative path of the recreation note, when one exists. */
	knowledgePath?: string | null
	/** Used to prefill an issue when someone would rather report than edit. */
	subject?: string | null
	/** A stub or missing profile needs authoring, not correcting. */
	tone?: 'improve' | 'author'
	/** Extra guidance specific to the page this appears on. */
	hint?: string | null
	/** Replaces the primary action with an in-site route (used on overviews). */
	primaryTo?: string | null
	primaryLabel?: string | null
}>(), {
	definitionPath: null,
	knowledgePath: null,
	subject: null,
	tone: 'improve',
	hint: null,
	primaryTo: null,
	primaryLabel: null,
})

const repoLink = useRepoLink()

const issueUrl = computed(() => repoLink.issue(
	props.subject ? `${props.subject}: ` : '',
	[
		props.subject ? `**Machine:** ${props.subject}` : '',
		props.definitionPath ? `**Definition:** \`${props.definitionPath}\`` : '',
		'',
		'**What is wrong**',
		'',
		'',
		'**Evidence** — manual page, VPX script line, PinMAME source, or a reading from the service menu',
		'',
	].join('\n'),
))

/** External links only; the primary in-site action is rendered separately. */
const links = computed(() => [
	{
		href: props.definitionPath && !props.primaryTo ? repoLink.edit(props.definitionPath) : null,
		icon: 'lucide:git-pull-request-arrow',
		label: props.tone === 'author' ? 'Start this definition' : 'Edit the definition',
		path: props.definitionPath,
		primary: true,
	},
	{
		href: props.knowledgePath ? repoLink.edit(props.knowledgePath) : null,
		icon: 'lucide:notebook-pen',
		label: 'Edit the note',
		path: props.knowledgePath,
		primary: false,
	},
	{
		href: issueUrl.value,
		icon: 'lucide:message-square-warning',
		label: 'Report a problem',
		path: null,
		primary: false,
	},
].filter(link => link.href))

const body = computed(() => props.hint ?? (props.tone === 'author'
	? 'Nobody has described this one yet. If you own it, have the manual, or have already built a working table for it, the definition is a single JSON file — and every address you name moves it closer to author-ready.'
	: 'Canonical machine fixes belong in the definition itself. Editing on GitHub forks it for you and opens the pull request; no local checkout needed.'))

const buttonClass = (primary: boolean) =>
	primary
		? 'bg-amber text-void hover:-translate-y-0.5'
		: 'border border-line text-ink-2 hover:border-amber/40 hover:text-ink'
</script>

<template>
	<section class="panel dotfield overflow-hidden">
		<div class="flex flex-wrap items-start gap-x-6 gap-y-4 p-5 sm:p-6">
			<div class="min-w-56 flex-1">
				<div class="flex items-center gap-2">
					<Icon name="lucide:git-pull-request-arrow" class="size-4 text-amber" />
					<h2 class="text-sm font-semibold">
						{{ tone === 'author' ? 'Help describe this machine' : 'Something wrong or missing?' }}
					</h2>
				</div>
				<p class="mt-2 max-w-2xl text-[13px] leading-relaxed text-ink-3">
					{{ body }}
				</p>
				<p class="mt-2 max-w-2xl text-[13px] leading-relaxed text-ink-4">
					Cite a source for anything you change — a manual page, a line in a working VPX script, PinMAME source, or a
					reading from the machine's own service menu. Claims without provenance cannot be validated.
				</p>
			</div>

			<div class="flex w-full shrink-0 flex-col gap-2 sm:w-auto">
				<NuxtLink
					v-if="primaryTo"
					:to="primaryTo"
					class="inline-flex items-center gap-2 rounded-lg px-3.5 py-2.5 text-[13px] font-medium transition-all"
					:class="buttonClass(true)"
				>
					<Icon name="lucide:list-checks" class="size-4 shrink-0" />
					{{ primaryLabel ?? 'Pick something to work on' }}
				</NuxtLink>
				<a
					v-for="link in links"
					:key="link.label"
					:href="link.href!"
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex items-center gap-2 rounded-lg px-3.5 py-2.5 text-[13px] font-medium transition-all"
					:class="buttonClass(link.primary && !primaryTo)"
					:title="link.path ?? undefined"
				>
					<Icon :name="link.icon" class="size-4 shrink-0" />
					{{ link.label }}
				</a>
			</div>
		</div>

		<div class="flex flex-wrap items-center gap-x-4 gap-y-1 border-t border-line px-5 py-3 text-[11px] text-ink-4 sm:px-6">
			<span class="eyebrow">Before you start</span>
			<a :href="repoLink.file('CONTRIBUTING.md')" target="_blank" rel="noopener noreferrer" class="num hover:text-amber">CONTRIBUTING.md</a>
			<a :href="repoLink.file('schemas/machine.schema.json')" target="_blank" rel="noopener noreferrer" class="num hover:text-amber">schemas/machine.schema.json</a>
			<a :href="repoLink.file('docs/MACHINE_DEFINITIONS_PLAN.md')" target="_blank" rel="noopener noreferrer" class="num hover:text-amber">docs/MACHINE_DEFINITIONS_PLAN.md</a>
			<NuxtLink to="/guide" class="hover:text-amber">
				How to read a definition
			</NuxtLink>
		</div>
	</section>
</template>
