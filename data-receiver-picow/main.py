import network
import socket
import ujson
import time
from machine import Pin
from time import sleep

# Initialization of the onboard LED
led_onboard = Pin("LED", Pin.OUT)

# Connect the Pico W to the WiFi
def connect_wifi():
    ssid = 'Your Wifi SSID' 
    password = 'Your Wifi password' 

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to WiFi...')
        # Toggle LED state (ON/OFF)
        led_onboard.toggle()
        # Wait 1 second
        sleep(1)

    print('WiFi connected:', wlan.ifconfig())
    # Turn off the LED after the connection is established
    led_onboard.value(0)

# HTTP server on the Pico W
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('Waiting for connections on', addr)

    while True:
        waiting = True
        while waiting:
            led_onboard.value(0)
            sleep(3)
            try:
                cl, addr = s.accept()
                waiting = False  # Request received, stop blinking
                led_onboard.value(1)  # LED stays on while processing the request
                print('Connection from', addr)
                request = cl.recv(1024)
                print('Request:', request)
        
                # If the request contains temperature data
                if request:
                    try:
                        headers, body = request.decode().split('\r\n\r\n', 1)  # Separate headers and body
                        content_length = int(next(h.split(":")[1].strip() for h in headers.split('\r\n') if "Content-Length" in h))
    
                        if len(body) < content_length:
                            body += cl.recv(content_length - len(body)).decode()  # Read the remaining body if necessary
                        
                        # Load JSON data into a dictionary
                        json_data = ujson.loads(body)
                        print("Received JSON data:", json_data)
                        
                        # Here you could process the received data further
                        # But the Pico W only sends back a confirmation
                        response = (f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK")
                    except Exception as e:
                        print(f"Error processing data: {e}")
                        response = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nError"
                else:
                    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot found"
                
                cl.send(response)
                cl.close()
            except OSError:
                pass  # No connection received, continue blinking

# Main logic
connect_wifi()
start_server()
