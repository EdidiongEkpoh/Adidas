# Importing required libraries
import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page configuration
st.set_page_config(layout="wide")

url = "https://raw.githubusercontent.com/EdidiongEkpoh/Portfolio/main/Adidas/Adidas.xlsx"
image_url = "https://raw.githubusercontent.com/EdidiongEkpoh/Portfolio/main/Adidas/adidas.png"

@st.cache_data
def load_data(url):
    # Read the Excel file from the URL
    data = pd.read_excel(url)
    return data

df = load_data(url) 
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])  # Converts 'InvoiceDate' column to datetime format



# Custom CSS for padding and image styling
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .adidas-image {
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load and display the Adidas logo

col1, col2 = st.columns([0.1, 0.9])

with col1:
    st.markdown(f'<img src="{image_url}" class="adidas-image" width="100"/>', unsafe_allow_html=True)  # Display the image with specified width  # Display the image with specified width

# HTML for dashboard title
html_title = '''
<style>
      .title-test {
      font-weight: bold;
      padding: 5px;
      border-radius: 6px;
      }
</style>
<center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center>
'''

with col2:
    st.markdown(html_title, unsafe_allow_html=True)  # Display the dashboard title

# Columns for displaying last update and first plot
col3, col4, col5 = st.columns([0.1, 0.45, 0.45])

with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")  # Display the last updated date

with col4:
    fig = px.bar(df, x="Retailer", y="TotalSales", labels={"TotalSales": "Total Sales {$}"},
                 title="Total Sales by Retailer", hover_data=["TotalSales"],
                 template="gridon", height=500)

    st.plotly_chart(fig, use_container_width=True)  # Display the bar plot

# Columns for viewing and downloading retailer-wise sales data
_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])

with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)  # Display retailer-wise sales data

with dwn1:
    st.download_button("Get Data", data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv",
                       mime="text/csv")  # Download button for retailer-wise sales data

# Create Month-Year column and group by Month-Year for plotting sales over time
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b %y")
result = df.groupby(by="Month_Year")['TotalSales'].sum().reset_index()

with col5:
    fig1 = px.line(result, x="Month_Year", y="TotalSales", title="Total Sales Over Time",
                   template="gridon")
    fig1.update_xaxes(tickangle=45)
    st.plotly_chart(fig1, use_container_width=True)  # Display the line plot

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)  # Display monthly sales data

with dwn2:
    st.download_button("Get Data", data=result.to_csv().encode("utf-8"),
                       file_name="MonthlySales.csv", mime="text/csv")  # Download button for monthly sales data

st.divider()  # Add a visual divider

# Group by State for plotting total sales and units sold
result1 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

# Create a combined bar and line plot
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name="Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["UnitsSold"],
                          mode="lines", name="Units Sold", yaxis="y2"))

fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales", showgrid=False),
    yaxis2=dict(title="Units Sold", overlaying="y", side="right"),
    template="gridon",
    legend=dict(x=1, y=1)
)

_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width=True)  # Display the combined plot

_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])
with view3:
    expander = st.expander("View Data for Sales by Unit Sold")
    expander.write(result1)  # Display sales by unit sold data

with dwn3:
    st.download_button("Get Data", data=result1.to_csv().encode("utf-8"),
                       file_name="Sales_by_UnitsSold.csv", mime="text/csv")  # Download button for sales by unit sold data

st.divider()  # Add a visual divider

_, col7 = st.columns([0.1, 1])
# Group by Region and City for treemap plot
treemap = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{: .2f} Lakh'.format(value / 1_00_000)

treemap["Total Sales (Formatted)"] = treemap["TotalSales"].apply(format_sales)
fig4 = px.treemap(treemap, path=["Region", "City"], values="TotalSales",
                  hover_name="Total Sales (Formatted)",
                  hover_data=["Total Sales (Formatted)"],
                  color="City", height=700)

fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in TreeMap")
    st.plotly_chart(fig4, use_container_width=True)  # Display the treemap

view4, dwn4 = st.columns([0.5, 0.5])
with view4:
    result2 = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum().reset_index()
    result2 = result2.sort_values(by="TotalSales", ascending=False)
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)  # Display total sales
