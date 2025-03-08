import os
import sys
import re
import requests
import pytz
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import isodate
from tabulate import tabulate
from rich.console import Console
from rich.text import Text
from googleapiclient.discovery import build
from save import txt, xlsx
from banner.banners import show_playlistbanner
from comments.languages.lang import get_message

console = Console()

SHOW_D = False
SHOW_V = False    
SHOW_L = False    
SHOW_C = False    
SHOW_DATE = False

config_file = "config.txt"
api_key = ""

if os.path.exists(config_file):
    with open(config_file, "r") as f:
        for line in f:
            if line.startswith("YT_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
                break

if not api_key:
    console.print("\n" + get_message("insert_api_key"), style="red")
    exit()

def check_api():
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(part="id", id="dQw4w9WgXcQ")
        request.execute()
    except Exception as e:
        error_message = str(e)
        if "quotaExceeded" in error_message:
            console.print("\n" + get_message("exceeded_quota"), style="yellow")
        elif "API key not valid" in error_message:
            console.print("\n" + get_message("invalid_api"), style="red")
        elif "API key expired" in error_message:
            console.print("\n" + get_message("api_deactivated"), style="red")
        elif "The project tied to this API key has been deleted" in error_message:
            console.print("\n" + get_message("api_deleted"), style="red")
        exit()

check_api()

def get_timezone():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('timezone', 'UTC')
        return 'UTC'
    except Exception as e:
        console.print(f"[!] {get_message('error_timezone')}: {str(e)}", style="red")
        return 'UTC'

def extract_playlist_id(user_input):
    if 'list=' in user_input:
        parts = user_input.split('list=')[1].split('&')[0]
        match = re.search(r'(PL[\w-]{32})', parts)
        if match:
            return match.group(0)
    
    match = re.search(r'(PL[\w-]{32})', user_input)
    return match.group(0) if match else user_input

def check_playlist(playlist_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    try:
        playlist_request = youtube.playlists().list(
            part="snippet",
            id=playlist_id
        )
        playlist_response = playlist_request.execute()
        if not playlist_response.get("items"):
            return (False, "\n" + get_message("playlist_not_exist"), "yellow")
        item = playlist_response["items"][0]
        if "status" in item and item["status"]["privacyStatus"] == "private":
            return (False, "\n" + get_message("playlist_private"), "yellow")
    except Exception as e:
        error_message = str(e)
        if "playlistNotFound" in error_message:
            return (False, "\n" + get_message("playlist_not_exist"), "yellow")
        elif "private" in error_message:
            return (False, "\n" + get_message("playlist_private"), "yellow")
        else:
            return (False, get_message("unknown_error", error_message=error_message), "red")
    return (True, None, None)

def get_number(message, minimum=1):
    while True:
        entry = input(message)
        try:
            number = int(entry)
            if number >= minimum:
                return number
            else:
                console.print(get_message("number_greater", minimum=minimum), style="yellow")
        except ValueError:
            console.print(get_message("only_numbers"), style="yellow")

def get_video_duration(playlist_id, start=1, end=5000):
    youtube = build("youtube", "v3", developerKey=api_key)
    videos = []
    next_page_token = None

    total_duration = 0
    duration_sum = []

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        if "items" not in response or not response["items"]:
            console.print("\n" + get_message("playlist_not_exist"), style="yellow")
            return

        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]
            videos.append((video_id, title))

        next_page_token = response.get("nextPageToken")
        if not next_page_token or len(videos) >= end:
            break

    videos = videos[start - 1:end]

    total_views = 0
    total_likes = 0
    total_comments = 0

    os.system("cls" if os.name == "nt" else "clear")
    
    total_videos = len(videos)
    video_data = []
    for count, (video_id, title) in enumerate(videos, start=1):
        progress = int((count / total_videos) * 100)
        progress_message = f"{get_message('creating_table')} [{progress}%]"
        console.print(progress_message, style="bold green", end="\r")
        
        parts = "contentDetails"
        if SHOW_V or SHOW_L or SHOW_C:
            parts += ",statistics"
        video_request = youtube.videos().list(
            part=parts,
            id=video_id
        )
        video_response = video_request.execute()
        if not video_response["items"]:
            continue
        item = video_response["items"][0]
        
        if SHOW_D:
            duration = item["contentDetails"]["duration"]
            duration_seconds = int(isodate.parse_duration(duration).total_seconds())
            hours, remainder = divmod(duration_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{hours:02d}h{minutes:02d}m{seconds:02d}s"
            total_duration += duration_seconds
            duration_sum.append(formatted_duration)
            row = [start + count - 1, formatted_duration, title]
        else:
            row = [start + count - 1, title]
        
        if SHOW_V or SHOW_L or SHOW_C:
            stats = item.get("statistics", {})
            views = int(stats.get("viewCount", "0"))
            likes = int(stats.get("likeCount", "0"))
            comments = int(stats.get("commentCount", "0"))
            total_views += views
            total_likes += likes
            total_comments += comments

            if SHOW_V:
                row.append(f"{views:,}".replace(",", "."))
            if SHOW_L:
                row.append(f"{likes:,}".replace(",", "."))
            if SHOW_C:
                row.append(f"{comments:,}".replace(",", "."))
        video_data.append(row)
    
    console.print(" " * 80, end="\r")
    
    if SHOW_D:
        header = [get_message("table_no"), get_message("table_duration"), get_message("table_title")]
    else:
        header = [get_message("table_no"), get_message("table_title")]
    if SHOW_V:
        header.append(get_message("table_views"))
    if SHOW_L:
        header.append(get_message("table_likes"))
    if SHOW_C:
        header.append(get_message("table_comments"))
    colalign = ["center"] * len(header)

    if SHOW_D:
        total_hours, remainder = divmod(total_duration, 3600)
        total_minutes, total_seconds = divmod(remainder, 60)
        formatted_total_duration = f"{total_hours:02d}h{total_minutes:02d}m{total_seconds:02d}s"
        total_row = [get_message("table_total"), formatted_total_duration, "--------------------"]
    else:
        total_row = [get_message("table_total"), "--------------------"]
    if SHOW_V:
        total_row.append(f"{total_views:,}".replace(",", "."))
    if SHOW_L:
        total_row.append(f"{total_likes:,}".replace(",", "."))
    if SHOW_C:
        total_row.append(f"{total_comments:,}".replace(",", "."))
    video_data.append(total_row)

    table = tabulate(
        video_data, 
        headers=header, 
        tablefmt="grid",
        colalign=colalign,
        stralign="center",
        disable_numparse=True
    )

    os.system("cls" if os.name == "nt" else "clear")
    console.print(table, style="bold white")
    
    if SHOW_DATE:
        try:
            timezone_str = get_timezone()
            tz = pytz.timezone(timezone_str)
            current_time = datetime.now(tz)
            formatted_date = current_time.strftime("%d-%m-%Y - %H:%M:%S")
            date_info = get_message("result_date", date=formatted_date, timezone=timezone_str)
            console.print(f"\n{date_info}", style="bold white")
        except Exception as e:
            console.print(f"\n[!] {get_message('error_date')}: {str(e)}", style="red")
    else:
        date_info = None

    while True:
        print()
        option_line = Text()
        option_line.append(get_message("save_as_xlsx"), style="bold green")
        option_line.append(" | ", style="white")
        option_line.append(get_message("save_as_txt"), style="bold green")
        option_line.append(" | ", style="white")
        option_line.append(get_message("exit"), style="bold red")
        console.print(option_line)
        option = console.input("\n[bold white]" + get_message("choose_option") + "[/bold white]").upper()

        if option == "1":
            while True:
                while True:
                    filename = console.input("\n[bold white]" + get_message("choose_file_name") + "[/bold white]").strip()
                    if not filename:
                        console.print("\n" + get_message("file_name_empty"), style="yellow")
                        continue
                    root, ext = os.path.splitext(filename)
                    if ext:
                        if ext.lower() != ".xlsx":
                            console.print("\n" + get_message("only_allowed", ext=".xlsx"), style="yellow")
                            continue
                    else:
                        filename += ".xlsx"
                    break

                if SHOW_D:
                    ds = duration_sum
                    ftd = formatted_total_duration
                    show_d_flag = True
                else:
                    ds = []
                    ftd = ""
                    show_d_flag = False

                success = xlsx.save_to_xlsx(video_data, header, filename, ds, ftd, show_d_flag, date_info)
                if success:
                    console.print("\n" + get_message("file_saved_success", filename=filename), style="bold green")
                    break
                else:
                    console.print("\n" + get_message("failed_save", type="XLSX"), style="red")

        elif option == "2":
            while True:
                while True:
                    filename = console.input("\n[bold white]" + get_message("choose_file_name") + "[/bold white]").strip()
                    if not filename:
                        console.print("\n" + get_message("file_name_empty"), style="yellow")
                        continue
                    root, ext = os.path.splitext(filename)
                    if ext:
                        if ext.lower() != ".txt":
                            console.print("\n" + get_message("only_allowed", ext=".txt"), style="yellow")
                            continue
                    else:
                        filename += ".txt"
                    break
                if SHOW_D:
                    ds = duration_sum
                    ftd = formatted_total_duration
                    show_d_flag = True
                else:
                    ds = []
                    ftd = ""
                    show_d_flag = False

                success = txt.save_to_txt(table, ds, ftd, show_d_flag, filename, date_info)
                if success:
                    console.print("\n" + get_message("file_saved_success", filename=filename), style="bold green")
                    break
                else:
                    console.print("\n" + get_message("failed_save", type="TXT"), style="red")

        elif option == "X":
            console.print("\n" + get_message("exiting"), style="bold green")
            sys.exit()

        else:
            console.print("\n" + get_message("invalid_option"), style="yellow")

def auto_mode(selected_mode, start_val=None, end_val=None):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        show_playlistbanner()
        if selected_mode == 1:
            console.print(get_message("mode_all"), style="cyan bold")
            console.print("\n" + get_message("exit"), style="bold red")
        elif selected_mode == 2:
            if start_val is not None and end_val is not None:
                console.print(get_message("mode_custom", start=start_val, end=end_val), style="cyan bold")
            else:
                console.print("Modo: Análise personalizável da playlist.", style="cyan bold")
            console.print("\n" + get_message("exit"), style="bold red")
            
        raw_input = console.input("\n[bold white]" + get_message("enter_playlist") + "[/bold white]").strip()
        user_input = raw_input.upper()
        
        if user_input == "X":
            console.print("\n" + get_message("exiting"), style="bold green")
            sys.exit()
            
        playlist_id = extract_playlist_id(raw_input)
        valid, err, style = check_playlist(playlist_id)
        if valid:
            break
        else:
            console.print(f"{err}\n", style=style)
            input(get_message("try_again"))

    if selected_mode == 1:
        get_video_duration(playlist_id)
    elif selected_mode == 2:
        if start_val is None or end_val is None:
            while True:
                start = get_number(get_message("start_video"))
                end = get_number(get_message("end_video"))
                if end >= start:
                    break
                else:
                    console.print("\n" + get_message("end_greater_than_start"), style="yellow")
        else:
            start = abs(start_val)
            end = abs(end_val)
            if start < 1:
                console.print(get_message("number_greater", minimum=1), style="yellow")
                sys.exit()
            if end < start:
                console.print("\n" + get_message("end_greater_than_start"), style="yellow")
                sys.exit()
        
        if start_val is None or end_val is None:
            console.print(get_message("mode_custom", start=start, end=end), style="cyan bold")
            
        get_video_duration(playlist_id, start, end)

if __name__ == "__main__":
    args = sys.argv[1:]
    valid_flags = {'-d', '-v', '-l', '-c', '-date'}

    SHOW_D = '-d' in args
    SHOW_V = '-v' in args
    SHOW_L = '-l' in args
    SHOW_C = '-c' in args
    SHOW_DATE = '-date' in args
    
    invalid_args = []
    numeric_args = []
    for arg in args:
        if arg in valid_flags:
            continue
        if arg.isdigit():
            num = int(arg)
            if num < 1:
                invalid_args.append(arg)
            else:
                numeric_args.append(num)
        else:
            invalid_args.append(arg)

    if invalid_args:
        console.print("\n" + get_message("invalid_entries", entries=', '.join(invalid_args)), style="yellow")
        sys.exit(1)

    if len(numeric_args) not in (0, 2):
        console.print("\n" + get_message("invalid_number_count"), style="yellow")
        sys.exit(1)

    if len(numeric_args) == 2:
        start_val, end_val = numeric_args
        if end_val < start_val:
            console.print("\n" + get_message("end_greater_than_start"), style="yellow")
            sys.exit(1)
        auto_mode(2, start_val, end_val)
    else:
        auto_mode(1)