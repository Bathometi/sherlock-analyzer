import requests
import json
from datetime import datetime
from pathlib import Path

def generate_mutations(username):
    """Генерує найпопулярніші варіації нікнейма"""
    mutations = {username}
    mutations.add(username.lower())
    mutations.add(username.upper())
    leet = username.replace('o', '0').replace('O', '0').replace('i', '1').replace('I', '1')
    mutations.add(leet)
    mutations.add(f"{username}_")
    mutations.add(f"_{username}")
    return list(mutations)

def save_report(username, stats_per_target, total_found, detailed_results):
    """Зберігає звіти в папку reports всередині проєкту sherlock-analyzer"""
    target_dir = Path("./reports")
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    base_filename = f"report_{username}_{timestamp}"
    
    txt_path = target_dir / f"{base_filename}.txt"
    json_path = target_dir / f"{base_filename}.json"

    # 1. Запис у TXT
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"============================================================\n")
        f.write(f"🔍 OSINT REPORT FOR TARGET: {username}\n")
        f.write(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"============================================================\n\n")
        
        f.write("📊 ПІДСУМКОВА СТАТИСТИКА ПО ВАРІАЦІЯХ:\n")
        for target, found_platforms in stats_per_target.items():
            count = len(found_platforms)
            platforms_str = ", ".join(found_platforms) if count > 0 else "0 знайдено"
            f.write(f"  -> {target:<12}: знайдено {count} ({platforms_str})\n")
        
        f.write(f"\n------------------------------------------------------------\n")
        f.write(f"✅ Всього знайдено підтверджених профілів: {total_found}\n\n")
        
        f.write("🔗 ДЕТАЛЬНІ ПОСИЛАННЯ:\n")
        for item in detailed_results:
            f.write(f"  [+] {item['platform']} ({item['target']}): {item['url']}\n")

    # 2. Запис у JSON
    json_data = {
        "target_username": username,
        "scan_timestamp": timestamp,
        "total_found": total_found,
        "summary_per_mutation": {k: len(v) for k, v in stats_per_target.items()},
        "found_accounts": detailed_results
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"\n📁 [ЗВІТИ ЗБЕРЕЖЕНО В ПАПКУ ПРОЄКТУ]:")
    print(f"  📄 TXT : {txt_path.resolve()}")
    print(f"  📊 JSON: {json_path.resolve()}")

def check_username(username, use_mutations=False):
    targets = generate_mutations(username) if use_mutations else [username]

    print(f"\n🔎 OSINT-пошук для цілі: {username}")
    if use_mutations:
        print(f"🌀 Активовано генерацію варіацій: {targets}")
    print("=" * 60)

    # Додано прапорець is_case_sensitive
    platforms = {
        "GitHub": {
            "url": "https://github.com/{}",
            "error_keywords": ["404 Not Found", "File Not Found"],
            "is_case_sensitive": True
        },
        "Telegram": {
            "url": "https://t.me/{}",
            "error_keywords": [],
            "is_case_sensitive": False
        },
        "YouTube": {
            "url": "https://www.youtube.com/@{}",
            "error_keywords": ["404 Not Found", "This page isn't available"],
            "is_case_sensitive": False
        },
        "Reddit": {
            "url": "https://www.reddit.com/user/{}",
            "error_keywords": ["nobody with that name", "page not found"],
            "is_case_sensitive": False
        },
        "DockerHub": {
            "url": "https://hub.docker.com/u/{}",
            "error_keywords": ["404", "Not Found"],
            "is_case_sensitive": False
        },
        "TikTok": {
            "url": "https://www.tiktok.com/@{}",
            "error_keywords": ["Couldn't find this account", "User not found"],
            "is_case_sensitive": False
        },
        "Pinterest": {
            "url": "https://www.pinterest.com/{}",
            "error_keywords": ["User not found", "Page not found"],
            "is_case_sensitive": False
        },
        "Medium": {
            "url": "https://medium.com/@{}",
            "error_keywords": ["404", "Out of print"],
            "is_case_sensitive": False
        },
        "Steam": {
            "url": "https://steamcommunity.com/id/{}",
            "error_keywords": ["The specified profile could not be found", "specified profile"],
            "is_case_sensitive": False
        },
        "Twitch": {
            "url": "https://www.twitch.tv/{}",
            "error_keywords": ["content is unavailable", "time machine"],
            "is_case_sensitive": False
        },
        "SoundCloud": {
            "url": "https://soundcloud.com/{}",
            "error_keywords": ["We can't find that user", "404 Not Found"],
            "is_case_sensitive": False
        },
        "Patreon": {
            "url": "https://www.patreon.com/{}",
            "error_keywords": ["404 Not Found"],
            "is_case_sensitive": False
        }
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    total_found_count = 0
    stats_per_target = {}
    detailed_results = []
    
    # Сет для збереження вже відправлених запитів: ("Telegram", "wenmaly")
    scanned_queries = set()

    for target in targets:
        stats_per_target[target] = []
        
        if len(targets) > 1:
            print(f"\n🎯 Скануємо варіацію: [{target}]")

        for platform, config in platforms.items():
            url = config["url"].format(target)
            error_keywords = config["error_keywords"]
            is_case_sensitive = config["is_case_sensitive"]

            # Визначаємо ключ перевірки (якщо платформа нечутлива — приводимо нік до lower)
            query_key = (platform, target if is_case_sensitive else target.lower())

            if query_key in scanned_queries:
                # Пропускаємо дублікат
                continue

            scanned_queries.add(query_key)

            try:
                response = requests.get(url, headers=headers, timeout=4, allow_redirects=True)
                
                is_found = False

                if platform == "Telegram":
                    if "extra_topic" in response.text or "tgme_page_title" in response.text:
                        is_found = True
                
                elif response.status_code == 200:
                    has_error_keyword = any(keyword.lower() in response.text.lower() for keyword in error_keywords)
                    if not has_error_keyword:
                        is_found = True

                if is_found:
                    print(f"  [+] [FOUND] {platform}: {url}")
                    stats_per_target[target].append(platform)
                    detailed_results.append({
                        "target": target,
                        "platform": platform,
                        "url": url
                    })
                    total_found_count += 1

            except requests.RequestException:
                pass

    # 📊 ПІДСУМОК У КІНЦІ ЗВІТУ
    print("\n" + "=" * 60)
    print("📊 ПІДСУМКОВА СТАТИСТИКА (З ДЕДУПЛІКАЦІЄЮ РЕГІСТРУ):")
    print("=" * 60)
    
    for target, found_platforms in stats_per_target.items():
        count = len(found_platforms)
        if count > 0:
            platforms_list = ", ".join(found_platforms)
            print(f"  -> {target:<12}: унікально знайдено {count} ({platforms_list})")
        else:
            print(f"  -> {target:<12}: 0 нових платформ")

    print("-" * 60)
    print(f"✅ Всього УНІКАЛЬНИХ підтверджених профілів: {total_found_count}")

    # 💾 АВТО-ЗБЕРЕЖЕННЯ ЗВІТУ
    save_report(username, stats_per_target, total_found_count, detailed_results)
