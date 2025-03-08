import tkinter as tk
from tkinter import filedialog
from comments.languages.lang import get_message

def save_to_txt(table_str, duration_list, total_duration_str, show_sum, default_filename=None, date_info=None):
    root = tk.Tk()
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    filename = filedialog.asksaveasfilename(
        title=get_message("choose_location"),
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        initialfile=default_filename if default_filename else ""
    )
    
    root.destroy()

    if not filename:
        return False
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(table_str)
            if date_info:
                f.write("\n" + date_info + "\n")
            f.write("\n" + get_message("markenting") + "\n")
        return True
    except Exception as e:
        return False