# Dockerfile untuk Praktik Pertemuan 1
# Aplikasi CRUD Flask dengan MySQL

# Menggunakan Python 3.11 sebagai base image
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Install system dependencies yang diperlukan untuk MySQL connector
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt terlebih dahulu untuk memanfaatkan Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file aplikasi ke container
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port 5000 untuk Flask
EXPOSE 5000

# Health check untuk memastikan aplikasi berjalan
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Command untuk menjalankan aplikasi
# Menggunakan python langsung karena file utama ada di parent directory
CMD ["python", "app.py"]