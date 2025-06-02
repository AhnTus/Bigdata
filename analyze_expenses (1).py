from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["finance"]
collection = db["expenses"]

# Lấy dữ liệu chi tiêu
cursor = collection.find({"type": "Expense"})
df = pd.DataFrame(list(cursor))

# Chuyển kiểu datetime & tạo cột thời gian
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M').astype(str)

# Thiết lập style chung
sns.set(style="whitegrid")


monthly_sum = df.groupby('month')['amount'].sum().sort_index()
category_sum = df.groupby('category')['amount'].sum().sort_values()

#1
# KPI: Tổng thu nhập, Tổng chi tiêu, Số dư ròng
df_income = collection.find({"type": "Income"})
df_income = pd.DataFrame(list(df_income))

df_expense = collection.find({"type": "Expense"})
df_expense = pd.DataFrame(list(df_expense))

total_income = df_income['amount'].sum()
total_expense = df_expense['amount'].sum()
net_balance = total_income - total_expense

# Dữ liệu
kpi_labels = ["Tổng thu", "Tổng chi", "Số dư ròng"]
kpi_values = [total_income, total_expense, net_balance]
colors = ['green', 'red', 'blue']

plt.figure(figsize=(6, 6))
sns.barplot(x=kpi_labels, y=kpi_values, palette=colors)
plt.title("TỔNG QUAN TÀI CHÍNH", fontsize=16)
plt.ylabel("Số tiền (VND)")
for i, value in enumerate(kpi_values):
    plt.text(i, value + max(kpi_values) * 0.03, f"{value:,.0f}", ha='center', fontsize=12)
plt.tight_layout()
plt.show()



# 2️⃣ Bar chart: Chi tiêu theo danh mục
# Lọc chi tiêu
df_expense = df[df['type'] == 'Expense']

# Nhóm theo tháng và danh mục, tính tổng
grouped = df_expense.groupby(['month', 'category'])['amount'].sum().reset_index()

# Với mỗi tháng, tìm danh mục chi nhiều nhất
idx = grouped.groupby('month')['amount'].idxmax()
top_spending = grouped.loc[idx].sort_values('month')

# Vẽ biểu đồ
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(15, 6))
sns.barplot(data=top_spending, x='month', y='amount', hue='category', dodge=False, palette='Set2')
plt.title('Danh mục chi tiêu nhiều nhất mỗi tháng')
plt.xlabel('Tháng')
plt.ylabel('Số tiền')
plt.xticks(rotation=45)
plt.legend(title='Danh mục', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# 3️⃣ Line chart: Chi tiêu theo tháng
pareto = df.groupby("category")["amount"].sum().sort_values(ascending=False)
cum_pct = pareto.cumsum() / pareto.sum()

plt.figure(figsize=(10, 5))
sns.barplot(x=pareto.index, y=pareto.values, color='skyblue')
plt.plot(pareto.index, cum_pct.values, color='red', marker='o')
plt.title("Biểu đồ: Chi tiêu theo danh mục", fontsize=14)
plt.ylabel("Số tiền")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 4️⃣ Pie chart: Tỷ lệ chi tiêu theo danh mục
plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x="category", y="amount")
plt.title("Phân phối chi tiêu từng danh mục – phát hiện bất thường", fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5️⃣ Stacked area chart: Chi tiêu các danh mục theo tháng
# Lọc giao dịch chi tiêu
df_expense = df[df['type'] == 'Expense']

# Sắp xếp giảm dần theo số tiền
top10 = df_expense.sort_values(by='amount', ascending=False).head(10)

# Chọn cột cần thiết và định dạng lại ngày
top10_display = top10[['date', 'description', 'amount']].copy()
top10_display['date'] = pd.to_datetime(top10_display['date']).dt.strftime('%d/%m/%Y')

# Tạo bảng bằng matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 3.5))  # chỉnh kích thước bảng
ax.axis('tight')
ax.axis('off')
table = ax.table(
    cellText=top10_display.values,
    colLabels=["Date", "Transaction Description", "Amount"],
    cellLoc='center',
    loc='center',
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)  # giãn dòng

plt.title("10 giao dịch chi lớn nhất", fontsize=13, fontweight='bold', pad=10)
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






