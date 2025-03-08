from rich.console import Console
from rich.text import Text

# Main Banner
def show_mainbanner():
    console = Console()
    banner_str = """
__   _______  _                _                    
\ \ / /_   _|/ \   _ __   __ _| |_   _ _______ _ __ 
 \ V /  | | / _ \ | '_ \ / _` | | | | |_  / _ \ '__|
  | |   | |/ ___ \| | | | (_| | | |_| |/ /  __/ |   
  |_|   |_/_/   \_\_| |_|\__,_|_|\__, /___\___|_|   
                                 |___/ BETA v0.1.0           
    """
    banner = Text(banner_str, style="bold red")
    version = banner.plain.find("BETA v0.1.0")
    if version != -1:
        banner.stylize("bold cyan", version, version + len("BETA v0.1.0"))
    console.print(banner)

# Playlist Checker Banner
def show_playlistbanner():
    console = Console()
    banner = Text("""
 ____  _             _ _     _    ____ _               _             
|  _ \| | __ _ _   _| (_)___| |_ / ___| |__   ___  ___| | _____ _ __ 
| |_) | |/ _` | | | | | / __| __| |   | '_ \ / _ \/ __| |/ / _ \ '__|
|  __/| | (_| | |_| | | \__ \ |_| |___| | | |  __/ (__|   <  __/ |   
|_|   |_|\__,_|\__, |_|_|___/\__|\____|_| |_|\___|\___|_|\_\___|_|   
               |___/                                                     
    """, style="bold red")
    console.print(banner)