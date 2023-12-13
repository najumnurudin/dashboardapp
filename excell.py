import streamlit as st
import mysql.connector
import random
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import calendar
from datetime import datetime
import os
import warnings
years = [datetime.today().year, datetime.today().year + 1]
months = list[calendar.month_name]
st.set_page_config(layout="wide", page_icon=':pen', page_title="I'M TIRED")
#ine the configuration settings for your MySQL database
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="test"
)
mycursor=mydb.cursor()
warnings.filterwarnings('ignore')
st.title(" :bar_chart: I'm tired of excell in streamlit")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
fl = st.file_uploader(":file_folder: UPload a file")
if fl is not None:
    filename = fl.name
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    os.chdir(r"C:\Users\DELL\Desktop\qwertyu")
    df = pd.read_csv("My_excell.csv", encoding="ISO-8859-1" )
    
    
col1, col2 = st.columns((2))
df['DATE'] = pd.to_datetime(df["DATE"])

startDate = pd.to_datetime(df["DATE"]).min()
endtDate = pd.to_datetime(df["DATE"]).max()



with col1:
    date1 = pd.to_datetime(st.date_input("Start date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End date", endtDate))
    
df = df[(df["DATE"] >= date1) & (df["DATE"] <= date2)].copy()


region = st.sidebar.multiselect("Choose the Region", df['REGION'].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df['REGION'].isin(region)]
 
state = st.sidebar.multiselect("Choose the State",df2["STATE"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['STATE'].isin(state)] 
    
city = st.sidebar.multiselect("Choose the City",df3["CITY"].unique())
if not region and not state and not city:
    filtered_data = df
    
elif not state and not city:
    filtered_data = df[df['REGION'].isin(region)]
    
elif not region and not city:
    filtered_data = df[df["STATE"].isin(state)]
    
    
elif state and city:
    filtered_data = df[df['STATE'].isin(state) & df['CITY'].isin(city)]
        
elif region and city:
    filtered_data = df[df['REGION'].isin(region) & df['CITY'].isin(city)]

    
elif region and state:
    filtered_data = df[df['REGION'].isin(region) & df['STATE'].isin(state )]
        
elif city:
    filtered_data = df3[df3['CITY'].isin(city)]
    
else:
    filtered_data = df3[df3['REGION'].isin(region) & df3['STATE'].isin(state) & df3['CITY'].isin(city)]



category_df = filtered_data.groupby(by = ['REGION'], as_index = False)['SALES'].sum()

with col1:
    st.subheader("Category wise sales")
    fig = px.bar(category_df, x = 'REGION', y = "SALES", text =['${:,.2f}'.format(x) for x in category_df['SALES']],
              template = 'seaborn')
    st.plotly_chart(fig, use_container_width=True )
    
with col2:
    st.subheader("Region wise")
    fig = px.pie(filtered_data, values = 'SALES', names = 'REGION')
    fig.update_traces(text = filtered_data['REGION'])
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category view data"):
        st.write(category_df)
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name="Category.csv", mime = 'tex/csv', help = 'Click to download the data as csv')
        
with cl2:
    with st.expander("Category data"):
        st.write(category_df)
        region = filtered_data.groupby(by = 'REGION', as_index = False)["SALES"].sum
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download", data = csv, file_name="Category.csv", mime = 'text/csv', help = 'Click to download the data as csv')
    

filtered_data['MONTH-YEAR'] = filtered_data['DATE'].dt.to_period("M")
st.subheader("Time series analysis")

linechart = pd.DataFrame(filtered_data.groupby(filtered_data['MONTH-YEAR'].dt.strftime("%Y : %b" ))['SALES'].sum()).reset_index()
fig2 = px.line(linechart, x = 'MONTH-YEAR', y = 'SALES', labels={"SALES" : "AMOUNT"}, height=500, width=1000, template='gridon')
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View data of time series"):
    st.write(linechart)
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data = csv, file_name="Timesseries.csv", mime='text/csv')


st.subheader("hierachical view of sales")
fig3 = px.treemap(filtered_data, path = ['REGION', 'STATE', 'CITY', 'DATE', 'SALES', 'PRODUCT SOLD'], values = 'SALES', hover_data=['SALES'],
                  color = 'TOTAL SALES')
fig3.update_layout(width=800, height=650)
st.plotly_chart(fig3, use_container_width=True)


chart1, chart2 = st.columns(2)
with chart1:
    st.subheader("Segment wise sales")
    fig = px.pie(filtered_data, values='SALES', names='REGION', template='plotly_dark')
    fig.update_traces(text = filtered_data["REGION"],textposition='inside')
    st.plotly_chart(fig, use_container_width=True)
with chart2:
    st.subheader("Category wise sales")
    fig = px.pie(filtered_data, values='SALES', names='REGION', template='gridon')
    fig.update_traces(text = filtered_data["REGION"],textposition='inside')
    st.plotly_chart(fig, use_container_width=True)
    
import plotly.figure_factory as ff
st.subheader(":point_down: Month wise sub category")

with st.expander("Summary Table"):
    table_value = st.number_input("Choose the amount of data to be displayed", value = 5)
    df_sample = df[0:table_value][['REGION', 'STATE', 'CITY', 'DATE', 'SALES', 'PRODUCT SOLD','PAYMENT']]
    fig = ff.create_table(df_sample, colorscale='Cividis')
    st.plotly_chart(fig, use_container_width=True)





























































