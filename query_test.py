import sqlite3
import pandas as pd
# 1. Mở cửa vào Database
conn = sqlite3.connect("company_data.db")
cursor = conn.cursor()

# 2. Viết truy vấn SQL (Ví dụ: Cập nhật tên khách hàng)

sql_query = "select * from customers"
df=pd.read_sql(sql_query,conn)
# 3. Thực thi lệnh
cursor.execute(sql_query)

# 4. BƯỚC SỐNG CÒN: Lưu lại thay đổi (Chỉ dùng khi UPDATE, INSERT, DELETE)
print(df.to_string())

# 5. Đóng cửa
conn.close()