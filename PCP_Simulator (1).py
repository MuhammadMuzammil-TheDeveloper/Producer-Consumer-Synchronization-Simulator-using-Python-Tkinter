import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

# Global variables:
buffer_size = 6
buffer = []

mutex = threading.Semaphore(1)
empty = threading.Semaphore(buffer_size)
full = threading.Semaphore(0)
running = False

# Main window:
root = tk.Tk() # creates the main application window
root.title("Process Synchronization Simulator")
root.state("zoomed")
root.configure(bg="#1e1e2f")

# Title:
title = tk.Label(
    root,
    text="Producer Consumer Synchronization Simulator",
    font=("Arial", 22, "bold"),
    bg="#1e1e2f",
    fg="white"
)
title.pack(pady=15)

# Main layout:
main_frame = tk.Frame(root, bg="#1e1e2f")
main_frame.pack(fill="both", expand=True)

# Left control panel:
left_panel = tk.Frame(
    main_frame,
    bg="#25253a", width=250
)
left_panel.pack(side="left", fill="y")

# Right content panel:
right_panel = tk.Frame(
    main_frame,
    bg="#1e1e2f"
)
right_panel.pack(
    side="right",
    fill="both",
    expand=True
)

# Buffer frame:
buffer_frame = tk.Frame(right_panel, bg="#1e1e2f")
buffer_frame.pack(pady=15)
buffer_boxes = []
for i in range(buffer_size):
    box = tk.Label(
        buffer_frame,
        text="EMPTY", width=10, height=4, bg="white", relief="solid", font=("Arial", 12, "bold")
    )
    box.grid(row=0, column=i, padx=10)
    buffer_boxes.append(box)

# Status frame:
status_frame = tk.Frame(right_panel, bg="#1e1e2f")
status_frame.pack(pady=10)

producer_status = tk.Label(
    status_frame,
    text="Producer Status : Waiting", font=("Arial", 13, "bold"), bg="#1e1e2f", fg="#00ffcc"
)
producer_status.grid(row=0, column=0, padx=50)

consumer_status = tk.Label(
    status_frame,
    text="Consumer Status : Waiting", font=("Arial", 13, "bold"), bg="#1e1e2f", fg="#ffcc00"
)
consumer_status.grid(row=0, column=1, padx=50)
# Buffer state:
buffer_state = tk.Label(
    right_panel,
    text="Buffer State : EMPTY", font=("Arial", 15, "bold"), bg="#1e1e2f", fg="white"
)
buffer_state.pack(pady=10)

# Left control section:
control_title = tk.Label(
    left_panel,
    text="CONTROL PANEL", font=("Arial", 16, "bold"), bg="#25253a", fg="white"
)
control_title.pack(pady=20)

# Speed control frame:
speed_frame = tk.Frame(left_panel, bg="#25253a")
speed_frame.pack(pady=20)

# Producer speed scale:
producer_scale_label = tk.Label(
    speed_frame,
    text="Producer Speed", font=("Arial", 12, "bold"), bg="#25253a", fg="#00ffcc"
)
producer_scale_label.pack(pady=5)
producer_scale = tk.Scale(
    speed_frame,
    from_=1, to=5, orient="horizontal", bg="#25253a", fg="white", troughcolor="#333", highlightthickness=0, length=180
)
producer_scale.set(3)
producer_scale.pack(pady=10)

# Consumer speed scale:
consumer_scale_label = tk.Label(
    speed_frame,
    text="Consumer Speed", font=("Arial", 12, "bold"), bg="#25253a", fg="#ffcc00"
)
consumer_scale_label.pack(pady=5)
consumer_scale = tk.Scale(
    speed_frame,
    from_=1, to=5, orient="horizontal", bg="#25253a", fg="white", troughcolor="#333", highlightthickness=0, length=180
)
consumer_scale.set(2)
consumer_scale.pack(pady=10)

# Event log:
log_label = tk.Label(
    right_panel,
    text="Event Log", font=("Arial", 16, "bold"), bg="#1e1e2f", fg="white"
)
log_label.pack()
log_box = tk.Text(
    right_panel,
    height=16, width=100, font=("Consolas", 11), bg="black", fg="white"
)
log_box.pack(pady=10)

# Log colors:
log_box.tag_config("producer", foreground="lime")
log_box.tag_config("consumer", foreground="cyan")
log_box.tag_config("system", foreground="yellow")

def update_buffer():
    for i in range(buffer_size):
        if i < len(buffer):
            buffer_boxes[i].config(
                text=str(buffer[i]),
                bg="#4caf50",
                fg="white"
            )
        else:
            buffer_boxes[i].config(
                text="EMPTY",
                bg="white",
                fg="black"
            )
    # Buffer state:
    if len(buffer) == 0:
        state = "EMPTY"
    elif len(buffer) == buffer_size:
        state = "FULL"
    else:
        state = "FILLED"
    buffer_state.config(
        text=f"Buffer State : {state}"
    )

def add_log(message, log_type="normal"):
    current_time = time.strftime("%H:%M:%S")
    log_box.insert(
        tk.END,
        f"[{current_time}] {message}\n",
        log_type
    )
    log_box.see(tk.END)
# Producer function:
def producer():
    global running 
    while running:
        speed = producer_scale.get()
        time.sleep(6 - speed)
        if not running:
            break
        item = random.randint(100, 999)
        empty.acquire()
        producer_status.config(
            text=f"Producer Status : Producing..."
        )
        time.sleep(0.8)
        if not running:
            break
        mutex.acquire() # enter critical section
        buffer.append(item)
        add_log(
            f"Producer produced item {item}",
            "producer"
        )
        update_buffer()
        mutex.release() # exit critical section
        full.release()
        producer_status.config(
            text=f"Producer Status : Waiting"
        )
# Consumer function:
def consumer():
    global running
    while running:
        speed = consumer_scale.get()
        time.sleep(6 - speed)
        if not running:
            break
        consumer_status.config(
            text=f"Consumer Status : Consuming..."
        )
        time.sleep(0.8)
        if not running:
            break
        full.acquire()
        mutex.acquire()
        if len(buffer) > 0:
            item = buffer.pop(0)
            add_log(
                f"Consumer consumed item {item}",
                "consumer"
            )
            update_buffer()
        mutex.release()
        empty.release()
        consumer_status.config(
            text=f"Consumer Status : Waiting"
        )
        time.sleep(0.8)

def start_simulation():
    global running
    if running:
        return
    running = True
    add_log(
        "Simulation Started",
        "system"
    )
    # Producers
    threading.Thread(
        target=producer,
        daemon=True
    ).start()
    # Consumers
    threading.Thread(
        target=consumer,
        daemon=True
    ).start()

def stop_simulation():
    global running
    running = False
    add_log(
        "Simulation Stopped",
        "system"
    )
    producer_status.config(
        text="Producer Status : Stopped"
    )
    consumer_status.config(
        text="Consumer Status : Stopped"
    )

def reset_simulation():
    global buffer
    global running
    global mutex, empty, full
    running = False
    time.sleep(0.5)
    buffer.clear()
    # Reset semaphores
    mutex = threading.Semaphore(1)
    empty = threading.Semaphore(buffer_size)
    full = threading.Semaphore(0)
    update_buffer()
    log_box.delete(1.0, tk.END)
    producer_status.config(
        text="Producer Status : Waiting"
    )
    consumer_status.config(
        text="Consumer Status : Waiting"
    )
    producer_scale.set(2)
    consumer_scale.set(2)
    add_log(
        "Simulation Reset",
        "system"
    )

button_frame = tk.Frame(left_panel, bg="#25253a")
button_frame.pack(pady=40)

start_btn = tk.Button(
    button_frame,
    text="Start", font=("Arial", 13, "bold"), bg="#4caf50", fg="white", width=14, height=2,command=start_simulation
)
start_btn.grid(row=0, column=0, pady=10)

stop_btn = tk.Button(
    button_frame,
    text="Stop", font=("Arial", 13, "bold"), bg="#f44336", fg="white", width=14,height=2, command=stop_simulation
)
stop_btn.grid(row=1, column=0, pady=10)

reset_btn = tk.Button(
    button_frame,
    text="Reset", font=("Arial", 13, "bold"), bg="#2196f3", fg="white", width=14, height=2, command=reset_simulation
)
reset_btn.grid(row=2, column=0, pady=10)

# Run window:
root.mainloop()