import requests
import random
import time

API_URL = "http://127.0.0.1:8000/assets/"

# Definimos 4 servidores fijos para simular una infraestructura real
servidores = [
    {"hostname": "Servidor-Finanzas-01", "ip": "192.168.1.50", "os": "Ubuntu 22.04"},
    {"hostname": "Servidor-RRHH-02", "ip": "192.168.1.51", "os": "Windows Server 2019"},
    {"hostname": "Gateway-Principal", "ip": "10.0.0.1", "os": "Cisco IOS"},
    {"hostname": "DB-Clientes", "ip": "192.168.1.100", "os": "RedHat Enterprise"}
]

riesgos = ["Bajo", "Medio", "Alto", "Crítico"]

def simular_ataques():
    print("Iniciando monitoreo activo de infraestructura...")
    
    while True:
        # 1. Elegir un servidor al azar de nuestra lista
        objetivo = random.choice(servidores)
        
        # 2. Asignarle un nuevo riesgo aleatorio
        nuevo_riesgo = random.choice(riesgos)
        
        payload = {
            "hostname": objetivo["hostname"],
            "ip_address": objetivo["ip"],
            "os_type": objetivo["os"],
            "risk_level": nuevo_riesgo
        }
        
        try:
            # Enviamos la actualización a la API
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                print(f"ACTUALIZADO: {objetivo['hostname']} -> Nivel: {nuevo_riesgo}")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Servidor caído (API no responde): {e}")
            
        # Esperar entre 2 y 5 segundos antes del siguiente cambio
        time.sleep(random.randint(2, 5))

if __name__ == "__main__":
    simular_ataques()