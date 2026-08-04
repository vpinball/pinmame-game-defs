/**
 * Links into the `pinmame-game-defs` repository. Always point at a file (and a
 * line where one is known) — the repository root tells a reader nothing about
 * the fact they are checking.
 */
export function useRepoLink() {
	const { repo } = useAppConfig()
	const { public: { repoBranch } } = useRuntimeConfig()

	const file = (path: string, line?: number) =>
		`${repo.url}/blob/${repoBranch}/${path}${line ? `#L${line}` : ''}`

	const dir = (path: string) => `${repo.url}/tree/${repoBranch}/${path}`

	/**
	 * GitHub's web editor. It forks on the visitor's behalf and lands them on the
	 * pull-request form, so "fix this line" needs no local checkout.
	 */
	const edit = (path: string) => `${repo.url}/edit/${repoBranch}/${path}`

	/** Same, for a file that does not exist yet. */
	const create = (directory: string, filename: string) =>
		`${repo.url}/new/${repoBranch}?filename=${encodeURIComponent(`${directory}/${filename}`)}`

	const issue = (title: string, body: string) =>
		`${repo.url}/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`

	/** The exact PinMAME commit the catalog was generated from. */
	const pinmame = (revision: string, path?: string) =>
		path
			? `https://github.com/vpinball/pinmame/blob/${revision}/${path}`
			: `https://github.com/vpinball/pinmame/tree/${revision}`

	return { repo, file, dir, edit, create, issue, pinmame }
}
