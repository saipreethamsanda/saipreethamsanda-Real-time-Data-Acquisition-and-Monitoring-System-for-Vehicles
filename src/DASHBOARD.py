import tkinter as tk
import serial
import threading
import time
import math

SERIAL_PORT = 'COM5'
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")

        # Create frames for each section
        self.brake_frame = tk.Frame(root)
        self.brake_frame.grid(row=0, column=1, pady=10)

        self.temp_frame = tk.Frame(root)
        self.temp_frame.grid(row=1, column=0, padx=20, pady=20)

        self.center_frame = tk.Frame(root)
        self.center_frame.grid(row=1, column=1, padx=20, pady=20)

        self.fuel_frame = tk.Frame(root)
        self.fuel_frame.grid(row=1, column=2, padx=20, pady=20)

        # Create temperature display
        self.create_temperature_display(self.temp_frame)

        # Create speed and RPM gauges
        self.create_speed_rpm_gauges(self.center_frame)

        # Create fuel level display
        self.create_fuel_display(self.fuel_frame)

        # Create brake status display
        self.create_brake_display(self.brake_frame)

        # Start threads to read data from Arduino/Nucleo
        threading.Thread(target=self.read_arduino_data, daemon=True).start()

    def create_temperature_display(self, frame):
        self.temp_canvas = tk.Canvas(frame, width=160, height=300, bg="white")
        self.temp_canvas.pack(pady=20)
        self.temp_canvas.create_rectangle(60, 100, 100, 300, outline="black")
        self.temperature_label = tk.Label(frame, text="Waiting for data...", font=("Helvetica", 24))
        self.temperature_label.pack()
        self.warning_label = tk.Label(frame, text="", font=("Helvetica", 16, "bold"))
        self.warning_label.pack(pady=10)

    def create_speed_rpm_gauges(self, frame):
        self.rpm_canvas = tk.Canvas(frame, width=300, height=300)
        self.rpm_canvas.grid(row=0, column=0, padx=20, pady=20)
        self.draw_gauge(self.rpm_canvas, "RPM", 8000)
        self.speed_canvas = tk.Canvas(frame, width=300, height=300)
        self.speed_canvas.grid(row=0, column=1, padx=20, pady=20)
        self.draw_gauge(self.speed_canvas, "Speed", 240)
        self.rpm_label = tk.Label(frame, text="RPM: --", font=("Helvetica", 14))
        self.rpm_label.grid(row=1, column=0, pady=10)
        self.speed_label = tk.Label(frame, text="Speed: -- km/h", font=("Helvetica", 14))
        self.speed_label.grid(row=1, column=1, pady=10)

    def create_fuel_display(self, frame):
        self.fuel_canvas = tk.Canvas(frame, width=160, height=300, bg="white")
        self.fuel_canvas.pack(pady=20)
        self.fuel_canvas.create_rectangle(60, 100, 100, 300, outline="black")
        self.fuel_status_label = tk.Label(frame, text="", font=("Helvetica", 16, "bold"))
        self.fuel_status_label.pack(pady=10)

    def create_brake_display(self, frame):
        self.brake_status_label = tk.Label(frame, text="Brakes Not Applied", font=("Helvetica", 24), bg="green", fg="black", width=20, height=3)
        self.brake_status_label.pack()

    def draw_gauge(self, canvas, label, max_value):
        canvas.create_oval(50, 50, 250, 250, outline="black", width=2)
        for angle in range(-210, 31, 10):
            x1 = 150 + 100 * math.cos(math.radians(angle))
            y1 = 150 + 100 * math.sin(math.radians(angle))
            x2 = 150 + 90 * math.cos(math.radians(angle))
            y2 = 150 + 90 * math.sin(math.radians(angle))
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            if angle % 30 == 0:
                tick_label = int((angle + 210) / 240 * max_value)
                x_text = 150 + 80 * math.cos(math.radians(angle))
                y_text = 150 + 80 * math.sin(math.radians(angle))
                canvas.create_text(x_text, y_text, text=str(tick_label), font=("Arial", 12))
        needle = canvas.create_line(150, 150, 150, 50, fill="red", width=2)
        if label == "RPM":
            self.rpm_needle = needle
            self.rpm_canvas = canvas
        else:
            self.speed_needle = needle
            self.speed_canvas = canvas

    def update_temperature_display(self, temperature):
        self.temperature_label.config(text=f"{temperature} °C")
        level = int((temperature / 50) * 200)
        self.temp_canvas.delete("thermometer_fill")
        self.temp_canvas.create_rectangle(60, 300 - level, 100, 300, fill="red" if temperature > 38 else "blue", outline="black", tag="thermometer_fill")
        if temperature > 38:
            self.warning_label.config(text="High Temperature Warning!", fg="red", font=("Helvetica", 16, "bold"))
        else:
            self.warning_label.config(text="")

    def update_rpm_gauge(self, rpm):
        angle = -120 + 240 * rpm / 8000
        x = 150 + 100 * math.cos(math.radians(angle - 90))
        y = 150 + 100 * math.sin(math.radians(angle - 90))
        self.rpm_canvas.coords(self.rpm_needle, 150, 150, x, y)
        self.rpm_label.config(text=f"RPM: {rpm}")

    def update_speed_gauge(self, speed_kmph):
        angle = -120 + 240 * speed_kmph / 240
        x = 150 + 100 * math.cos(math.radians(angle - 90))
        y = 150 + 100 * math.sin(math.radians(angle - 90))
        self.speed_canvas.coords(self.speed_needle, 150, 150, x, y)
        self.speed_label.config(text=f"Speed: {speed_kmph:.2f} km/h")

    def update_fuel_display(self, level):
        height = int((level / 1023) * 200)
        if height < 100:
            color = "red"
            label_text = "Very Low"
        elif height < 150:
            color = "orange"
            label_text = "Low"
        elif height < 350:
            color = "yellow"
            label_text = "Medium"
        elif height < 450:
            color = "light green"
            label_text = "High"
        else:
            color = "green"
            label_text = "Very High"
        self.fuel_canvas.delete("thermometer_fill")
        self.fuel_canvas.create_rectangle(60, 300 - height, 100, 300, fill=color, outline="black", tag="thermometer_fill")
        self.fuel_status_label.config(text=label_text, fg=color)

    def update_brake_display(self, status):
        if status == "brakes are working":
            self.brake_status_label.config(text="Brakes Working", bg="red", fg="white")
            self.root.after(1000, self.reset_brake_display)  # Reset to green after 1 second
        else:
            self.brake_status_label.config(text="Brakes Not Applied", bg="green", fg="black")

    def reset_brake_display(self):
        self.brake_status_label.config(text="Brakes Not Applied", bg="green", fg="black")

    def read_arduino_data(self):
        while True:
            if ser.in_waiting > 0:
                arduino_data = ser.readline().decode('utf-8').rstrip()
                print(f"Received data: {arduino_data}")
                try:
                    if "Temperature:" in arduino_data:
                        temperature = float(arduino_data.split(":")[1].strip().rstrip('C'))
                        self.update_temperature_display(temperature)
                    elif "Water Level Sensor Value:" in arduino_data:
                        level = int(arduino_data.split(":")[1].strip())
                        self.update_fuel_display(level)
                    elif "RPM:" in arduino_data:
                        rpm_part = arduino_data.split('|')[0].strip()
                        rpm = int(rpm_part.split(':')[1].strip())
                        self.update_rpm_gauge(rpm)
                        speed_part = arduino_data.split('|')[1].strip()
                        speed_kmph = float(speed_part.split(':')[1].strip().split()[0])
                        self.update_speed_gauge(speed_kmph)
                    elif arduino_data == "brakes are working":
                        self.update_brake_display("brakes are working")
                    else:
                        self.update_brake_display("Brakes Not Applied")
                except Exception as e:
                    print(f"Error: {e}")

            time.sleep(0.1)

def main():
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
