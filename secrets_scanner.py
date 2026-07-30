import re

def scan_file_for_leaks(filename):
    print(f"🔍 Скануємо файл: {filename}")
    print("=" * 45)

    # 1. Словник регулярних виразів
    patterns = {
        "AWS Access Key": r"AKIA[0-9A-Z]{16}",
        "GitHub Token": r"ghp_[a-zA-Z0-9]{36}",
        "Password/Credential": r"password\s*=\s*[^\s]+",
        "Email Address": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "IP Address": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    }

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        report_lines = []
        for leak_type, pattern in patterns.items():
            matches = list(set(re.findall(pattern, content)))
            if matches:
                header = f"[!] [ALERT] Знайдено {leak_type} ({len(matches)} шт.):"
                print(header)
                report_lines.append(header)
                for match in matches:
                    line = f"    -> {match}"
                    print(line)
                    report_lines.append(line)
                print("-" * 45)
                report_lines.append("-" * 45)

        # Збереження результатів у файл
        with open("found_leaks.txt", "w", encoding="utf-8") as out_file:
            out_file.write(f"--- ЗВІТ СКАНУВАННЯ: {filename} ---\n\n")
            out_file.write("\n".join(report_lines))

        print("\n✅ Звіт успішно збережено у файл: found_leaks.txt")

    except FileNotFoundError:
        print(f"[-] Помилка: Файл '{filename}' не знайдено!")
