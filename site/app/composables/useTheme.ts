export type Theme = 'dark' | 'light'

const STORAGE_KEY = 'pmg-theme'

export function useTheme() {
	const theme = useState<Theme>('theme', () => 'dark')

	function apply(next: Theme) {
		theme.value = next
		if (import.meta.client) {
			document.documentElement.dataset.theme = next
			try {
				localStorage.setItem(STORAGE_KEY, next)
			}
			catch {
				// Private-mode browsers: the toggle still works for this session.
			}
		}
	}

	const toggle = () => apply(theme.value === 'dark' ? 'light' : 'dark')

	onMounted(() => {
		let stored: string | null = null
		try {
			stored = localStorage.getItem(STORAGE_KEY)
		}
		catch { /* ignore */ }
		if (stored === 'light' || stored === 'dark') apply(stored)
		else theme.value = (document.documentElement.dataset.theme as Theme) ?? 'dark'
	})

	return { theme, toggle, apply }
}
