import csv
import json
import streamlit as st

# Cấu hình giao diện Web hiển thị tốt trên cả Máy tính & Điện thoại di động
st.set_page_config(
    page_title="JSON Converter - ALBUM+SS",
    page_icon="⚙️",
    layout="centered"
)

st.title("⚙️ Công Cụ Chuyển Đổi CSV Sang JSON")
st.write("Trích lọc cột 'ALBUM+SS' từ tệp CSV")
st.write("---")

# Sử dụng công cụ chọn tệp web của Streamlit (Thay thế cho filedialog của Tkinter)
uploaded_file = st.file_uploader("Tải file .csv từ máy tính hoặc điện thoại lên đây:", type=["csv"])

if uploaded_file is not None:
    try:
        # Đọc dữ liệu từ file được tải lên
        file_container = uploaded_file.read().decode("utf-8").splitlines()
        reader = list(csv.reader(file_container))
        
        if len(reader) > 0:
            header_row = reader[0]
            col_index = -1
            target_header = "ALBUM+SS"

            # Tìm cột có tên tiêu đề "ALBUM+SS"
            for idx, cell in enumerate(header_row):
                if cell.strip() == target_header:
                    col_index = idx
                    break

            if col_index == -1:
                col_index = 9  # Mặc định lấy cột J nếu không tìm thấy tiêu đề
                st.warning("Không tìm thấy cột 'ALBUM+SS'. Hệ thống tự động chọn cột J (Cột thứ 10).")

            # Duyệt qua các hàng để ghép nối chuỗi dữ liệu thô
            json_fragments = []
            for row in reader[1:]:
                if col_index < len(row):
                    cell_value = row[col_index].strip()
                    if cell_value:  # Bỏ qua dòng trống
                        json_fragments.append(cell_value)

            full_json_str = "\n".join(json_fragments)

            # Thử định dạng lại cấu trúc JSON
            try:
                parsed_json = json.loads(full_json_str)
                final_output = json.dumps(parsed_json, indent=4, ensure_ascii=False)
                st.success("Tải file thành công! Cú pháp JSON hoàn toàn hợp lệ.")
            except json.JSONDecodeError as e:
                st.warning(f"Dữ liệu chưa đúng chuẩn cú pháp JSON: {e}. Hệ thống vẫn cho tải xuống định dạng thô.")
                final_output = full_json_str

            st.write("### Kết quả chuyển đổi thử nghiệm:")
            # Hiển thị xem trước 500 ký tự đầu tiên
            st.code(final_output[:500] + ("\n..." if len(final_output) > 500 else ""), language="json")

            # Tạo nút tải xuống định dạng Web (Thay thế cho asksaveasfilename của Tkinter)
            st.download_button(
                label="📥 TẢI FILE .JSON VỀ MÁY",
                data=final_output,
                file_name="album_ss.json",
                mime="application/json",
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi xử lý dữ liệu: {e}")