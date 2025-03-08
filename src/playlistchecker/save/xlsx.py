import xlsxwriter
import re
import tkinter as tk
from tkinter import filedialog
from comments.languages.lang import get_message

def parse_duration(duration_str):
    m = re.match(r'(\d{2})h(\d{2})m(\d{2})s', duration_str)
    if m:
        h, m_, s = map(int, m.groups())
        return h * 3600 + m_ * 60 + s
    return None

def format_duration(total_seconds):
    h = total_seconds // 3600
    remainder = total_seconds % 3600
    m_ = remainder // 60
    s = remainder % 60
    return f"{h:02d}h{m_:02d}m{s:02d}s"

def save_to_xlsx(data, headers, default_filename, duration_list, total_duration_str, show_sum, date_info=None):
    if not isinstance(duration_list, list):
        duration_list = [duration_list]
    
    if parse_duration(total_duration_str) is None:
        total_seconds = 0
        for d in duration_list:
            secs = parse_duration(d)
            if secs is not None:
                total_seconds += secs
        total_duration_str = format_duration(total_seconds)

    root = tk.Tk()
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    filename = filedialog.asksaveasfilename(
        title=get_message("choose_location"),
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
        initialfile=default_filename
    )
    
    root.destroy()

    if not filename:
        return False
    
    try:
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        
        header_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'center', 
            'valign': 'vcenter', 'bg_color': '#D3D3D3'
        })
        
        data_format = workbook.add_format({
            'border': 1, 'align': 'center', 'valign': 'vcenter'
        })
        
        total_format = workbook.add_format({
            'border': 1, 'align': 'center', 'valign': 'vcenter',
            'bg_color': '#D3D3D3'
        })
        
        total_bold_format = workbook.add_format({
            'bold': True, 'border': 1, 'align': 'center',
            'valign': 'vcenter', 'bg_color': '#D3D3D3'
        })
        
        sum_line_format = workbook.add_format({
            'align': 'left', 'valign': 'vcenter', 'border': 0,
            'text_wrap': True
        })

        for col_idx, header in enumerate(headers):
            worksheet.write(0, col_idx, header, header_format)

        for row_idx, row in enumerate(data, start=1):
            if row_idx == len(data):
                for col_idx, value in enumerate(row):
                    fmt = total_bold_format if col_idx == 0 else total_format
                    worksheet.write(row_idx, col_idx, value, fmt)
            else:
                for col_idx, value in enumerate(row):
                    worksheet.write(row_idx, col_idx, value, data_format)

        col_widths = [len(str(header)) for header in headers]
        for row in data:
            for col_idx, cell in enumerate(row):
                col_widths[col_idx] = max(col_widths[col_idx], len(str(cell)))
                
        for col_idx, width in enumerate(col_widths):
            adjusted_width = (width + 2) * 1.2
            worksheet.set_column(col_idx, col_idx, adjusted_width)
        
        last_row = len(data) + 1
        if date_info:
            worksheet.merge_range(
                last_row, 0,
                last_row, len(headers)-1,
                date_info,
                sum_line_format
            )
            last_row += 2
        else:
            last_row += 1

        worksheet.merge_range(
            last_row, 0,
            last_row, len(headers)-1,
            get_message("markenting"),
            sum_line_format
        )

        workbook.close()
        return True
    except Exception as e:
        print(f"Error generating Excel file: {str(e)}")
        return False