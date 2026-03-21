"""Makalu 67 device panel for BaseCamp Linux hub."""
import subprocess
import threading
import tkinter as tk
import customtkinter as ctk

from shared.ui_helpers import (
    BG, BG2, BG3, FG, FG2, BLUE, YLW, GRN, RED, BORDER,
    AccordionSection, pick_color, _rgb_hex,
)

# (name, code, has_speed, has_color1, has_color2, has_direction)
_RGB_EFFECTS = [
    ("Static",       1, False, True,  False, False),
    ("Breathing",    5, True,  True,  True,  False),
    ("RGB Breathing",6, True,  False, False, False),
    ("Rainbow",      2, True,  False, False, True),
    ("Responsive",   7, False, True,  False, False),
    ("Yeti",         8, True,  True,  True,  False),
    ("Off",          0, False, False, False, False),
]
_EFFECT_MAP = {name: (code, hs, hc1, hc2, hd) for name, code, hs, hc1, hc2, hd in _RGB_EFFECTS}
_EFFECT_NAMES = [e[0] for e in _RGB_EFFECTS]


class Makalu67Panel(ctk.CTkFrame):
    """Panel for Makalu 67 mouse."""

    VID = 0x3282
    PID = 0x0003

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self._app       = app
        self._connected = False
        self._sections  = []

        self._build_ui()

    # ── Translation delegation ────────────────────────────────────────────────

    def T(self, key, **kwargs):
        return self._app.T(key, **kwargs)

    def _reg(self, widget, key, attr="text"):
        return self._app._reg(widget, key, attr)

    # ── Subprocess helper ──────────────────────────────────────────────────────

    def _cmd(self, *args):
        """Return command list for Makalu controller subprocess."""
        return self._app._cmd_for_device("makalu67", *args)

    def _run_async(self, cmd, on_done=None):
        """Run command in background thread, call on_done(ok, stdout) on main thread."""
        def _worker():
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                ok = r.returncode == 0 and r.stdout.strip() == "ok"
                if on_done:
                    self.after(0, lambda: on_done(ok, r.stdout.strip()))
            except Exception as e:
                if on_done:
                    self.after(0, lambda: on_done(False, str(e)))
        threading.Thread(target=_worker, daemon=True).start()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Not-connected banner
        self._banner = ctk.CTkFrame(self, fg_color="#3b1515", corner_radius=6)
        self._banner_lbl = ctk.CTkLabel(
            self._banner,
            text="Makalu 67 not connected",
            font=("Helvetica", 11), text_color=RED,
        )
        self._banner_lbl.pack(pady=8, padx=16)
        if not self._connected:
            self._banner.pack(fill="x", padx=12, pady=(8, 4))

        scroll = ctk.CTkScrollableFrame(self, fg_color=BG, corner_radius=0)
        scroll.pack(fill="both", expand=True, pady=(4, 0))

        self._build_rgb_section(scroll)

        self._app.update_idletasks()
        for s in self._sections:
            s.measure()

    def _build_rgb_section(self, scroll):
        s = _PlaceholderSection(scroll, self._app, "💡", "RGB Lighting")
        self._sections.append(s)
        self._rgb_section = s
        self._build_rgb_content(s.content)

    def _build_rgb_content(self, parent):
        # ── Effect dropdown ──────────────────────────────────────────────────
        mode_row = ctk.CTkFrame(parent, fg_color="transparent")
        mode_row.pack(fill="x", padx=10, pady=(10, 2))
        ctk.CTkLabel(mode_row, text="Effect", font=("Helvetica", 11),
                     text_color=FG2).pack(side="left", padx=(0, 6))
        self._rgb_mode_var = tk.StringVar(value=_EFFECT_NAMES[0])
        ctk.CTkOptionMenu(
            mode_row, variable=self._rgb_mode_var, values=_EFFECT_NAMES,
            command=lambda _: self._rgb_update_controls(),
            fg_color=BG3, button_color=BG3, button_hover_color=BG2,
            text_color=FG, font=("Helvetica", 11), width=180, height=32,
        ).pack(side="left")

        # ── Speed buttons ─────────────────────────────────────────────────────
        self._rgb_speed_row = ctk.CTkFrame(parent, fg_color="transparent")
        self._rgb_speed_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(self._rgb_speed_row, text="Speed", font=("Helvetica", 11),
                     text_color=FG2, width=120, anchor="w").pack(side="left")
        self._rgb_speed_var = tk.StringVar(value="Medium")
        self._rgb_speed_seg = ctk.CTkSegmentedButton(
            self._rgb_speed_row, values=["Slow", "Medium", "Fast"],
            variable=self._rgb_speed_var,
            command=lambda _: self._apply_rgb(),
            fg_color=BG3, selected_color=BLUE, selected_hover_color="#0284c7",
            unselected_color=BG3, unselected_hover_color=BG2,
            text_color=FG, font=("Helvetica", 11), height=28)
        self._rgb_speed_seg.pack(side="left")

        # ── Direction buttons ─────────────────────────────────────────────────
        self._rgb_dir_row = ctk.CTkFrame(parent, fg_color="transparent")
        self._rgb_dir_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(self._rgb_dir_row, text="Direction", font=("Helvetica", 11),
                     text_color=FG2, width=120, anchor="w").pack(side="left")
        self._rgb_dir_var = tk.StringVar(value="→")
        self._rgb_dir_seg = ctk.CTkSegmentedButton(
            self._rgb_dir_row, values=["←", "→"],
            variable=self._rgb_dir_var,
            command=lambda _: self._apply_rgb(),
            fg_color=BG3, selected_color=BLUE, selected_hover_color="#0284c7",
            unselected_color=BG3, unselected_hover_color=BG2,
            text_color=FG, font=("Helvetica", 11), height=28)
        self._rgb_dir_seg.pack(side="left")

        # ── Brightness dropdown ──────────────────────────────────────────────
        self._rgb_bri_row = ctk.CTkFrame(parent, fg_color="transparent")
        self._rgb_bri_row.pack(fill="x", padx=10, pady=2)
        ctk.CTkLabel(self._rgb_bri_row, text="Brightness", font=("Helvetica", 11),
                     text_color=FG2, width=120, anchor="w").pack(side="left")
        self._rgb_bri_var = tk.StringVar(value="100%")
        ctk.CTkOptionMenu(
            self._rgb_bri_row, variable=self._rgb_bri_var,
            values=["0%", "25%", "50%", "75%", "100%"],
            command=lambda _: self._apply_rgb(),
            fg_color=BG3, button_color=BG3, button_hover_color=BG2,
            text_color=FG, font=("Helvetica", 11), width=120, height=28,
        ).pack(side="left")

        # ── Color buttons ────────────────────────────────────────────────────
        color_row = ctk.CTkFrame(parent, fg_color="transparent")
        color_row.pack(fill="x", padx=10, pady=2)
        self._rgb_color1 = (0, 118, 204)
        self._rgb_color2 = (255, 0, 0)

        ctk.CTkLabel(color_row, text="Color 1", font=("Helvetica", 11),
                     text_color=FG2).pack(side="left", padx=(0, 4))
        self._rgb_c1_btn = ctk.CTkButton(
            color_row, text="", width=40, height=28, corner_radius=4,
            fg_color=_rgb_hex(self._rgb_color1),
            hover_color=_rgb_hex(self._rgb_color1),
            command=lambda: self._pick_rgb_color(1))
        self._rgb_c1_btn.pack(side="left", padx=(0, 12))

        self._rgb_c2_lbl = ctk.CTkLabel(color_row, text="Color 2",
                                         font=("Helvetica", 11), text_color=FG2)
        self._rgb_c2_btn = ctk.CTkButton(
            color_row, text="", width=40, height=28, corner_radius=4,
            fg_color=_rgb_hex(self._rgb_color2),
            hover_color=_rgb_hex(self._rgb_color2),
            command=lambda: self._pick_rgb_color(2))

        # ── Color presets ────────────────────────────────────────────────────
        _PRESETS = [
            (255,   0,   0), (204,   0,  67), (235,  64,  52), (220,  41, 188),
            (179,  53, 127), ( 71,   0, 204), (  0,  60, 204), (  0, 118, 204),
            (  0, 204, 181), ( 41, 255, 204), ( 91, 222,  98), (152, 235,  53),
        ]
        self._rgb_preset_row = ctk.CTkFrame(parent, fg_color="transparent")
        preset_row = self._rgb_preset_row
        preset_row.pack(fill="x", padx=10, pady=(2, 4))
        ctk.CTkLabel(preset_row, text="Presets", font=("Helvetica", 11),
                     text_color=FG2, width=120, anchor="w").pack(side="left")
        swatch_frame = ctk.CTkFrame(preset_row, fg_color="transparent")
        swatch_frame.pack(side="left")
        for rgb in _PRESETS:
            hex_col = _rgb_hex(rgb)
            btn = ctk.CTkButton(
                swatch_frame, text="", width=22, height=22, corner_radius=3,
                fg_color=hex_col, hover_color=hex_col,
                command=lambda c=rgb: self._apply_preset(c))
            btn.pack(side="left", padx=1)

        # ── Apply row ────────────────────────────────────────────────────────
        self._rgb_apply_row = ctk.CTkFrame(parent, fg_color="transparent")
        self._rgb_apply_row.pack(fill="x", padx=10, pady=(6, 10))
        ctk.CTkButton(
            self._rgb_apply_row, text="Apply",
            font=("Helvetica", 11), fg_color=BLUE, hover_color="#0284c7",
            text_color=FG, width=120, height=32, command=self._apply_rgb,
        ).pack(side="left")
        self._rgb_status = ctk.CTkLabel(self._rgb_apply_row, text="",
                                         text_color=FG2, font=("Helvetica", 11))
        self._rgb_status.pack(side="left", padx=(10, 0))

        self._rgb_update_controls()

    def _rgb_update_controls(self):
        name = self._rgb_mode_var.get()
        _, hs, hc1, hc2, hd = _EFFECT_MAP.get(name, (0, False, False, False, False))
        self._rgb_speed_seg.configure(state="normal" if hs else "disabled")
        self._rgb_c1_btn.configure(state="normal" if hc1 else "disabled")
        if hd:
            self._rgb_dir_row.pack(fill="x", padx=10, pady=2,
                                   after=self._rgb_speed_row)
        else:
            self._rgb_dir_row.pack_forget()
        if hc1:
            self._rgb_preset_row.pack(fill="x", padx=10, pady=(2, 4))
        else:
            self._rgb_preset_row.pack_forget()
        if hc2:
            self._rgb_c2_lbl.pack(side="left", padx=(0, 4))
            self._rgb_c2_btn.pack(side="left")
        else:
            self._rgb_c2_lbl.pack_forget()
            self._rgb_c2_btn.pack_forget()
        if hasattr(self, "_rgb_section"):
            self._app.update_idletasks()
            s = self._rgb_section
            was_open = s._open
            s.measure()
            if was_open:
                s._content.configure(height=s._natural_h)

    def _pick_rgb_color(self, which):
        initial = self._rgb_color1 if which == 1 else self._rgb_color2
        rgb = pick_color(self._app, initial_rgb=initial, title="Farbe wählen",
                         show_brightness=False)
        if rgb is None:
            return
        h = _rgb_hex(rgb)
        if which == 1:
            self._rgb_color1 = rgb
            self._rgb_c1_btn.configure(fg_color=h, hover_color=h)
        else:
            self._rgb_color2 = rgb
            self._rgb_c2_btn.configure(fg_color=h, hover_color=h)
        self._apply_rgb()

    def _apply_preset(self, rgb):
        h = _rgb_hex(rgb)
        self._rgb_color1 = rgb
        self._rgb_c1_btn.configure(fg_color=h, hover_color=h)
        self._apply_rgb()

    def _apply_rgb(self):
        if getattr(self, "_applying", False):
            return
        self._applying = True

        name = self._rgb_mode_var.get()
        code, hs, hc1, hc2, hd = _EFFECT_MAP.get(name, (0, False, False, False, False))
        self._rgb_status.configure(text="Applying…", text_color=YLW)

        r1, g1, b1 = self._rgb_color1
        r2, g2, b2 = self._rgb_color2
        bri = {"0%": 0, "25%": 25, "50%": 50, "75%": 75, "100%": 100}.get(self._rgb_bri_var.get(), 100)
        spd = {"Slow": 0, "Medium": 1, "Fast": 2}.get(self._rgb_speed_var.get(), 1) if hs else 0
        dir_ = 1 if self._rgb_dir_var.get() == "→" else 0

        if hc2:
            cmd = self._cmd("rgb", "code2", str(code),
                            str(r1), str(g1), str(b1),
                            str(r2), str(g2), str(b2), str(bri), str(spd), str(dir_))
        else:
            cmd = self._cmd("rgb", "code", str(code),
                            str(r1), str(g1), str(b1), str(bri), str(spd), str(dir_))

        def _done(ok, msg):
            self._applying = False
            if ok:
                self._rgb_status.configure(text="Applied ✓", text_color=GRN)
                self.after(3000, lambda: self._rgb_status.configure(text=""))
            else:
                self._rgb_status.configure(
                    text=f"Failed: {msg[:50]}" if msg else "Failed", text_color=RED)

        self._run_async(cmd, _done)

    # ── Public interface ──────────────────────────────────────────────────────

    def set_connected(self, connected: bool):
        """Show or hide the 'not connected' banner."""
        self._connected = connected
        if connected:
            self._banner.pack_forget()
        else:
            self._banner.pack(fill="x", padx=12, pady=(8, 4),
                              before=self.winfo_children()[1])

    def apply_lang(self):
        """Called by App when language changes."""
        pass

    def _stop_cpu_proc(self):
        """No-op stub — Makalu panel has no background process."""
        return False

    def _start_cpu_auto(self):
        """No-op stub."""
        pass


# ── Helper: accordion section with plain string title ─────────────────────────

class _PlaceholderSection:
    """Accordion section with a plain string title (not a lang key)."""

    def __init__(self, parent, app, icon, title):
        self._app       = app
        self._open      = False
        self._natural_h = 0

        self._outer = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
        self._outer.pack(fill="x", pady=2)

        self._header = ctk.CTkFrame(self._outer, fg_color=BG2, corner_radius=6,
                                    cursor="hand2")
        self._header.pack(fill="x")

        accent = tk.Frame(self._header, bg=YLW, width=4)
        accent.pack(side="left", fill="y")

        ctk.CTkLabel(self._header, text=icon, font=("Helvetica", 14),
                     text_color=YLW, width=30).pack(side="left", padx=(8, 4))

        ctk.CTkLabel(self._header, text=title,
                     font=("Helvetica", 11, "bold"),
                     text_color=FG, anchor="w").pack(
                         side="left", fill="x", expand=True, padx=4, pady=12)

        self._chevron = ctk.CTkLabel(self._header, text="▶",
                                      font=("Helvetica", 10), text_color=FG2, width=24)
        self._chevron.pack(side="right", padx=(0, 12))

        self._content = ctk.CTkFrame(self._outer, fg_color=BG2, corner_radius=0, height=0)
        self._content.pack(fill="x", pady=(1, 0))
        self._content.pack_propagate(False)

        def _bind_all(w):
            w.bind("<Button-1>", self._toggle)
            for child in w.winfo_children():
                _bind_all(child)
        _bind_all(self._header)

    @property
    def content(self):
        return self._content

    def measure(self):
        self._content.pack_propagate(True)
        self._app.update_idletasks()
        self._natural_h = self._content.winfo_reqheight()
        self._content.pack_propagate(False)
        if not self._open:
            self._content.configure(height=0)
        else:
            self._content.configure(height=self._natural_h)

    def open(self):
        if self._open:
            return
        self._open = True
        self._chevron.configure(text="▼")
        if self._natural_h > 0:
            self._content.configure(height=self._natural_h)

    def close(self):
        if not self._open:
            return
        self._open = False
        self._chevron.configure(text="▶")
        self._content.configure(height=0)

    def _toggle(self, event=None):
        self.close() if self._open else self.open()
