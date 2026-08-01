# 📊 Baseline Metrics & Acceptance Criteria (v1.0-baseline)

**Дата фіксації:** 2026-08-01  
**Версія:** `v1.0-baseline`  
**Кількість платформ у базі:** 12  
**Паралельні потоки (Threads):** 10  

---

## 🧪 Результати контрольних тестів (Current Flaws & Behavior):

### 1. Known-Positive Test (`CONTROLLED_TEST_ACCOUNT` + `--mutate`):
* **Згенеровано запитів:** 38 унікальних комбінацій
* **Знайдено підтверджених профілів:** 7 – 10 (показано деваріацію результатів)
* **Час виконання:** 4.14s – 8.55s
* **Потенційні причини нестабільності:** Timeouts, rate-limits, blocked responses або динамічна зміна поведінки платформ під час паралельних запитів.

### 2. Known-Negative Test (`xqzt9999_not_exist_test_123` + `--mutate`):
* **Згенеровано запитів:** 49
* **Raw False-Positive Matches:** 12
* **Unique Affected Platforms:** 3 (Reddit, TikTok, Twitch)
* **Технічна причина:** Платформи повертають `fallback / dynamic HTML with HTTP 200` (боти отримують сторінку авторизації або генеративний інтерфейс, де відсутні поточні `error_keywords`).

---

## 🎯 Acceptance Criteria для наступних Спринтів:

1. **False Positives Control:** Звести кількість false-positives до **0** для синтетичних/неіснуючих акаунтів без втрати `known-positive` результатів.
2. **Explicit Error States:** Впровадити обробку та відображення розширених статусів відповіді замість бінарного FOUND/NOT_FOUND:
   - `FOUND`
   - `NOT_FOUND`
   - `UNKNOWN`
   - `BLOCKED`
   - `RATE_LIMITED`
   - `TIMEOUT`
   - `ERROR`
3. **Architecture Decoupling:** Винести конфігурацію платформ та правила детекції у зовнішній `platforms.json`.
