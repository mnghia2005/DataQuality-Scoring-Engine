import pandas as pd
import sqlite3
import os

# Đường dẫn tới file CSV cũ của bạn
csv_path = "data/dirty_customer_data.csv" 

# 1. Khởi tạo kết nối (Nó sẽ tự động tạo ra file company_data.db nếu chưa có)
db_path = "company_data.db"
conn = sqlite3.connect(db_path)

try:
    # 2. Đọc file CSV lên
    df = pd.read_csv(csv_path)
    
    # 3. Phép thuật của Pandas: Bê nguyên cái bảng này nhét vào Database
    # Đặt tên bảng là 'customers'
    df.to_sql("customers", conn, if_exists="replace", index=False)
    
    print("🎉 TUYỆT VỜI! Đã đổ thành công dữ liệu vào bảng 'customers' trong Database.")
except FileNotFoundError:
    print(f"❌ Lỗi: Không tìm thấy file CSV tại {csv_path}. Bạn kiểm tra lại đường dẫn nhé!")
finally:
    # 4. Nhớ đóng cửa lại khi làm xong
    conn.close()