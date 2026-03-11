from deep_translator import GoogleTranslator
from rich.console import Console
from rich.table import Table

console = Console()

BASE_STRINGS = {
    "title": "Instagram Activity Master PRO",
    "dev": "Muhammed Emir Çeliksu",
    "detect": "Scanning browsers on your system...",
    "browser_table": "Compatible Platforms",
    "select_browser": "Select browser to fetch session",
    "shadow_mode": "Generating Shadow Profile...",
    "session_fetch": "Fetching session... Please wait.",
    "cleaning": "CLEANING OPERATION",
    "fetching": "Fetching items...",
    "not_found": "Your account is already clean!",
    "found": "items ready to be swept.",
    "done": "OPERATION COMPLETED!",
    "count": "Cleaned Items",
    "time": "Duration",
    "menu_1": "Sweep Likes",
    "menu_2": "Sweep Saved",
    "menu_3": "Sweep Comments (Browser Required)",
    "menu_4": "Full Cleaning (Delete All)",
    "menu_0": "Safe Exit",
    "comment_scanning": "Scanning comments, please wait...",
}

class LanguageManager:
    def __init__(self):
        self.lang_code = "en"
        self.ui = BASE_STRINGS.copy()

    def set_language(self):
        table = Table(title="Select Language", border_style="cyan")
        table.add_column("Code", style="bold yellow")
        table.add_column("Language")
        langs = [("en", "English"), ("tr", "Türkçe"), ("es", "Español"), ("fr", "Français"), ("de", "Deutsch"), ("ru", "Pусский"), ("ar", "العربية"), ("zh-CN", "中文")]
        for c, n in langs: table.add_row(c, n)
        console.print(table)
        
        selected = console.input("[bold magenta]Enter language code (default 'en'): [/bold magenta]") or "en"
        self.lang_code = selected
        
        if self.lang_code != "en":
            with console.status(f"[bold yellow]Translating UI to {self.lang_code}..."):
                try:
                    translator = GoogleTranslator(source='en', target=self.lang_code)
                    for key, val in BASE_STRINGS.items():
                        if key not in ["dev", "title"]:
                            trans = translator.translate(val)
                            if trans: self.ui[key] = trans
                except:
                    console.print("[red]Translation service limited, using English.[/red]")
        return self.ui
