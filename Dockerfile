# 1. Bắt đầu từ một hệ điều hành Linux có cài sẵn Python (Siêu nhẹ)
FROM python:3.10-slim

# 2. Tạo một thư mục làm việc bên trong Container tên là /app
WORKDIR /app

# 3. Copy file đồ nghề vào trước và dán lệnh cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy toàn bộ code của bạn (app.py, main.py, thư mục templates...) vào trong Container
COPY . .

# 5. Mở cổng 5000 để web có thể giao tiếp với bên ngoài
EXPOSE 5000

# 6. Nút bấm khởi động: Lệnh để chạy Server Flask khi Container bật lên
CMD ["python", "app.py"]