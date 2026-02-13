import streamlit as st
import pandas as pd
import plotly.express as px 

st.title("Sales Report")

df = pd.read_csv('sales.csv')
#st.subheader("Data Preview")
#st.dataframe(df.head())

#st.subheader("Summary Statistics")
#st.write(df.describe())

st.audio('Future_Metro_Boomin_The_Weeknd_-_Young_Metro_Official_Music_Video_256KBPS.webm' ,autoplay=True, loop=True)

st.sidebar.text_input("Enter Your Name")

with st.expander("Data Preview"):
    st.dataframe(df.head())

with st.expander("Data From"):
    st.link_button("View Data Source", "https://www.kaggle.com/datasets/vinothkannaece/sales-dataset")

st.subheader('Reports Summary')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"${df['Sales_Amount'].sum():,.2f}")

with col2:
    st.metric("Total Products", df['Product_Category'].nunique())

with col3:
    st.metric("Total Regions", df['Region'].nunique())


tab1, tab2, tab3 = st.tabs(["Sales by Product & Region", "Sales Trends", "Customer Insights"])

with tab1:
    #Show Product Sales by type
    st.sidebar.subheader("Filter by Product Category")
    product_categories = df['Product_Category'].unique()
    selected_category = st.sidebar.multiselect("Select a Product Category", product_categories)

    st.subheader("Total Sales by Product")
    sales_by_product = df.groupby('Product_Category')['Sales_Amount'].sum().reset_index()
    sales_by_product = sales_by_product[sales_by_product['Product_Category'].isin(selected_category)]
    st.bar_chart(sales_by_product.set_index('Product_Category'), horizontal=True)


    #Show Sales by Region
    sales_region = df['Region'].unique()
    selected_region = st.sidebar.multiselect('Select a region', sales_region)

    st.subheader("Total Sales by Region")
    sales_by_region = df.groupby('Region')['Sales_Amount'].sum().reset_index()
    sales_by_region = sales_by_region[sales_by_region['Region'].isin(selected_region)]
    st.bar_chart(sales_by_region.set_index('Region'), horizontal=True)

with tab2:
    st.subheader("Sales Trends Over Time")
    df['Sale_Date'] = pd.to_datetime(df['Sale_Date'])
    df['Month'] = df['Sale_Date'].dt.to_period('M')
    sales_trends = df.groupby('Month')['Sales_Amount'].sum().reset_index()
    sales_trends['Month'] = sales_trends['Month'].astype(str)
    st.line_chart(sales_trends.set_index('Month'))

    #Product Sales Trends by Product Category
    st.subheader("Product Sales Trends Overtime")
    df['Month'] = df['Sale_Date'].dt.to_period('M')
    sales_trends_product = df.groupby(['Month', 'Product_Category'])['Sales_Amount'].sum().reset_index()
    sales_trends_product['Month'] = sales_trends_product['Month'].astype(str)
    sales_trends_product_pivot = sales_trends_product.pivot(index='Month', columns='Product_Category', values='Sales_Amount')
    st.line_chart(sales_trends_product_pivot)

    #Sales Trends by Region
    st.subheader("Sales Trends by Region")
    sales_trends_region = df.groupby(['Month', 'Region'])['Sales_Amount'].sum().reset_index()
    sales_trends_region['Month'] = sales_trends_region['Month'].astype(str)
    sales_trends_region_pivot = sales_trends_region.pivot(index='Month', columns='Region', values='Sales_Amount')
    st.line_chart(sales_trends_region_pivot)

    
with tab3:
    #Show Top Customers
    st.subheader("Customer Insights")
    top_customers = df.groupby('Sales_Rep')['Sales_Amount'].sum().reset_index().sort_values(by='Sales_Amount', ascending=False).head(10)
    st.bar_chart(top_customers.set_index('Sales_Rep'), horizontal=False)

    #Returning Customers vs New Customers
    st.subheader("Returning Customers")
    r_vs_new = df['Customer_Type'].value_counts().reset_index()
    r_vs_new.columns = ['Customer_Type', 'Count']
    fig1 = px.pie(r_vs_new, values='Count', names='Customer_Type', title='Returning vs New Customers')
    st.plotly_chart(fig1)

    #Payment Types Chart
    st.subheader("Payment Types")
    payments = df["Payment_Method"].value_counts().reset_index()
    payments.columns = ['Payment_Method', 'Count']
    fig2 = px.pie(payments, values='Count', names = 'Payment_Method', title='Payment Methods' )
    st.plotly_chart(fig2)
