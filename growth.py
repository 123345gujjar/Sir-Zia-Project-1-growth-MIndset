import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
     <style>
     .stApp{
        background-color: black;
        color: white;
     }
     </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper Integrated By Muhammed Shahzaib")
st.write("Transform your File Between CSV and Excel With Built-In Data Cleaning And Visualization. Created for Quarter 3!!!!")

# File uploader
uploaded_files = st.file_uploader("Upload Your File (only CSV and Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Processing uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # File type handling
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File Type: {file_ext}")
            continue

        # File Details
        st.write("Preview of the DataFrame:")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from the File: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values: {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Have Been Filled!")

            # Column selection after cleaning
            st.subheader("Select Columns to Keep")
            columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Data Visualization
            st.subheader("Data Visualization")
            show_viz = st.checkbox(f"Show Visualization for {file.name}")
            numeric_df = df.select_dtypes(include='number')
            if show_viz:
                if numeric_df.shape[1] >= 2:
                    st.bar_chart(numeric_df.iloc[:, :2])
                else:
                    st.warning("There are fewer than two numeric columns to plot.")

            # Conversion options
            st.subheader("Conversion Options")
            conservation_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conservation_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conservation_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)

                # Provide download button
                st.download_button(
                    label=f"Download {file.name} as {conservation_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

                st.success("File Processing Completed Successfully!")

