import psutil
import time
from datetime import datetime
import os
from pynput import keyboard, mouse
import openai

# Configura tu clave API de OpenAI aquí
openai.api_key = 'tu-clave-api'

class UsageTracker:
    def __init__(self, history_dir="history", interval=60):
        self.history_dir = history_dir   # Directorio donde se guardará el historial
        self.interval = interval         # Intervalo de tiempo entre cada registro de procesos
        self.history = []                # Lista para almacenar el historial de uso
        self.key_history = []            # Lista para almacenar el historial de teclas presionadas
        self.mouse_history = []          # Lista para almacenar el historial de movimientos y clics del ratón

        # Crear el directorio si no existe
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

    def get_process_info(self):
        processes = []
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(process.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes

    def save_history(self, filename, history):
        with open(filename, 'w') as file:
            for entry in history:
                file.write(f"{entry}\n")

    def on_press(self, key):
        try:
            self.key_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Key pressed: {key.char}")
        except AttributeError:
            self.key_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Key pressed: {key}")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Mouse clicked at ({x}, {y}) with {button}")
        else:
            self.mouse_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Mouse released at ({x}, {y}) with {button}")

    def on_move(self, x, y):
        self.mouse_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Mouse moved to ({x}, {y})")

    def start_listeners(self):
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)

        keyboard_listener.start()
        mouse_listener.start()

    def track_usage(self):
        self.start_listeners()

        try:
            while True:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                process_info = self.get_process_info()
                self.history.append(f"Timestamp: {current_time}")
                for info in process_info:
                    self.history.append(f"PID: {info['pid']}, Name: {info['name']}, CPU: {info['cpu_percent']}%, Memory: {info['memory_percent']}%")
                
                # Crear carpeta diaria
                today = datetime.now().strftime("%Y-%m-%d")
                day_history_dir = os.path.join(self.history_dir, f"history_{today}")
                if not os.path.exists(day_history_dir):
                    os.makedirs(day_history_dir)

                # Guardar historial en archivos de texto por día
                process_filename = os.path.join(day_history_dir, "process_history.txt")
                key_filename = os.path.join(day_history_dir, "key_history.txt")
                mouse_filename = os.path.join(day_history_dir, "mouse_history.txt")

                self.save_history(process_filename, self.history)
                self.save_history(key_filename, self.key_history)
                self.save_history(mouse_filename, self.mouse_history)

                # Limpiar los historiales para el próximo intervalo
                self.history.clear()
                self.key_history.clear()
                self.mouse_history.clear()

                # Esperar el intervalo especificado antes de la siguiente captura
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Tracking stopped by user.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def download_history(self, date):
        day_history_dir = os.path.join(self.history_dir, f"history_{date}")
        process_filename = os.path.join(day_history_dir, "process_history.txt")
        key_filename = os.path.join(day_history_dir, "key_history.txt")
        mouse_filename = os.path.join(day_history_dir, "mouse_history.txt")

        if os.path.exists(process_filename):
            with open(process_filename, 'r') as file:
                print("Process History:\n")
                print(file.read())
        else:
            print(f"No process history found for date: {date}")

        if os.path.exists(key_filename):
            with open(key_filename, 'r') as file:
                print("Key History:\n")
                print(file.read())
        else:
            print(f"No key history found for date: {date}")

        if os.path.exists(mouse_filename):
            with open(mouse_filename, 'r') as file:
                print("Mouse History:\n")
                print(file.read())
        else:
            print(f"No mouse history found for date: {date}")

    def ask_chatgpt(self, question):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def run(self):
        while True:
            print("1. Start tracking usage")
            print("2. Download history")
            print("3. Ask ChatGPT")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.interval = int(input("Enter the tracking interval in seconds: "))
                print("Tracking usage. Press Ctrl+C to stop.")
                self.track_usage()
            elif choice == '2':
                date = input("Enter the date (YYYY-MM-DD) to download history: ")
                self.download_history(date)
            elif choice == '3':
                question = input("Enter your question for ChatGPT: ")
                answer = self.ask_chatgpt(question)
                print(f"ChatGPT Response:\n{answer}")
            elif choice == '4':
                print("Exiting.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tracker = UsageTracker()
    tracker.run()
