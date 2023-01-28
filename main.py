import streamlit as st
import pandas as pd
import plotly.express as pl
from IPython.display import display



pd.set_option("display.precision", 2)
pd.options.display.max_rows = 500
pd.set_option("display.max.columns", None)


st.markdown("<h1 style='text-align:center'>Data Ananlysis</h1>",unsafe_allow_html=True)
# st.title("Data Ananlysis")

#make uploader empty after file upload
holder = st.empty()
file = holder.file_uploader("")
if file:
    holder.empty()


    try:
        original_data = pd.read_csv(file)

        data = original_data.copy()
        cat_columns = list(data.select_dtypes(include=["object"]).columns)
        numerical_columns = list(data.select_dtypes(include=["int","float"]).columns)
        tab1 , tab2 , tab3 , tab4 = st.tabs(["View Data","View Charts","Describe Data","C"])
    


        with tab1:
            st.header("View Data")
            data = original_data.copy()
            # st.text(data.style)
            st.dataframe(data)
            # st.text(data.head(3).T)
        with tab2:
            try:
                col1,col2 = st.columns([1,3])
                

                with col1:
                    column_type = st.selectbox("Types of Columns",("Categorical Columns","Numerical Columns"))
                    if column_type == "Categorical Columns":
                        chart_type = st.selectbox("",("Bar","Boxplot"))
                        if chart_type == "Bar":
                            selected_bar_columns = st.multiselect("categorical Columns",cat_columns,max_selections=2)
                            
                            selected_column = selected_bar_columns[0]
                            image = pl.bar(y=selected_column,data_frame=data[selected_column].value_counts())
                        elif chart_type =="Boxplot":
                            selected_bar_columns = st.multiselect("categorical Columns",cat_columns,max_selections=2)
                            
                            selected_column = selected_bar_columns[0]
                            image = pl.box(y=selected_column,data_frame=data[selected_column].value_counts())

                    elif column_type == "Numerical Columns":
                        # selected_numerical_columns = st.multiselect("numerical columns",numerical_columns,max_selections=2)
                        chart_type = st.selectbox("",("Line","Boxplot"))
                        if chart_type =="Boxplot":
                            selected_bar_columns = st.multiselect("numerical Columns",numerical_columns,max_selections=2)
                            
                            selected_column = selected_bar_columns[0]
                            image = pl.box(y=selected_column,data_frame=data[selected_column].value_counts())
                with col2:
                    st.plotly_chart(image)
            except IndexError:
                pass

            
        with tab3:
            
            data = original_data.copy()
            null_data = data.isnull().sum().reset_index()
            null_data.columns = ["Columns","Null Values"]
            dtype_data = data.dtypes.reset_index()
            dtype_data.columns = ["Columns","Data type"]
            dtype = null_data.merge(dtype_data,on="Columns")
            unique_data = data.nunique().reset_index()
            unique_data.columns = ["Columns","Unique Values"]
            des_data = dtype.merge(unique_data,on="Columns")
            # des_data.columns = ["         Columns","   Null Values","  Data type","   Unique Values"]
            st.text("Description of Dataset")
            st.table(des_data.head(des_data.shape[0]))

            st.text("Description of Numerical Columns")    
            st.table(data.describe().T)
            st.text("Description of Object Columns")
            st.table(data.describe(include="object").T)
        
        

    except Exception as e:
        print(e)
        st.text(e)
        st.text("Please upload correct csv file.")


