# Skateball — observed continuous-output startup burst

Source: the three current-revision empty-state harness traces retained under `review-artifacts/skateball-1980/harness/`; binary and scenario pins are in `evidence/runtime/by35/skateball-1980-solenoid-tests.json`. The primary curator extracted the exact callback event times below. Times are seconds from each harness run's own start and are observations, not physical pulse specifications.

| Driver | Public output | Rising edge (s) | Falling edge (s) |
|---|---:|---:|---:|
| skatebll | 17 | 5.753528 | 5.819939 |
| skatebll | 18 | 5.753868 | 5.819955 |
| skatebll | 19 | 5.753878 | 5.819965 |
| skatebll | 20 | 5.753884 | 5.819974 |
| skatebla | 17 | 5.763071 | 5.829483 |
| skatebla | 18 | 5.763413 | 5.829498 |
| skatebla | 19 | 5.763423 | 5.829508 |
| skatebla | 20 | 5.763429 | 5.829517 |
| skateblb | 17 | 5.748698 | 5.814993 |
| skateblb | 18 | 5.749022 | 5.815008 |
| skateblb | 19 | 5.749035 | 5.815013 |
| skateblb | 20 | 5.749041 | 5.815019 |

Raw trace pins:
- `skatebll-coil-run.json`: SHA-256 `9a516f328d79f22b8b3ef20e0bfc8b416386faad9bf9e13f6e7095f7b89bb3c3`.
- `skatebla-coil-run.json`: SHA-256 `fd305baaab277a8abf906234554266bd9af703599e8c9e7f09b7b737e28332d5`.
- `skateblb-coil-run.json`: SHA-256 `1ad53e61bfbcb0968996bd31643ef54c619a0f41107cbd31baa93e4148fbb34b`.

These are all events for outputs 17–20 in the first eight seconds of each retained run. The startup burst is visible on all four continuous outputs; the later service-test pairings separately identify fitted coin-lockout 18 and flipper-enable relay 19. The game's own A3 wiring marks the loads behind 17 and 20 N/U.

The underlying PIA write sequence or ROM initialization causing this burst has not been pinned. `by35.c`'s inverted continuous-bit transport and the temporal proximity of the events do not prove a reset or self-test cause. Physical non-fitment is documented, but the published state remains unexplained, so 17/20 availability stays unknown. A lack of later activity is not proof of unused address space.
