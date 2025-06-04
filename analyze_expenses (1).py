# app.py
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["finance"]
collection = db["expenses"]

st.set_page_config(page_title="Chi tiêu cá nhân", layout="wide")

# Load dữ liệu
@st.cache_data
def load_data():
    data = list(collection.find({"type": "Expense"}))
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

df = load_data()

st.title("📊 Phân tích Chi tiêu Cá nhân")

# Bộ lọc nâng cao
st.sidebar.header("🎯 Bộ lọc")
months = sorted(df["month"].unique())
categories = sorted(df["category"].dropna().unique())

selected_month = st.sidebar.selectbox("Chọn tháng", months)
selected_categories = st.sidebar.multiselect("Chọn danh mục", categories, default=categories)
amount_range = st.sidebar.slider("Khoảng tiền (VND)", 0, int(df["amount"].max()), (0, int(df["amount"].max())))

filtered_df = df[(df["month"] == selected_month) &
                 (df["category"].isin(selected_categories)) &
                 (df["amount"] >= amount_range[0]) &
                 (df["amount"] <= amount_range[1])]

# Giao diện thêm dữ liệu
st.sidebar.header("➕ Thêm giao dịch")
with st.sidebar.form("add_transaction"):
    date = st.date_input("Ngày")
    category = st.selectbox("Danh mục", categories)
    amount = st.number_input("Số tiền", min_value=0)
    description = st.text_input("Mô tả")
    submitted = st.form_submit_button("Thêm")
    if submitted:
        collection.insert_one({
            "date": pd.to_datetime(date),
            "category": category,
            "amount": amount,
            "description": description,
            "type": "Expense",
            "user_id": "user01"
        })
        st.success("✅ Đã thêm giao dịch mới.")
        st.experimental_rerun()

# Xoá giao dịch
st.sidebar.header("🗑️ Xoá giao dịch")
if st.sidebar.checkbox("Xoá tất cả giao dịch đã lọc"):
    if st.sidebar.button("Xác nhận xoá"):
        deleted = collection.delete_many({
            "month": selected_month,
            "category": {"$in": selected_categories},
            "amount": {"$gte": amount_range[0], "$lte": amount_range[1]}
        })
        st.sidebar.success(f"Đã xoá {deleted.deleted_count} bản ghi.")
        st.experimental_rerun()

# KPI
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Tổng chi tiêu", f"{filtered_df['amount'].sum():,.0f} VND")
with col2:
    st.metric("Số giao dịch", len(filtered_df))
with col3:
    st.metric("Danh mục", filtered_df['category'].nunique())

# Biểu đồ tròn theo danh mục
st.subheader(f"🧁 Chi tiêu theo danh mục - {selected_month}")
category_sum = filtered_df.groupby("category")["amount"].sum()
fig1, ax1 = plt.subplots()
category_sum.plot.pie(autopct='%1.1f%%', ax=ax1)
ax1.set_ylabel("")
st.pyplot(fig1)

# Gợi ý tiết kiệm
st.subheader("💡 Gợi ý tiết kiệm")
monthly_avg = df.groupby("category")["amount"].mean()
current = filtered_df.groupby("category")["amount"].sum()
for cat in current.index:
    if cat in monthly_avg:
        if current[cat] > monthly_avg[cat] * 1.2:
            st.warning(f"Danh mục '{cat}' vượt 20% so với trung bình. Cân nhắc tiết chế.")

# Hiển thị bảng dữ liệu
st.subheader("📋 Chi tiết giao dịch")
st.dataframe(filtered_df[["date", "category", "amount", "description"]].sort_values(by="date", ascending=False))







