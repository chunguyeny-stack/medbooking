FROM python:3.11-slim

WORKDIR /app

# Cài dependencies hệ thống cần thiết cho pymssql
# - gcc: Trình biên dịch C
# - freetds-dev: Thư viện kết nối SQL Server (thay thế cho unixodbc-dev)
RUN apt-get update && apt-get install -y \
    gcc \
    freetds-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt và cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code backend vào container
COPY . .

# Mở port 8000
EXPOSE 8000

# Chạy FastAPI với uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]