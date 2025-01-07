import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime, timedelta
import json
import os

def create_gradient(width, height, start_color, end_color):
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new("L", (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return ImageTk.PhotoImage(base)

def create_rounded_rectangle(width, height, radius, color, opacity):
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=color + (opacity,))
    return ImageTk.PhotoImage(image)

class CheckInOut:
    def __init__(self, root):
        self.root = root
        self.root.title("Check In")
        self.root.attributes("-fullscreen", True) 


        self.check_in_data = {}

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        

        gradient_bg = create_gradient(screen_width, screen_height, '#1a2a6c', '#f72585')
        bg_label = tk.Label(root, image=gradient_bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = gradient_bg 

  
        glass_frame = tk.Label(root, image=create_rounded_rectangle(400, 250, 30, (255, 255, 255), 128))
        glass_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(root, text="Check In", font=("Helvetica", 20, "bold"), bg="white", fg="#333")
        title_label.place(relx=0.5, rely=0.25, anchor="center")


        self.create_rounded_entry(0.5, 0.45)

        self.create_rounded_button("Check In", self.check_in, 0.45, 0.55, "#6a0dad")
        self.create_rounded_button("Check Out", self.check_out, 0.55, 0.55, "#d63384")

    def create_rounded_entry(self, relx, rely):
        entry_canvas = tk.Canvas(self.root, width=220, height=40, bg='white', highlightthickness=0)
        entry_canvas.place(relx=relx, rely=rely, anchor="center")


        entry_canvas.create_oval(0, 0, 20, 40, fill='white', outline='black', width=2)  
        entry_canvas.create_oval(200, 0, 220, 40, fill='white', outline='black', width=2) 
        entry_canvas.create_rectangle(20, 0, 200, 40, fill='white', outline='black', width=2)

     
        self.id_entry = tk.Entry(
            self.root, font=("Helvetica", 14), bd=0, justify="center", highlightthickness=0
        )
        self.id_entry.place(relx=relx, rely=rely, anchor="center", width=200, height=30)

    def create_rounded_button(self, text, command, relx, rely, color):
        button_canvas = tk.Canvas(self.root, width=100, height=40, bg='white', highlightthickness=0)
        button_canvas.place(relx=relx, rely=rely, anchor="center")

        button_canvas.create_oval(0, 0, 40, 40, fill=color, outline=color) 
        button_canvas.create_oval(60, 0, 100, 40, fill=color, outline=color)  
        button_canvas.create_rectangle(20, 0, 80, 40, fill=color, outline=color)

 
        button_canvas.create_text(50, 20, text=text, fill="white", font=("Helvetica", 12, "bold"))
        button_canvas.bind("<Button-1>", lambda event: command()) 

    def check_in(self):
        student_id = self.id_entry.get()
        if not student_id:
            print("Please enter a Student ID.")
            return

        if student_id in self.check_in_data:
            print(f"Student ID {student_id} is already checked in.")
            return

        self.check_in_data[student_id] = datetime.now()
        print(f"Checked in: {student_id} at {self.check_in_data[student_id]}")

        self.id_entry.delete(0, tk.END)

    def check_out(self):
        student_id = self.id_entry.get()
        if student_id not in self.check_in_data:
            print(f"No active check-in for Student ID {student_id}. Please check in first.")
            return

        check_out_time = datetime.now()
        time_spent = check_out_time - self.check_in_data[student_id]
        print(f"Checked out: {student_id} at {check_out_time}")
        print(f"Time spent: {time_spent}")

        self.log_time_data(student_id, self.check_in_data[student_id], check_out_time, time_spent)

        del self.check_in_data[student_id]

        self.id_entry.delete(0, tk.END)

    def log_time_data(self, student_id, check_in_time, check_out_time, time_spent):
        total_seconds = int(time_spent.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        formatted_time_spent = f"{hours}hrs {minutes}min {seconds}sec"

        compiled_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        check_in_str = check_in_time.strftime("%Y-%m-%d %H:%M:%S")
        check_out_str = check_out_time.strftime("%Y-%m-%d %H:%M:%S")
        time_spent_str = str(time_spent)

        data = {
            "check_in": f"Checked in: {student_id} at {check_in_str}",
            "check_out": f"Checked out: {student_id} at {check_out_str}",
            "time_spent": f"Time spent: {time_spent_str}",
        }

        # Define directory for logs
        log_directory = "Student_Logs"
        os.makedirs(log_directory, exist_ok=True)

        individual_filename = os.path.join(log_directory, f"{student_id}.json")
        master_filename = os.path.join(log_directory, "master_log.json")

        individual_records = {
            "compiled_time": 0.0,
            "logs": [],
        }

        if os.path.exists(individual_filename):
            with open(individual_filename, 'r') as f:
                individual_records = json.load(f)
                if isinstance(individual_records['compiled_time'], str):
                    try:
                        individual_records['compiled_time'] = float(individual_records['compiled_time'])
                    except ValueError:
                        individual_records['compiled_time'] = 0.0

        individual_records['logs'].append(data)

        individual_records['compiled_time'] += time_spent.total_seconds()

        with open(individual_filename, 'w') as f:
            json.dump(individual_records, f, indent=4)

        master_records = {"logs": []}

        if os.path.exists(master_filename) and os.path.getsize(master_filename) > 0:
            with open(master_filename, 'r') as f:
                try:
                    master_records = json.load(f)
                except json.JSONDecodeError:
                    print("Master log is corrupted or empty. Initializing new log.")
                    master_records = {"logs": []}

        student_compiled_time = individual_records['compiled_time']
        student_entry = {
            "student_id": student_id,
            "compiled_time": student_compiled_time
        }

        existing_entry = next((entry for entry in master_records["logs"] if entry["student_id"] == student_id), None)
        if existing_entry:
            existing_entry["compiled_time"] = student_compiled_time
        else:
            master_records['logs'].append(student_entry)

        with open(master_filename, 'w') as f:
            json.dump(master_records, f, indent=4)

        print(f"Logged data for student {student_id} at {compiled_time}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CheckInOut(root)
    root.mainloop()
