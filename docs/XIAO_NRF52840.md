# DX Xiao nRF52840 / S140 7.3.0

The DX Xiao SuperMini uses the Xiao pinout and factory S140 7.3.0
(`INFO_UF2.TXT`: `Model: DX XIAO nRF52840`). It is not the Pro Micro
SuperMini targeted by the standard release UF2.

The application must be linked at **0x27000**, rather than 0x26000.
Copying a standard UF2 can overwrite the last SoftDevice page. Changing
UF2 block addresses alone cannot relocate an already linked application.

## Build

Install Arduino CLI and the pinned dependencies:

```sh
python -m pip install adafruit-nrfutil
python tools/build-xiao.py --install-deps
# Subsequent builds:
python tools/build-xiao.py
```

Use `--cli PATH` if Arduino CLI is not on PATH, or `--tinyusb PATH` for a
non-default TinyUSB library location. The script uses the Seeed Xiao
variant, S140 7.3.0 API and v7 linker script, and TinyUSB 3.6.0 (the version
used by Adafruit nRF52 core 1.7.0) instead of Seeed's bundled 1.7.0.
It supplies OpenPuck's USB flags
and linker wrappers, temporarily generates the ignored version header, and checks
the output's block addresses and vector table.

The Xiao sketchbook and TinyUSB library live under `build/xiao-arduino`,
so they do not override the USB library used by standard or Raytac builds.
The existing version header is restored even if compilation fails.
`OPK_BUILD_VERSION` is honored for CI/release builds; otherwise an exact
version tag is used when present. The installed Seeed core is shared through
Arduino's normal package directory.

Output: `build/xiao/OpenPuck-xiao-s140-7.3.0.uf2`.
Double-tap reset and copy this file onto the board's UF2 drive.
The build command does not flash the board.

The blue LED is active-low at P0.06 (Xiao D12); it retains OpenPuck's
wake-pulse behavior. The external QSPI flash is not used for persistence;
the core's internal LittleFS remains at 0xED000..0xF3FFF.

## Updates and recovery

Use the UF2 drive for application updates. Staged WebUSB updates are
disabled on this target: the existing v1 protocol does not transmit the
image's linked base address and cannot reliably reject a standard image.
WebUSB configuration and the UF2 reboot command remain available.
Full-board wipe starts at 0x27000, preserving S140 7.3.0.

If a standard image has overwritten SoftDevice, restore the **DX Xiao**
manufacturer's combined bootloader/SoftDevice ZIP via USB serial DFU:

```sh
python -m pip install adafruit-nrfutil
python -m nordicsemi --verbose dfu serial --package "dxXiao_nrf52840_bootloader_s140_7.3.0.zip" --port COM3 --baudrate 115200 --singlebank
```

Select the board's actual bootloader COM port and full package path.
The ZIP is a serial DFU package, not a file to copy to the UF2 drive.
The manufacturer's nice!nano package has different board pin assignments.

Compilation and UF2 layout checks do not establish USB/RF hardware operation.
After flashing, verify enumeration in Steam mode, WebUSB configuration,
controller pairing, and wireless input on the physical board.
