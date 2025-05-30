from pymongo import MongoClient
import pandas as pd

# Kết nối tới MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["finance"]  # tên database
collection = db["expenses"]  # tên collection

# Lấy toàn bộ dữ liệu type = Expense
cursor = collection.find({"type": "Expense"})

# Chuyển thành pandas DataFrame
df = pd.DataFrame(list(cursor))

# Hiển thị 5 dòng đầu tiên để kiểm tra
print(df.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Chuyển date về kiểu datetime
df['date'] = pd.to_datetime(df['date'])

# Tạo cột tháng
df['month'] = df['date'].dt.to_period('M').astype(str)

# Hiển thị 5 dòng để kiểm tra
print(df[['date', 'month', 'category', 'amount']].head())

category_sum = df.groupby('category')['amount'].sum().sort_values()

plt.figure(figsize=(10, 6))
sns.barplot(x=category_sum.values, y=category_sum.index, palette='Blues_r')
plt.title('Tổng chi tiêu theo danh mục')
plt.xlabel('Số tiền')
plt.ylabel('Danh mục')
plt.tight_layout()
plt.show()

monthly_sum = df.groupby('month')['amount'].sum()

plt.figure(figsize=(12, 5))
monthly_sum.plot(kind='line', marker='o', color='green')
plt.title('Tổng chi tiêu theo tháng')
plt.ylabel('Số tiền')
plt.xlabel('Tháng')
plt.grid(True)
plt.tight_layout()
plt.show()

category_ratio = df.groupby("category")["amount"].sum()

plt.figure(figsize=(8, 8))
plt.pie(category_ratio, labels=category_ratio.index, autopct="%1.1f%%", startangle=140)
plt.title("Tỉ lệ chi tiêu theo danh mục")
plt.axis("equal")
plt.show()

pivot = df.pivot_table(values='amount', index='month', columns='category', aggfunc='sum')
pivot.plot(figsize=(12, 6))
plt.title("Chi tiêu từng danh mục theo tháng")
plt.xlabel("Tháng")
plt.ylabel("Số tiền")
plt.legend(title="Danh mục")
plt.tight_layout()
plt.show()

# --------- CRUD DEMO ---------

# CREATE
new_expense = {
    "date": "2025-05-28T00:00:00",
    "amount": 120000,
    "category": "Entertainment",
    "description": "Xem phim CGV",
    "type": "Expense",
    "user_id": "user01"
}
collection.insert_one(new_expense)
print("✅ CREATE: Đã thêm bản ghi.")

# READ
record = collection.find_one({"description": "Xem phim CGV"})
print("📄 READ: Bản ghi tìm được:", record)

# UPDATE
collection.update_one(
    {"description": "Xem phim CGV"},
    {"$set": {"amount": 150000, "category": "Leisure"}}
)
print("✅ UPDATE: Đã cập nhật bản ghi.")

# DELETE
collection.delete_one({"description": "Xem phim CGV"})
print("🗑️ DELETE: Đã xoá bản ghi.")

# --- Insight tổng kết ---
print("\n🎯 Insight tổng hợp:")
print("👉 Tháng chi tiêu nhiều nhất:", monthly_sum.idxmax(), f"({monthly_sum.max():,.0f} VNĐ)")
print("👉 Danh mục chi tiêu cao nhất:", category_sum.idxmax(), f"({category_sum.max():,.0f} VNĐ)")
print("👉 Trung bình chi tiêu mỗi tháng:", df.groupby('month')['amount'].sum().mean())
print("👉 Mức chi cao nhất:", df['amount'].max())
