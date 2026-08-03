import json

def load_platforms(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"[+] Успішно завантажено {len(data)} платформ з бази!")
            
            # Виведемо інформацію для перевірки
            for platform_id, config in data.items():
                print(f"  -> {config['name']}: {config['url_template']}")
                print(f"     Детектор: {config['detector']['type']} | Case Sensitive: {config['case_sensitive']}\n")
                
            return data
    except Exception as e:
        print(f"[-] Помилка читання JSON: {e}")

if __name__ == "__main__":
    load_platforms('platforms.json')
