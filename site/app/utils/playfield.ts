import type { Device, SpatialPlacement } from '~/types/defs'

/** The VPX default playfield — the space these coordinates normalise to. */
export const PF_WIDTH = 952
export const PF_HEIGHT = 2162

/** Marker radius in viewBox units; two markers touch at twice this apart. */
export const PF_MARKER = 13

/**
 * Normalised distance below which two placements visibly overlap. Slightly
 * under `2 * PF_MARKER / PF_WIDTH`, so markers group only once they actually
 * collide rather than merely sit near each other.
 */
export const PF_CLUSTER_RADIUS = 0.02

export interface PlacementRef {
	device: Device
	placement: SpatialPlacement
}

export interface PlayfieldCluster {
	key: string
	/** Centroid, in viewBox units. */
	cx: number
	cy: number
	members: PlacementRef[]
	deviceIds: string[]
	/** The kind colour when the cluster is uniform, else a neutral stack. */
	color: string
	uniformKind: boolean
	/** A single shared role, or null when the cluster mixes them. */
	role: SpatialPlacement['role'] | null
	hasEmitter: boolean
}

export const placementsOf = (devices: Device[]): PlacementRef[] =>
	devices.flatMap(device =>
		!device.spatial || device.spatial.status === 'not_applicable'
			? []
			: device.spatial.placements.map(placement => ({ device, placement })),
	)

/**
 * Greedy spatial clustering.
 *
 * A playfield stacks devices in the same spot — a standup target's switch sits
 * under its insert lamp, a pop bumper's skirt switch under its coil. Drawn
 * individually they overlap into an unreadable blob, so anything that collides
 * becomes one marker carrying a count.
 *
 * Greedy rather than k-means: the input is small, the result must be stable
 * across renders, and "these two are on top of each other" needs no smarter
 * definition than a distance threshold.
 */
export function clusterPlacements(
	refs: PlacementRef[],
	radius = PF_CLUSTER_RADIUS,
): PlayfieldCluster[] {
	const taken = new Array(refs.length).fill(false)
	const clusters: PlayfieldCluster[] = []

	for (let i = 0; i < refs.length; i++) {
		if (taken[i]) continue
		taken[i] = true
		const seed = refs[i]!
		const members = [seed]

		for (let j = i + 1; j < refs.length; j++) {
			if (taken[j]) continue
			const other = refs[j]!
			const dx = seed.placement.x - other.placement.x
			const dy = seed.placement.y - other.placement.y
			if (Math.hypot(dx, dy) <= radius) {
				taken[j] = true
				members.push(other)
			}
		}

		const cx = members.reduce((sum, m) => sum + m.placement.x, 0) / members.length
		const cy = members.reduce((sum, m) => sum + m.placement.y, 0) / members.length
		const kinds = new Set(members.map(m => m.device.kind))
		const roles = new Set(members.map(m => m.placement.role))

		clusters.push({
			key: `${seed.device.id}:${seed.placement.id}`,
			cx: cx * PF_WIDTH,
			cy: cy * PF_HEIGHT,
			members,
			deviceIds: [...new Set(members.map(m => m.device.id))],
			uniformKind: kinds.size === 1,
			color: kinds.size === 1 ? kindColor(members[0]!.device.kind) : 'var(--color-ink-2)',
			role: roles.size === 1 ? members[0]!.placement.role : null,
			hasEmitter: members.some(m => m.placement.role === 'emitter'),
		})
	}

	return clusters
}

/** Rounded outline with the arch a playfield has at the backglass end. */
export function playfieldOutline(arch = 380, foot = 44) {
	const w = PF_WIDTH
	const h = PF_HEIGHT
	return `M 0 ${h - foot} L 0 ${arch} Q 0 0 ${arch} 0 L ${w - arch} 0 Q ${w} 0 ${w} ${arch}`
		+ ` L ${w} ${h - foot} Q ${w} ${h} ${w - foot} ${h} L ${foot} ${h} Q 0 ${h} 0 ${h - foot} Z`
}
