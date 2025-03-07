import streamlit as st
import pandas as pd
import os
from io import BytesIO  # ✅ Import BytesIO

# Set up the app
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("🚀Data Sweeper")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning visualization. 📊✨")

# File uploader
uploaded_files = st.file_uploader("Upload Your File (CSV OR EXCEL):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue  

        # Display file information
        st.write(f"📂 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")

        # Show 5 rows of the DataFrame
        st.write("🔍 **Preview of Data**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"🧹 Data Cleaning Options for {file.name}")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("🔍 **Remove Duplicates**")
                if st.button(f"Remove Duplicates ({file.name})"):
                    df = df.drop_duplicates()
                    st.success("✅ Duplicates Removed!")
                    st.dataframe(df.head())

            with col2:
                st.write("📊 **Fill Missing Values**")
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean(axis=0))
                    st.success("✅ Missing Values have been Filled!")
                    st.dataframe(df.head())

        # Choose Specific Columns to Keep
        st.subheader("📝 Select Columns to Keep")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion Options
        st.subheader("♻️ Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_Type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="xlsxwriter")  # ✅ Fixed `index=False`
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_Type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # ✅ Fixed MIME type formatting

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_Type
            )

st.success("✅ All Files Processed!")
