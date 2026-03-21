#!/usr/bin/env python3
"""
Makalu 67 Controller
VID: 0x3282, PID: 0x0003
Protocol: HID Feature Reports on Interface 1

Protocol reverse-engineered from USB capture (Windows VirtualBox session).
Report ID 0xA1, 64 bytes, SET_REPORT to Interface 1.
Response: Report ID 0xA0, byte[1]=0x01 = OK.

Command 0x0C layout (64 bytes):
  [0]      = 0xA1  (Report ID)
  [1]      = 0x0C  (command = Update_lighting_settings)
  [5]      = 0x01  (always 1)
  [16]     = effect (0=Off, 1=Static, 2=Rainbow, 5=Breathing, 6=RGB Breathing, 7=Responsive, 8=Yeti)
  [17]     = R
  [18]     = G
  [19]     = B
  [41]     = brightness (0–100); device always saves to flash (resp[1]=0x03 for all values)
  [42]     = param1 (always 0)
  [43]     = param2 (animation speed: 0=slow, 1=medium, 2=fast)
"""
import sys
import time

try:
    import hid
    HID_AVAILABLE = True
except ImportError:
    HID_AVAILABLE = False

VID = 0x3282
PID = 0x0003

REPORT_ID    = 0xA1
RESP_ID      = 0xA0
CMD_LIGHTING = 0x0C

# Confirmed effect codes (physical testing, PID 0x0003)
EFFECT_OFF          = 0
EFFECT_STATIC       = 1
EFFECT_RAINBOW      = 2
EFFECT_BREATHING    = 5
EFFECT_RGB_BREATHING= 6
EFFECT_RESPONSIVE   = 7
EFFECT_YETI         = 8


# ── Device access ─────────────────────────────────────────────────────────────

def find_path():
    """Return path of Interface 1 hidraw node, or None."""
    if not HID_AVAILABLE:
        return None
    seen = set()
    for d in hid.enumerate(VID, PID):
        if d.get('interface_number') == 1:
            p = d['path']
            if p not in seen:
                seen.add(p)
                return p
    return None


def open_device():
    path = find_path()
    if path is None:
        raise RuntimeError("Makalu 67 not found (VID=0x3282 PID=0x0003 IF1)")
    dev = hid.Device(path=path)
    return dev


# ── Lighting ──────────────────────────────────────────────────────────────────

def _lighting_report(effect, r=0, g=0, b=0, brightness=100, param1=0, param2=0):
    buf = [0] * 64
    buf[0]  = REPORT_ID
    buf[1]  = CMD_LIGHTING
    buf[5]  = 0x01
    buf[16] = effect
    buf[17] = r & 0xFF
    buf[18] = g & 0xFF
    buf[19] = b & 0xFF
    buf[41] = max(0, min(100, brightness))  # brightness 0-100 (also acts as save flag)
    buf[42] = param1
    buf[43] = param2
    return buf


def _send_lighting(dev, buf):
    dev.send_feature_report(bytes(buf))
    time.sleep(0.05)
    resp = dev.get_feature_report(REPORT_ID, 64)
    ok = len(resp) >= 1 and resp[0] == RESP_ID
    return ok, resp


def set_lighting_off(brightness=100):
    dev = open_device()
    try:
        buf = _lighting_report(EFFECT_OFF, brightness=brightness)
        ok, _ = _send_lighting(dev, buf)
        return ok
    finally:
        dev.close()


def set_lighting_static(r, g, b, brightness=100):
    dev = open_device()
    try:
        buf = _lighting_report(EFFECT_STATIC, r, g, b, brightness=brightness)
        ok, _ = _send_lighting(dev, buf)
        return ok
    finally:
        dev.close()


def set_lighting_breathing(r=0, g=0, b=0, brightness=100, speed=1):
    dev = open_device()
    try:
        buf = _lighting_report(EFFECT_BREATHING, r, g, b, brightness=brightness,
                               param1=speed, param2=speed)  # both params control speed
        ok, _ = _send_lighting(dev, buf)
        return ok
    finally:
        dev.close()


def set_lighting_rainbow(brightness=100):
    dev = open_device()
    try:
        buf = _lighting_report(EFFECT_RAINBOW, brightness=brightness, param1=1, param2=1)
        ok, _ = _send_lighting(dev, buf)
        return ok
    finally:
        dev.close()


def set_lighting_rgb_breathing(brightness=100):
    dev = open_device()
    try:
        buf = _lighting_report(EFFECT_RGB_BREATHING, brightness=brightness, param1=1, param2=1)
        ok, _ = _send_lighting(dev, buf)
        return ok
    finally:
        dev.close()


def set_lighting_responsive(brightness=100):
    dev = open_device()
    try:
        buf = _lighting_report(EFFECT_RESPONSIVE, brightness=brightness, param1=1, param2=1)
        ok, _ = _send_lighting(dev, buf)
        return ok
    finally:
        dev.close()


def set_lighting_yeti(brightness=100):
    dev = open_device()
    try:
        buf = _lighting_report(EFFECT_YETI, brightness=brightness, param1=1, param2=1)
        ok, _ = _send_lighting(dev, buf)
        return ok
    finally:
        dev.close()


# ── CLI ───────────────────────────────────────────────────────────────────────

def _die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def _usage():
    print("""Usage: makalu-controller <command> [args]

Commands:
  rgb off                     Turn LEDs off
  rgb static <R> <G> <B>      Static color  (0-255 each)
  rgb breathing [R G B]       Breathing effect (optional color)
  rgb rainbow                 Rainbow cycling effect
  rgb live static <R> <G> <B> Live preview (no flash write)
  status                      Check device presence
""")


def main():
    args = sys.argv[1:]
    if not args:
        _usage()
        sys.exit(1)

    cmd = args[0]

    if cmd == "status":
        path = find_path()
        if path:
            print(f"connected: {path.decode() if isinstance(path, bytes) else path}")
        else:
            print("not connected")
            sys.exit(1)

    elif cmd == "rgb":
        if len(args) < 2:
            _die("rgb: subcommand required (off/static/breathing/rainbow/live)")

        live = args[1] == "live"
        sub_args = args[2:] if live else args[1:]
        sub = sub_args[0] if sub_args else ""
        save = not live

        try:
            if sub == "off":
                ok = set_lighting_off(brightness=100)
            elif sub == "static":
                if len(sub_args) < 4:
                    _die("rgb static requires R G B")
                r, g, b = int(sub_args[1]), int(sub_args[2]), int(sub_args[3])
                ok = set_lighting_static(r, g, b)
            elif sub == "breathing":
                r = int(sub_args[1]) if len(sub_args) > 1 else 0
                g = int(sub_args[2]) if len(sub_args) > 2 else 0
                b = int(sub_args[3]) if len(sub_args) > 3 else 0
                ok = set_lighting_breathing(r, g, b)
            elif sub == "rainbow":
                ok = set_lighting_rainbow()
            elif sub == "code":
                if len(sub_args) < 2:
                    _die("rgb code requires effect code")
                code = int(sub_args[1])
                r   = int(sub_args[2]) if len(sub_args) > 2 else 0
                g   = int(sub_args[3]) if len(sub_args) > 3 else 0
                b   = int(sub_args[4]) if len(sub_args) > 4 else 0
                bri = int(sub_args[5]) if len(sub_args) > 5 else 100
                spd = int(sub_args[6]) if len(sub_args) > 6 else 0
                dir_ = int(sub_args[7]) if len(sub_args) > 7 else 0
                dev = open_device()
                try:
                    buf = _lighting_report(code, r, g, b, brightness=bri, param1=dir_, param2=spd)
                    ok, _ = _send_lighting(dev, buf)
                finally:
                    dev.close()
            elif sub == "code2":
                # rgb code2 <effect> <R> <G> <B> <R2> <G2> <B2> <brightness> [speed]
                if len(sub_args) < 8:
                    _die("rgb code2 requires effect R G B R2 G2 B2")
                code = int(sub_args[1])
                r,  g,  b  = int(sub_args[2]), int(sub_args[3]), int(sub_args[4])
                r2, g2, b2 = int(sub_args[5]), int(sub_args[6]), int(sub_args[7])
                bri = int(sub_args[8]) if len(sub_args) > 8 else 100
                spd  = int(sub_args[9])  if len(sub_args) > 9  else 0
                dir_ = int(sub_args[10]) if len(sub_args) > 10 else 0
                dev = open_device()
                try:
                    buf = _lighting_report(code, r, g, b, brightness=bri, param1=dir_, param2=spd)
                    # Zone 2 layout — both Breathing and Yeti confirmed by USB capture:
                    # standard RGB order, same as Zone 1, buf[23]=0x00 always
                    buf[20] = r2 & 0xFF
                    buf[21] = g2 & 0xFF
                    buf[22] = b2 & 0xFF
                    buf[23] = 0x00
                    ok, _ = _send_lighting(dev, buf)
                finally:
                    dev.close()
            else:
                _die(f"rgb: unknown subcommand '{sub}'")
            print("ok" if ok else "failed")
        except RuntimeError as e:
            _die(str(e))

    else:
        _die(f"unknown command '{cmd}'")


if __name__ == "__main__":
    main()
