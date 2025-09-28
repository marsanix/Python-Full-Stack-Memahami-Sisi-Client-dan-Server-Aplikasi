# Konfigurasi Database untuk Praktik Pertemuan 1
# Mendukung environment Docker dan local development

import os

# Konfigurasi Database
# Menggunakan environment variables jika tersedia (untuk Docker)
# Fallback ke konfigurasi local jika tidak ada

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME', 'python_fullstack_smp'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'toor'),
    'charset': 'utf8mb4',
    'autocommit': True,
    'raise_on_warnings': True
}

# Flask Configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'kunci_rahasia_untuk_flash_message')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    
    # Database URL untuk SQLAlchemy (jika diperlukan di masa depan)
    DATABASE_URL = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Development Configuration
class DevelopmentConfig(Config):
    DEBUG = True
    
# Production Configuration  
class ProductionConfig(Config):
    DEBUG = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}