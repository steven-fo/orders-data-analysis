import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

orders_customers_df = pd.read_csv("../data/orders_customers.csv")


datetime_columns = ["order_purchase_timestamp", "order_delivered_carrier_date"]
orders_customers_df.sort_values(by="order_purchase_timestamp", inplace=True)
orders_customers_df.reset_index(inplace=True)

for column in datetime_columns:
    orders_customers_df[column] = pd.to_datetime(orders_customers_df[column])

min_date = orders_customers_df["order_purchase_timestamp"].min()
max_date = orders_customers_df["order_purchase_timestamp"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang watu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = orders_customers_df[(orders_customers_df["order_purchase_timestamp"] >= str(start_date)) &
                              (orders_customers_df["order_purchase_timestamp"] <= str(end_date))]

st.header('Dashboard Penjualan :sparkles:')

st.subheader("State With Most and Least Orders")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="order_id", y="customer_state", data=main_df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=False).reset_index().head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Orders", fontsize=30)
ax[0].set_title("State with Most Orders", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="order_id", y="customer_state", data=main_df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=True).reset_index().head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Orders", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("State with Least Orders", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Number of Orders by Status")

fig, ax = plt.subplots(figsize=(16,8))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    y="order_id",
    x="order_status",
    data=main_df.groupby(by="order_status").order_id.nunique().sort_values(ascending=False).reset_index(),
    palette=colors
)
ax.set_ylabel(None)
ax.set_xlabel("Number of Orders", fontsize=30)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)