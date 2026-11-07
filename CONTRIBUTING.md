# Contributing to Captain Tsubasa II — NES Static Recompilation

Thanks for wanting to help! This project is a **static recompilation**, which means the C code is generated **ahead of time** from a recorded play session (a "trace"). Anything the player never did during that session has no compiled code — and that's where bugs come from.

The single most useful contribution is **a trace that reaches the bug you hit**. Below is the exact procedure.

## 🐛 Why bugs happen (30-second explanation)

When NESRecomp compiles the game, it only translates addresses that are in `game_safe.toml`. If the game jumps to an address that isn't there, the runtime falls back to the slow interpreter. You'll see one of:

1. **Freeze** — picture stops, but audio continues.
2. **Slowdown** — FPS drops for a moment and recovers.
3. **Crash** — the window closes.

Each of these is a missing address. A trace that reaches the bug tells us which one.

## 📋 Before you report

1. Reproduce the bug **at least twice** on the current `main` build.
2. Note **exactly** what you did — which menu, which match, which button.
3. If you can, grab a **screenshot** of the failure.

## 🎥 Recording a trace with FCEUX

You only need to record **30–60 seconds around the bug**, not a full playthrough.

1. Open the **original ROM** (`cb2.nes`) in **FCEUX**.
2. Top menu → **`Debug`** → **`Trace Logger`**.
3. Tick **`Log to File`** and pick a path, e.g. `trace_bug.txt`.
4. Press **`Start`**.
5. Play the game and do **exactly** what triggered the bug. Add **~15 seconds of context before** and **after** the failure.
6. Press **`Stop`** in the Trace Logger window.

You will end up with a very large file (often hundreds of MB). That's normal — we shrink it next.

## ✂️ Trimming the trace

The pipeline only needs about **2,000,000 lines** to reconstruct missing functions. Raw traces can be tens of gigabytes.

If you have Python available:
```bash
python trim_trace.py trace_bug.txt
```

If not, use PowerShell:
```powershell
Get-Content trace_bug.txt -TotalCount 2000000 | Set-Content trace_bug_trimmed.txt
```

## 📤 Submitting

1. Open a **New Issue** on GitHub.
2. Title: short and specific (e.g., `Crash after 3rd match kickoff`).
3. Description must include:
   - **Steps to reproduce** (numbered).
   - **What you expected** vs **what happened**.
   - The **trimmed trace** attached by drag-and-drop into the Issue editor.

Zip the trace if it's over 20 MB — GitHub allows up to 100 MB per file.

## 🧪 What NOT to submit

- **No ROMs.** Copyright.
- **No compiled `.exe`, `.dll`, `.lib`.** Copyright.
- **No `generated/*.c` files.** Copyright.
- **No full un-trimmed traces.** 2 GB files time out the upload.

## 🛠️ Contributing to the tooling itself

If you want to improve the pipeline, `CMakeLists.txt`, or the Python scripts:

1. Fork the repo.
2. Create a branch: `git checkout -b fix/my-idea`.
3. Test locally with your own ROM.
4. Open a Pull Request with a short description of *why* the change is useful and *what* you tested.

**Ideas we'd love help with:**
- Auto-detection of `framework/` and `common/` paths from `recomp_config.json`.
- A `setup.ps1` that downloads NESRecomp and SDL2 automatically.
- A trace merger — combining traces from several playthroughs into one big `game.toml`.
- Detection of missing addresses from `--capture-log` output, appended to `game_safe.toml`.
- Runtime fixes in `framework/` (SDL2 vsync, audio buffer size, gamepad mapping).

## ❤️ Thank you

Every crash report with a trace brings the build closer to a full native recompile. You don't need to know C or assembly — just record a log and describe what happened.

---

# 🇷🇺 Участие в разработке Captain Tsubasa II — NES Static Recompilation

Спасибо, что хотите помочь! Этот проект — **статическая рекомпиляция**. Это значит, что C-код генерируется **заранее** на основе записанной игровой сессии («трассировки»). Всё, что игрок не сделал во время этой сессии, не имеет скомпилированного кода — именно отсюда берутся баги.

Самый полезный вклад — это **трассировка, которая доходит до момента бага**. Ниже описана точная процедура.

## 🐛 Почему появляются баги (объяснение на 30 секунд)

Когда NESRecomp компилирует игру, он переводит только те адреса, которые есть в `game_safe.toml`. Если игра переходит по адресу, которого там нет, рантайм переключается на медленный интерпретатор. Вы увидите одно из следующего:

1. **Зависание** — картинка останавливается, но звук продолжается.
2. **Просадка FPS** — кадры падают на пару секунд, затем восстанавливаются.
3. **Краш** — окно игры закрывается.

Каждый из этих случаев — это отсутствующий адрес. Трассировка, дошедшая до бага, покажет нам, какой именно.

## 📋 Перед тем как сообщить о баге

1. Воспроизведите баг **как минимум дважды** на текущей сборке `main`.
2. Запишите **точно**, что вы делали — какое меню, какой матч, какая кнопка.
3. Если можете, сделайте **скриншот** ошибки.

## 🎥 Запись трассировки в FCEUX

Вам нужно записать всего **30–60 секунд вокруг бага**, а не прохождение целиком.

1. Откройте **оригинальный ROM** (`cb2.nes`) в **FCEUX**.
2. Верхнее меню → **`Debug`** → **`Trace Logger`**.
3. Поставьте галочку **`Log to File`** и выберите путь, например `trace_bug.txt`.
4. Нажмите **`Start`**.
5. Играйте и сделайте **ровно то**, что вызвало баг. Добавьте **~15 секунд контекста до** и **после** ошибки.
6. Нажмите **`Stop`** в окне Trace Logger.

У вас получится очень большой файл (часто сотни мегабайт). Это нормально — сейчас мы его уменьшим.

## ✂️ Обрезка трассировки

Пайплайну нужно всего около **2 000 000 строк**, чтобы восстановить недостающие функции. Сырые логи могут весить десятки гигабайт.

Если у вас есть Python:
```bash
python trim_trace.py trace_bug.txt
```

Если нет, используйте PowerShell:
```powershell
Get-Content trace_bug.txt -TotalCount 2000000 | Set-Content trace_bug_trimmed.txt
```

## 📤 Отправка

1. Откройте **New Issue** на GitHub.
2. Заголовок: короткий и конкретный (например, `Crash after 3rd match kickoff`).
3. В описании обязательно укажите:
   - **Шаги для воспроизведения** (по пунктам).
   - **Что вы ожидали** vs **что произошло**.
   - **Обрезанную трассировку**, прикрепленную перетаскиванием в редактор Issue.

Заархивируйте трассировку в ZIP, если она весит больше 20 МБ — GitHub принимает файлы до 100 МБ.

## 🧪 Что НЕ нужно отправлять

- **Никаких ROM-файлов.** Авторские права.
- **Никаких скомпилированных `.exe`, `.dll`, `.lib`.** Авторские права.
- **Никаких файлов `generated/*.c`.** Авторские права.
- **Никаких полных необрезанных трассировок.** Файлы на 2 ГБ не загрузятся и их невозможно проверить.

## 🛠️ Помощь с инструментами

Если вы хотите улучшить пайплайн, `CMakeLists.txt` или Python-скрипты:

1. Сделайте форк репозитория.
2. Создайте ветку: `git checkout -b fix/my-idea`.
3. Проверьте локально со своим ROM.
4. Откройте Pull Request с коротким описанием, *почему* это изменение полезно и *что* вы проверили.

**Идеи, которым мы будем рады:**
- Автоопределение путей `framework/` и `common/` из `recomp_config.json`.
- Скрипт `setup.ps1`, который сам скачивает NESRecomp и SDL2.
- Объединитель трассировок — склеивание логов из нескольких прохождений в один большой `game.toml`.
- Детектор отсутствующих адресов из вывода `--capture-log`, с добавлением их в `game_safe.toml`.
- Фиксы рантайма в `framework/` (SDL2 vsync, размер аудиобуфера, маппинг геймпада).

## ❤️ Спасибо

Каждый отчет о краше с трассировкой приближает сборку к полной нативной рекомпиляции. Вам не нужно знать C или ассемблер — просто запишите лог и опишите, что произошло.
