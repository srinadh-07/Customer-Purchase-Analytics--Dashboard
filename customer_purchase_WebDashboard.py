import pandas as pd 
import numpy as np
import plotly.express as px
import dash
from dash import dcc,html
import plotly.figure_factory as ff
df=pd.read_csv(r"D:\vs\uncleaned_customer_purchase_data_500_rows.csv")
# print(df)
# print(df.columns)
# print(df["Customer_ID"].value_counts())
df["Customer_ID"] = df["Customer_ID"].fillna(-1)
# print(df["Customer_ID"].value_counts())
df["Product"]=df["Product"].fillna(df["Product"].mode()[0])
df["Category"]=df.groupby("Product")["Category"].transform(lambda x: x.fillna(x.mode()[0]))
df["Quantity"]=df["Quantity"].fillna(df["Quantity"].mean())
df["Quantity"]=df["Quantity"].astype(int)
df["Unit_Price"]=df["Unit_Price"].fillna(df["Unit_Price"].mean())
df["Unit_Price"]=df["Unit_Price"].astype(int)
df["Purchase_Date"]=pd.to_datetime(df["Purchase_Date"])
df["Total_Amount"]=df["Total_Amount"].fillna(df["Total_Amount"].mean())
df["Total_Amount"]=df["Total_Amount"].astype(int)
# print(df.groupby("Product")["Total_Amount"].sum().sort_values(ascending=False).head(1))
# print(df.groupby("Category")["Total_Amount"].sum().sort_values(ascending=False).head(1))
# print(df)
sales_by_product = df.groupby("Product", as_index=False)["Total_Amount"].sum()
sales_by_product = sales_by_product.sort_values(by="Total_Amount", ascending=False)
fig1 = px.bar(
    sales_by_product,
    x="Product",
    y="Total_Amount",
    color="Total_Amount",
    color_continuous_scale="Blues",
    title="Total Sales by Product",
    labels={"Total_Amount": "Total Sales (₹)"}
)
fig1.update_layout(
    xaxis_title="Product",
    yaxis_title="Total Sales",
    xaxis_tickangle=-45,
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(255,255,255,1)',
    font=dict(size=14),
    height=500
)

quantity_by_product = df.groupby("Product", as_index=False)["Quantity"].sum()
quantity_by_product = quantity_by_product.sort_values(by="Quantity", ascending=False)
fig2 = px.bar(
    quantity_by_product,
    x="Product",
    y="Quantity",
    color="Quantity",
    color_continuous_scale="Viridis",
    title="Quantity Sold by Product",
    labels={"Quantity": "Total Quantity Sold"}
)
fig2.update_layout(
    xaxis_title="Product",
    yaxis_title="Quantity Sold",
    xaxis_tickangle=-45,
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
    font=dict(size=14),
    height=500
)
fig2.update_traces(
    text=quantity_by_product["Quantity"],
    textposition="outside"
)

category_sales = df.groupby("Category", as_index=False)["Total_Amount"].sum()
fig3 = px.pie(
    category_sales,
    names="Category",
    values="Total_Amount",
    title="Sales Distribution by Category",
    color_discrete_sequence=px.colors.qualitative.Set3,
    hole=0.4
)
fig3.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Total Sales: ₹%{value:,.0f}<br>Percentage: %{percent}",
    marker=dict(line=dict(color="#fff", width=2))
)

fig3.update_layout(
    title_x=0.5,
    font=dict(size=14),
    showlegend=True
)

df["Unit_Price"] = df["Total_Amount"] / df["Quantity"]

fig4 = px.box(
    df,
    x="Category",
    y="Unit_Price",
    color="Category",
    title="Unit Price Distribution by Category",
    points="all"
)

fig4.update_layout(
    xaxis_title="Category",
    yaxis_title="Unit Price",
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
    font=dict(size=14),
    boxmode='group',
    height=500
)

df["Purchase_Date"] = pd.to_datetime(df["Purchase_Date"])
df["Month"] = df["Purchase_Date"].dt.to_period("M").astype(str)

monthly_sales = df.groupby("Month", as_index=False)["Total_Amount"].sum()
monthly_sales = monthly_sales.sort_values("Month")

fig5 = px.line(
    monthly_sales,
    x="Month",
    y="Total_Amount",
    title="Monthly Sales Trend",
    markers=True,
    labels={"Total_Amount": "Total Sales", "Month": "Month"}
)

fig5.update_layout(
    title_x=0.5,
    font=dict(size=14),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
    xaxis_tickangle=-45,
    height=500
)

df["Week"] = df["Purchase_Date"].dt.to_period("W").astype(str)
weekly_sales = df.groupby("Week", as_index=False)["Total_Amount"].sum().sort_values("Week")

fig6 = px.bar(
    weekly_sales,
    x="Week",
    y="Total_Amount",
    title="Weekly Sales",
    color="Total_Amount",
    color_continuous_scale="Tealgrn"
)

fig6.update_layout(
    xaxis_title="Week",
    yaxis_title="Total Sales",
    title_x=0.5,
    xaxis_tickangle=-45,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
    font=dict(size=14),
    height=500
)

customer_spend = df.groupby("Customer_ID")["Total_Amount"].sum().reset_index()

fig7 = px.bar(
    customer_spend,
    x="Customer_ID",
    y="Total_Amount",
    title="Total Spend by Customer",
    labels={"Customer_ID": "Customer ID", "Total_Amount": "Total Spend"},
    template="plotly_white"
)

fig7.update_layout(
    xaxis=dict(
        tickangle=45,
        rangeslider=dict(visible=True),  # Scrollable
        type='category'
    )
)


fig8 = px.histogram(df, x="Quantity", nbins=20, title="Distribution of Quantity Purchased")

fig8.update_layout(
    xaxis_title="Quantity",
    yaxis_title="Count",
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
    font=dict(size=14),
    height=500
)

fig9 = px.histogram(
    df,
    x="Quantity",
    nbins=20,
    title="Distribution of Quantity Purchased",
    color_discrete_sequence=["#636EFA"]
)

fig9.update_layout(
    xaxis_title="Quantity Purchased",
    yaxis_title="Number of Orders",
    title_x=0.5,
    bargap=0.2,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='white',
    font=dict(size=14),
    height=500
)

fig9.update_traces(marker_line_color='white', marker_line_width=1)


df["Category"] = df["Category"].str.capitalize()

fig10 = px.scatter(
    df,
    x="Quantity",
    y="Unit_Price",
    color="Category",
    title="Quantity vs Unit Price",
    labels={
        "Quantity": "Quantity",
        "Unit_Price": "Unit Price",
        "Category": "Category"
    },
    template="plotly_white"
)
fig10.update_traces(marker=dict(size=10, opacity=0.7))
fig10.update_layout(title_font_size=20)

df["Category"] = df["Category"].str.capitalize()

fig11 = px.box(
    df,
    y="Total_Amount",
    color="Category",
    title="Total Amount Distribution",
    labels={"Total_Amount": "Total Amount"},
    template="plotly_white"
)

fig11.update_traces(marker=dict(opacity=0.5))
fig11.update_layout(title_font_size=20)


missing_df = df.isnull().astype(int)
fig12 = ff.create_annotated_heatmap(
    z=missing_df.values,
    x=list(df.columns),
    y=list(df.index.astype(str)),
    colorscale="Viridis",
    showscale=True
)

fig12.update_layout(
    title_text="Missing Value Heatmap",
    title_font_size=20,
    xaxis_title="Columns",
    yaxis_title="Index",
    template="plotly_white"
)

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("CUSTOMER PURCHASE ANALYSIS DASHBOARD", style={"textAlign": "center"}),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7),
    dcc.Graph(figure=fig8),
    dcc.Graph(figure=fig9),
    dcc.Graph(figure=fig10),
    dcc.Graph(figure=fig11),
    dcc.Graph(figure=fig12)
    
    ])
if __name__ == '__main__':
    app.run(debug=True)
