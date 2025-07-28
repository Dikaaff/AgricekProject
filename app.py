from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
import io
import base64
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# API Keys
<<<<<<< HEAD
OPENWEATHER_API_KEY = "secret"
DEEPSEEK_API_KEY = "secret"
=======
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
>>>>>>> 73621cf (Update API key system and environment variable support)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_with_ai():
    try:
        data = request.get_json()
        message = data.get('message', '')

        # OpenRouter API config
<<<<<<< HEAD
        OPENROUTER_API_KEY = "secret"
=======
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
>>>>>>> 73621cf (Update API key system and environment variable support)
        OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'openai/gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'system',
                    'content': 'Anda adalah ahli agronomi Indonesia yang membantu petani. Jawab hanya pertanyaan tentang pertanian, tanaman, hama, pupuk, dan budidaya dalam bahasa Indonesia yang mudah dipahami petani.'
                },
                {
                    'role': 'user',
                    'content': message
                }
            ],
            'max_tokens': 500,
            'temperature': 0.7
        }

        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            reply = response_data['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        else:
            return jsonify({'error': f'Chatbot gagal merespons. Kode: {response.status_code}'}), 500

    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan pada sistem chat: {str(e)}'}), 500
    
@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        data = request.get_json()
        location = data.get('location', '')

        # Dapatkan koordinat dari nama kota
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPENWEATHER_API_KEY}"
        geo_response = requests.get(geocoding_url)
        geo_data = geo_response.json()

        if not geo_data:
            return jsonify({'error': 'Lokasi tidak ditemukan'}), 404

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Ambil data cuaca
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=id"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        # Ambil info penting
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']

        # Buat rekomendasi
        recommendation = generate_farming_recommendation(temperature, humidity, wind_speed, description)

        return jsonify({
            'location': geo_data[0]['name'],
            'temperature': round(temperature, 1),
            'humidity': humidity,
            'wind_speed': round(wind_speed, 1),
            'description': description,
            'icon': icon,
            'recommendation': recommendation
        })

    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan koneksi: {str(e)}'}), 500




@app.route('/analyze-plant', methods=['POST'])
def analyze_plant():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Tidak ada gambar yang diunggah'}), 400
            
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'File tidak valid'}), 400
            
        # Read and process image
        image_data = file.read()
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Format gambar tidak didukung'}), 400
            
        # Simple plant analysis (placeholder - you can integrate with ML models)
        analysis_result = analyze_plant_health(img)
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'error': 'Terjadi kesalahan saat menganalisis gambar'}), 500

def generate_farming_recommendation(temp, humidity, wind_speed, weather_desc):
    """Generate farming recommendation based on weather conditions"""
    recommendations = []
    
    # Temperature recommendations
    if temp >= 25 and temp <= 30:
        recommendations.append("🌱 Suhu ideal untuk sebagian besar tanaman")
    elif temp > 30:
        recommendations.append("🌡️ Suhu tinggi - perbanyak penyiraman")
    elif temp < 20:
        recommendations.append("❄️ Suhu rendah - lindungi tanaman sensitif")
    
    # Humidity recommendations
    if humidity >= 60 and humidity <= 80:
        recommendations.append("💧 Kelembapan baik untuk pertumbuhan")
    elif humidity > 80:
        recommendations.append("⚠️ Kelembapan tinggi - waspada penyakit jamur")
    elif humidity < 40:
        recommendations.append("🏜️ Udara kering - tingkatkan penyiraman")
    
    # Weather-based recommendations
    if 'hujan' in weather_desc.lower():
        recommendations.append("🌧️ Hujan - tunda penyemprotan pestisida")
    elif 'cerah' in weather_desc.lower():
        recommendations.append("☀️ Cuaca cerah - waktu baik untuk panen")
    
    return recommendations

def analyze_plant_health(image):
    """Simple plant health analysis using OpenCV"""
    # Convert to HSV for better color analysis
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define green color range (healthy plants)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    
    # Define yellow/brown range (potentially unhealthy)
    lower_yellow = np.array([15, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    
    # Create masks
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Calculate percentages
    total_pixels = image.shape[0] * image.shape[1]
    green_pixels = np.sum(green_mask > 0)
    yellow_pixels = np.sum(yellow_mask > 0)
    
    green_percentage = (green_pixels / total_pixels) * 100
    yellow_percentage = (yellow_pixels / total_pixels) * 100
    
    # Generate analysis result
    if green_percentage > 30:
        health_status = "Sehat"
        recommendations = [
            "🌱 Tanaman terlihat sehat",
            "💧 Lanjutkan pola penyiraman rutin",
            "🌞 Pastikan mendapat sinar matahari cukup"
        ]
    elif yellow_percentage > 20:
        health_status = "Perlu Perhatian"
        recommendations = [
            "⚠️ Terdeteksi daun menguning",
            "💧 Periksa sistem penyiraman",
            "🧪 Pertimbangkan pemupukan",
            "🔍 Periksa adanya hama atau penyakit"
        ]
    else:
        health_status = "Kurang Optimal"
        recommendations = [
            "🚨 Tanaman memerlukan perawatan khusus",
            "💧 Sesuaikan jadwal penyiraman",
            "🌱 Pertimbangkan penggantian media tanam",
            "👨‍🌾 Konsultasi dengan ahli pertanian"
        ]
    
    return {
        'health_status': health_status,
        'green_percentage': round(green_percentage, 1),
        'yellow_percentage': round(yellow_percentage, 1),
        'recommendations': recommendations
    }

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
=======
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
>>>>>>> 73621cf (Update API key system and environment variable support)
