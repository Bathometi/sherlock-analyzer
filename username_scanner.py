import requests

def generate_mutations(username):
    """Генерує найпопулярніші варіації нікнейма (leetspeak, підкреслення, регістр)"""
    mutations = {username}  # set виключає дублікати
    
    # 1. Різні регістри
    mutations.add(username.lower())
    mutations.add(username.upper())
    
    # 2. Популярні leetspeak-заміни (o -> 0, i -> 1, e -> 3, a -> 4)
    leet = username.replace('o', '0').replace('O', '0')
    leet = leet.replace('i', '1').replace('I', '1')
    mutations.add(leet)

    # 3. Варіації з підкресленням на початку/в кінці
    mutations.add(f"{username}_")
    mutations.add(f"_{username}")

    return list(mutations)

def check_username(username, use_mutations=False):
    targets = generate_mutations(username) if use_mutations else [username]

    print(f"\n🔎 OSINT-пошук для цілі: {username}")
    if use_mutations:
        print(f"🌀 Активовано генерацію варіацій: {targets}")
    print("=" * 60)

    platforms = {
        "GitHub": "https://github.com/{}",
        "Telegram": "https://t.me/{}",
        "YouTube": "https://www.youtube.com/@{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "DockerHub": "https://hub.docker.com/u/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Medium": "https://medium.com/@{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "Twitch": "https://www.twitch.tv/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "Patreon": "https://www.patreon.com/{}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    found_accounts = []

    for target in targets:
        if len(targets) > 1:
            print(f"\n🎯 Скануємо варіацію: [{target}]")

        for platform, url_pattern in platforms.items():
            url = url_pattern.format(target)
            try:
                response = requests.get(url, headers=headers, timeout=4, allow_redirects=True)
                
                if platform == "Telegram":
                    if "extra_topic" in response.text or "tgme_page_title" in response.text:
                        print(f"  [+] [FOUND] {platform}: {url}")
                        found_accounts.append(f"{platform} ({target}): {url}")
                elif response.status_code == 200:
                    print(f"  [+] [FOUND] {platform}: {url}")
                    found_accounts.append(f"{platform} ({target}): {url}")

            except requests.RequestException:
                pass  # Пропускаємо помилки з'єднання для швидкості

    print("=" * 60)
    print(f"✅ Всього знайдено підтверджених профілів: {len(found_accounts)}\n")
