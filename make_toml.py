import re

trace_file = "trace_trimmed.txt"
out_file = "game.toml"

all_funcs = set()

print("Читаю трассировку...")
with open(trace_file, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        for match in re.finditer(r'(?:JSR|JMP)\s+\$([0-9A-Fa-f]{4})', line):
            addr = int(match.group(1), 16)
            if addr not in (0xC500, 0xFFF0, 0xC506):
                all_funcs.add(addr)

print(f"Всего найдено уникальных адресов: {len(all_funcs)}")

with open(out_file, "w", encoding="utf-8") as f:
    f.write("[game]\n")
    f.write('name = "Capitan Tsubasa II"\n')
    f.write("mapper = 4\n\n")

    # Запихиваем ВООБЩЕ ВСЕ адреса в fixed
    f.write("[functions]\n")
    f.write("fixed = [\n")
    for addr in sorted(list(all_funcs)):
        f.write(f"  0x{addr:04X},\n")
    f.write("]\n\n")

    f.write("[entrypoints]\n")
    f.write('reset = "0xFFF0"\n')
    f.write('nmi = "0xC500"\n')
    f.write('irq = "0xC506"\n')

print(f"✅ Файл {out_file} обновлён! Все функции запихнуты в fixed.")