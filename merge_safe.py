import re

def load_toml_funcs(filename):
    funcs = set()
    if not __import__('os').path.exists(filename):
        return funcs
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        # Ищем все адреса внутри fixed = [ ... ]
        match = re.search(r'fixed\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if match:
            addrs = re.findall(r'0x([0-9A-Fa-f]{4})', match.group(1))
            for addr in addrs:
                funcs.add(int(addr, 16))
    return funcs

# 1. Берем рабочие 70 функций
working_funcs = load_toml_funcs("game.toml")
print(f"Загружено рабочих функций: {len(working_funcs)}")

# 2. Берем ВСЕ функции из чистого TOML
all_clean_funcs = load_toml_funcs("game_clean.toml")
print(f"Загружено функций из статики: {len(all_clean_funcs)}")

# 3. Оставляем из статики ТОЛЬКО фиксированный банк ($C000 - $FFFF)
safe_additions = set()
for addr in all_clean_funcs:
    if addr >= 0xC000:
        safe_additions.add(addr)

print(f"Безопасных функций из фиксированного банка ($C000+): {len(safe_additions)}")

# 4. Объединяем
merged_funcs = working_funcs.union(safe_additions)
print(f"ИТОГО функций в новом game_safe.toml: {len(merged_funcs)}")

# 5. Записываем
with open("game_safe.toml", "w", encoding="utf-8") as f:
    f.write("[game]\n")
    f.write('name = "Capitan Tsubasa II"\n')
    f.write("mapper = 4\n\n")
    f.write("[functions]\n")
    f.write("fixed = [\n")
    for addr in sorted(list(merged_funcs)):
        f.write(f"  0x{addr:04X},\n")
    f.write("]\n\n")
    f.write("[entrypoints]\n")
    f.write('reset = "0xFFF0"\n')
    f.write('nmi = "0xC500"\n')
    f.write('irq = "0xC506"\n')

print("✅ Файл game_safe.toml создан!")