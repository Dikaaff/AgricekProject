# Gunakan base image resmi Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Salin semua file ke dalam container
COPY . .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose port (Railway biasanya pakai PORT env)
ENV PORT=5000
EXPOSE $PORT

# Jalankan aplikasi
CMD ["python", "app.py"]
