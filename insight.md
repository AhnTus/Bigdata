
# 📋 Báo cáo Insight – Phân tích Chi tiêu Cá nhân (bản cải thiện)

**Sinh viên thực hiện:**
- Phạm Nguyễn Tuân – 2221050253
- Đào Anh Tú – 2221050231

---

## 🎯 Mục tiêu
Phân tích dữ liệu chi tiêu cá nhân bằng MongoDB nhằm:
- Theo dõi và tổng hợp thu nhập – chi tiêu
- Phát hiện danh mục chi tiêu lớn nhất và biến động theo thời gian
- Đưa ra các gợi ý tiết kiệm và phát hiện bất thường

---

## 📊 Dữ liệu sử dụng

- Tổng số bản ghi: ~1500 dòng
- Loại giao dịch: `Expense`, `Income`
- Trường dữ liệu chính:
  - `date`, `amount`, `category`, `description`, `type`, `user_id`

---

## 🔍 Insight 1 – Tổng quan tài chính (KPI)

- ✅ **Tổng thu nhập**:  ~[tổng thu thực tế]
- ✅ **Tổng chi tiêu**:  ~[tổng chi thực tế]
- ✅ **Số dư ròng** (thu – chi): dương => chi tiêu không vượt quá thu nhập

📌 **Gợi ý**: Duy trì tỷ lệ chi dưới 70% thu nhập, trích ít nhất 20% để tiết kiệm.

---

## 🔍 Insight 2 – Danh mục chi tiêu

- **Danh mục chi lớn nhất**: `Food & Drink`
- **Danh mục phổ biến tiếp theo**: `Transportation`, `Entertainment`
- Một số danh mục như `Utilities`, `Rent` có tính chu kỳ.

📌 **Gợi ý**: Thiết lập hạn mức tháng cho nhóm `Food & Drink`.

---

## 🔍 Insight 3 – Chi tiêu theo tháng

- **Tháng chi tiêu cao nhất**: 2023-06
- **Tháng chi tiêu thấp nhất**: 2023-01
- Có xu hướng tăng mạnh vào mùa hè, dịp cuối năm.

📌 **Gợi ý**: Lập kế hoạch chi tiêu trước các tháng "cao điểm".

---

## 🔍 Insight 4 – Phát hiện bất thường

- Qua biểu đồ **boxplot**, một số giao dịch có giá trị rất cao (> 2 triệu), bất thường so với mức trung bình.
- Những giao dịch này thuộc danh mục `Education`, `Shopping`.

📌 **Gợi ý**: Nên gắn cờ/ghi chú cho các chi tiêu đột biến để kiểm soát tốt hơn.

---

## 🔍 Insight 5 – Top giao dịch chi lớn nhất

| STT | Ngày       | Nội dung giao dịch      | Số tiền (VNĐ) |
|-----|------------|--------------------------|----------------|
| 1   | 05/06/2023 | Mua laptop               | 18,000,000     |
| 2   | 12/07/2023 | Đóng học phí đại học     | 9,000,000      |
| ... | ...        | ...                      | ...            |

📌 **Gợi ý**: Cân nhắc chia nhỏ hoặc lên kế hoạch trước với các khoản chi lớn.

---

## ✅ Kết luận

- Quản lý chi tiêu bằng MongoDB giúp cá nhân hiểu rõ hơn về dòng tiền.
- Dữ liệu phân loại rõ ràng giúp phát hiện và phân tích dễ dàng.
- Hệ thống có thể mở rộng để nhắc chi, gợi ý tiết kiệm theo danh mục, dự báo tương lai.

---
