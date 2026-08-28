# Transcription: Capcom Big Bang Bar operators manual, printed page 42 (PDF page 46)

Source: `manual.capcom.big-bang-bar.1996` (SHA-256 `5fc11391e3092298e31775fdff5944554fc78db2bdb9240aa39fa9eab5dabca5`),
Game Diagnostics section, C2-02: ALIEN MOTOR failure messages. Transcribed from
the rendered page (this file's companion image is a native-resolution crop of
the same bullet).

> - **Can't Find Home Position**: The encoder wheel has two notches very close
>   together. This is the motor's "home" position. This error message indicates
>   that the motor driver couldn't find the double notch because **the opto
>   (which reads the encoder wheel)** is dirty, inoperative, or that the encoder
>   wheel is misaligned.
>
> - **Speed Won't Stabilize**: The motor must run at a fairly constant speed,
>   for a number of revolutions, during this test. This message indicates that
>   the motors' gears may be binding or that the mechanism's rotation is
>   impaired by an obstruction.
>
> - **Calibration Cancelled**: The test was interrupted by the operator pressing
>   both flipper buttons.
>
> - **Calibration Error**: An unknown software error occurred during
>   calibration. Contact your local distributor or report the failure to Capcom
>   Field Service at the number indicated at the front of this manual.

Printed footer: "Page 42".

Note: "the opto (which reads the encoder wheel)" is the diagnostics section's
own construction statement for switch 57 (Alien Motor), matching the Alien Mech
Assembly parts list's encoder disc (MT00501) and A0020000 opto PCB assembly.
