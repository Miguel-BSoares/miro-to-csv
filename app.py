import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Miro CSV to Excel Converter", layout="centered")

st.title("Miro CSV → Excel Converter")
st.write("Upload a Miro-exported CSV file and download it as a clean Excel (.xlsx) table.")

uploaded_file = st.file_uploader("Upload Miro CSV", type=["csv"])

# Optional: paste CSV content manually
csv_text = st.text_area("Or paste CSV content here", placeholder="col1,col2,col3
A,B,C") 

if uploaded_file or csv_text.strip():
    try:
                if uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_csv(BytesIO(csv_text.encode()), sep=",")
        st.subheader("Preview")
        st.dataframe(df, use_container_width=True)

        # Convert to Excel in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='MiroData')

        st.download_button(
            label="Download Excel File",
            data=output.getvalue(),
            file_name="miro_converted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
