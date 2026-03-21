<h1>Mountain Everest Max Keyboard Protocol</h1>

<h1>Introduction</h1>
This document provides a detailed breakdown of the reverse-engineered protocol for the Mountain Everest Max keyboard.
It is intended for advanced users, developers, and Linux enthusiasts who wish to customize or extend the functionality of the keyboard.
The Mountain Everest Max is a modular mechanical keyboard with a customizable dial, RGB lighting, and programmable keys.
This document focuses on the communication protocol, key mappings, lighting effects, and other advanced features.

> **⚠️ WARNING**  
> Information is based on re-engineering and may be incomplete or partially incorrect.  
> Sending random commands or modifying existing commands may damage your keyboard!
> **Use at own risk!!!!**

This document aims mostly at messages that are interesting for a Linux user.  

<h1>Table of Contents</h1>

- [1. Communication Basics](#1-communication-basics)
  - [1.1. Interface Breakdown](#11-interface-breakdown)
  - [1.2. Communication Types](#12-communication-types)
- [2. Profile Related Commands](#2-profile-related-commands)
  - [2.1. Retrieve Profile Information](#21-retrieve-profile-information)
  - [2.2. Profile Mapping](#22-profile-mapping)
  - [2.3. Resetting Images for Physical Profiles](#23-resetting-images-for-physical-profiles)
  - [2.4. Switching Logical Profiles](#24-switching-logical-profiles)
  - [2.5. Querying Profile Slots](#25-querying-profile-slots)
    - [2.5.1. Example](#251-example)
      - [2.5.1.1. Description](#2511-description)
  - [2.6. Querying Profiles Settings](#26-querying-profiles-settings)
- [3. Dial Interaction](#3-dial-interaction)
  - [3.1. Querying Dial Settings](#31-querying-dial-settings)
  - [3.2. Modifying a Dial Item](#32-modifying-a-dial-item)
  - [3.3. Loading a Dial Image](#33-loading-a-dial-image)
  - [3.4. Resetting the Dial Image](#34-resetting-the-dial-image)
  - [3.5. Setting PC Info](#35-setting-pc-info)
  - [3.6. Setting Volume](#36-setting-volume)
  - [3.7. Setting Time on the Dial](#37-setting-time-on-the-dial)
- [4. Key Remapping](#4-key-remapping)
- [5. Defining Keyboard lighting](#5-defining-keyboard-lighting)
  - [5.1. Static Color (mode 0x00)](#51-static-color-mode-0x00)
  - [5.2. Breathing (mode 0x01)](#52-breathing-mode-0x01)
    - [5.2.1. Single Color Breathing](#521-single-color-breathing)
    - [5.2.2. Dual Color Breathing](#522-dual-color-breathing)
    - [5.2.3. Rainbow Breathing](#523-rainbow-breathing)
  - [5.3. Mode 0x02](#53-mode-0x02)
  - [5.4. Reactive Mode (mode 0x03)](#54-reactive-mode-mode-0x03)
  - [5.5. Wave](#55-wave)
    - [5.5.1. Single Color Wave](#551-single-color-wave)
    - [5.5.2. Four Color Wave](#552-four-color-wave)
    - [5.5.3. Rainbow Wave](#553-rainbow-wave)
  - [5.6. Mode 0x05](#56-mode-0x05)
  - [5.7. Yeti (mode 0x06)](#57-yeti-mode-0x06)
  - [5.8. Tornado (mode 0x07)](#58-tornado-mode-0x07)
    - [5.8.1. Single Color Tornado](#581-single-color-tornado)
    - [5.8.2. Rainbow Tornado](#582-rainbow-tornado)
  - [5.9. Mode 0x08](#59-mode-0x08)
  - [5.10. Matrix (mode 0x09)](#510-matrix-mode-0x09)
  - [5.11. Custom Mode (mode 0x0a)](#511-custom-mode-mode-0x0a)
    - [5.11.1. Enable Custom Mode Definition](#5111-enable-custom-mode-definition)
    - [5.11.2. Define the Mode Parameters](#5112-define-the-mode-parameters)
    - [5.11.3. Define the Static Colors](#5113-define-the-static-colors)
    - [5.11.4. Define the Static Colors for Side Lighting](#5114-define-the-static-colors-for-side-lighting)
    - [5.11.5. Bind Keys to a Specific Mode](#5115-bind-keys-to-a-specific-mode)
    - [5.11.6. Complete the Update](#5116-complete-the-update)
    - [5.11.7. Query the Custom Data (Key Mappings and Static Colors)](#5117-query-the-custom-data-key-mappings-and-static-colors)
      - [5.11.7.1. Query Key Mappings](#51171-query-key-mappings)
      - [5.11.7.2. Query Static Color Map](#51172-query-static-color-map)
      - [5.11.7.3. Alternate Query Command](#51173-alternate-query-command)
    - [5.11.8. Make Changes Persistent](#5118-make-changes-persistent)
  - [5.12. Mode 0x0b](#512-mode-0x0b)
  - [5.13. Turn Off the Background Lighting (Mode 0x0c)](#513-turn-off-the-background-lighting-mode-0x0c)
- [6. Image Download](#6-image-download)
  - [6.1. General Mechanism](#61-general-mechanism)
  - [6.2. Initialization of the process](#62-initialization-of-the-process)
  - [6.3. Query Command](#63-query-command)
  - [6.4. Start of Transfer](#64-start-of-transfer)
  - [6.5. Final Packet](#65-final-packet)
  - [6.6. Additional Notes](#66-additional-notes)
- [7. Game Mode](#7-game-mode)
  - [7.1. Game Mode Settings](#71-game-mode-settings)
    - [7.1.1. Unknown Command](#711-unknown-command)
    - [7.1.2. Core Indicator LEDs Off](#712-core-indicator-leds-off)
    - [7.1.3. Core Indicator LEDs On](#713-core-indicator-leds-on)
    - [7.1.4. Core Indicator LEDs Check State](#714-core-indicator-leds-check-state)
    - [7.1.5. Specific Enable/Disable Key Command](#715-specific-enabledisable-key-command)
    - [7.1.6. Specific Enable/Disable Key Command Check State](#716-specific-enabledisable-key-command-check-state)
- [8. Special Commands](#8-special-commands)
  - [8.1. Run Browser / Open Folder / Run Program Command](#81-run-browser--open-folder--run-program-command)
    - [8.1.1. Data Byte Descriptions](#811-data-byte-descriptions)
    - [8.1.2. Example for a Long Folder Name](#812-example-for-a-long-folder-name)
- [9. Messages initiated by keyboard](#9-messages-initiated-by-keyboard)
  - [9.1. Normal messages](#91-normal-messages)
  - [9.2. Message sent if key mapped to a special command is pressed](#92-message-sent-if-key-mapped-to-a-special-command-is-pressed)
- [10. Key mappings](#10-key-mappings)
  - [10.1. Mappings for US-International ANSI](#101-mappings-for-us-international-ansi)
  - [10.2. Pseudo Keys](#102-pseudo-keys)
  - [10.3. Hotkeys](#103-hotkeys)
    - [10.3.1. Profile Switching](#1031-profile-switching)
    - [10.3.2. RGB Settings](#1032-rgb-settings)
    - [10.3.3. Media Controls](#1033-media-controls)
    - [10.3.4. Additional Functions](#1034-additional-functions)
- [11. Color Mappings](#11-color-mappings)
  - [11.1. Mappings for US-International ANSI](#111-mappings-for-us-international-ansi)
  - [11.2. Mapping of side colors to leds](#112-mapping-of-side-colors-to-leds)
- [12. Version History](#12-version-history)

# 1. Communication Basics

- Commands are always 64 bytes long.
- All remaining unspecified bytes must be 0.
- Re-engineering is done using a US International ANSI keyboard, firmware version 57.24.20.
- For **direction** the numbers translate to the following:

| Value | Meaning                       |
| ----- | ------------------------------|
|   0   | From left to right            |
|   1   | From top-left to bottom-right |
|   2   | From top to bottom            |
|   3   | From top-right to bottom-left |
|   4   | From right to left            |
|   5   | From bottom-right to top-left |
|   6   | From bottom to top            |
|   7   | From bottom-left to top-right |
|   8   | Clockwise                     |
|   9   | Counter Clockwise             |

The table below gives a broad overview of the start of commands and the associated action.
These are detailed in the chapters below.

| Command     | Action |
| ----------- | ---------------------------------------------------------------- |
| 0x11 0x00 | Retrieve profile information |
| 0x11 0x01 0x00 0x00 0x02 | Get current profile and effect slot settings |
| 0x11 0x01 0x00 0x01 | Query profile settings |
| 0x11 0x01 0x00 0x02 | Queries static color settings (query results of 0x14 0x2c 0x00) |
| 0x11 0x01 0x00 0x03 | Queries custom mode key mappings (query results of 0x14 0xa0) |
| 0x11 0x14 | Map logical profile to physical profile |
| 0x11 0x81 | Set PC info on dial |
| 0x11 0x83 | Set Volume on dial |
| 0x11 0x80 | Prerequisite to set time |
| 0x11 0x84 | Set time on dial |
| 0x12 0x06 | Game Mode: Enable/disable specific keys |
| 0x12 0x07 | Game Mode: Set/reset core indicator leds |
| 0x17 | Game Mode:  |
| 0x13 0x42 | Reset display button images |
| 0x13 0x42 0x00 0x00 0x01| Reset dial button image to the default mountain image |
| 0x13 0x55 | Commit changes to flash |
| 0x14 0x00 | Switch to a logical profile |
| 0x14 0x20 | Redefine a key |
| 0x14 0x21 | Redefine a key with modifiers |
| 0x14 0x2c 0x00 | Define static color lighting |
| 0x14 0x2c 0x01 | Define breathing lighting |
| 0x14 0x2c 0x03 | Define reactive lighting |
| 0x14 0x2c 0x04 | Define wave lighting |
| 0x14 0x2c 0x06 | Define yeti lighting |
| 0x14 0x2c 0x07 | Define tornado lighting |
| 0x14 0x2c 0x09 | Define matrix lighting |
| 0x14 0x2c 0x0a | Define custom mode lighting |
| 0x14 0x2c 0x0c | Turn off lighting |
| 0x14 0x2d 0x00 0x0a | Define static colors for side leds |
| 0x14 0xa0 | Define custom mode for each key |
| 0x15 | Assigns a sequence of key presses to a key |
| 0x17 | special commands |
| 0xaa 0x55 0x10 | Signal transfer of images (and probably also other software) |
| 0xaa 0x55 0x21 | Initiate software upload (including updating dial and display key images) |
| 0xaa 0x55 0x22 | Query actual state |

## 1.1. Interface Breakdown

| Interface | Purpose                                                 |
| --------- | ------------------------------------------------------- |
| #0        | Primary interface; image loading, configuration queries |
| #1, #2    | Likely for macropad and displaypad communication        |
| #3        | Autonomous messages (e.g., key presses)                 |
| #4        | Asynchronous replies (0x84)                             |
| #5        | Most PC to keyboard commands                            |

## 1.2. Communication Types

- Interfaces 3, 4, 5: URB_INTERRUPT messages.
- Interface 0: SET_REPORT and GET_REPORT.

---

# 2. Profile Related Commands

## 2.1. Retrieve Profile Information

| Command     | Response                                                         |
| ----------- | ---------------------------------------------------------------- |
| `0x11 0x00` | `0x11 0x00 0x00 0x00 0x57 0x00 0x00 0x00 0x06 0x0a profile slot` |

- This command returns information, including the **profile number** and the **slot nnumber**.  
- The meaning of the other returned values is still unknown.
It is possible that the value `0x57` refers to the firmware version of the keyboard.

## 2.2. Profile Mapping

There is a distinction between:  

- **Profiles as shown in the UI (logical profiles).**  
- **Profiles as stored in the hardware (physical profiles).**  

The logical profiles selected using the dial or the FN key are mapped to one of the five physical profiles.  
This mapping is managed with the following command.

| Command     | Description                                                                   |
| ----------- | ----------------------------------------------------------------------------- |
| `0x11 0x14` | Command to map the logical profiles to physical ones and set dial properties. |

See section [3. Dial Interaction](#3-dial-interaction) for details.

## 2.3. Resetting Images for Physical Profiles

To reset display button images of a specific physical profile to default:

| Command                                        | Profile Description                                |
| ---------------------------------------------- | -------------------------------------------------- |
| `0x13 0x42 0x00 0x00 0x0f`                     | Resets images for the **first physical profile**.  |
| `0x13 0x42 0x00 0x00 0x00 0x0f`                | Resets images for the **second physical profile**. |
| `0x13 0x42 0x00 0x00 0x00 0x00 0x0f`           | Resets images for the **third physical profile**.  |
| `0x13 0x42 0x00 0x00 0x00 0x00 0x00 0x0f`      | Resets images for the **fourth physical profile**. |
| `0x13 0x42 0x00 0x00 0x00 0x00 0x00 0x00 0x0f` | Resets images for the **fifth physical profile**.  |

**Notes:**

- The last byte (`0x0f`) represents a **bitmap**.  
- To reset only the first bitmap of the first physical profile:  
  
  | Command                         | Description                                                 |
  | ------------------------------- | ----------------------------------------------------------- |
  | `0x13 0x42 0x00 0x00 0x00 0x01` | Resets only the first bitmap of the first physical profile. |

The command structure suggests that it is also possible to reset the images for multiple profiles
at the same time but this is not further tested.

## 2.4. Switching Logical Profiles

To switch to a specific logical profile:

| Command                            | Description                                      |
|------------------------------------| ------------------------------------------------ |
| `0x14 0x00 0x00 0x00 profno slot`  | Command to switch to a specific logical profile. |

| Parameter    | Description                                                         |
|--------------|---------------------------------------------------------------------|
| **`profno`** | Logical profile number. Profile `0` corresponds to **custom mode**. |
| **`slot`**   | Color slot applied to the keyboard. See the following table.        |

| Slot | Effect Name | Effect-ID |
|:----:| ----------- |:---------:|
|  0   | Static      | 0x00      |
|  1   | Color wave  | 0x04      |
|  2   | Tornado     | 0x07      |
|  3   | Breathing   | 0x01      |
|  4   | Reactive    | 0x03      |
|  5   | Matrix      | 0x09      |
|  6   | Custom      | 0x0a      |
|  7   | Yeti        | 0x06      |
|  8   | Off         | 0x0c      |

The relationship between profile and effect is indirect; A profile contains 9 slots and every slot contains an effect.
If you choose a 'Lighting' on the dialpad then the corresponding slot is selected which contains not only the effect;
It also contains the effect parameters like speed, brightness, colormode, colors and direction if appropriate.
It is technically possible to store another effect into a slot but neither the Keyboard (dialpad) nor the basecamp
software supports this.

## 2.5. Querying Profile Slots

The Keyboard has 6 Profiles with 9 Slots to hold color Effects; The slot can be selected on the
Dialpad under the menupoint 'Lighting'.

To get the current profile and slot Settings:  
Command: `0x11 0x01 0x00 0x00 0x02`

Response: 2 packets; from both packets the Header (7 bytes) has to be remove to get the response body.

>Header: `0x11 0x01 0x00 0x00 0x06 0x09 0xxx`; last byte is the package sequence number (down-counting).  
Guess: `0x06` stands for the number of profiles and `0x09` for the number of slots per profile

>The body contains 6 sets of 9 bytes describing the slotsettings for the profile and 6 bytes describing the active slot
of the profile.

### 2.5.1. Example

|  Profile  | Content |
|:---------:|---------|
|     0     | 0x04 0x0c 0x0c 0x0c 0x0c 0x0c 0x0c 0x0c 0x0c |
|     1     | 0x00 0x04 0x07 0x01 0x03 0x09 0x0a 0x06 0x0c |
|     2     | 0x00 0x04 0x07 0x01 0x03 0x09 0x0a 0x06 0x0c |
|     3     | 0x00 0x04 0x07 0x01 0x03 0x09 0x0a 0x06 0x0c |
|     4     | 0x00 0x04 0x07 0x01 0x03 0x09 0x0a 0x06 0x0c |
|     5     | 0x00 0x04 0x07 0x01 0x03 0x09 0x0a 0x06 0x0c |

Active Slots: 0x00 0x01 0x00 0x03 0x05 0x02

#### 2.5.1.1. Description

Profile 0 is the custom profile; the slots are referring to the effect id Profile  0 has the effects Colorwave and 8 times Off;

Profile 1 to 5 have the standard settings (Static, Colorwave, Tornado, Breathing, Reactive, Matrix, Custom, Yeti and Off)
>The active Slot of Profile 0 is 0 (Colorwave!)  
> Profile 1 is (Colorwave)  
> Profile 2 is 0 (Static)  
> Profile 3 is 3 (Breathing)  
> Profile 4 is 5 (Matrix) and  
> Profile 5 is 2 (Tornado)

⚠️ It maybe possible to change the effect id's in the Profile 1 to 5 but this is not recommended;
(I have done this accientally and it is not working perfect)

## 2.6. Querying Profiles Settings

Querying the profile settings is done through command `0x11 0x01 0x00 0x01`. This command returns the setting of an effect for a specific profile.

| Command                            | Response                                                      |
|------------------------------------|---------------------------------------------------------------|
| `0x11 0x01 0x00 0x01 prof_nr slot` | `0x11 0x01 0x00 0x01 profile slot effect-id 0x00 profiledata` |

The profiledata is structured as described in the **[Defining Keyboard lighting](#5-defining-keyboard-lighting)** section; The meaning of the profiledata starting with byte 9 is equal to the meaning in those section starting with byte 5.

To save changes permanently on the keyboard you have to execute the [Make Changes Persistent](#5118-make-changes-persistent) command.

# 3. Dial Interaction

## 3.1. Querying Dial Settings

Querying the dial settings is done through command `0x11 0x14`. This command returns the state of the dial.

| Command     | Response                                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| `0x11 0x14` | `0x11 0x14 0x00 0x01 0x02 items 0x00 r g b menu tlo thi offlo offhi p1 p2 p3 p4 p5 0x02 00 0x32 0x00 0x00 ledbri dialbri` |

| Parameter        | Description                                                                             |
| ---------------- | --------------------------------------------------------------------------------------- |
| **`items`**      | Bitmask specifying selectable menu items on the dial:                                   |
|                  | - `0x01`: Clock                                                                         |
|                  | - `0x02`: Profile                                                                       |
|                  | - ...                                                                                   |
|                  | - `0xFF`: All items are selectable.                                                     |
| **`r, g, b`**    | Color of the circle in the dial pad (e.g., volume icon).                                |
| **`menu`**       | Initial menu to be shown in the dial (Possible values):                                 |
|                  | - `0x00`: Image                                                                         |
|                  | - `0x10`: Clock                                                                         |
|                  | - `0x30`: Stopwatch                                                                     |
|                  | - `0x40`: Timer                                                                         |
|                  | - `0x70`: Volume                                                                        |
|                  | - `0x80`: Brightness                                                                    |
|                  | - `0x90`: PC Info - CPU                                                                 |
|                  | - `0xA0`: PC Info - GPU                                                                 |
|                  | - `0xB0`: PC Info - HD                                                                  |
|                  | - `0xC0`: PC Info - Network                                                             |
|                  | - `0xD0`: PC Info - RAM                                                                 |
|                  | - `0xE0`: APM                                                                           |
|                  | The initial menu is also shown as sceensaver                                            |
| **`tlo`**        | Low byte of screensaver timeout (in seconds), activated if **menu** is OR-ed with `1`.  |
| **`thi`**        | High byte of screensaver timeout.                                                       |
| **`offlo`**      | Low byte of dial turnoff timeout, (in seconds), activated if **menu** is OR-ed with `2`.|
| **`offhi`**      | High byte of dial turnoff timeout.                                                      |
| **`p1` to `p5`** | Profile-related slots for selectable profiles on the dial.                              |
|                  | - The values in `p1` to `p5` correspond to physical profiles.                           |
|                  | - Values `0x11` to `0x15` indicate profiles are selectable.                             |
|                  | - If a profile is not selectable it is not shown in the Profile menu on the dial        |
|                  | - Example: `p1 = 1, p2 = 2` (standard mapping) or `p1 = 2, p2 = 1` (reverses profiles). |
| **`ledbri`**     | Brightness of the LEDs.                                                                 |
| **`dialbri`**    | Brightness of the dial.                                                                 |
|                  | Values:                                                                                 |
|                  | - `0x80`: Brightness 0.                                                                 |
|                  | - `0x99`, `0xB2`, `0xCB`, `0xE4`: Intermediate brightness levels.                       |
|                  | - `0xFF`: Maximum brightness.                                                           |
|                  | - Other values have no effect                                                            |

> **Notes**
>
> - Some captures show the 5th and 21st bytes as `0x01` instead of `0x02`. Purpose unclear.  
> - Additional bytes for LED brightness have been observed after `ledbri` and `dialbri`.

## 3.2. Modifying a Dial Item

1. Query the dial settings using:  
   **Command:** `0x11 0x14`  
2. Modify the desired fields and send the updated packet back to the keyboard.

## 3.3. Loading a Dial Image

See [6. Image Download](#6-image-download)

## 3.4. Resetting the Dial Image

| Command                    | Description                                          |
| -------------------------- | ---------------------------------------------------- |
| `0x13 0x41 0x00 0x00 0x01` | Resets the dial image to the default mountain image. |

## 3.5. Setting PC Info

| Command                 | Description                         |
| ----------------------- | ----------------------------------- |
| `0x11 0x81 ix 0x00 val` | Sets PC info for a specified field. |

| Parameter | Description                                                                       |
| --------- | --------------------------------------------------------------------------------- |
| **`ix`**  | Field to modify:                                                                  |
|           | - `0`: CPU usage (%)                                                              |
|           | - `1`: GPU usage (%)                                                              |
|           | - `2`: HD usage (%)                                                               |
|           | - `3`: Network usage (MB/s)                                                       |
|           | - `4`: RAM usage (%)                                                              |
|           | - `5`: APM                                                                        |
| **`val`** | Value to set (0–100). If `val` > 100, display becomes garbled (but maxes at 100). |

## 3.6. Setting Volume

| Command                      | Description                                                                                                 |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `0x11 0x83 0x00 0x00 volume` | Sets the volume dial to a new value (0–100). If `volume` > 100, display becomes garbled (but maxes at 100). |

## 3.7. Setting Time on the Dial

| Step | Command                                                              | Description                                                                                 |
| ---- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1    | `0x11 0x80 0x00 0x00 0x01`                                           | Required for time setting to work.                                                          |
| 2    | `0x11 0x84 0x00 0x01 0x00 0x00 month day hour minute 0x01 0x00 mode` | Set the time with the specified `month, day, hour, minute`, and clock mode.                 |
| 3    | `0x11 0x84`                                                          | Query the current clock mode: `mode1` (analog or digital) and `mode2` (12-hour or 24-hour). |

# 4. Key Remapping

**Note:** Key bindings apply to the currently selected profile.
It is impossible to redefine key bindings in other profiles.

| Action                      | Command                                    | Description                                                        |
| --------------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| **Redefine a Key**          | `0x14 0x20 key 0x00 newkey`                | Redefines a key (`key`) to a new value (`newkey`).                 |
| **Reset a Key**             | `0x14 0x20 key 0x00 key`                   | Resets a key (`key`).                                              |
| **Disable a Key**           | `0x14 0x20 key 0x00 0x00`                  | Disables a key (`key`).                                            |
| **Redefine with Modifiers** | `0x14 0x21 key 0x00 newkey mode`           | Redefines a key with modifiers. `mode` is a bitmask for modifiers. |
| **Multi-Key Mapping**       | `0x15 key nritems seq key1 dir1 delay ...` | Assigns a sequence of key presses to a key.                        |

# 5. Defining Keyboard lighting

The commands defining the keyboard lighting all start with 0x14 0x2c.  
The third byte indicates the mode  

## 5.1. Static Color (mode 0x00)

| **Command**    | `0x14 0x2c 0x00 0x00 0xff brightness 0x00 0xff 0xff r g b`                                |
| -------------- | ----------------------------------------------------------------------------------------- |
| **Effect**     | Static color                                                                              |
| **Parameters** | **r, g, b**: RGB values (0–255) for color. <br> **brightness**: Brightness level (0–100). |

## 5.2. Breathing (mode 0x01)

### 5.2.1. Single Color Breathing

| **Command**    | `0x14 0x2c 0x01 0x00 speed brightness 0x00 0xff 0xff r g b`                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Single color breathing effect                                                                                                                                 |
| **Parameters** | **speed**: Speed of the breathing effect (e.g., fast or slow). <br> **brightness**: Brightness level (0–100). <br> **r, g, b**: RGB values (0–255) for color. |

### 5.2.2. Dual Color Breathing

| **Command**    | `0x14 0x2c 0x01 0x00 speed brightness 0x10 0xff 0xff r1 g1 b1 r2 g2 b2`                                                                                                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Dual color breathing effect (alternating colors)                                                                                                                                                                                         |
| **Parameters** | **speed**: Speed of the breathing effect (e.g., fast or slow). <br> **brightness**: Brightness level (0–100). <br> **r1, g1, b1**: RGB values (0–255) for the first color. <br> **r2, g2, b2**: RGB values (0–255) for the second color. |

### 5.2.3. Rainbow Breathing

| **Command**    | `0x14 0x2c 0x01 0x00 speed brightness 0x02 0xff 0xff`                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Rainbow breathing effect                                                                                      |
| **Parameters** | **speed**: Speed of the breathing effect (e.g., fast or slow). <br> **brightness**: Brightness level (0–100). |

## 5.3. Mode 0x02

This mode seems unused.

## 5.4. Reactive Mode (mode 0x03)

| **Command**    | `0x14 0x2c 0x03 0x00 speed brightness 0x00 0xff 0xff r1 g1 b1 0x00 0x00 0x00 0x00 0x00 0x00 r2 g2 b2`                                                                                                                                                 |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Reactive mode where the lighting changes when a key is pressed and returns to neutral when released                                                                                                                                                   |
| **Parameters** | **speed**: Speed of the reactive effect. <br> **brightness**: Brightness level (0–100). <br> **r1, g1, b1**: RGB values (0–255) when the key is pressed. <br> **r2, g2, b2**: RGB values (0–255) for the neutral color (when the key is not pressed). |

## 5.5. Wave

### 5.5.1. Single Color Wave

| **Command**    | `0x14 0x2c 0x04 0x00 speed brightness 0x00 direction 0x00 0x01 0x64 r g b 0xff`                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Effect**     | Single color wave effect                                                                                                                                                                                           |
| **Parameters** | **speed**: Speed of the wave. <br> **brightness**: Brightness level (0–100). <br> **direction**: Direction of the wave (0-7). <br> **r, g, b**: RGB values (0–255) for the color. |

### 5.5.2. Four Color Wave

| **Command**    | `0x14 0x2c 0x04 0x00 speed brightness 0x00 direction 0x02 0x04 0x19 r1 g1 b1 0x32 r2 g2 b2 0x48 r3 g3 b3 0x64 r4 g4 b4`                                                                                                                                                                                                                                                                                              |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Four color wave effect, cycling through four colors                                                                                                                                                                                                                                                                                                                                                                  |
| **Parameters** | **speed**: Speed of the wave. <br> **brightness**: Brightness level (0–100). <br> **direction**: Direction of the wave (0-7). <br> **r1, g1, b1**: RGB values (0–255) for the first color. <br> **r2, g2, b2**: RGB values (0–255) for the second color. <br> **r3, g3, b3**: RGB values (0–255) for the third color. <br> **r4, g4, b4**: RGB values (0–255) for the fourth color. |

### 5.5.3. Rainbow Wave

| **Command**    | `0x14 0x2c 0x04 0x00 speed brightness 0x02 direction 0x02 0x00 0xff 0x00 0x00 0x00 0xff`                                                                       |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Rainbow wave effect                                                                                                                                            |
| **Parameters** | **speed**: Speed of the wave. <br> **brightness**: Brightness level (0–100). <br> **direction**: Direction of the wave (0-7). |

## 5.6. Mode 0x05

This mode seems unused.

## 5.7. Yeti (mode 0x06)

| **Command**    | `0x14 0x2c 0x06 0x00 speed brightness 0x00 0xff 0xff r1 g1 b1 0x00 0x00 0x00 0x00 0x00 0x00 r2 g2 b2`                                                                                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Yeti effect with two colors in a rhythmic pattern                                                                                                                                                         |
| **Parameters** | **speed**: Speed of the effect. <br> **brightness**: Brightness level (0–100). <br> **r1, g1, b1**: RGB values (0–255) for the first color. <br> **r2, g2, b2**: RGB values (0–255) for the second color. |

## 5.8. Tornado (mode 0x07)

### 5.8.1. Single Color Tornado

| **Command**    | `0x14 0x2c 0x07 0x00 speed brightness 0x00 direction 0x00 0x01 0x64 r g b 0xff`                                                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Effect**     | Single color tornado effect                                                                                                                                                                                                    |
| **Parameters** | **speed**: Speed of the tornado effect. <br> **brightness**: Brightness level (0–100). <br> **direction**: Direction of the tornado (9 for clockwise, 10 for counterclockwise). <br> **r, g, b**: RGB values (0–255) for the color. |

### 5.8.2. Rainbow Tornado

| **Command**    | `0x14 0x2c 0x07 0x00 speed brightness 0x02 direction 0x02 0x00 0xff 0x00 0x00 0x00 0xff`                                                                                   |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Rainbow tornado effect                                                                                                                                                     |
| **Parameters** | **speed**: Speed of the tornado effect. <br> **brightness**: Brightness level (0–100). <br> **direction**: Direction of the tornado (9 for clockwise, 10 for counterclockwise). |

## 5.9. Mode 0x08

This mode seems unused.

## 5.10. Matrix (mode 0x09)

| **Command**    | `0x14 0x2c 0x09 0x00 speed brightness 0x00 0xff 0xff r1 g1 b1 0x00 0x00 0x00 0x00 0x00 0x00 r2 g2 b2`                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Matrix effect where colors can fill a grid pattern                                                                                                                                                               |
| **Parameters** | **speed**: Speed of the matrix effect. <br> **brightness**: Brightness level (0–100). <br> **r1, g1, b1**: RGB values (0–255) for the first color. <br> **r2, g2, b2**: RGB values (0–255) for the second color. |

## 5.11. Custom Mode (mode 0x0a)

Custom mode allows you to specify the lighting per key.
You can specify for each led (including the side leds) what color mode it will be in.
So some keys can be bound to static color where other keys are bound to breathing and yet others to e.g. yeti.

The caveat is that for all modes except static mode there is only a single setting available. So for e.g. reactive you can specify the
pressed color and the default color, but that applies to all keys that are marked as reactive. So it is not possible to have one key with red as
pressed color and another one with green as pressed color. Also for wave, tornado and breathing you can only specify one submode. So one key cannot be
breathing rainbow and another key breathing red.  
There is an exception for static mode. In that mode it is possible to set colors to individual keys. How to do this is explained later on.

In order to define your custom color scheme the following things need to be done.

- enable custom mode
- define the mode parameters (if appropriate)
- define the static colors (if appropriate)
- bind the keys to a specific mode
- completing the update
- optionally make the data persistent

Remember: mode is between 0x00 and 0x0c (inclusive).

We'll discuss these items in the subsequent sections.

### 5.11.1. Enable Custom Mode Definition

| **Command**    | `0x14 0x2c 0x0a 0x00 0xff brightness 0x00`    |
| -------------- | --------------------------------------------- |
| **Effect**     | Enable custom mode for lighting customization |
| **Parameters** | **brightness**: Brightness level (0–100).     |

### 5.11.2. Define the Mode Parameters

These define the settings for different lighting effects like breathing, wave, etc.

| **Command**    | `0x14, 0x2c, 0x04, 0x01, speed, brightness, 0x00, direction, 0x00, 0x01, 0x64, r, g, b, 0xff`                                                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Defines lighting effects like wave or breathing                                                                                                                                                                      |
| **Parameters** | **speed**: Speed of the effect. <br> **brightness**: Brightness level (0–100). <br> **direction**: Direction of the wave (0-7). <br> **r, g, b**: RGB values (0–255) for the color. |

### 5.11.3. Define the Static Colors

Used to set the color for each LED on the keyboard (up to 126 LEDs). It sends 8 packets, each for a subset of the keys.

| **Command**    | `0x14 0x2c 0x00 0x01 ix brightness 0x00`                                          |
| -------------- | :-------------------------------------------------------------------------------- |
| **Effect**     | Defines static colors for each LED, broken into packets.                          |
| **Parameters** | **ix**: Index of the packet (0–7). <br> **brightness**: Brightness level (0–100). |

The command is followed by 57 bytes specifying the r, g, b, values for 19 LEDs. ix 0 is for the first 19, ix 1 for the 2nd 19 and so on.

### 5.11.4. Define the Static Colors for Side Lighting

This defines static colors for side LEDs, using a similar approach with smaller packets.

| **Command**    | `0x14 0x2d 0x0a 0x00 ix 0xff 0x00`     |
| -------------- | -------------------------------------- |
| **Effect**     | Defines static color for the side LEDs |
| **Parameters** | **ix**: Index of the packet (0–2).     |

The command is followed by 57 bytes specifying the r, g, b, values for 19 LEDs. ix 0 is for the first 19, ix 1 for the 2nd 19 and ix 2 for the remaining 7 (there are in total 45 side LEDs). The last packet is padded with zeroes.

### 5.11.5. Bind Keys to a Specific Mode

This command allows assigning a lighting mode to each individual key.

| **Command**    | `0x14 0xa0 0x00 0x01` followed by 60 bytes with key mode mappings                                                                                      |
| -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effect**     | Binds a lighting mode (e.g., static, breathing, wave) to specific keys on the keyboard.                                                                |
| **Parameters** | A sequence of 60 bytes where each byte represents the mode for a specific key. Mode 0 is static, mode 4 is wave, and mode 1 is breathing, for example. |

As there is only room for 60 key mappings (a packet is 64 bytes and the first four are used by 0x14 0xa0 0x00 0x00) the remainder of the keys are sent using two additional packets. Byte 3 (index 2) serves as index. So the 2nd packet starts with
**0x14 0xa0 0x01 0x01**
and the third one with
**0x14 0xa0 0x02 0x01**

### 5.11.6. Complete the Update

Final commands to confirm the changes and apply the configuration.

| **Command**    | `0x14 0xa0 0x00 0x01` <br> `0x14 0xa0 0x01 0x01` <br> `0x14 0xa0 0x02 0x01`                   |
| -------------- | :-------------------------------------------------------------------------------------------- |
| **Effect**     | This commits the changes to the keyboard lighting setup.                                      |
| **Parameters** | No specific parameters. These commands ensure that changes to the lighting modes are applied. |

### 5.11.7. Query the Custom Data (Key Mappings and Static Colors)

Commands to query and fetch the current custom lighting configuration.

#### 5.11.7.1. Query Key Mappings

| **Command**    | `0x11 0x01 0x00 0x03 profile 0x02`                      |
| -------------- | :------------------------------------------------------ |
| **Effect**     | Queries the current key-to-mode mappings.               |
| **Parameters** | Returns the mapping for all keys, split into 3 packets. |

#### 5.11.7.2. Query Static Color Map

| **Command**    | `0x11 0x01 0x00 0x02 profile 0x02`                                                              |
| -------------- | :---------------------------------------------------------------------------------------------- |
| **Effect**     | Queries the current static color settings for the keyboard.                                     |
| **Parameters** | Returns the static color data in 7 packets, with each packet containing 59 bytes of color data. |

#### 5.11.7.3. Alternate Query Command

| **Command**    | `0x11 0x01 0x00 0x01 profile 0x02`                                      |
| -------------- | :---------------------------------------------------------------------- |
| **Effect**     | An alternate way to query the static color map or other data.           |
| **Parameters** | Returns data with a different structure, useful for further inspection. |

### 5.11.8. Make Changes Persistent

This command commits the changes and ensures they persist even after restarting the device. It is possible to save any effect to any slots
but the menunames on the dialpad are fixed connected to the slot number and would not reflect the real effect.

| **Command**    | `0x13 0x55 0x00 0x00 slot_nr`                                                                                             |
| -------------- | :------------------------------------------------------------------------------------------------------------------------ |
| **Effect**     | Makes the lighting setup persistent to the slot. Without this command, changes may be lost after restarting the keyboard. |
| **Parameters** | No parameters. This is a final step to save the changes permanently.                                                      |

## 5.12. Mode 0x0b

This mode seems unused.

## 5.13. Turn Off the Background Lighting (Mode 0x0c)

This command turns off the lighting by setting brightness to 0 or using black.

| **Command**    | `0x14, 0x2c, 0x0c, 0x00, 0xff, 64, 0xff, 0xff, 0xff`          |
| -------------- | :------------------------------------------------------------ |
| **Effect**     | Turns off the background lighting.                            |
| **Parameters** | No parameters. This command completely disables the lighting. |

# 6. Image Download

This section describes how to download images to the Display keys and to de Dial.  
Images to be downloaded are encoded in **RGB565 format** (5 red bits, 6 green bits, 5 blue bits), with **2 bytes per pixel**.  
Display key images are 72x72 pixels, the dial image is 240x204 pixels.

> **⚠️ WARNING**  
> The commands to upload an image are also used to update the firmware.
> It is **strongly discouraged** to experiment with arguments in the messages
as this could effectively **ruin** your keyboard or pad!
> **Use at own risk!!!!**

## 6.1. General Mechanism

Image download is achieved through `SET_REPORT` messages, with `GET_REPORT` messages used to control the transfer.  
In `libhidapi` terms, this involves `hid_get_feature_report` and `hid_send_feature_report` calls. Both operations use **64-byte data transfers**.  
The following steps apply:

- The host sends a SET_REPORT **Command** to the keyboard.  
- The keyboard acknowledges reception of the command.
- The host sends a GET_REPORT message to the keyboard.  
- The keyboard sends a **Response**  to the host.
- The **fourth byte of the response** indicates success or failure:  
  - `0xfa`: Success or command executed.  
  - `0xfb`: Not accepted (e.g., busy or try again).  

## 6.2. Initialization of the process

Starts the process:

| Command               | Response              |
| --------------------- | --------------------- |
| `0xaa 0x55 0x21 dest` | `0xaa 0x55 0x21 0xfa` |

This sets the destination for the uploaded data.  
`dest` = 0x03 for the dial and 0x04 for the display keys.

## 6.3. Query Command

This queries the actual state. It seems to be a confirmation of the previous command.

| Command          | Response                   |
| ---------------- | -------------------------- |
| `0xaa 0x55 0x22` | `0xaa 0x55 0x22 0xfa dest` |

## 6.4. Start of Transfer

Signals the beginning of the image transfer:

| Command                                                             | Response (success)    | Response (failure)    |
| ------------------------------------------------------------------- | --------------------- | --------------------- |
| `0xaa 0x55 0x10 sl sm sh clow chigh 0x00 0x00 0x02 profileno ledno` | `0xaa 0x55 0x10 0xfa` | `0xaa 0x55 0x10 0xfb` |

Explanation of Bytes  

| Byte Position     | Description                                  |
| ----------------- | -------------------------------------------- |
| **`sl, sm, sh`**  | Image size                                   |
| **`clow, chigh`** | Checksum of all pixel values (16-bit).       |
| **`profileno`**   | Profile number                               |
| **`ledno`**       | LED to update                                |

`sl, sm, sh` is the image size.  
For display keys: size = `0x002880` for 72x72: `sl = 0x80`, `sm = 0x28`, `sh = 0x00`; total: 10,368 bytes = 72 × 72 × 2  
For dial image: size = `0x017e80` for 240*204: `sl = 0x80`, `sm = 0x7e`, `sh = 0x01`; total: 97,920 bytes = 240 × 204 × 2  

`**clow, chigh**` is the checkum of the image, It is just a addition of all bytes.

`**profileno**` is the profile number, 1 for the dial image, 1-5 for the display keys.

`**ledno**` is the led number, 1 for the dial  image, 1 to 4 for the display keys (1 being the leftmost key)

The image data is transferred a number of packets. Each packet contains 64 bytes (so data for 32 pixels).  
For display images a total of 10,468/64 so 162 packets are to be sent.
For dial images a total of 97,920/64 so 1530 packets are to be sent.  

The response on this command for all but the last packet is:

| Response (success)             | Response (failure)    |
| ------------------------------ | --------------------- |
| `0xaa 0x55 0x10 0xfa sl sm sh` | `0xaa 0x55 0x10 0xfb` |

- In case of failure, retransmit is required.  
- **`sl` , `sm` and `sh`** indicate the total size of data received so far.

>**⚠️  WARNING**  
It is not advised to use image sizes greater than the above mentioned values.  
This will probably exceed the size of the internal buffer and could brick your Numpad or Dialpad.

## 6.5. Final Packet

The final packet’s response:

| Response                                             |
| ---------------------------------------------------- |
| `0xaa 0x55 0x10 0xfa 0x80 0x28 0x00 clow chigh 0xfe` |

- **`0xfe`**: Indicates transfer completion.  
- Second **`0xfa`**: Confirms successful transfer.

## 6.6. Additional Notes

- Even if the checksum doesn’t match, the LEDs will flicker, and the new icon will display.  
- The total download time for one display icon is ~**4.5 seconds**, likely due to writing to flash memory.  
- The total download time for a dial image is ~**30 seconds**, likely due to writing to flash memory.  
- While the image size of a display icon is **72x72 pixels**, the visible area is limited to ~**64x64 pixels**.

# 7. Game Mode

## 7.1. Game Mode Settings

The settings modified by the commands in this section are effective only when the keyboard is in **Game Mode**.  
To toggle **Game Mode**, press **FN-PAUSE**.  
Commands for Game Mode begin with `0x12`.

### 7.1.1. Unknown Command

| **Command**  | `0x12 0x08 0x00 0x01 0x00`                                                                                                               |
| ------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Response** | `0x12 0x08 0x00 0x01 0x00`                                                                                                               |
| **Purpose**  | The exact purpose of this command is unclear.                                                                                            |
| **Note**     | In testing, this command was observed to be sent before `0x12 0x06` and `0x12 0x07`, but it was found unnecessary before these commands. |

### 7.1.2. Core Indicator LEDs Off

| **Command**           | `0x12 0x07 0x00 0x01 0x01`                          |
| --------------------- | :-------------------------------------------------- |
| **Response**          | `0x12 0x07 0x00 0x01 0x01`                          |
| **5th Byte (Effect)** | `0x1` = LEDs off, `0x0` = LEDs on                   |
| **Effect**            | Disables Caps Lock, Scroll Lock, and Num Lock LEDs. |

### 7.1.3. Core Indicator LEDs On

| **Command**  | `0x12 0x07 0x00 0x01 0x00`                         |
| ------------ | :------------------------------------------------- |
| **Response** | `0x12 0x07 0x00 0x01 0x00`                         |
| **Effect**   | Enables Caps Lock, Scroll Lock, and Num Lock LEDs. |

### 7.1.4. Core Indicator LEDs Check State

| **Command**   | `0x12 0x07 0x00 0x00 0x00`        |
| ------------- | :-------------------------------- |
| **Response**  | `0x12 0x07 0x00 0x00 effect`      |
| **Effect**    | Get State of Core Indicator LEDs. |

### 7.1.5. Specific Enable/Disable Key Command

| **Command**        | `0x12 0x06 0x00 0x01 bits`             |
| ------------------ | :------------------------------------- |
| **Response**       | `0x12 0x06 0x00 0x01 bits`             |
| **Bits (Bitmask)** | See below for the meaning of each bit. |

| **Bit** | **Description**     |
| ------- | ------------------- |
| `0x01`  | Disable Shift + Tab |
| `0x02`  | Disable Alt + F4    |
| `0x04`  | Disable Windows Key |
| `0x08`  | Disable Alt + Tab   |

- **To disable** a specific function, set the bit to `1`.
- **To enable** a specific function, set the bit to `0`.

### 7.1.6. Specific Enable/Disable Key Command Check State

| **Command**        | `0x12 0x06 0x00 0x0 0x00`               |
| ------------------ | :-------------------------------------- |
| **Response**       | `0x12 0x06 0x00 0x00 bits`              |
| **Bits (Bitmask)** | See above for the meaning of each bit.  |

# 8. Special Commands

## 8.1. Run Browser / Open Folder / Run Program Command

| **Command** | `0x17 key size seq data`                                                                                                              |
| ----------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| **Key**     | The key used to invoke the command.                                                                                                   |
| **Size**    | The length of the data, including the terminating 0 byte.                                                                             |
| **Seq**     | The sequence number, used when the data doesn't fit into one packet. Starts at 1, but if the data fits in one packet, the value is 0. |
| **Data**    | The data to be acted upon. The first byte specifies the operation to be performed.                                                    |

### 8.1.1. Data Byte Descriptions

| **Byte Value** | **Action**                                       |
| -------------- | ------------------------------------------------ |
| `0x01`         | Run program (remaining data is the URL).         |
| `0x02`         | Run in browser (remaining data is the URL).      |
| `0x03`         | Unknown action.                                  |
| `0x04`         | Open folder (remaining data is the folder name). |

**Note**: The mode byte only exists in the first packet.

### 8.1.2. Example for a Long Folder Name

Here is the message to be sent when key F1 (keycode 0x70) is to be mapped to open a folder.
Note that the ASCII text is for illustration purposes only. The message is only the hex bytes.

```text
17 70 3c 01 04
43 3a 5c 50 72 6f 67 72 61 6d 20 46 69 6c 65 73
C  :  \  P  r  o  g  r  a  m     F  i  l  e  s 
5c 4d 69 63 72 6f 73 6f 66 74 20 56 69 73 75 61
\  M  i  c  r  o  s  o  f  t     V  i  s  u  a 
6c 20 53 74 75 64 69 6f 5c 32 30 32 32 5c 43 6f
l     S  t  u  d  i  o  \  2  0  2  2  \  C  o 
6d 6d 75 6e 69 74 79 5c 43 6f 6d
m  m  u  n  i  t  y  \  C  o  m 
```

```text
17 70 3c 02 6d
6f 6e 37 5c 49 44 45 5c 43 6f 6d 6d 6f 6e 45 78
o  n  7  \  I  D  E  \  C  o  m  m  o  n  E  x 
74 65 6e 73 69 6f 6e 73 5c 4d 69 63 72 6f 73 6f
t  e  n  s  i  o  n  s  \  M  i  c  r  o  s  o 
66 74 5c 43 6c 69 65 6e 74 44 69 61 67 6e 6f 73
f  t  \  C  l  i  e  n  t  D  i  a  g  n  o  s 
74 69 63 73 5c 41 70 70 52 65 73
t  i  c  s  \  A  p  p  R  e  s 
```

```text
17 70 2e 03 70  
6f 6e 73 69 76 65 6e 65 73 73 5c 56 69 65 77 5c
o  n  s  i  v  e  n  e  s  s  \  V  i  e  w  \ 
44 69 61 67 6e 6f 73 74 69 63 73 43 6f 6d 6d 6f
D  i  a  g  n  o  s  t  i  c  s  C  o  m  m  o 
6e 5c 6c 69 73 74 43 6f 6e 74 72 6f 6c 00 00 00
n  \  l  i  s  t  C  o  n  t  r  o  l  .  .  . 
00 00 00 00 00 00 00 00 00 00 00
```

# 9. Messages initiated by keyboard

All these messages are sent on interface #3.

## 9.1. Normal messages

If a key is pressed a message starting with `0x0100` is sent.  
After these two bytes there are 16 more bytes implementing n-key rollover.
These bytes are bitmasks that are 1 if the corresponding key is pressed.  
The first byte specifies the meta keys. A clipping from wireshark illustrates this mapping.

```text
    .... ...0 = Key: LeftControl (0xe0): UP
    .... ..0. = Key: LeftShift (0xe1): UP
    .... .0.. = Key: LeftAlt (0xe2): UP
    .... 0... = Key: LeftGUI (0xe3): UP
    ...0 .... = Key: RightControl (0xe4): UP
    ..0. .... = Key: RightShift (0xe5): UP
    .0.. .... = Key: RightAlt (0xe6): UP
    0... .... = Key: RightGUI (0xe7): UP
```

The next bytes map to bytes as specified in the HID usage table for keyboard.
but not all entries in that map are
present in the wireshark disassembly. Probably one of the descriptors specifies what is present and what not.
The HID usage table can be found in chapter 10 of [HID Usage Tables 1.5](https://usb.org/sites/default/files/hut1_5.pdf).

A reference to a list giving the mapping from bit to key will be added in due time.
For now refer to the disassembly in wireshark.

## 9.2. Message sent if key mapped to a special command is pressed

0x17 0x70 len 0x00 mode name/command  
len is the length of the message. The mode field is included in the length.  
mode is the mode as specified in [8.1.1. Data Byte Descriptions](#811-data-byte-descriptions).  
name/command is the argument that is assigned to the key  

Only 60 (0x3c) bytes fit in the reply. If that is not enough the 4th byte of the packet is 0x01.
Subsequent packets are sent each incrementing the 4th byte until the whole data is received.
The last packet thus has a payload size < 60 bytes.  
This is similar to the way the data is defined.

# 10. Key mappings

## 10.1. Mappings for US-International ANSI

| nr  | hex  | ch                                       |
|:---:|:----:|:---------------------------------------- |
| 1   | 0x1  | `                                        |
| 2   | 0x2  | 1                                        |
| 3   | 0x3  | 2                                        |
| 4   | 0x4  | 3                                        |
| 5   | 0x5  | 4                                        |
| 6   | 0x6  | 5                                        |
| 7   | 0x7  | 6                                        |
| 8   | 0x8  | 7                                        |
| 9   | 0x9  | 8                                        |
| 10  | 0xA  | 9                                        |
| 11  | 0xB  | 0                                        |
| 12  | 0xC  | -                                        |
| 13  | 0xD  | =                                        |
| 14  | 0xE  | keycode 132                              |
| 15  | 0xF  | Backspace                                |
| 16  | 0x10 | Tab                                      |
| 17  | 0x11 | q                                        |
| 18  | 0x12 | w                                        |
| 19  | 0x13 | e                                        |
| 20  | 0x14 | r                                        |
| 21  | 0x15 | t                                        |
| 22  | 0x16 | y                                        |
| 23  | 0x17 | u                                        |
| 24  | 0x18 | i                                        |
| 25  | 0x19 | o                                        |
| 26  | 0x1A | p                                        |
| 27  | 0x1B | [                                        |
| 28  | 0x1C | ]                                        |
| 29  | 0x1D | \\                                       |
| 30  | 0x1E | Caps Lock                                |
| 31  | 0x1F | a                                        |
| 32  | 0x20 | s                                        |
| 33  | 0x21 | d                                        |
| 34  | 0x22 | f                                        |
| 35  | 0x23 | g                                        |
| 36  | 0x24 | h                                        |
| 37  | 0x25 | j                                        |
| 38  | 0x26 | k                                        |
| 39  | 0x27 | l                                        |
| 40  | 0x28 | ;                                        |
| 41  | 0x29 | '                                        |
| 43  | 0x2B | Enter                                    |
| 44  | 0x2C | shift-L (keycode 50)                     |
| 46  | 0x2E | z                                        |
| 47  | 0x2F | x                                        |
| 48  | 0x30 | c                                        |
| 49  | 0x31 | v                                        |
| 50  | 0x32 | b                                        |
| 51  | 0x33 | n                                        |
| 52  | 0x34 | m                                        |
| 53  | 0x35 | ,                                        |
| 54  | 0x36 | .                                        |
| 55  | 0x37 | /                                        |
| 56  | 0x38 | keycode 97                               |
| 57  | 0x39 | shift-R (keycode 62)                     |
| 58  | 0x3A | control-L                                |
| 59  | 0x3B | Super-L (left key with the windows logo) |
| 60  | 0x3C | Alt-L                                    |
| 61  | 0x3D | Space                                    |
| 62  | 0x3E | Alt-R                                    |
| 63  | 0x3F | Super-R (right key with windows logo)    |
| 64  | 0x40 | control-R                                |
| 75  | 0x4B | INSERT                                   |
| 76  | 0x4C | DELETE                                   |
| 79  | 0x4F | Cursor left                              |
| 80  | 0x50 | HOME                                     |
| 81  | 0x51 | END                                      |
| 82  | 0x52 | KP_1 (Numpad 1)                          |
| 83  | 0x53 | Cursor up                                |
| 84  | 0x54 | Cursor down                              |
| 85  | 0x55 | PG UP                                    |
| 86  | 0x56 | PG DN                                    |
| 89  | 0x59 | Cursor right                             |
| 90  | 0x5A | NumLock                                  |
| 91  | 0x5B | KP_7 (Numpad 7)                          |
| 92  | 0x5C | KP_4 (Numpad 4)                          |
| 95  | 0x5F | KP_Divide                                |
| 96  | 0x60 | KP_8 (Numpad 8)                          |
| 97  | 0x61 | KP_5 (Numpad 5)                          |
| 98  | 0x62 | KP_2 (Numpad 2)                          |
| 99  | 0x63 | KP_0 (Numpad 0)                          |
| 100 | 0x64 | KP_Multiply                              |
| 101 | 0x65 | KP_9 (Numpad 9)                          |
| 102 | 0x66 | KP_6 (Numpad 6)                          |
| 103 | 0x67 | KP_3 (Numpad 3)                          |
| 104 | 0x68 | KP_Decimal                               |
| 105 | 0x69 | KP_Minus                                 |
| 106 | 0x6A | KP_Plus                                  |
| 108 | 0x6C | KP_ENTER                                 |
| 110 | 0x6E | ESC                                      |
| 112 | 0x70 | F1                                       |
| 113 | 0x71 | F2                                       |
| 114 | 0x72 | F3                                       |
| 115 | 0x73 | F4                                       |
| 116 | 0x74 | F5                                       |
| 117 | 0x75 | F6                                       |
| 118 | 0x76 | F7                                       |
| 119 | 0x77 | F8                                       |
| 120 | 0x78 | F9                                       |
| 121 | 0x79 | F10                                      |
| 122 | 0x7A | F11                                      |
| 123 | 0x7B | F12                                      |
| 124 | 0x7C | PRT SCN                                  |
| 125 | 0x7D | SCR LK                                   |
| 126 | 0x7E | PAUSE                                    |
| 170 | 0xAA | D1 (leftmost LED key)                    |
| 171 | 0xAB | D2 (second LED key)                      |
| 172 | 0xAC | D3 (third LED key)                       |
| 173 | 0xAD | D4 (rightmost LED key)                   |
| 180 | 0xB4 | Dialpad next track                       |
| 181 | 0xB5 | Dialpad prev track                       |
| 183 | 0xB7 | Dialpad play/pause                       |
| 184 | 0xB8 | Dialpad mute                             |
| 187 | 0xBB | Dial volume up                           |
| 188 | 0xBC | Dial volume down                         |

## 10.2. Pseudo Keys

These are virtual keys that do not physically exist on the keyboard but can be used in key mappings to assign new functions or redefine existing keys.

| nr  | hex  | ch                                                        |
|:---:|:----:|:--------------------------------------------------------- |
| 160 | 0xA0 | Profile 1 (Use this to bind a key to switch to Profile 1) |
| 161 | 0xA1 | Profile 2                                                 |
| 162 | 0xA2 | Profile 3                                                 |
| 163 | 0xA3 | Profile 4                                                 |
| 164 | 0xA4 | Profile 5                                                 |
| 230 | 0xE6 | F13                                                       |
| 231 | 0xE7 | F14                                                       |
| 232 | 0xE8 | F15                                                       |
| 233 | 0xE9 | F16                                                       |
| 234 | 0xEA | F17                                                       |
| 235 | 0xEB | F18                                                       |
| 236 | 0xEC | F19                                                       |
| 237 | 0xED | F20                                                       |
| 238 | 0xEE | F21                                                       |
| 239 | 0xEF | F22                                                       |
| 240 | 0xF0 | F23                                                       |
| 241 | 0xF1 | F24                                                       |

The numbering for physical keys remains consistent across all language variants of the ANSI keyboard layout.  
For example, the key directly below the **ESC** key will always have the keycode `0x1`. Subsequent keys are numbered sequentially, so the key to the right of ESC (often the '1' key) will have keycode 0x2.  
For the next row, the **Tab** key always has the keycode `0x10`, with all following keys continuing from there. However, on an **ISO** keyboard, the keycode `0x1D` does not exist.

The **Caps Lock** key always has the keycode `0x1E`, with subsequent keys continuing from there. On an **ISO** keyboard, there is an additional key above the **Right Shift** key that corresponds to `0x2D`, which does not exist on an ANSI layout.

The **Left Shift** key always has the keycode `0x2C` on both ANSI and ISO keyboards. On an **ISO** keyboard, there is an additional key between the **Left Shift** and **Z** keys, which has the keycode `0x2D`. **Z** then has keycode 0x2E, and so on.

The actual characters produced by the keys depend on the language setting of the
keyboard. For instance, the first row of letters on a **French ISO** keyboard
starts with `azerty`, whereas the **German ISO** layout starts with `qwertz`.
In both cases, the first letter (`a` on the French layout, `q` on the German layout)
will have the internal keycode `0x11`.

## 10.3. Hotkeys

The following hotkeys are available:

### 10.3.1. Profile Switching

- **FN + 1/2/3/4/5**: Switch to profile 1/2/3/4/5 (Default: Profile 1)

### 10.3.2. RGB Settings

- **FN + Left Arrow**: Cycle RGB modes forward  
- **FN + Right Arrow**: Cycle RGB modes backward  
- **FN + Up Arrow**: Toggle brightness levels (Off / Level 1 / Level 2 / Level 3)

### 10.3.3. Media Controls

- **FN + Page Up**: Increase volume  
- **FN + Page Down**: Decrease volume  
- **FN + End**: Next track  
- **FN + Delete**: Previous track  
- **FN + Insert**: Play/Pause  
- **FN + Home**: Mute

### 10.3.4. Additional Functions

- **FN + R** (hold for 5+ seconds): Reset all settings to factory defaults  
- **FN + Pause**: Enable Game Mode (Locks Windows keys)  

# 11. Color Mappings

## 11.1. Mappings for US-International ANSI

| Color Index | Key                                                    |
|:-----------:|:------------------------------------------------------:|
| 0           | esc                                                    |
| 1           | `                                                      |
| 2           | tab                                                    |
| 3           | capslock                                               |
| 4           | lshift                                                 |
| 5           | lctrl                                                  |
| 6           | num lock                                               |
| 7           | KP_+                                                   |
| 8           | unused                                                 |
| 9           | F1                                                     |
| 10          | 1                                                      |
| 11          | q                                                      |
| 12          | a                                                      |
| 13          | unused (probably key between L-shift and z on ISO kbd) |
| 14          | L windows                                              |
| 15          | KP_-                                                   |
| 16          | KP_*                                                   |
| 17          | unused                                                 |
| 18          | F2                                                     |
| 19          | 2                                                      |
| 20          | w                                                      |
| 21          | s                                                      |
| 22          | z                                                      |
| 23          | L alt                                                  |
| 24          | KP_/                                                   |
| 25          | unused                                                 |
| 26          | unused                                                 |
| 27          | F3                                                     |
| 28          | 3                                                      |
| 29          | e                                                      |
| 30          | d                                                      |
| 31          | x                                                      |
| 32          | unused                                                 |
| 33          | KP_enter                                               |
| 34          | KP_1                                                   |
| 35          | unused                                                 |
| 36          | F4                                                     |
| 37          | 4                                                      |
| 38          | r                                                      |
| 39          | f                                                      |
| 40          | c                                                      |
| 41          | space                                                  |
| 42          | KP_2                                                   |
| 43          | KP_3                                                   |
| 44          | unused                                                 |
| 45          | F5                                                     |
| 46          | 5                                                      |
| 47          | t                                                      |
| 48          | g                                                      |
| 49          | v                                                      |
| 50          | unused                                                 |
| 51          | KP_4                                                   |
| 52          | KP_5                                                   |
| 53          | unused                                                 |
| 54          | F6                                                     |
| 55          | 6                                                      |
| 56          | y                                                      |
| 57          | h                                                      |
| 58          | b                                                      |
| 59          | unused                                                 |
| 60          | KP_6                                                   |
| 61          | KP_7                                                   |
| 62          | unused                                                 |
| 63          | F7                                                     |
| 64          | 7                                                      |
| 65          | u                                                      |
| 66          | j                                                      |
| 67          | n                                                      |
| 68          | R alt                                                  |
| 69          | KP_8                                                   |
| 70          | KP_9                                                   |
| 71          | unused                                                 |
| 72          | F8                                                     |
| 73          | 8                                                      |
| 74          | i                                                      |
| 75          | k                                                      |
| 76          | m                                                      |
| 77          | R windows                                              |
| 78          | KP_0                                                   |
| 79          | KP_dot                                                 |
| 80          | unused                                                 |
| 81          | F9                                                     |
| 82          | 9                                                      |
| 83          | o                                                      |
| 84          | l                                                      |
| 85          | <                                                      |
| 86          | FN                                                     |
| 87          | backspace                                              |
| 88          | delete                                                 |
| 89          | unused                                                 |
| 90          | F10                                                    |
| 91          | 0                                                      |
| 92          | p                                                      |
| 93          | :                                                      |
| 94          | >                                                      |
| 95          | R control                                              |
| 96          | insert                                                 |
| 97          | end                                                    |
| 98          | unused                                                 |
| 99          | F11                                                    |
| 100         | -                                                      |
| 101         | {                                                      |
| 102         | "                                                      |
| 103         | ?                                                      |
| 104         | L arrow                                                |
| 105         | home                                                   |
| 106         | PG DN                                                  |
| 107         | unused                                                 |
| 108         | F12                                                    |
| 109         | +                                                      |
| 110         | }                                                      |
| 111         | unused (maybe used on ISO)                             |
| 112         | unused (maybe used on ISO)                             |
| 113         | D arrow                                                |
| 114         | SCR LK                                                 |
| 115         | PG UP                                                  |
| 116         | unused                                                 |
| 117         | PRT SCN                                                |
| 118         | unused                                                 |
| 119         | \|                                                     |
| 120         | ENTER                                                  |
| 121         | R shift                                                |
| 122         | R arrow                                                |
| 123         | Pause                                                  |
| 124         | U arrow                                                |
| 125         | unused                                                 |
| 126         | unused                                                 |

## 11.2. Mapping of side colors to leds

**Note**: This is a general representation of the layout. The LEDs opposite each
other may not be perfectly aligned, and LEDs shown in the corners may or may not
actually be located in the corner.

```text
13 14  15  7  6   5   4  3  2  1  0
16                                9
17   US international ANSI        8
18                               10
19                               11
20 21 22 23 24 25 26 27 28 29 30 12

31 44  43 42
32        41
33 Numpad 40
34        39
35 36  37 38
```

# 12. Version History

**v0.0 (2025-01-09)**: First markdown version.  
**v0.1 (2025-01-29)**: Major rewrite and added version info.  
**v0.2 (2025-01-30)**: Several cleanups; add section on keyboard initiated messages.  
**v0.2.1 (2025-01-31)**: Added a bit more on keyboard messages. Added warning.  
**v0.2.2 (2025-01-31)**: Fixed markdown lint warnings.  
**v0.3 (2025-02-08)**: Extend section for Profile handling.  
**v0.3.1 (2025-02-14)**: Added Profile Slot section.  
**v0.3.2 (2025-02-15)**: Reworded a few things.  
**v0.3.3 (2025-02-15)**: Lightning -> Lighting.  
**v0.4.0 (2025-02-16)**: Add Command Summary; also fixed some spelling issues.  
**v0.4.1 (2025-03-06)**: Add Commands for getting states of Key Game Mode and Core Indicator LEDs.  
**v0.4.2 (2025-04-13)**: Extend command description for Make Change persistent.  

