#Domain:Food Ordersing System
#Concept:Semaphore

import threading
import time
import random
import tkinter as tk
from tkinter import ttk
# Define the maximum number of chefs available
MAX_CHEFS = 3
# Semaphore to control access to chefs
chef_semaphore = threading.Semaphore(MAX_CHEFS)
# Function representing a customer placing an order
def place_order(order_id, output_text, progress_bar):
    output_text.insert(tk.END, f"Customer {order_id} is placing an order...\n")
    output_text.see(tk.END) 
    # Customer waits for a chef to become available
    chef_semaphore.acquire()
    output_text.insert(tk.END, f"Order {order_id} is being prepared by a chef.\n")
    output_text.see(tk.END)
    # Simulate time taken to prepare food and update progress
    preparation_time = random.randint(2, 5)
    for i in range(101):
        time.sleep(preparation_time / 100)
        progress_bar['value'] = i
        root.update_idletasks()
    output_text.insert(tk.END, f"Order {order_id} has been prepared in {preparation_time} seconds.\n")
    output_text.see(tk.END)    
    # Release the chef (make them available for the next order)
    chef_semaphore.release()
# Function to simulate multiple customers placing orders at the same time
def simulate_customers(output_text, progress_bar):
    customer_threads = []    
    # Simulate 7 customers placing orders
    for i in range(1, 8):
        customer_thread = threading.Thread(target=place_order, args=(i, output_text, progress_bar))
        customer_threads.append(customer_thread)
        customer_thread.start()
        # Small delay between customers arriving to place orders
        time.sleep(random.uniform(0.5, 1.5))    
    # Wait for all customer threads to complete
    for thread in customer_threads:
        thread.join()
# GUI function
def start_simulation():
    output_text.delete(1.0, tk.END)  # Clear previous text
    progress_bar['value'] = 0  # Reset progress bar
    threading.Thread(target=simulate_customers, args=(output_text, progress_bar)).start()
# Set up the main window
root = tk.Tk()
root.title("Food Ordering System Simulation")
root.geometry("600x500")
root.configure(bg='#f2f2f2')
# Create a Title Frame for the title to prevent blocking
title_frame = tk.Frame(root, bg='#f2f2f2', pady=10)
title_frame.grid(row=0, column=0, sticky=tk.N)
# Title Label
title_label = tk.Label(title_frame, text="Online Food Ordering System", font=("Arial", 18, "bold"), bg='#f2f2f2', fg='#333')
title_label.pack()
# Create a frame for output text
frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
# Create a Text widget to display order status
output_text = tk.Text(frame, height=15, width=60, wrap=tk.WORD, font=("Arial", 12))
output_text.grid(row=1, column=0, padx=10, pady=10)
# Create a Scrollbar for the Text widget
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=output_text.yview)
scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
output_text['yscrollcommand'] = scrollbar.set
# Create a Progress Bar
progress_label = tk.Label(root, text="Order Progress", font=("Arial", 12), bg='#f2f2f2')
progress_label.grid(row=2, column=0, pady=10)
progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.grid(row=3, column=0, pady=10)
# Create a Button to start the simulation
start_button = tk.Button(root, text="Start Simulation", command=start_simulation, bg='#4CAF50', fg='white', font=("Arial", 14), width=20, height=2)
start_button.grid(row=4, column=0, pady=20)
# Start the Tkinter event loop
root.mainloop()
