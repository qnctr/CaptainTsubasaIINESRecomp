# Captain Tsubasa II — NES Static Recompilation

Static recompilation of the Japanese NES game **Captain Tsubasa II: Super Striker** into native C code, using [NESRecomp](https://github.com/mstan/nesrecomp).

**This is NOT an emulator.** The game is translated once into C, compiled with your system's compiler, and runs natively on your CPU.

> 🚧 **Current status:** Playable. The game boots, plays audio, renders graphics and dialogues. ~479 functions are natively recompiled (about 74% of CPU cycles). Some code from MMC3 switchable banks still falls back to the interpreter. See [Known Issues](#known-issues).

## ✨ Features

- **Native execution** — no 6502 interpreter on the hot path.
- **SDL2 frontend** — fullscreen, scale, save states, screenshots, traces.
- **Reproducible pipeline** — one script and one config file to rebuild everything.
- **Open tooling** — you bring your own ROM, you get your own build.

### Screenshots

<img width="770" height="752" alt="image" src="https://github.com/user-attachments/assets/d5f75d67-c341-44c5-a958-87642dbe0af7" />
<img width="770" height="752" alt="image" src="https://github.com/user-attachments/assets/9220d7d5-743d-41fd-8aa3-e39a6353cdbf" />
<img width="770" height="752" alt="image" src="https://github.com/user-attachments/assets/2bc04fd1-6898-450c-9172-ce26fc449fee" />

## 📜 Legal

- This repository contains **only tooling and configuration**. It does **not** contain the original ROM, the recompiled C sources, or the compiled binary.
- You must provide your own legally obtained copy of the ROM.
- NESRecomp and its runtime are the work of [mstan](https://github.com/mstan/nesrecomp) and are distributed under their own license.
- All game assets and code belong to **Tecmo / Koei Tecmo**.

## ⚙️ Requirements

| Component | Version | Notes |
|---|---|---|
| Python | 3.10+ | For the pipeline and helper scripts |
| CMake | 3.20+ | `winget install Kitware.CMake` |
| MSVC Build Tools | 2022 | `winget install Microsoft.VisualStudio.2022.BuildTools` |
| SDL2 (VC) | 2.30+ | Extract to `D:/SDL2` |
| NESRecomp CLI | latest | Download the release ZIP, extract `nesrecomp.exe` into `./nesrecomp/` |
| NESRecomp runtime | same version | Copy `framework/` and `common/` into the project root |
| FCEUX | latest | Only needed for generating trace logs |

## 🚀 Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/qnctr/CaptainTsubasaIINESRecomp
   cd CaptainTsubasaIINESRecomp
   ```

2. **Place your ROM** — put `cb2.nes` in the project root. (Not redistributed here.)

3. **Install dependencies** (once):
   ```powershell
   winget install Kitware.CMake
   winget install Microsoft.VisualStudio.2022.BuildTools
   ```

4. **Configure the pipeline** — edit `recomp_config.json`:
   ```json
   {
     "rom_path": "cb2.nes",
     "trace_file": "trace_trimmed.txt",
     "nesrecomp_path": "nesrecomp/nesrecomp.exe",
     "sdl2_dir": "D:/SDL2"
   }
   ```

5. **Generate the game config** (base pass, ~70 functions from the trace):
   ```bash
   python make_toml.py
   ```

6. **Optional: broaden coverage** (stable build, ~479 functions):
   ```bash
   python merge_safe.py
   ```

7. **Recompile and build** — run the full pipeline:
   ```bash
   python recomp_pipeline.py
   ```

8. **Run the game**:
   ```bash
   cd build/Release
   cb2_cyc.exe cb2.nes
   ```

## 🎮 Controls

| Action | Key |
|---|---|
| D-Pad | Arrows |
| A | Z |
| B | X |
| Start | Enter |
| Select | Right Shift |
| Fullscreen | F11 |
| Quit | Esc |

## 🧠 How it works

1. **Trace:** Run the game in FCEUX with the Trace Logger on. This records every executed instruction.

2. **Config:** `make_toml.py` extracts every `JSR`/`JMP` target from the trace → `game.toml`. `merge_safe.py` adds safe `$C000+` addresses found by static scan → `game_safe.toml`.

3. **Recompile:** NESRecomp translates each labeled instruction into a C function, preserving cycle accuracy.

4. **Build:** CMake links the generated C with the NESRecomp SDL2 runtime into `cb2_cyc.exe`.

## ⚠️ Known Issues

- **Coverage is not 100%.** Code in MMC3 switchable banks (`$8000–$BFFF`) that wasn't executed during the FCEUX trace falls back to the interpreter. This can cause slowdowns or crashes in later scenes.
- **No audio debugging yet.** Some tracks play at the wrong pitch or tempo on certain systems.
- **Save states** work, but cross-version compatibility is not guaranteed.
- **Static analysis path (`game_clean.toml`) is broken.** Do not use it — it contains false positives from ROM graphics/text and will hang the game on boot.

## 🐛 Found a bug? Want to help?

If the game freezes, crashes, or slows down, it means the game entered a piece of code that wasn't captured in our trace logs.

The best way to help is to **record a trace that reaches the bug**. 

You don't need to know C or assembly. Just play the game in FCEUX, record a log, and attach it to a new Issue. A detailed step-by-step guide (how to record, how to trim the file, and what to attach) is in our **[CONTRIBUTING.md](./CONTRIBUTING.md)**.

## 💡 Other ways to support the project

- **Star this repository** ⭐ — it helps other NES fans find the project.
- **Share it** — post it on Reddit (r/emulation, r/romhacking) or Twitter.
- **Test on different hardware** — let us know if it runs well on your PC, or if you find glitches.
- **Improve the tooling** — if you know Python or CMake, look at the "open for PRs" list in [CONTRIBUTING.md](./CONTRIBUTING.md).

## 🙏 Credits

- [mstan/nesrecomp](https://github.com/mstan/nesrecomp) — the recompiler and runtime.
- [FCEUX](https://fceux.com) — trace capture.
- [Rido911](https://github.com/Rido911) — inspiration and early NESRecomp experiments.
- **Tecmo / Koei Tecmo** — original game.

---

## 🇷🇺 Русская версия

Проект занимается **статической рекомпиляцией** японской NES-игры *Captain Tsubasa II: Super Striker* в нативный C-код с помощью NESRecomp. Это **не эмулятор**.

### Что работает сейчас

- Игра запускается, играет музыка, рисует графику и диалоги.
- Около **479 функций** скомпилированы нативно (~74% циклов CPU).
- Часть кода из переключаемых банков MMC3 (`$8000–$BFFF`) всё ещё уходит в интерпретатор — возможны просадки FPS и вылеты в поздних сценах (см. *Known Issues*).

### Быстрый старт

1. Клонируй репозиторий.
2. Положи свой `cb2.nes` в корень (ROM **не** распространяется).
3. Установи зависимости: CMake, MSVC Build Tools, SDL2 (распакуй в `D:/SDL2`).
4. Скачай исходники NESRecomp и скопируй `framework/` и `common/` в корень проекта.
5. Поправь `recomp_config.json` (пути к ROM, трассировке, `nesrecomp.exe`, SDL2).
6. Запусти `python make_toml.py`, затем `python merge_safe.py` (опционально, но даёт более стабильный билд на 479 функций).
7. Запусти `python recomp_pipeline.py` — он всё пересоберёт.
8. Играй: `build/Release/cb2_cyc.exe cb2.nes`.

### Как помочь

Самый полезный вклад — **прислать трассировку из FCEUX**, которая доходит до бага, и открыть Issue с её описанием. Подробная инструкция — в [CONTRIBUTING.md](./CONTRIBUTING.md).

### Юридическое

В репозитории **нет** ROM, скомпилированного C-кода и `.exe`. Всё это пользователь собирает сам из своей копии игры. Права на игру принадлежат **Tecmo / Koei Tecmo**, права на NESRecomp — его автору **mstan**.
