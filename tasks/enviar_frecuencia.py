import serial
import requests
import time

# Configura el puerto serial (ajusta 'COM7' según tu sistema operativo y puerto)
ser = serial.Serial('COM7', 9600)  # Ajusta el puerto y la velocidad según tu configuración

# URL de tu servidor Django
server_url = 'http://127.0.0.1:8000/api/frecuencia/'

print(f"Iniciando el script. Enviando datos a: {server_url}")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:
                frecuencia = float(line)
                print(f'Dato recibido desde Arduino: {frecuencia} BPM')
                data = {'frecuencia': frecuencia}
                response = requests.post(server_url, data=data)
                
                if response.status_code == 200:
                    print(f'Enviado correctamente. Respuesta del servidor: {response.text}')
                else:
                    print(f'Error al enviar. Código de estado: {response.status_code}')
            
            except ValueError:
                print(f'Dato no válido recibido desde Arduino: {line}')
    
    except Exception as e:
        print(f'Error en la comunicación serial: {e}')
    
    time.sleep(1)
    
