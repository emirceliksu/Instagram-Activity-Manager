import time
import os
import shutil
from selenium.webdriver.common.by import By
from rich.console import Console
from rich.panel import Panel

console = Console()

class CommentManager:
    def __init__(self, ui, browser_opener):
        self.ui = ui
        self.browser_opener = browser_opener

    def sweep(self):
        console.print(Panel(f"[bold cyan]{self.ui['menu_3'].upper()}[/bold cyan]", expand=False))
        driver = None
        temp_dir = None
        removed = 0
        
        try:
            driver, temp_dir = self.browser_opener()
            if not driver: return 0
            
            driver.get("https://www.instagram.com/your_activity/interactions/comments/")
            time.sleep(10)
            
            while True:
                try:
                    # Multi-language button detection
                    select_btn = driver.find_elements(By.XPATH, "//span[text()='Select' or text()='Seç' or text()='Seleccionar' or text()='Sélectionner']")
                    if not select_btn: break
                    select_btn[0].click()
                    time.sleep(2)
                    
                    items = driver.find_elements(By.XPATH, "//div[@role='button' and contains(@aria-label, 'Comment')]")
                    if not items: break
                    
                    for item in items[:25]:
                        item.click()
                        time.sleep(0.1)
                    
                    delete_btn = driver.find_elements(By.XPATH, "//div[@role='button' and (text()='Delete' or text()='Sil' or text()='Eliminar' or text()='Supprimer')]")
                    if delete_btn:
                        delete_btn[0].click()
                        time.sleep(2)
                        confirm = driver.find_elements(By.XPATH, "//button[text()='Delete' or text()='Sil' or text()='Eliminar' or text()='Supprimer']")
                        if confirm:
                            confirm[0].click()
                            time.sleep(5)
                            removed += 25
                    else:
                        break
                except:
                    break
        except Exception as e:
            console.print(f"[red]Error during comment cleanup: {e}[/red]")
        finally:
            if driver: driver.quit()
            if temp_dir and os.path.exists(temp_dir):
                try: shutil.rmtree(temp_dir)
                except: pass
        
        return removed
