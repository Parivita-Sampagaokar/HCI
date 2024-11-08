import tkinter as tk
from tkinter import messagebox, StringVar
from ttkbootstrap import Style
from fpdf import FPDF
from datetime import datetime

# Initialize main window
root = tk.Tk()
style = Style(theme='cyborg')
root.title("Railway Ticket Booking")
root.geometry("500x500")

# Global variables to store user and train details
user_details = {}
train_details = {
    "departure": "",
    "destination": "",
    "travel_date": ""
}

# Sample data for popular railway stations in India
stations = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru", "Hyderabad", "Ahmedabad", "Jaipur", "Pune", "Goa","Nagpur"]

# Sample data for train options
train_options = [
    {"train_name": "Rajdhani Express", "departure_time": "06:00 AM", "price": "Rs. 1200"},
    {"train_name": "Shatabdi Express", "departure_time": "02:30 PM", "price": "Rs. 2900"},
    {"train_name": "Duronto Express", "departure_time": "09:00 PM", "price": "Rs. 1100"}
]

# Step 1: Personal details form
def personal_details():
    clear_frame()
    
    tk.Label(root, text="Enter Personal Details").pack(pady=10)
    
    tk.Label(root, text="Name:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()
    
    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()
    
    tk.Label(root, text="Phone Number:").pack()
    phone_entry = tk.Entry(root)
    phone_entry.pack()
    
    submit_btn = tk.Button(root, text="Submit", command=lambda: save_personal_details(name_entry.get(), email_entry.get(), phone_entry.get()))
    submit_btn.pack(pady=10)

def save_personal_details(name, email, phone):
    if name and email and phone:
        user_details["name"] = name
        user_details["email"] = email
        user_details["phone"] = phone
        train_search()
    else:
        messagebox.showerror("Error", "All fields are required!")

# Step 2: Train search form
def train_search():
    clear_frame()
    
    tk.Label(root, text="Search Trains").pack(pady=10)
    
    # Dropdown for departure station
    tk.Label(root, text="Departure Station:").pack()
    departure_var = StringVar(root)
    departure_var.set(stations[0])  # Default value
    departure_menu = tk.OptionMenu(root, departure_var, *stations)
    departure_menu.pack()
    
    # Dropdown for destination station
    tk.Label(root, text="Destination Station:").pack()
    destination_var = StringVar(root)
    destination_var.set(stations[1])  # Default value
    destination_menu = tk.OptionMenu(root, destination_var, *stations)
    destination_menu.pack()
    
    # Date entry for travel date
    tk.Label(root, text="Travel Date (YYYY-MM-DD):").pack()
    date_entry = tk.Entry(root)
    date_entry.pack()
    
    search_btn = tk.Button(root, text="Search Trains", command=lambda: display_trains(departure_var.get(), destination_var.get(), date_entry.get()))
    search_btn.pack(pady=10)

def display_trains(departure, destination, travel_date):
    if departure and destination and travel_date:
        if departure == destination:
            messagebox.showerror("Error", "Departure and destination cannot be the same!")
            return
        try:
            # Verify date format
            datetime.strptime(travel_date, "%Y-%m-%d")
            
            # Save train search details
            train_details["departure"] = departure
            train_details["destination"] = destination
            train_details["travel_date"] = travel_date
            
            clear_frame()
            
            tk.Label(root, text="Available Trains").pack(pady=10)
            
            # Display multiple train options
            for option in train_options:
                option_text = f"{option['train_name']} - {option['departure_time']} - {option['price']}"
                tk.Label(root, text=option_text).pack()
                book_btn = tk.Button(root, text="Book This Train", command=lambda opt=option: booking_confirmation(opt))
                book_btn.pack(pady=5)
        
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Step 3: Booking confirmation
def booking_confirmation(selected_train):
    clear_frame()
    
    tk.Label(root, text="Confirm Your Booking").pack(pady=10)
    tk.Label(root, text=f"Train: {selected_train['train_name']}").pack()
    tk.Label(root, text=f"Route: {train_details['departure']} to {train_details['destination']}").pack()
    tk.Label(root, text=f"Date: {train_details['travel_date']} at {selected_train['departure_time']}").pack()
    tk.Label(root, text=f"Price: {selected_train['price']}").pack()
    
    payment_btn = tk.Button(root, text="Proceed to Payment", command=lambda: payment_processing(selected_train))
    payment_btn.pack(pady=10)

# Step 4: Payment and ticket generation
def payment_processing(selected_train):
    # Dummy payment confirmation
    payment_confirmed = messagebox.askyesno("Payment", "Confirm Payment?")
    if payment_confirmed:
        generate_ticket_pdf(selected_train)
        thank_you_message()

def generate_ticket_pdf(selected_train):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Railway Ticket", ln=True, align='C')
    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer line
    
    # User Details
    pdf.cell(200, 10, txt=f"Name: {user_details['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user_details['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {user_details['phone']}", ln=True)
    
    # Train Details
    pdf.cell(200, 10, txt=f"Train: {selected_train['train_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Route: {train_details['departure']} to {train_details['destination']}", ln=True)
    pdf.cell(200, 10, txt=f"Travel Date: {train_details['travel_date']}", ln=True)
    pdf.cell(200, 10, txt=f"Departure Time: {selected_train['departure_time']}", ln=True)
    pdf.cell(200, 10, txt=f"Price: {selected_train['price']}", ln=True)
    
    pdf.output("TrainTicket.pdf")

def thank_you_message():
    messagebox.showinfo("Thank You", "Your booking is complete. Ticket saved as TrainTicket.pdf.")
    root.destroy()

# Utility function to clear the window
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Start the application with personal details form
personal_details()
root.mainloop()
