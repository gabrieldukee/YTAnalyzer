import sys
import os
import subprocess
import importlib.util
import re
from comments.languages.lang import get_message, set_language
import comments.languages.lang as lang

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def install_dependencies_from_requirements():
    try:
        dependency_msg = get_message("dependencies")
    except Exception:
        dependency_msg = "dependencies"
    
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        packages = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pkg = (line.split("==")[0]
                       .split(">=")[0]
                       .split("<=")[0]
                       .split(">")[0]
                       .split("<")[0].strip())
            packages.append(pkg)
    except FileNotFoundError:
        packages = []
    
    mapping = {}
    for pkg in packages:
        if pkg.lower() == "google-api-python-client":
            mapping[pkg] = "googleapiclient"
        elif pkg.lower() == "xlsxwriter":
            mapping[pkg] = "xlsxwriter"
        else:
            mapping[pkg] = pkg

    missing_packages = []
    for pkg in packages:
        mod_name = mapping.get(pkg, pkg)
        if importlib.util.find_spec(mod_name) is None:
            missing_packages.append(pkg)
    
    if not missing_packages:
        return
    
    total = len(missing_packages)
    count = 0
    for pkg in missing_packages:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        count += 1
        progress = int((count / total) * 100)
        clear_screen()
        print(f"{dependency_msg} [{progress}%]")
    clear_screen()

install_dependencies_from_requirements()

from rich.console import Console
from rich.text import Text 
from banner.banners import show_mainbanner

console = Console()

def select_language():
    clear_screen()
    show_mainbanner()
    console.print("[1] English", style="bold green")
    console.print("[2] Português (Brasil)", style="bold green")
    console.print("\n" + get_message("exit"), style="bold red")
    while True:
        choice = console.input("\n[bold white]" + get_message("choose_option") + "[/bold white]").upper()
        if choice == '1':
            set_language("1")
            console.print("\n" + get_message("language_set_en"), style="bold green")
            break
        elif choice == '2':
            set_language("2")
            console.print("\n" + get_message("language_set_pt"), style="bold green")
            break
        elif choice == 'X':
            console.print("\n" + get_message("exiting"), style="bold green")
            sys.exit()
        else:
            console.print("\n" + get_message("invalid_option"), style="yellow")
    input("\n" + get_message("press_enter_to_continue"))

def show_help():
    while True:
        clear_screen()
        show_mainbanner()
        
        if lang.LANGUAGE == "1":
            help_filepath = os.path.join("comments", "languages", "help", "en-help.txt")
        else:
            help_filepath = os.path.join("comments", "languages", "help", "pt-help.txt")
        
        try:
            with open(help_filepath, "r", encoding="utf-8") as file:
                help_content = file.read()
            
            formatted_text = Text()
            current_position = 0
            
            pattern = r'(\*{1,3})(.*?)(\*{1,3})(?![*])'
            
            for match in re.finditer(pattern, help_content, flags=re.DOTALL):
                start, end = match.start(), match.end()
                asterisks_open = match.group(1)
                content = match.group(2)
                asterisks_close = match.group(3)
                
                if current_position < start:
                    normal_text = help_content[current_position:start]
                    formatted_text.append(normal_text, style="white")
                
                if len(asterisks_open) == 1 and len(asterisks_close) == 1:
                    style = "bold white"
                elif len(asterisks_open) == 2 and len(asterisks_close) == 2:
                    style = "bold cyan"
                elif len(asterisks_open) == 3 and len(asterisks_close) == 3:
                    style = "bold yellow"
                else:
                    style = "white"
                
                formatted_text.append(content, style=style)
                current_position = end
            
            remaining_text = help_content[current_position:]
            if remaining_text:
                formatted_text.append(remaining_text, style="white")
            
            console.print(formatted_text, markup=False)
        except FileNotFoundError:
            console.print(get_message("help_not_found"), style="red")
        
        options_line = f"[bold green]{get_message('languages')}[/] [white]|[/] [bold red]{get_message('exit')}[/]"
        console.print(options_line)
        
        choice = console.input("\n[bold white]" + get_message("choose_option") + "[/bold white]").upper()
        if choice == 'X':
            console.print("\n" + get_message("exiting"), style="bold green")
            sys.exit()
        elif choice == 'L':
            select_language()
        else:
            console.print("\n" + get_message("invalid_option"), style="yellow")
            input("\n" + get_message("press_enter_to_continue"))

def run_playlist_checker(args):
    main_path = os.path.join("src", "playlistchecker", "main.py")
    if not os.path.isfile(main_path):
        console.print(f"File not found: {main_path}", style="red")
        sys.exit(1)
    subprocess.run([sys.executable, main_path] + args)

if __name__ == "__main__":
    if '-playlist' in sys.argv[1:]:
        playlist_args = [arg for arg in sys.argv[1:] if arg != '-playlist']
        run_playlist_checker(playlist_args)
    else:
        show_help()