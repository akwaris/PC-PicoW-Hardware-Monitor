import wmi
import time
import requests

# Connection to OpenHardwareMonitor
w = wmi.WMI(namespace="root/OpenHardwareMonitor")

# URL of the Pico W Server
url = "http://192.168.0.33/update_temperature"
headers = {'Content-Type': 'application/json'}

# Endless Loop to get the values and send them
while True:
    cpu_temp = None
    gpu_temp = None
    ram_used = None
    ram_total = 32.00

    # Going through all Sensors and find the ones we need
    infos = w.Sensor()
    for sensor in infos:
        if sensor.SensorType == "Temperature":
            if "CPU" in sensor.Name and cpu_temp is None:
                cpu_temp = sensor.Value
            if "GPU" in sensor.Name and gpu_temp is None:
                gpu_temp = sensor.Value

        if sensor.SensorType == "Data":
            if "Used Memory" in sensor.Name and ram_used is None:
                ram_used = sensor.Value

        # Break the loop if all values are found
        if cpu_temp is not None and gpu_temp is not None and ram_used is not None:
            break

    # Summarizing the values
    if cpu_temp is not None and gpu_temp is not None and ram_used is not None:
        message = (f"CPU: {cpu_temp}°C, GPU: {gpu_temp}°C, Used RAM: {ram_used:.2f}GB, Total RAM: {ram_total}")
        data = {'cpu_temp': cpu_temp,
                'gpu_temp': gpu_temp,
                'ram_used': round(ram_used,2),
                'ram_total': ram_total    
        }
        print(message)

        try:
            # HTTP POST Request to the Pico W
            response = requests.post(url, json=data, headers=headers)
            print("Sent:", message)
            print("Response from Pico W:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to Pico W: {e}")


    # Interval of 5 seconds
    time.sleep(5)
