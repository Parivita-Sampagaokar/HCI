import tkinter as tk
from tkinter import messagebox, StringVar, IntVar
from ttkbootstrap import Style
from fpdf import FPDF

# Initialize main window
root = tk.Tk()
style = Style(theme='cyborg')
root.title("Movie Ticket Booking")
root.geometry("600x700")

# Global variables to store user and booking details
user_details = {}
booking_details = {
    "movie": "",
    "show_time": "",
    "ticket_count": 0,
    "selected_seats": []
}

# Sample data for popular recent Indian movies
movies = [
    {"title": "Jawan", "show_times": ["10:00 AM", "1:30 PM", "5:00 PM", "8:30 PM"], "price": "Rs. 250"},
    {"title": "Gadar 2", "show_times": ["11:00 AM", "2:00 PM", "6:00 PM", "9:00 PM"], "price": "Rs. 140"},
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
        movie_selection()
    else:
        messagebox.showerror("Error", "All fields are required!")

# Step 2: Movie selection form
def movie_selection():
    clear_frame()
    
    tk.Label(root, text="Select Movie").pack(pady=10)
    
    # Dropdown for movie selection
    tk.Label(root, text="Movie:").pack()
    movie_var = StringVar(root)
    movie_var.set(movies[0]["title"])  # Default value
    movie_menu = tk.OptionMenu(root, movie_var, *[movie["title"] for movie in movies])
    movie_menu.pack()
    
    # Dropdown for show time
    tk.Label(root, text="Show Time:").pack()
    show_time_var = StringVar(root)
    show_time_var.set(movies[0]["show_times"][0])  # Default time for first movie
    show_time_menu = tk.OptionMenu(root, show_time_var, *movies[0]["show_times"])
    show_time_menu.pack()
    
    # Number of tickets
    tk.Label(root, text="Number of Tickets:").pack()
    ticket_count_var = IntVar(root)
    ticket_count_entry = tk.Entry(root, textvariable=ticket_count_var)
    ticket_count_entry.pack()
    
    def update_show_times(*args):
        selected_movie = next((m for m in movies if m["title"] == movie_var.get()), None)
        if selected_movie:
            show_time_var.set(selected_movie["show_times"][0])  # Reset to first show time
            show_time_menu["menu"].delete(0, "end")
            for time in selected_movie["show_times"]:
                show_time_menu["menu"].add_command(label=time, command=tk._setit(show_time_var, time))
    
    # Update show times based on selected movie
    movie_var.trace("w", update_show_times)
    
    search_btn = tk.Button(root, text="Book Tickets", command=lambda: seat_selection(movie_var.get(), show_time_var.get(), ticket_count_var.get()))
    search_btn.pack(pady=10)

# Step 3: Seat selection
# Step 3: Seat selection
def seat_selection(movie, show_time, ticket_count):
    if not ticket_count or int(ticket_count) <= 0:
        messagebox.showerror("Error", "Please enter a valid number of tickets.")
        return

    clear_frame()
    booking_details["movie"] = movie
    booking_details["show_time"] = show_time
    booking_details["ticket_count"] = int(ticket_count)
    booking_details["selected_seats"] = []
    
    tk.Label(root, text="Select Your Seats").pack(pady=10)
    
    # Screen label
    screen_label = tk.Label(root, text="SCREEN", font=("Arial", 16, "bold"))
    screen_label.pack()

    # Create a 5x5 grid for seats
    seats_frame = tk.Frame(root)
    seats_frame.pack(pady=10)
    seat_buttons = []

    # Helper function to create a button with correct command binding
    def create_seat_button(seat, row, col):
        button = tk.Button(seats_frame, text=seat, bg="blue", width=5, height=2)
        button.config(command=lambda: toggle_seat(seat, button))
        button.grid(row=row, column=col, padx=5, pady=5)
        return button

    def toggle_seat(seat, button):
        if seat in booking_details["selected_seats"]:
            booking_details["selected_seats"].remove(seat)
            button.config(bg="blue")
        else:
            if len(booking_details["selected_seats"]) < booking_details["ticket_count"]:
                booking_details["selected_seats"].append(seat)
                button.config(bg="red")
            else:
                messagebox.showinfo("Info", "You have already selected the required number of seats.")

    # Create seat buttons
    for row in range(5):
        seat_row = []
        for col in range(5):
            seat = f"{chr(65+row)}{col+1}"
            button = create_seat_button(seat, row, col)
            seat_row.append(button)
        seat_buttons.append(seat_row)
    
    proceed_btn = tk.Button(root, text="Confirm Booking", command=booking_confirmation)
    proceed_btn.pack(pady=10)

# Step 4: Booking confirmation
def booking_confirmation():
    if len(booking_details["selected_seats"]) != booking_details["ticket_count"]:
        messagebox.showerror("Error", "Please select the required number of seats.")
        return

    clear_frame()
    
    selected_movie = next((m for m in movies if m["title"] == booking_details["movie"]), None)
    
    tk.Label(root, text="Confirm Your Booking").pack(pady=10)
    tk.Label(root, text=f"Movie: {selected_movie['title']}").pack()
    tk.Label(root, text=f"Show Time: {booking_details['show_time']}").pack()
    tk.Label(root, text=f"Number of Tickets: {booking_details['ticket_count']}").pack()
    tk.Label(root, text=f"Seats: {', '.join(booking_details['selected_seats'])}").pack()
    tk.Label(root, text=f"Price per Ticket: {selected_movie['price']}").pack()
    total_price = int(selected_movie['price'].strip("$")) * booking_details["ticket_count"]
    tk.Label(root, text=f"Total Price: ${total_price}").pack()
    
    payment_btn = tk.Button(root, text="Proceed to Payment", command=lambda: payment_processing(selected_movie))
    payment_btn.pack(pady=10)

# Step 5: Payment and booking confirmation PDF generation
def payment_processing(selected_movie):
    payment_confirmed = messagebox.askyesno("Payment", "Confirm Payment?")
    if payment_confirmed:
        generate_booking_pdf(selected_movie)
        thank_you_message()

def generate_booking_pdf(selected_movie):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Movie Ticket Booking Confirmation", ln=True, align='C')
    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer line
    
    # User Details
    pdf.cell(200, 10, txt=f"Name: {user_details['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user_details['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {user_details['phone']}", ln=True)
    
    # Booking Details
    pdf.cell(200, 10, txt=f"Movie: {selected_movie['title']}", ln=True)
    pdf.cell(200, 10, txt=f"Show Time: {booking_details['show_time']}", ln=True)
    pdf.cell(200, 10, txt=f"Number of Tickets: {booking_details['ticket_count']}", ln=True)
    pdf.cell(200, 10, txt=f"Seats: {', '.join(booking_details['selected_seats'])}", ln=True)
    pdf.cell(200, 10, txt=f"Price per Ticket: {selected_movie['price']}", ln=True)
    total_price = int(selected_movie['price'].strip("$")) * booking_details["ticket_count"]
    pdf.cell(200, 10, txt=f"Total Price: Rs. {total_price}", ln=True)
    
    pdf.output("MovieBookingConfirmation.pdf")

def thank_you_message():
    messagebox.showinfo("Thank You", "Your booking is complete. Confirmation saved as MovieBookingConfirmation.pdf.")
    root.destroy()

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Start the application
personal_details()
root.mainloop()
