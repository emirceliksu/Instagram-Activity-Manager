import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

class LikeManager:
    def __init__(self, client, ui, archiver):
        self.cl = client
        self.ui = ui
        self.archiver = archiver
        self.total_removed = 0

    def sweep(self, mod="beğeni"):
        console.print(Panel(f"[bold cyan]{self.ui['cleaning']} - {mod.upper()}[/bold cyan]", expand=False))
        items = []
        
        with console.status(f"[bold yellow]{self.ui['fetching']}") as status:
            try:
                if mod == "beğeni":
                    items = self.cl.liked_medias(amount=0)
                else:
                    try:
                        colls = self.cl.collections()
                        target_id = colls[0].pk if colls else "0"
                        offset = None
                        while True:
                            batch = self.cl.collection_medias(target_id, amount=200, last_media_pk=offset)
                            if not batch: break
                            items.extend(batch)
                            offset = batch[-1].pk
                            if len(batch) < 200: break
                    except:
                        items = self.cl.collection_medias("all", amount=0)
            except Exception as e:
                console.print(f"[bold red]Error: {e}[/bold red]")
                return 0

        if not items:
            console.print(f"[bold green]{self.ui['not_found']}")
            return 0

        removed_in_session = 0
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(bar_width=40, pulse_style="cyan"), TaskProgressColumn(), TextColumn("[bold magenta]{task.completed}/{task.total}"), console=console) as progress:
            task = progress.add_task(f"[green]{mod}...", total=len(items))
            for media in items:
                try:
                    if mod == "beğeni": self.cl.media_unlike(media.id)
                    else: self.cl.media_unsave(media.id)
                    
                    self.archiver(f"https://www.instagram.com/p/{media.code}/")
                    removed_in_session += 1
                    progress.advance(task)
                    time.sleep(random.uniform(0.1, 0.3))
                except:
                    pass
        return removed_in_session
