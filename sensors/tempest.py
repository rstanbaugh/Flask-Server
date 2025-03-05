import os
import json
import socket
import requests
import threading
import signal

# Constants
STATION_ID = 161526  # Hardcoded station ID
API_KEY = os.getenv("TEMPEST_API_KEY")
API_URL = f"https://swd.weatherflow.com/swd/rest/observations/station/{STATION_ID}?api_key={API_KEY}"
UDP_PORT = 50222

# Global storage for weather data
weather_data = None

# Thread-safe event for stopping loops
stop_event = threading.Event()

def get_weather():
    """Fetch weather data from the API and return it."""
    global weather_data

    if weather_data:  # ✅ If data exists from UDP, return it
        return weather_data

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        weather_data = response.json()  # ✅ Store data globally
        print("Initial Weather Data:", json.dumps(weather_data, indent=2))
        return weather_data  # ✅ Return fetched data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"error": "Failed to fetch data"}

def listen_udp():
    """Listen for weather updates over UDP and update global weather_data."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", UDP_PORT))
    print(f"Listening for UDP data on port {UDP_PORT}...")

    while not stop_event.is_set():
        try:
            data, _ = udp_socket.recvfrom(4096)
            message = json.loads(data.decode("utf-8"))
            print("Received UDP update:", message)
            global weather_data
            weather_data = message  # ✅ Store received UDP data
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("Received malformed UDP data")
        except OSError:
            break

    udp_socket.close()
    print("UDP listener stopped.")

def key_listener():
    """Listen for key input to terminate the program."""
    print("\nPress 'q' to quit...")
    while not stop_event.is_set():
        user_input = input().strip().lower()
        if user_input == "q":
            stop_event.set()
            break

# Graceful shutdown on Ctrl+C
def signal_handler(sig, frame):
    print("\nShutting down.")
    stop_event.set()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    print("Fetching initial weather data...")
    get_weather()

    # Start UDP listener in a separate thread
    udp_thread = threading.Thread(target=listen_udp, daemon=True)
    udp_thread.start()

    # Start key listener in the main thread
    key_listener()

    udp_thread.join()
    print("Exited gracefully.")