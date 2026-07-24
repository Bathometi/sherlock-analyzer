import re

# 1. Словник із регулярками для різних секретів та логів
PATTERNS = {
    "AWS Access Key": r"AKIA[A-Z0-9]{16}",
    "GitHub Token": r"ghp_[a-zA-Z0-9]{36}",
    "Password/Credential": r"(?i)(?:password|passwd|pwd)[=:]\S+",
    "Email Address": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "IP Address": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
}

log_file = "test_ips.txt"

print(f"🔍 Скануємо файл: {log_file}\n" + "=" * 45)

try:
    with open(log_file, "r") as file:
        logs = file.read()

    # Пошук збігів за кожним паттерном
    for secret_type, regex in PATTERNS.items():
        matches = re.findall(regex, logs)
        if matches:
            print(f"[!] [ALERT] Знайдено {secret_type} ({len(matches)} шт.):")
            for match in matches:
                print(f"    -> {match}")
            print("-" * 45)
        else:
            print(f"[-] {secret_type}: витоків не виявлено.")

except FileNotFoundError:
    print(f"[X] Помилка: файл {log_file} не знайдено!")
