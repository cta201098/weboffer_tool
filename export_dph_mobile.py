import csv
import json
import streamlit as st

# Configure web interface to display well on both Desktop & Mobile devices
st.set_page_config(
    page_title="JSON Converter - ALBUM",
    page_icon="⚙️",
    layout="centered"
)

st.title("⚙️ JSON Converter - ALBUM")

# Add Test mode checkbox
test_mode = st.checkbox("Test mode", help="When enabled, will search for 'STG ALBUM' header instead of 'PROD ALBUM' and use column 11 as default")

if test_mode:
    st.write("Read colum with header 'STG ALBUM' from CSV (Test Mode)")
else:
    st.write("Read colum with header 'PROD ALBUM' from CSV")
st.write("---")

# Use Streamlit's web file picker (Replace Tkinter's filedialog)
uploaded_file = st.file_uploader("Import .csv file here:", type=["csv"])

if uploaded_file is not None:
    try:
        # Read data from uploaded file
        file_container = uploaded_file.read().decode("utf-8").splitlines()
        reader = list(csv.reader(file_container))
        
        if len(reader) > 0:
            header_row = reader[0]
            col_index = -1
            
            # Set target_header and default col_index based on test_mode
            if test_mode:
                target_header = "STG ALBUM"
                default_col_index = 11  # Column L (12th column, 0-indexed = 11)
            else:
                target_header = "PROD ALBUM"
                default_col_index = 9   # Column J (10th column, 0-indexed = 9)

            # Find column with target header name
            for idx, cell in enumerate(header_row):
                if cell.strip() == target_header:
                    col_index = idx
                    break

            if col_index == -1:
                col_index = default_col_index
                if test_mode:
                    st.warning(f"Column '{target_header}' not found. System automatically selects column L (Column 12).")
                    # Validate data in column 11 before proceeding
                    if len(reader) > 1 and len(reader[1]) > col_index:
                        sample_data = reader[1][col_index].strip()
                        if not sample_data:
                            st.warning("Column L appears to be empty. Please check the data.")
                        else:
                            st.info(f"Using data from column L. Sample data: {sample_data[:50]}...")
                    else:
                        st.error("Cannot access column L or insufficient data.")
                else:
                    st.warning(f"Column '{target_header}' not found. System automatically selects column J (Column 10).")

            json_fragments = []
            for row in reader[1:]:
                if col_index < len(row):
                    cell_value = row[col_index].strip()
                    if cell_value:  # skip empty cells
                        json_fragments.append(cell_value)

            full_json_str = "\n".join(json_fragments)

            # Parse the JSON to check if it's valid and pretty-print it
            try:
                parsed_json = json.loads(full_json_str)
                final_output = json.dumps(parsed_json, indent=4, ensure_ascii=False)
                st.success("Import file successfully!")
            except json.JSONDecodeError as e:
                st.warning(f"The data seems wrong: {e}. But still allow to download raw data.")
                final_output = full_json_str

            st.write("### The preview result:")
            # Display preview of first 500 characters
            st.code(final_output[:500] + ("\n..." if len(final_output) > 500 else ""), language="json")

            # Create web download button (Replace Tkinter's asksaveasfilename)
            st.download_button(
                label="📥 DOWNLOAD .JSON",
                data=final_output,
                file_name="dph.json",
                mime="application/json",
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Some error occurred when handling the data: {e}")
