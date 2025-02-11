# PC-PicoW-Hardware-Monitor

A simple project to monitor your PC's CPU, GPU, and RAM usage and send the data to a Raspberry Pi Pico W, which hosts an HTTP server to receive and display the information.

## Features
- Reads CPU temperature, GPU temperature, and RAM usage from a Windows PC.
- Sends the data as JSON to a Raspberry Pi Pico W.
- Pico W receives and processes the data through a simple HTTP server.
- LED on the Pico W blinks while waiting and stays on when receiving data.

## Requirements
### PC (Sender)
- Windows PC with **OpenHardwareMonitor** installed, download here: https://openhardwaremonitor.org/downloads/
- Python 3 installed
- Required Python libraries:
  ```sh
  pip install wmi requests
  ```

### Raspberry Pi Pico W (Receiver)
- MicroPython installed on the Pico W
- Required MicroPython libraries:
  - `network`
  - `socket`
  - `ujson`
  - `machine`

## Setup Guide

### 1. Configure the Raspberry Pi Pico W
1. Flash **MicroPython** onto your Pico W if you haven't already.
2. Copy `pico_server.py` onto your Pico W and modify the WiFi credentials:
   ```python
   ssid = 'Your Wifi SSID'
   password = 'Your Wifi password'
   ```
3. Run `pico_server.py` on the Pico W.
4. Note down the IP address shown in the console (e.g., `192.168.0.33`).

### 2. Configure the PC Script
1. Install **OpenHardwareMonitor** and ensure it is running.
2. Copy `pc_sender.py` to your PC.
3. Update the URL in `pc_sender.py` to match the Pico W’s IP address:
   ```python
   url = "http://192.168.0.33/update_temperature"
   ```
4. Run `pc_sender.py` to start sending data.

## How It Works
1. The PC reads the CPU, GPU, and RAM data using **OpenHardwareMonitor**.
2. The script sends the data to the Pico W every 5 seconds via HTTP POST.
3. The Pico W receives the data and prints it to the console.
4. The LED on the Pico W indicates data reception status.

## Example Output
### PC Console Output
```
CPU: 45.0°C, GPU: 50.0°C, Used RAM: 12.5GB, Total RAM: 32.0GB
Sent: CPU: 45.0°C, GPU: 50.0°C, Used RAM: 12.5GB, Total RAM: 32.0GB
Response from Pico W: 200 OK
```

### Pico W Console Output
```
Connection from ('192.168.0.50', 54032)
Received JSON data: {'cpu_temp': 45.0, 'gpu_temp': 50.0, 'ram_used': 12.5, 'ram_total': 32.0}
```

## Future Enhancements
- Display the data on a web interface.
- Store historical data.
- Add alerts if temperature exceeds a threshold.
- Extend the project by connecting the Pico W to an **ePaper display** or a **lightweight LCD** to show real-time data.
- Create a **detailed web dashboard** to visualize statistics and trends over time.
- The possibilities are open—it's up to you how you want to use the data!

## License
This project is open-source under the MIT License.

---
Happy Monitoring! 🚀

