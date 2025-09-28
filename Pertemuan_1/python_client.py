import requests

# Meminta data dari server
response = requests.get('http://127.0.0.1:5000')
print(response.text)  # Akan mencetak: "Halo! Ini adalah server Python!"