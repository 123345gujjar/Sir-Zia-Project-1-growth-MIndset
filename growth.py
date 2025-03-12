import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title ="Data Sweeper" , layout='wide')

#custom css
st.markdown(
    """
     <style>
     .stApp{
        background-color: black;
        color:white;
     }
     </style>
    """,
    unsafe_allow_html=True

)

#Title and dscription

st.title("Data Sweeper Intergiling By Muhammed Shahzaib")
st.write("Transform your File Between CVS and Excel With Built-In DAta Claening And visulising Creating This Project For Quater 3!!!!")

#FILE UPLODER
uploaded_file=st.file_uploader("Upload Your File (only CVS And Excel):", type=["cvs","xlxs"],except_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext= os.path.splitext(file.name)[-1].lower()

        if file_ext==".cvs":
            df=pd.read_csv(file)

        elif file_ext=="xlsx":
            df=pd.read_excel(file)
            
        else:
            st.error(f"Unsupported File TYpe:{file_ext}")
            continue

        #File Details
        st.write("Prewie The Head of The Data frame")
        st.dataframe(df.head())

        #data claening option

        st.subheader("Data Cleaning Option")
    if st.checkbox(f"Clean Data For{file.name}"):
            col1,col2=st.columns(2)

            with col1:
               if st.button(f"Remove Duplicates From The File:{file.name}"):
                  df.drop_duplicates(inplace=True)  
                  st.write("Dupliace Remove!!")

               with col2:
                  if st.button(f"Fill Mising Value:{file.name}"):
                     numeric_cols= df.select_dtypes(includes=['number']).columns
                     df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                     st.write("Mising Value Has been Filled!!!!")


                     st.subheader("Select Column To Keep")
                     columns=st.multiselect(f"Choose Column For {file.name}",df.columns , default=df.columns)
                     df=df(columns)

                  #DATA VISULIZATION

                  st.subheader("Data Visulization")
                  st.checkbox(f"Show Visulization For{file.name}")
                  st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

                  #Conservation Option

                  st.subheader("Coservation Option")
                  conservation_type=st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
                  if st.button(f"convert{file.name}"):
                     buffer=BytesIO()
                     if conservation_type=="CVS":
                        df.to.cvs(buffer,index=False)
                        file_name=file.name.replace(file_ext,".cvs")
                        mime_type="text/cvs"

                     elif conservation_type=="Excel":
                        df.to.excel(buffer,index=False)
                        file_name=file.name.replace(file_ext,".xlsx")
                        mime_type="application/vnd.openxmlformats-officedocuments.spreadsheethtml.sheet"
                        buffer.seek(0)

                        st.download_button(
                           label=f"Download{file.name} as {conservation_type}",
                           data=buffer,
                           file_name=file_name,
                           mime=mime_type
                        )

                        st.sucess("All File Proceed Sucessfully!!!!!!!!!!!")
                      




                     



        
        
    

