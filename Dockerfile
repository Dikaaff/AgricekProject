# Gunakan Python versi stabil
FROM python:3.10-slim

# Set workdir di dalam container
WORKDIR /app

# Install dependensi sistem yang diperlukan untuk numpy, opencv, dll
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Salin semua file dari project ke container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port Railway
ENV PORT 5000
EXPOSE 5000

# Jalankan app.py
CMD ["python", "app.py"]
