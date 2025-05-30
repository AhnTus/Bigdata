import pandas as pd
import json

# Đọc file CSV
df = pd.read_csv("Personal_Finance_Dataset.csv")
df.dropna(inplace=True)

# Chuyển cột Date thành ISO format để phù hợp MongoDB
df["Date"] = pd.to_datetime(df["Date"])

# Đổi tên cột cho dễ xử lý
records = df.to_dict(orient="records")

for r in records:
    r["date"] = r.pop("Date").isoformat()
    r["amount"] = float(r.pop("Amount"))
    r["category"] = r.pop("Category")
    r["description"] = r.pop("Transaction Description")
    r["type"] = r.pop("Type")  # Thêm dòng này nếu bạn muốn giữ loại (Expense/Income)
    
    r["user_id"] = "user01"  # Liên kết với collection 'users'

# Ghi ra file JSON
with open("expenses.json", "w") as f:
    json.dump(records, f, indent=2)

print("✅ Dữ liệu đã được chuyển sang expenses.json")
