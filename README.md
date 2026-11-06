# Captain Tsubasa Vol. II: Super Striker — NES Static Recompilation

A **static recompilation** of the Famicom/NES game *Captain Tsubasa Vol. II: Super Striker* (Tecmo, 1990) into portable C code, buildable as a native Windows/Linux executable.

Unlike an emulator that interprets 6502 instructions on the fly, this project **translates the game's assembly into native C** at build time. This allows the game to be patched, translated, and modified like any modern software — while the original game runs at full speed with cycle-accurate hardware emulation.

## ✨ Features

- **Native C code** for the game's logic (~74% of CPU cycles)
- **Cycle-accurate hardware** emulation (PPU, APU, MMC3 mapper)
- **SDL2 frontend** with window, audio, keyboard & gamepad input
- **One-command pipeline** — from ROM & trace to `.exe`
- **Extension-ready** — perfect for ROM hacking and localization

## 🚀 Quick Start

You will need your own copy of the ROM. We do **not** distribute the ROM or the recompiled C code (that would be copyright infringement).

### Prerequisites

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| [NESRecomp](https://github.com/mstan/nesrecomp/releases) | latest | Static recompiler |
| [FCEUX](https://fceux.com/) | 2.6+ | Emulator with trace logger |
| [Visual Studio 2022](https://visualstudio.microsoft.com/) | 17.14+ | C compiler (Windows) |
| [CMake](https://cmake.org/) | 3.20+ | Build system |
| [SDL2-devel-VC](https://github.com/libsdl-org/SDL/releases) | 2.30+ | Window/audio |

### Step 1 — Get the ROM

Obtain `Captain Tsubasa Vol. II - Super Striker (J) [!].nes` (Mapper 4 / MMC3).

### Step 2 — Record a trace in FCEUX

1. Open the ROM in **FCEUX**.
2. Go to `Debug → Trace Logger → Log to File` and save as `trace.txt`.
3. Play for ~60 seconds (menus, match, movement) to capture the game's code paths.
4. Stop. The file will be large (~2 GB is normal).

### Step 3 — Configure paths (Important!)

Open `recomp_config.json` and **change the paths to match your system**. You need to specify where you extracted NESRecomp and SDL2:

```json
{
  "rom_file": "cb2.nes",
  "trace_file": "trace.txt",
  "work_dir": "D:/Captain Tsubasa II",
  "nesrecomp_dir": "D:/NESRecomp",
  "sdl2_dir": "D:/SDL2"
}
```

*(Note: You do not need to edit `CMakeLists.txt`. The pipeline script generates it automatically based on the paths you provide here).*

### Step 4 — Run the pipeline

Open a terminal in the project folder and run:

```bash
python recomp_pipeline.py --config recomp_config.json
```

The script will do the following:

1. Copy the required `framework` and `common` files from NESRecomp.
2. Trim `trace.txt` to 2M lines (saves RAM).
3. Extract all `JSR`/`JMP` targets and generate `game.toml`.
4. Run NESRecomp to translate 6502 assembly into C.
5. Generate `CMakeLists.txt` and `game.c`, then compile the `.exe`.

### Step 5 — Play

Copy the `.exe` and `SDL2.dll` from `build/Release/` anywhere, put your `cb2.nes` next to it, and run:

```bash
cb2.exe cb2.nes
```

## 🎮 Default Controls

| NES | Keyboard | Gamepad |
| :--- | :--- | :--- |
| D-Pad | Arrow keys | D-Pad |
| A | `Z` | A |
| B | `X` | X |
| Start | `Enter` | Start |
| Select | `\` | Back |
| Menu | `Esc` | RB |
| Fast-forward | `Tab` | RT |
| Fullscreen | `F11` | — |
| Screenshot | `F12` | — |

Full rebinding is available via `config.ini` next to the `.exe`.

## ⚖️ Legal

This project contains **no copyrighted game data**. It is a set of tools and configuration files that allow a user who owns the original ROM to recompile it locally. The generated C code is considered a derivative work and is **not** distributed.

The original game *Captain Tsubasa Vol. II: Super Striker* is © 1990 Tecmo. This project is not affiliated with or endorsed by Tecmo or Nintendo.

## 🙏 Credits

- **[mstan](https://github.com/mstan/nesrecomp)** — NESRecomp, without which this would be impossible.
- **FCEUX team** — the emulator used for trace generation.
- **Rido911** — for invaluable brainstorming, testing, and helping crack the hardest parts.

---

## 🇷🇺 Русская версия

Этот проект — статическая рекомпиляция игры *Captain Tsubasa II* с NES в portable C-код. В отличие от эмулятора, игра компилируется в **нативный код**, который можно патчить и переводить как обычное ПО.

**Установка:**

1. Скачайте NESRecomp, SDL2, Visual Studio 2022 и CMake.
2. Запишите `trace.txt` в эмуляторе FCEUX, поиграв пару минут.
3. **Обязательно откройте `recomp_config.json` и пропишите свои пути к NESRecomp и SDL2.**
4. Запустите `python recomp_pipeline.py --config recomp_config.json`. *(Скрипт сам сгенерирует `CMakeLists.txt` с правильными путями).*

**Проект не содержит ROM-файла или скомпилированного C-кода** — только инструменты и конфиги. Пользователь сам скармливает свой ром.
