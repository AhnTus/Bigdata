
# 📊 Phân tích Chi tiêu Cá nhân với MongoDB

Đồ án này thực hiện phân tích dữ liệu tài chính cá nhân sử dụng cơ sở dữ liệu MongoDB, thư viện Python và trực quan hóa bằng biểu đồ. Hệ thống giúp người dùng hiểu rõ hơn về thói quen chi tiêu, phát hiện các danh mục tốn kém và xu hướng theo thời gian.

---

## 🗂️ Nội dung

- Kết nối và lưu trữ dữ liệu chi tiêu vào MongoDB
- Thực hiện đầy đủ CRUD (Create, Read, Update, Delete)
- Truy vấn nâng cao bằng aggregation (`groupby`, `pivot`)
- Trực quan hóa dữ liệu bằng biểu đồ (matplotlib, seaborn)
- Phân tích và rút ra insight tài chính

---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Vai trò |
|----------|---------|
| MongoDB  | Lưu trữ dữ liệu chi tiêu |
| PyMongo  | Kết nối Python với MongoDB |
| Pandas   | Xử lý và phân tích dữ liệu |
| Matplotlib, Seaborn | Vẽ biểu đồ trực quan |

---

## 🧾 Cấu trúc cơ sở dữ liệu MongoDB

**Database**: `finance`

### 📁 Collection: `expenses`
```json
{
  "date": "2025-05-01T00:00:00",
  "amount": 120000,
  "category": "Entertainment",
  "description": "Xem phim CGV",
  "type": "Expense",
  "user_id": "user01"
}
```

### 📁 Collection: `categories`
Chứa mô tả các loại chi tiêu.

### 📁 Collection: `users`
Chứa thông tin người dùng.

---

## 🔄 Thao tác CRUD (đã thực hiện)

- ✅ Thêm bản ghi chi tiêu mới (Create)
- ✅ Tìm kiếm bản ghi (Read)
- ✅ Cập nhật thông tin chi tiêu (Update)
- ✅ Xoá bản ghi (Delete)

---

## 📊 Trực quan hóa

- Biểu đồ **đường**: Tổng chi tiêu theo tháng
- Biểu đồ **tròn**: Tỉ lệ chi tiêu theo danh mục
- Biểu đồ **cột ngang**: So sánh các nhóm chi tiêu
- Biểu đồ **pivot**: Chi tiêu theo danh mục theo thời gian

---

## 🎯 Insight nổi bật

- Danh mục chi tiêu nhiều nhất: `Food & Drink`
- Tháng chi tiêu cao nhất: `2023-06` với hơn 30,000 VNĐ
- Một số danh mục chi tiêu đều đặn theo chu kỳ hàng tháng như `Rent`, `Utilities`

---

## 📁 File chính

- `analyze_expenses.py`: script thực hiện kết nối MongoDB, xử lý và trực quan dữ liệu
- `expenses.json`, `categories.json`, `users.json`: dữ liệu gốc

---

## ✅ Hướng phát triển

- Tạo web app bằng Flask/Streamlit
- Gợi ý tiết kiệm theo hành vi chi tiêu
- Tự động đồng bộ từ file sao kê ngân hàng/Momo

---

## 👤 Thông tin

- Sinh viên: Phạm Nguyễn Tuân-2221050253
             Đào Anh Tú-2221050231
- Môn học: Dữ liệu lớn và ứng dụng 
- Trường: Đại học Mỏ-Địa chất
- Năm học: 2024-2025

---
