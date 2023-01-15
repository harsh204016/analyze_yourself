import streamlit as st
import pandas as pd
import plotly.express as pl



st.markdown("<h1 style='text-align:center'>Data Ananlysis</h1>",unsafe_allow_html=True)
# st.title("Data Ananlysis")

#make uploader empty after file upload
holder = st.empty()
file = holder.file_uploader("")
if file:
    # holder.empty()


    try:
        data = pd.read_csv(file)

        cat_columns = list(data.select_dtypes(include=["object"]).columns)
        numerical_columns = list(data.select_dtypes(include=["int","float"]).columns)
        # print(cat_columns,numerical_columns)
        tab1 , tab2 , tab3 , tab4 = st.tabs(["View Data","View Charts","A","B"])
        with tab1:
            st.text(data.head(5).T)
        with tab2:
            column_type = st.selectbox("",("Categorical Columns","Numerical Columns"))
            if column_type == "Categorical Columns":
                chart_type = st.selectbox("",("Bar","Boxplot"))
                if chart_type == "Bar":
                    selected_bar_columns = st.multiselect("categorical Columns",cat_columns,max_selections=1)
                    st.image(pl.bar(x=selected_bar_columns[0],data_frame=data))
                selected_cat_columns = st.multiselect("categorical Columns",cat_columns,max_selections=3)
                
            elif column_type == "Numerical Columns":

                selected_numerical_columns = st.multiselect("numerical columns",numerical_columns,max_selections=2)
        
        st.image()

    except Exception as e:
        st.text("Please upload correct csv file.")


