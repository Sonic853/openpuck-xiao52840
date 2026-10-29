#pragma once

#if defined(ARDUINO_Seeed_XIAO_nRF52840)
#define OPK_BOARD_XIAO_NRF52840 1
#endif

#if defined(OPK_BOARD_XIAO_NRF52840)
#include <nrf_sdm.h>
#if SD_VERSION != 7003000
#error "The Xiao target requires S140 7.3.0 headers and linker layout"
#endif

// The factory S140 7.3.0 occupies one more page than S140 6.1.1.
#define OPK_APP_BASE 0x27000UL
#else
#define OPK_APP_BASE 0x26000UL
#endif

#if defined(OPK_BOARD_MDBT50Q_CX_40)
// The staged updater rewrites an Adafruit-format bootloader settings page.
#define OPK_HAS_ADAFRUIT_DFU 0
#else
#define OPK_HAS_ADAFRUIT_DFU 1
#endif

// The panel's v1 transfer does not carry the image's linked base address.
#if defined(OPK_BOARD_XIAO_NRF52840)
#define OPK_HAS_STAGED_UPDATE 0
#else
#define OPK_HAS_STAGED_UPDATE OPK_HAS_ADAFRUIT_DFU
#endif
