import json
import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def check_account(username, platform_config):
    url = platform_config["url_template"].format(username)
    detector = platform_config["detector"]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        status_code = response.status_code
        text = response.text

        if detector["type"] == "status_code":
            if status_code == 200:
                return "FOUND", url
            elif status_code == detector["value"]:
                return "NOT_FOUND", url
        
        elif detector["type"] == "text_presence":
            if status_code == 200 and detector["value"] in text:
                return "FOUND", url
            else:
                return "NOT_FOUND", url

        elif detector["type"] == "text_absence":
            if status_code == 200 and detector["value"] not in text:
                return "FOUND", url
            else:
                return "NOT_FOUND", url

        return "UNKNOWN", url
    except Exception:
        return "ERROR", url

def main():
    console.print("\n[bold cyan]🔎 OSINT ANALYZER CLI ENGINE v2.0[/bold cyan]\n", style="bold underline")
    
    # Введення таргета прямо в терміналі!
    username = Prompt.ask("[bold yellow]Введіть нікнейм для пошуку[/bold yellow]")

    with open("platforms.json", "r") as f:
        platforms = json.load(f)

    # Створюємо гарну таблицю
    table = Table(title=f"Результати для: [bold magenta]{username}[/bold magenta]")
    table.add_column("Платформа", style="bold white")
    table.add_column("Статус", justify="center")
    table.add_column("Клікабельне Посилання", style="blue underline")

    with console.status("[bold green]Скануємо мережі...") as status:
        for p_id, config in platforms.items():
            result, url = check_account(username, config)
            
            if result == "FOUND":
                status_str = "[bold green]✅ ЗНАЙДЕНО[/bold green]"
            elif result == "NOT_FOUND":
                status_str = "[bold red]❌ НЕ ЗНАЙДЕНО[/bold red]"
            else:
                status_str = f"[bold yellow]⚠️ {result}[/bold yellow]"

            # Клікабельне посилання в терміналі
            link = f"[link={url}]{url}[/link]"
            table.add_row(config["name"], status_str, link)

    console.print(table)

if __name__ == "__main__":
    main()
