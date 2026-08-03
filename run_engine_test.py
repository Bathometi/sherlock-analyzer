import json
from detector import check_platform

# Завантажуємо бази
with open('platforms.json', 'r', encoding='utf-8') as f:
    platforms = json.load(f)

test_targets = ["WenMaly", "xqzt9999_not_exist_test_123"]

for target in test_targets:
    print(f"\n==================================================")
    print(f"🔎 ТЕСТУВАННЯ ДЕТЕКТОРА ДЛЯ ЦІЛІ: {target}")
    print(f"==================================================")
    
    for platform_id, config in platforms.items():
        result = check_platform(target, config)
        
        # Відображення результату з колірними акцентами або статусами
        status = result["status"]
        if status == "FOUND":
            icon = "✅ [FOUND]"
        elif status == "NOT_FOUND":
            icon = "❌ [NOT_FOUND]"
        else:
            icon = f"⚠️ [{status}]"
            
        print(f"{icon:<15} {config['name']:<10} -> {result['reason']} (Code: {result['code']})")
