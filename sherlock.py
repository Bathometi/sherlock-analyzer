import argparse
import secrets_scanner
import log_analyzer
import username_scanner

def main():
    parser = argparse.ArgumentParser(description="Sherlock OSINT & Log Analyzer Tool")

    parser.add_argument("--scan-secrets", help="Шлях до файлу для пошуку витоків даних")
    parser.add_argument("--analyze-log", help="Шлях до лог-файлу для аналізу логів")
    parser.add_argument("--search-user", help="Юзернейм для пошуку акаунтів у соцмережах")
    parser.add_argument("--mutate", action="store_true", help="Автоматично генерувати варіації нікнейма")

    args = parser.parse_args()

    if args.scan_secrets:
        print("[+] Запуск сканера секретів...")
        secrets_scanner.scan_file_for_leaks(args.scan_secrets)

    elif args.analyze_log:
        print("[+] Запуск аналітика логів...")
        log_analyzer.analyze_access_log(args.analyze_log)

    elif args.search_user:
        print(f"[+] Запуск OSINT-пошуку акаунтів для: {args.search_user}")
        username_scanner.check_username(args.search_user, use_mutations=args.mutate)

    else:
        print("[-] Не вказано жодного прапорця! Використовуй --help для довідки.")

if __name__ == "__main__":
    main()
