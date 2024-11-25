import pandas as pd
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import plotly.express as px


df = pd.read_excel('GustoAnalisys.xlsx')

st.title("Gusto DashBoard")
# Date input for filtering
with st.sidebar:
    start_date = st.date_input("Start Date", value=df['Date'].min())
    end_date = st.date_input("End Date", value=df['Date'].max())
tab1, tab2 = st.tabs(["Cutomers", "Cutomers With Products"])


date_filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
dynamic_filters_super = DynamicFilters(date_filtered_df, filters=['Beat','Category'], filters_name="Super")
dynamic_filters_super.display_filters(location='sidebar')
filtered_df_super = dynamic_filters_super.filter_df()


with tab1:
    # Display the filtered dataframe
    costumers_data = filtered_df_super.groupby(['Date','Customer','LAT','LONG']).aggregate({'Total Amount':'sum','Quantity':'sum'}).reset_index()
    costumers_data['LAT']=df['LAT'].astype(float)
    costumers_data['LONG']=df['LONG'].astype(float)
    
    fig = px.scatter_mapbox(costumers_data, lat='LAT', lon='LONG', hover_name='Customer')
    # Update layout for map style and zoom level
    fig.update_layout(mapbox_style='open-street-map',
                    margin={'r':0,'t':0,'l':0,'b':0})
    st.plotly_chart(fig)
    # costumers_data = filtered_df[['Date' , 'Customer']].drop_duplicates()
    repeat_orders = costumers_data.groupby('Customer').size().reset_index(name='Count')

    repeat_count = repeat_orders.groupby('Count').size().reset_index(name='Repeat Count')

    # st.dataframe(costumers_data)
    st.write('No. Of Outlets: '+ str(costumers_data['Customer'].nunique()))
    st.write('Total Sales: '+ str(costumers_data['Total Amount'].sum()))

    st.write('Total QTY: '+str(costumers_data['Quantity'].sum()))
    # Display the Repeat Orders
    st.write("Repeat Orders:")
    st.dataframe(repeat_orders)

    st.write("Repeat Count:")
    st.dataframe(repeat_count)

with tab2:
    costumers_products_data = filtered_df_super.groupby(['Date','Customer', 'Product' ,'LAT','LONG']).aggregate({'Total Amount':'sum','Quantity':'sum'}).reset_index()
    # st.write(costumers_products_data)
    dynamic_filters = DynamicFilters(costumers_products_data, filters=['Product'])

    dynamic_filters.display_filters(location='columns', num_columns=2, gap='large')
    filetered_costumers_products_data = dynamic_filters.filter_df()
    filetered_costumers_products_data['LAT']=df['LAT'].astype(float)
    filetered_costumers_products_data['LONG']=df['LONG'].astype(float)
    fig = px.scatter_mapbox(filetered_costumers_products_data, lat='LAT', lon='LONG', hover_name='Customer')
    fig.update_layout(mapbox_style='open-street-map',
                    margin={'r':0,'t':0,'l':0,'b':0})
    st.plotly_chart(fig)
    repeat_product_orders = filetered_costumers_products_data.groupby(['Customer' , 'Product']).size().reset_index(name='Count')

    repeat_product_count = repeat_product_orders.groupby('Count').size().reset_index(name='Number Of Oultes')


    st.write('No. Of Outlets: '+ str(filetered_costumers_products_data['Customer'].nunique()))
    st.write('Total Sales: '+ str(filetered_costumers_products_data['Total Amount'].sum()))

    st.write('Total QTY: '+str(filetered_costumers_products_data['Quantity'].sum()))

    st.write("Repeat Orders:")
    st.dataframe(repeat_product_orders)

    st.write("Repeat Count:")
    st.dataframe(repeat_product_count)