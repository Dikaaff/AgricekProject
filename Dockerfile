# Gunakan image python yang sudah pasti support distutils
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependensi sistem
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy semua file
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Jalankan aplikasi
CMD ["python", "app.py"]
