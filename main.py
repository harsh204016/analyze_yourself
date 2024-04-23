import streamlit as st
import pandas as pd
import plotly.express as pl


pd.set_option("display.precision", 2)
pd.options.display.max_rows = 500
pd.set_option("display.max.columns", None)


st.markdown("<h1 style='text-align:center; color:orange'>Analyze your Tabular Data YourSelf</h1>",unsafe_allow_html=True)
st.text("\n")

#make uploader empty after file upload
holder = st.sidebar.empty()
file = holder.file_uploader("Upload only csv file")


if file:
    # holder.empty()
    original_data = pd.read_csv(file)
    data = original_data.copy()

    is_duplicates = st.sidebar.radio("Do you want to remove duplicates ?",(True,False))
    if is_duplicates:
        data.drop_duplicates(inplace=True)
    is_null = st.sidebar.radio("Do you want to remove Null Values ?",(True,False))
    if is_null:
        data.dropna(inplace=True)

    try:
        
        cat_columns = list(data.select_dtypes(include=["object"]).columns)
        numerical_columns = list(data.select_dtypes(exclude=["object"]).columns)
        
        tab1 , tab2 , tab3  = st.tabs(["Data Head","Data Description","View Charts"])
    
        with tab1:
            data = original_data.copy()
            st.markdown('<h4 style="text-align: center; color: orange;">First 10 rows</h1>',unsafe_allow_html=True)
            st.dataframe(data.head(10))

            st.markdown('<h4 style="text-align: center; color: orange;">Last 10 rows</h1>',unsafe_allow_html=True)
            st.dataframe(data.tail(10))

        with tab2:
            data = original_data.copy()
            col1 , col2 = st.columns(2)
            with col1:
                st.markdown('<h6 style="text-align: left; color: violet;">Shape of Data</h1>',unsafe_allow_html=True)
                st.write(data.shape)
            with col2:
                st.markdown('<h6 style="text-align: left; color: violet;">Total null Values </h1>',unsafe_allow_html=True)
                st.write(data.isnull().sum().sum())

            null_data = data.isnull().sum().reset_index()
            null_data.columns = ["Columns","Null Values"]
            dtype_data = data.dtypes.reset_index()
            dtype_data.columns = ["Columns","Data type"]
            dtype = null_data.merge(dtype_data,on="Columns")
            unique_data = data.nunique().reset_index()
            unique_data.columns = ["Columns","Unique Values"]
            des_data = dtype.merge(unique_data,on="Columns")
            des_data.columns = ["         Columns","   Null Values","  Data type","   Unique Values"]
            
            st.markdown('<h4 style="text-align: center; color: orange;">Description of Dataset</h1>',unsafe_allow_html=True)
            st.table(des_data.head(des_data.shape[0]))

            
            st.markdown('<h4 style="text-align: center; color: blueviolet;">Description of Numerical Columns</h1>',unsafe_allow_html=True)
            st.table(data.describe().T)
            
            if len(cat_columns) > 0:
                st.markdown('<h4 style="text-align: center; color: darkolivegreen;">Description of Categorical Columns</h1>',unsafe_allow_html=True)
                st.table(data.describe(include="object").T)

            
        with tab3:
            try:
                col1,col2 = st.columns([1,3])
                
                with col1:
                    global image
                    st.text("\n")
                    select_cols = []
                    if len(cat_columns) > 0: 
                        select_cols.append("Categorical Columns")
                    if len(numerical_columns) > 0: 
                        select_cols.append("Numerical Columns")
                    
                    column_type = st.selectbox("Types of Columns",select_cols)

                    if column_type == "Categorical Columns":
                        chart_type = st.selectbox("Type of Plot",("Bar","Pie","Boxplot"))

                        if chart_type == "Bar":
                            st.text("\n")
                            selected_bar_columns = st.multiselect("Select Categorical Columns",cat_columns,max_selections=3)
                            # st.write(type(selected_bar_columns))
                            if len(selected_bar_columns) > 1:
                                x = selected_bar_columns[0]
                                y = selected_bar_columns[1]
                                image = pl.bar(x=x,y=y,color = y , data_frame=data)
                            else:
                                x = selected_bar_columns[0]
                                image = pl.bar(x=x,color = x , data_frame=data)
                            # st.write(type(selected_column))

                            
                            # st.plotly_chart(image)
                        
                        if chart_type == "Pie":
                            st.text("\n")
                            selected_columns = st.multiselect("Select Categorical Columns",cat_columns,max_selections=2)
                            
                            selected_column = selected_columns[0]
                            image = pl.pie(values=selected_column, data_frame=data)
                        

                        if chart_type =="Boxplot":
                            st.text("\n")
                            selected_bar_columns = st.multiselect("Select Categorical Columns",cat_columns,max_selections=2)
                            
                            selected_column = selected_bar_columns[0]
                            image = pl.box(y=selected_column,data_frame=data[selected_column].value_counts())

                    if column_type == "Numerical Columns":
                        chart_type = st.selectbox("Type of Plot",("Scatter","Line","Histogram","Boxplot"))
                        if chart_type =="Scatter":
                            st.text("\n")
                            selected_columns = st.multiselect("Select Numerical Columns",numerical_columns,max_selections=3)
                            
                            selected_first_column = selected_columns[0]
                            selected_second_column = selected_columns[1]
                            image = pl.scatter(x= selected_first_column , y=selected_second_column,data_frame=data)

                        elif chart_type =="Boxplot":
                            st.text("\n")
                            selected_bar_columns = st.multiselect("Select Numerical Columns",numerical_columns,max_selections=2)
                            
                            selected_column = selected_bar_columns[0]
                            image = pl.box(y=selected_column,data_frame=data)
                        elif chart_type == "Histogram":
                            st.text("\n")
                            selected_columns = st.multiselect("Select Numerical Columns",numerical_columns,max_selections=3)
                            
                            selected_column = selected_columns[0]
                            bins = int(st.text_input("No of bins"))
                            if bins:
                                image = pl.histogram(x=selected_column,data_frame=data,nbins=bins)

                            

                        elif chart_type == "Line":
                            st.text("\n")
                            selected_bar_columns = st.multiselect("Select Numerical Columns",numerical_columns,max_selections=3)
                            
                            selected_column = selected_bar_columns[0]
                            
                            image = pl.line(y=selected_column,data_frame=data)
                with col2:
                    st.plotly_chart(image)
            except IndexError:
                pass
            
        with tab4:
            col1 , col2 = st.columns(2)
            with col1:
                column_type = st.selectbox("Date",data.columns.to_list())
            with col2:
                column_type = st.selectbox("Value",data.columns.to_list())


    except Exception as e:
        print(e)
        st.text(e)
        


