import argparse
import secrets_scanner  # Імпортуємо наш готовий модуль!

def main():
    parser = argparse.ArgumentParser(description="Sherlock OSINT & Log Analyzer Tool")

    parser.add_argument("--scan-secrets", help="Шлях до файлу для пошуку витоків даних")
    parser.add_argument("--analyze-log", help="Шлях до лог-файлу для аналізу логів")

    args = parser.parse_args()

    if args.scan_secrets:
        print(f"[+] Запуск сканера секретів для файлу: {args.scan_secrets}\n")
        # Викликаємо функцію з нашого secrets_scanner.py і передаємо їй файл!
        secrets_scanner.scan_file_for_leaks(args.scan_secrets)

    elif args.analyze_log:
        print(f"[+] Запуск аналізу логів для файлу: {args.analyze_log}")

    else:
        print("[-] Не вказано жодного прапорця! Використовуй --help для довідки.")

if __name__ == "__main__":
    main()
