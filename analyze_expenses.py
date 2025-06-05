from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["finance"]
collection = db["expenses"]

# Lấy dữ liệu chi tiêu (chỉ cần lấy 1 lần)
cursor = collection.find({"type": "Expense"})
df = pd.DataFrame(list(cursor))

# Kiểm tra nếu DataFrame rỗng
if df.empty:
    print("Không có dữ liệu chi tiêu để phân tích.")
else:
    # Chuyển kiểu datetime & tạo cột thời gian (làm 1 lần)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    df['year'] = df['date'].dt.year # Thêm cột năm ở đây

    # Thiết lập style chung
    sns.set(style="whitegrid")

    # Tính toán tổng chi tiêu theo tháng và danh mục (cho phần insights cuối)
    monthly_sum = df.groupby('month')['amount'].sum().sort_index()
    category_sum = df.groupby('category')['amount'].sum().sort_values()

    #1. Tổng quan tài chính
    # Tổng thu nhập, Tổng chi tiêu, Số dư ròng
    # Cần lấy dữ liệu thu nhập riêng
    df_income = collection.find({"type": "Income"})
    df_income = pd.DataFrame(list(df_income))

    total_income = df_income['amount'].sum() if not df_income.empty else 0
    total_expense = df['amount'].sum() # Sử dụng df đã tải
    net_balance = total_income - total_expense

    # Dữ liệu
    kpi_labels = ["Tổng thu", "Tổng chi", "Số dư ròng"]
    kpi_values = [total_income, total_expense, net_balance]
    colors = ['green', 'red', 'blue']

    plt.figure(figsize=(6, 6))
    sns.barplot(x=kpi_labels, y=kpi_values, palette=colors)
    plt.title("TỔNG QUAN TÀI CHÍNH", fontsize=16)
    plt.ylabel("Số tiền (USD)")
    for i, value in enumerate(kpi_values):
        plt.text(i, value + max(kpi_values) * 0.03, f"{value:,.0f}", ha='center', fontsize=12)
    plt.tight_layout()
    plt.show()

    #2. Top 10 giao dịch chi tiêu lớn nhất
    # df đã là dữ liệu chi tiêu
    top10 = df.sort_values(by='amount', ascending=False).head(10)

    # Chọn cột cần thiết và định dạng lại ngày
    top10_display = top10[['date', 'description', 'amount']].copy()
    top10_display['date'] = pd.to_datetime(top10_display['date']).dt.strftime('%d/%m/%Y')

    # Tạo bảng
    fig, ax = plt.subplots(figsize=(7, 3.5))
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
    table.scale(1, 1.5)
    plt.title("10 giao dịch chi lớn nhất", fontsize=13, fontweight='bold', pad=10)
    plt.tight_layout()
    plt.show()


    #3. Tổng chi tiêu theo năm
    # Sử dụng cột 'year' đã tạo ở trên
    annual_expense = df.groupby('year')['amount'].sum()

    # Vẽ biểu đồ
    plt.figure(figsize=(8, 5))
    sns.barplot(x=annual_expense.index.astype(str), y=annual_expense.values, palette='Reds')

    plt.title("TỔNG CHI TIÊU THEO NĂM", fontsize=14)
    plt.xlabel("Năm")
    plt.ylabel("Tổng chi tiêu (USD)")

    # Thêm nhãn số trên mỗi cột
    for i, v in enumerate(annual_expense.values):
        plt.text(i, v + annual_expense.max() * 0.02, f"{v:,.0f}", ha='center', fontsize=11)

    plt.tight_layout()
    plt.show()

    #4. Tỷ lệ chi tiêu theo danh mục
    # df đã là dữ liệu chi tiêu
    expense_by_category = df.groupby('category')['amount'].sum().sort_values(ascending=False)

    # Vẽ biểu đồ tròn
    plt.figure(figsize=(8, 8))
    plt.pie(
        expense_by_category,
        labels=expense_by_category.index,
        autopct='%1.1f%%',
        startangle=140,
        wedgeprops={'edgecolor': 'white'}
    )
    plt.title('TỶ LỆ CHI TIÊU THEO DANH MỤC', fontsize=14)
    plt.tight_layout()
    plt.show()

    #5. Lọc chi tiêu theo tháng
    # df đã là dữ liệu chi tiêu
    # Sử dụng cột 'month' đã tạo ở trên
    grouped = df.groupby(['month', 'category'])['amount'].sum().reset_index()

    # Với mỗi tháng, tìm danh mục chi nhiều nhất
    idx = grouped.groupby('month')['amount'].idxmax()
    top_spending = grouped.loc[idx].sort_values('month')

    # Vẽ biểu đồ
    plt.figure(figsize=(15, 6))
    sns.barplot(data=top_spending, x='month', y='amount', hue='category', dodge=False, palette='Set2')
    plt.title('Danh mục chi tiêu nhiều nhất mỗi tháng')
    plt.xlabel('Tháng')
    plt.ylabel('Số tiền(USD)')
    plt.xticks(rotation=45)
    plt.legend(title='Danh mục', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # --- Insight tổng kết ---
    print("\n🎯 Insight tổng hợp:")
    print("👉 Tháng chi tiêu nhiều nhất:", monthly_sum.idxmax(), f"({monthly_sum.max():,.0f} USD)")
    print("👉 Danh mục chi tiêu cao nhất:", category_sum.idxmax(), f"({category_sum.max():,.0f} USD)")
    print("👉 Trung bình chi tiêu mỗi tháng:", df.groupby('month')['amount'].sum().mean())
    print("👉 Mức chi cao nhất:", df['amount'].max())



# --------- CRUD ---------
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
