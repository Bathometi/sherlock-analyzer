import requests

def check_platform(username, platform_config):
    """
    Універсальний детектор, який повертає структурований доказ (Evidence).
    """
    url = platform_config["url_template"].format(username)
    timeout = platform_config.get("timeout", 10)
    detector = platform_config["detector"]
    det_type = detector["type"]
    target_value = detector["value"]

    # Шаблони заголовків, щоб сайти не сприймали нас за "голого" бота
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        status_code = response.status_code
        html_text = response.text

        # --- СТРАТЕГІЯ 1: Перевірка за HTTP Status Code ---
        if det_type == "status_code":
            if status_code == 200:
                return {"status": "FOUND", "url": url, "code": status_code, "reason": "HTTP 200 OK"}
            elif status_code == target_value: # наприклад 404
                return {"status": "NOT_FOUND", "url": url, "code": status_code, "reason": f"HTTP {status_code}"}
            elif status_code == 429:
                return {"status": "RATE_LIMITED", "url": url, "code": status_code, "reason": "Rate limited (429)"}
            elif status_code in [403, 401]:
                return {"status": "BLOCKED", "url": url, "code": status_code, "reason": "Access forbidden/blocked"}
            else:
                return {"status": "UNKNOWN", "url": url, "code": status_code, "reason": f"Unexpected status code {status_code}"}

        # --- СТРАТЕГІЯ 2: Пошук ТЕКСТУ ВІДСУТНОСТІ (text_absence) ---
        elif det_type == "text_absence":
            if status_code == 200:
                if target_value in html_text:
                    # Текст присутності акаунта ЗНАЙДЕНО в HTML
                    return {"status": "FOUND", "url": url, "code": status_code, "reason": "Presence text matched"}
                else:
                    return {"status": "NOT_FOUND", "url": url, "code": status_code, "reason": "Absence text missing"}
            else:
                return {"status": "UNKNOWN", "url": url, "code": status_code, "reason": f"HTTP {status_code}"}

        # --- СТРАТЕГІЯ 3: Пошук ТЕКСТУ ПОМИЛКИ (text_presence) ---
        elif det_type == "text_presence":
            if status_code == 200:
                if target_value in html_text:
                    # Текст помилки ЗНАЙДЕНО -> акаунту НЕМАЄ
                    return {"status": "NOT_FOUND", "url": url, "code": status_code, "reason": "Error keyword found in HTML"}
                else:
                    return {"status": "FOUND", "url": url, "code": status_code, "reason": "No error keyword in HTML"}
            else:
                return {"status": "UNKNOWN", "url": url, "code": status_code, "reason": f"HTTP {status_code}"}

    except requests.exceptions.Timeout:
        return {"status": "TIMEOUT", "url": url, "code": None, "reason": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"status": "ERROR", "url": url, "code": None, "reason": str(e)}
