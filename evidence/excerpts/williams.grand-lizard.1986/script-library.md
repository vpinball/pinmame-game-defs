# Retained S11.VBS flipper input constants

Source: machine-neutral retained `review-artifacts/vpm-script-libs/s11.vbs`,
SHA256 5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91,
and core.vbs SHA256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69.
Curator checked the constants and key-handler code, not a physical schematic.

S11.VBS defines swLRFlip = 82, swLLFlip = 84, swURFlip = 81, swULFlip = 83.
Its vpmKeyDown/vpmKeyUp pass lower flipper keys to Controller.Switch(swLRFlip)
and Controller.Switch(swLLFlip), while upper key writes depend on the
cvpmFlips2 upper solenoid-number settings. The misleading upper 81/83 constants
do not make the System 11 ROM read the core's EOS-column bits.
Synthetic solenoid constants are sLRFlipper = 46 and sLLFlipper = 48; their power
partners 45/47 are also set by PinMAME core when the button is held enabled.
