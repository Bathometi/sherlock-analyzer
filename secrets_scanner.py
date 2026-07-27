import re

PATTERNS = {
    "AWS Access Key": r"AKIA[A-Z0-9]{16}",
    "GitHub Token": r"ghp_[a-zA-Z0-9]{36}",
    "Password/Credential": r"(?i)(?:password|passwd|pwd)[=:]\S+",
    "Email Address": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "IP Address": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
}

log_file = "test_ips.txt"
report_file = "found_leaks.txt"

print(f"🔍 Скануємо файл: {log_file}\n" + "=" * 45)

try:
    with open(log_file, "r") as file:
        logs = file.read()

    # Відкриваємо файл звіту для запису ("w" - write mode)
    with open(report_file, "w", encoding="utf-8") as report:
        report.write(f"=== OSINT LEAK DETECTION REPORT ===\n")
        report.write(f"Source Log File: {log_file}\n")
        report.write("=" * 45 + "\n\n")

        for secret_type, regex in PATTERNS.items():
            matches = re.findall(regex, logs)
            if matches:
                # Вивід у консоль
                print(f"[!] [ALERT] Знайдено {secret_type} ({len(matches)} шт.):")
                
                # Запис у звітний файл
                report.write(f"[ALERT] {secret_type} ({len(matches)} matches):\n")

                for match in matches:
                    print(f"    -> {match}")
                    report.write(f"    -> {match}\n")

                print("-" * 45)
                report.write("-" * 45 + "\n")
            else:
                print(f"[-] {secret_type}: витоків не виявлено.")

    print(f"\n✅ Звіт успішно збережено у файл: {report_file}")

except FileNotFoundError:
    print(f"[X] Помилка: файл {log_file} не знайдено!")
