import csv
import json
from tkinter import Tk, filedialog, messagebox, Button, Label

def center_window(window, width=450, height=220):
    """Hàm tự động tính toán tọa độ để căn giữa màn hình cho mọi máy Mac/Windows"""
    # Lấy kích thước độ phân giải thực tế của màn hình thiết bị
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Tính toán tọa độ x, y để đặt cửa sổ vào chính giữa
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    # Thiết lập kích thước hệ thống hình học
    window.geometry(f"{width}x{height}+{x}+{y}")

def process_conversion(root_window):
    """Hàm xử lý đọc tệp dữ liệu CSV và xuất tệp tin JSON"""
    file_path_csv = filedialog.askopenfilename(
        title="Chọn tệp CSV nguồn của bạn",
        filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")],
        parent=root_window
    )

    if not file_path_csv:
        return

    try:
        with open(file_path_csv, mode='r', encoding='utf-8') as f:
            reader = list(csv.reader(f))

        if not reader:
            messagebox.showerror("Lỗi", "Tệp CSV được chọn không chứa dữ liệu.", parent=root_window)
            return

        header_row = reader[0]
        col_index = -1
        target_header = "ALBUM+SS"

        for idx, cell in enumerate(header_row):
            if cell.strip() == target_header:
                col_index = idx
                break

        if col_index == -1:
            col_index = 9  # Mặc định lấy cột J nếu không tìm thấy tiêu đề

        json_fragments = []
        for row in reader[1:]:
            if col_index < len(row):
                cell_value = row[col_index].strip()
                if cell_value:
                    json_fragments.append(cell_value)

        full_json_str = "\n".join(json_fragments)

        try:
            parsed_json = json.loads(full_json_str)
            final_output = json.dumps(parsed_json, indent=4, ensure_ascii=False)
        except json.JSONDecodeError:
            final_output = full_json_str

        save_path = filedialog.asksaveasfilename(
            title="Chọn nơi lưu file JSON kết quả",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All Files", "*.*")],
            initialfile="album_ss.json",
            parent=root_window
        )

        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(final_output)
            messagebox.showinfo(
                "Thành công", 
                f"Đã chuyển đổi và lưu file thành công tại:\n{save_path}", 
                parent=root_window
            )

    except Exception as e:
        messagebox.showerror("Lỗi hệ thống", f"Đã xảy ra lỗi ngoài ý muốn:\n{e}", parent=root_window)

def create_main_gui():
    root = Tk()
    root.title("Công cụ xuất dữ liệu Weboffer")
    
    # 1. Thực hiện căn giữa bảng điều khiển trên màn hình
    center_window(root, width=460, height=220)
    root.config(bg="#f5f5f7")  # Thiết kế màu nền xám nhẹ sang trọng theo phong cách macOS
    
    # 2. Tiêu đề bảng điều khiển
    title_label = Label(
        root, 
        text="BẢNG CHUYỂN ĐỔI CSV SANG JSON", 
        font=("Helvetica", 14, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f"
    )
    title_label.pack(pady=20)
    
    # 3. Phụ chú hướng dẫn
    desc_label = Label(
        root, 
        text="Trích xuất cột 'ALBUM+SS' từ tệp CSV Google Sheet", 
        font=("Helvetica", 11),
        bg="#f5f5f7",
        fg="#86868b"
    )
    desc_label.pack(pady=5)

    # 4. Nút kích hoạt tác vụ chuyển đổi
    btn_start = Button(
        root, 
        text="BẮT ĐẦU CHUYỂN ĐỔI", 
        command=lambda: process_conversion(root),
        font=("Helvetica", 12, "bold"),
        fg="white",
        bg="#0071e3",  # Màu xanh dương quy chuẩn của hệ thống Apple
        highlightbackground="#f5f5f7",
        padx=15,
        pady=8
    )
    btn_start.pack(pady=15)
    
    root.mainloop()

if __name__ == "__main__":
    create_main_gui()