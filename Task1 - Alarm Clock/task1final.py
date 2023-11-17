import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import winsound

class AlarmClock:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Alarm Clock")
        self.master.geometry("400x200")

        self.style = ttk.Style()
        self.style.theme_use("vista")  # You can change the theme (e.g., "vista", "winnative")

        self.label = ttk.Label(self.master, text="Set Alarm (24-hour format):", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.master, font=("Helvetica", 14))
        self.entry.pack(pady=10)

        self.set_button = ttk.Button(self.master, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=20)

        # Additional Labels for showing alarm status and countdown
        self.status_label = ttk.Label(self.master, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.countdown_label = ttk.Label(self.master, text="", font=("Arial", 12, "bold"))
        self.countdown_label.pack(pady=10)

    def set_alarm(self):
        alarm_time_str = self.entry.get()

        try:
            current_time = datetime.now()
            alarm_time = datetime.strptime(alarm_time_str, "%H:%M")
            alarm_datetime = datetime(current_time.year, current_time.month, current_time.day, alarm_time.hour, alarm_time.minute)

            # Check if the alarm time is in the future
            if alarm_datetime < current_time:
                alarm_datetime = alarm_datetime.replace(year=current_time.year, month=current_time.month, day=current_time.day + 1)

            time_difference = alarm_datetime - current_time

            if time_difference.total_seconds() > 0:
                self.master.after(1000, lambda: self.update_countdown(alarm_datetime))  # Update countdown every second
                self.label.config(text=f"Alarm set for {alarm_time_str}")
                self.status_label.config(text="Alarm is set!")
            else:
                self.status_label.config(text="Please set a future time.")
        except ValueError:
            self.status_label.config(text="Invalid time format. Use HH:MM")

    def update_countdown(self, alarm_time):
        current_time = datetime.now()
        time_difference = alarm_time - current_time

        if time_difference.total_seconds() > 0:
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown_str = f"Time Left: {hours:02}:{minutes:02}:{seconds:02}"
            self.countdown_label.config(text=countdown_str)
            self.master.after(1000, lambda: self.update_countdown(alarm_time))
        else:
            self.trigger_alarm()

    def trigger_alarm(self):
        self.label.config(text="Alarm! Wake up!", foreground="red")  # Change text color to red
        self.status_label.config(text="Alarm is ringing!", foreground="red")
        winsound.Beep(1000, 2000)  # Plays a system beep sound for 2 seconds

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="white")  # Set background color
    alarm_clock = AlarmClock(root)
    root.mainloop()
