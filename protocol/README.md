# Sherpa  

<span style="color:red">⚠️ **WARNING: This project is discontinued!**

Unfortunately my Everest Max broke down while under warranty and Mountain was apparently not willing or interested to repair or replace my broken unit.
I also ordered a new one but that one was returned by DHL before even reaching me as apparently it was damaged.
So this marks the end of this project. :-(
It was fun while it lasted :-)

As it seems Mountain and be quiet! (the parent company of Mountain) are not interested in Linux or Mac support better avoid those brands if you are using those OS-es.
</span>  

---
This is an unofficial support page for the **Mountain Everest Max** keyboard, including its Media Pad and Numpad.  
Please note that this page is **not endorsed by Mountain**, and the author is not affiliated with the company.  

<span style="color:red">**⚠️ WARNING: This project is a work in progress and still in its early stages.  
**Use at your own risk.**  
Please report any problems or suggestions via the issue tracker.**</span>  

---

## Purpose  

The Sherpa project provides information and code related to the **Mountain Everest Max** and **Core** keyboards. Some details may also apply to the **Mountain Everest 60** keyboard.  

The primary focus of this project is **Linux support**, as Mountain does not officially support Linux.  

This project is based on reverse engineering (using firmware version 57.24.20).  
Feel free to contribute by submitting merge requests or raising issues regarding the information or code provided here.  

The code is licensed under **GPLv2**.  

### Python GUI Frontend  
A Python-based GUI frontend for this project is also under development. For more details, see [README_python](README_python.md).  

---

## What Works Out of the Box on Linux  

Most basic functionalities work without additional configuration:  
- **Keyboard Functionality**: All regular keys, including those on the Media Pad, function as expected. Local hotkeys also work.  
- **Display Dial Features**:  
  - Volume control (note: display accuracy is limited).  
  - Brightness control.  
  - Timer.  
  - Stopwatch.  
  - Profile switching.  
  - Lighting mode switching.  
- **Numpad**: Fully operational. Some key bindings for LED keys also work (e.g., Hibernate and Calculator).  

---

## What Does Not Work Out of the Box  

Some features are not supported out of the box:  
- Clock display on the Media Pad dial.  
- PC info settings on the dial.  
- APM and custom settings on the dial.  
- Volume display on the dial.  
- Configuring or modifying lighting modes.  
- Downloading new firmware.  
- Defining the functionality of the LCD buttons on the Numpad.  
- Using the LCD buttons on the Numpad.  
- Redefining keys.  
- Creating or modifying profiles.  

Other limitations may exist.  

---

## Additional Software  

### LED Control  
To control the keyboard's LEDs, consider using **OpenRGB**. Visit <https://www.openrgb.org> for more information.  

### Key Remapping  
For remapping keys or assigning commands/macros:  
- **Bash**: Use the `bind` command.  
- **X11**: Use **Input Remapper**. See <https://github.com/sezanzeb/input-remapper>.  

---

## Protocol Description  

For details on the protocol used by the keyboard, refer to the [Protocol Description](protocol.md).  

---

## Software Overview  

The `src` directory contains the following components:  

### `sherpa.cpp`  
A multicall binary providing functionality for:  
- Setting APM, clock, volume, PC info, dial color, dial menu, and more.  
- Switching the dial menu and changing colors/modes.  

Use the `--help` flag to display usage instructions.  

The `examples` directory contains hints on updating features like volume or PC info at regular intervals, depending on your Linux distribution. Sample code for custom color modes is also available.  

### `loadicon.cpp`  
Allows loading images onto the display keys of the Numpad. Images must be in BMP format (RGB565). See the **Tips and Tricks** document for instructions on creating compatible images.  

### `raw.cpp`  
A low-level program for sending arbitrary byte streams.  
⚠️ Use this tool cautiously, as incorrect commands could damage your keyboard. Use at your own risk.

The other files in the src directory are helpers for the above-mentioned programs.

**Note**: The software is tested only on Ubuntu 24.04 with firmware version 57.24.20 on the Everest Max.  

To build the software just run `make`

---

## References and Additional Reading  

### Reviews and Analysis  
- [TechPowerUp Review](https://www.techpowerup.com/review/mountain-everest-max/): A detailed review of the Everest Max, including a disassembly.  
- [Developpez Media Dock Analysis](https://hardware.developpez.com/tests/mountain/everest-max-dock-media-hack/): Explains how to control the volume dial and set the time. The `setclock` and `setvolume` programs are derived from this.  
- [Arch Linux Forum Thread](https://bbs.archlinux.org/viewtopic.php?id=295832): Describes how to map keys on a MacroPad, which may also apply to the Everest Max.  

### OpenRGB Support  
- [OpenRGB Issue #1085](https://gitlab.com/CalcProgrammer1/OpenRGB/-/issues/1085)  
- [OpenRGB Merge Request #1653](https://gitlab.com/CalcProgrammer1/OpenRGB/-/merge_requests/1653)  

### USB Reverse Engineering  
- [USB Reverse Engineering Guide](https://www.devalias.net/devalias/2018/05/13/usb-reverse-engineering-down-the-rabbit-hole/): Insights into USB reverse engineering.  

### Microcontroller Information  
The keyboard uses the **Holtek HT32F52352 Cortex M0+ MCU**. Based on firmware size, the Media Pad and Numpad likely use the **HT32F52342 MCU** (64KB on-chip flash memory).  

- [Holtek HT32F52342/52 Datasheet](https://www.holtek.com/webapi/116711/HT32F52342_52_Datasheetv160.pdf)  
- [Holtek HT32F52342/52 User Manual](https://www.holtek.com/webapi/187541/HT32F52342-52_UserManualv130.pdf)  

Visit the [Holtek website](https://www.holtek.com) for additional SDK and starter kit resources, which may aid in firmware reverse engineering.  
