# Fresh-state ROM audit: startup blocked

Retained external artifact:
`review-artifacts/gottlieb.joker-poker.1978/runtime/log-diagnostic-arguments.json`,
SHA-256 `eb85ad85fe8bf58f3f91c729bf893305805aff6b67d6aedc67a74b1cb373f1ef`.
The diagnostic ran against the pinned System 1 build and the legal local game ROM
archive. Its callbacks record both inherited common-program files
`A1752CF.bin` and `A1753CE.bin` as **NOT FOUND**, followed by the missing-required-ROM
error. The machine state goes from starting (2) to stopped (0), without ready.

The two earlier fresh-state scenario attempts also stopped before ready; their
service/gameplay injections did not run. No output transition, self-test sequence,
successful switch response, or physical fitment is inferred from these failures.
This is a tooling/input limitation, not evidence that a controller route is unused.
An authorized copy of the inherited System 1 ROM pair is needed before retrying
the same bounded gameplay/service work.

Method: manual inspection of retained diagnostic JSON, GPT Sol, 2026-10-21.
