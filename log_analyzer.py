import re
from collections import Counter

def analyze_access_log(filename):
    print(f"\n📊 Аналізуємо лог-файл: {filename}")
    print("=" * 50)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        ip_list = []
        suspicious_requests = []

        # Регулярка для витягування IP, URL та статус-коду
        log_pattern = r'(\d+\.\d+\.\d+\.\d+).*?"[A-Z]+\s+(\S+)\s+HTTP/.*?"\s+(\d+)'

        for line in lines:
            match = re.search(log_pattern, line)
            if match:
                ip, url, status = match.groups()
                ip_list.append(ip)

                # Фіксуємо підозрілу активність (спроби залізти в адмінку або помилки)
                if "admin" in url or "config" in url or status in ["401", "403", "404"]:
                    suspicious_requests.append((ip, url, status))

        # Підраховуємо топ-IP за кількістю запитів
        ip_counts = Counter(ip_list)

        print("📈 ТОП IP-адрес за кількістю запитів:")
        for ip, count in ip_counts.most_common():
            print(f"   -> {ip}: {count} запитів")

        print("-" * 50)

        if suspicious_requests:
            print("🚨 [ALERT] Виявлено підозрілі запити / спроби сканування:")
            for ip, url, status in suspicious_requests:
                print(f"   [!] IP {ip} намагався відкрити '{url}' (Статус: {status})")
        else:
            print("✅ Підозрілих запитів не виявлено.")

        print("=" * 50)

    except FileNotFoundError:
        print(f"[-] Помилка: Лог-файл '{filename}' не знайдено!")
