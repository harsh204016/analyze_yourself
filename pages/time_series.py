import streamlit as st



file = st.sidebar.file_uploader()
if file:
    st.dataframe(file)


st.write("coming soon")


