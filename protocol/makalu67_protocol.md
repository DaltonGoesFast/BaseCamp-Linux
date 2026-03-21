# Makalu 67 Protocol Documentation
VID: 0x3282 | PID: 0x0003 (Linux) / 0x0002 (older revision, Makalu.dll)

Reverse-engineered from USB capture (Windows VirtualBox session + Linux physical testing).

---

## Device Access

- Interface 0: Boot mouse (movement, buttons), EP 0x81 IN Interrupt 8B
- Interface 1: Feature reports (RGB, DPI, config), EP 0x82 IN Interrupt 64B
- hidraw node is dynamic — always use `hid.enumerate(0x3282, 0x0003)` with `interface_number == 1`

udev rule (Fedora/Nobara — no plugdev group):
```
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="3282", ATTRS{idProduct}=="0003", MODE="0666", TAG+="uaccess"
```

---

## Command Protocol

All communication: **HID Feature Reports** via `send_feature_report` / `get_feature_report`.
- Report ID: `0xA1` (64 bytes sent)
- Response ID: `0xA0` (64 bytes received, byte[1] = 0x01 or 0x03 = success)

The payload maps to the device's internal FullData profile buffer:
`buf[N]` = `FullData[N-1]` (offset by 1 for the Report ID byte).

---

### Command 0x0C — Update Lighting Settings

```
Byte  Value   Description
----  ------  -----------
[0]   0xA1    Report ID
[1]   0x0C    Command = Update_lighting_settings
[5]   0x01    Always 1

Zone 1  (RGB byte order):
[16]  effect  Effect code (see table below)
[17]  R       Red   (0–255)
[18]  G       Green (0–255)
[19]  B       Blue  (0–255)

Zone 2 — dual-color effects only (byte order differs per effect, confirmed by USB capture):

Breathing (effect 5):
[20]  R2      Red   channel of color 2  ✅ standard RGB — same order as Zone 1
[21]  G2      Green channel of color 2
[22]  B2      Blue  channel of color 2
[23]  0x00    Always zero

Yeti (effect 8):
[20]  R2      Red   channel of color 2  ✅ standard RGB — same order as Zone 1
[21]  G2      Green channel of color 2
[22]  B2      Blue  channel of color 2
[23]  0x00    Always zero

[41]  brightness  LED brightness 0–100 (confirmed by physical testing)
                  Device always saves to flash regardless of value (resp[1]=0x03 for all values).
                  Note: DLL suggested 0x64=save/0x00=live, but this was wrong.
[42]  param1      Always 0
[43]  param2      Animation speed: 0=slow, 1=medium, 2=fast (confirmed by Breathing capture)
all others = 0x00
```

### Response
```
[0]   0xA0    Response report ID
[1]   0x01    Acknowledged (live preview)
      0x03    Acknowledged (flash save)
```

---

### Effect Codes (confirmed PID 0x0003, physical testing)

| Code | Name          | Colors  | Notes                        |
|------|---------------|---------|------------------------------|
| 0    | Off           | —       | All LEDs off                 |
| 1    | Static        | 1       | Solid color                  |
| 2    | Rainbow       | —       | Color cycling, no color input|
| 5    | Breathing     | 1 or 2  | Fade in/out — Zone 2 uses standard RGB (buf[20]=R2, buf[21]=G2, buf[22]=B2, buf[23]=0x00) |
| 6    | RGB Breathing | —       | Breathing with rainbow colors|
| 7    | Responsive    | —       | Reacts to mouse clicks       |
| 8    | Yeti          | 1 or 2  | Wave/ripple effect — Zone 2 uses standard RGB (same as Breathing) |

Codes 3, 4 are duplicates of 2 and 1 respectively (skipped in UI).

---

## Not Yet Reverse-Engineered
- DPI levels (5 slots, 200–26000 DPI per Makalu.dll)
- Polling rate (125 / 250 / 500 / 1000 Hz)
- Button remapping (6 buttons)
- Profile selection (3 profiles)
- Read current settings back from device
