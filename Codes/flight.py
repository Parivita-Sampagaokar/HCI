import tkinter as tk
from tkinter import messagebox, StringVar
from ttkbootstrap import Style
from fpdf import FPDF
from datetime import datetime
from PIL import Image, ImageTk
import qrcode

# UPI Details (mock for the example)
upi_id = '9545731750@ptyes'
rec_name = 'FLIGHTINDIA2024'

# Initialize main window
root = tk.Tk()
style = Style(theme='morph')
root.title("Flight Ticket Booking")
root.geometry("500x500")

# Global variables to store user and flight details
user_details = {}
flight_details = {
    "takeoff": "",
    "destination": "",
    "departure_date": ""
}

# Sample data for takeoff and destination locations in India
locations = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Goa","Nagpur"]

# Sample data for flight options
flight_options = [
    {"flight_name": "Flight ABC123", "flight_time": "08:00 AM", "price": "Rs. 11500"},
    {"flight_name": "Flight XYZ456", "flight_time": "02:00 PM", "price": "Rs. 6800"},
    {"flight_name": "Flight LMN789", "flight_time": "06:00 PM", "price": "Rs. 3700"}
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
        flight_search()
    else:
        messagebox.showerror("Error", "All fields are required!")

# Step 2: Flight search form
def flight_search():
    clear_frame()
    
    tk.Label(root, text="Search Flights").pack(pady=10)
    
    # Dropdown for takeoff place
    tk.Label(root, text="Takeoff Place:").pack()
    takeoff_var = StringVar(root)
    takeoff_var.set(locations[0])  # Default value
    takeoff_menu = tk.OptionMenu(root, takeoff_var, *locations)
    takeoff_menu.pack()
    
    # Dropdown for destination place
    tk.Label(root, text="Destination:").pack()
    destination_var = StringVar(root)
    destination_var.set(locations[1])  # Default value
    destination_menu = tk.OptionMenu(root, destination_var, *locations)
    destination_menu.pack()
    
    # Date entry for departure date
    tk.Label(root, text="Departure Date (YYYY-MM-DD):").pack()
    date_entry = tk.Entry(root)
    date_entry.pack()
    
    search_btn = tk.Button(root, text="Search Flights", command=lambda: display_flights(takeoff_var.get(), destination_var.get(), date_entry.get()))
    search_btn.pack(pady=10)

def display_flights(takeoff, destination, departure_date):
    if takeoff and destination and departure_date:
        if takeoff == destination:
            messagebox.showerror("Error", "Takeoff and destination cannot be the same!")
            return
        try:
            # Verify date format
            datetime.strptime(departure_date, "%Y-%m-%d")
            
            # Save flight search details
            flight_details["takeoff"] = takeoff
            flight_details["destination"] = destination
            flight_details["departure_date"] = departure_date
            
            clear_frame()
            
            tk.Label(root, text="Available Flights").pack(pady=10)
            
            # Display multiple flight options
            for option in flight_options:
                option_text = f"{option['flight_name']} - {option['flight_time']} - {option['price']}"
                tk.Label(root, text=option_text).pack()
                book_btn = tk.Button(root, text="Book This Flight", command=lambda opt=option: booking_confirmation(opt))
                book_btn.pack(pady=5)
        
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Step 3: Booking confirmation
def booking_confirmation(selected_flight):
    clear_frame()
    
    tk.Label(root, text="Confirm Your Booking").pack(pady=10)
    tk.Label(root, text=f"Flight: {selected_flight['flight_name']}").pack()
    tk.Label(root, text=f"Departure: {flight_details['takeoff']} to {flight_details['destination']}").pack()
    tk.Label(root, text=f"Date: {flight_details['departure_date']} at {selected_flight['flight_time']}").pack()
    tk.Label(root, text=f"Price: {selected_flight['price']}").pack()
    
    payment_btn = tk.Button(root, text="Proceed to Payment", command=lambda: payment_processing(selected_flight))
    payment_btn.pack(pady=10)

# Step 4: Payment and ticket generation
def payment_processing(selected_flight):
    # Dummy payment confirmation
    payment_confirmed = messagebox.askyesno("Payment", "Confirm Payment?")
    if payment_confirmed:
        generate_ticket_pdf(selected_flight)
        show_qr(selected_flight)

def show_qr(selected_flight):
         total_price=selected_flight['price']
         upi_url = f'upi://pay?pa={upi_id}&pn={rec_name}&am={total_price}'
         qr = qrcode.make(upi_url)
         qr.save("upi_qr.png")

         qr_window = tk.Toplevel()
         qr_window.title("Scan to Pay")
         qr_window.geometry("400x400")

         qr_img = Image.open("upi_qr.png")
         qr_img = qr_img.resize((250, 250), Image.LANCZOS)
         qr_img = ImageTk.PhotoImage(qr_img)

         qr_label = tk.Label(qr_window, image=qr_img)
         qr_label.image = qr_img
         qr_label.pack(pady=10)

         instruction_label = tk.Label(qr_window, text="Scan the QR code to make the payment")
         instruction_label.pack(pady=10)

         pay_button = tk.Button(qr_window, text="Confirm Payment", command=lambda: thank_you_message(qr_window))
         pay_button.pack(pady=10)

def generate_ticket_pdf(selected_flight):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Flight Ticket", ln=True, align='C')
    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer line
    
    # User Details
    pdf.cell(200, 10, txt=f"Name: {user_details['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user_details['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {user_details['phone']}", ln=True)
    
    # Flight Details
    pdf.cell(200, 10, txt=f"Flight: {selected_flight['flight_name']}", ln=True)
    pdf.cell(200, 10, txt=f"From: {flight_details['takeoff']} To: {flight_details['destination']}", ln=True)
    pdf.cell(200, 10, txt=f"Departure Date: {flight_details['departure_date']}", ln=True)
    pdf.cell(200, 10, txt=f"Departure Time: {selected_flight['flight_time']}", ln=True)
    pdf.cell(200, 10, txt=f"Price: {selected_flight['price']}", ln=True)
    
    pdf.output("FlightTicket.pdf")

def thank_you_message(qr_window):
    qr_window.destroy()
    messagebox.showinfo("Payment Successful","Thank You. Your booking is complete. Ticket saved as FlightTicket.pdf.")
    root.destroy()

# Utility function to clear the window
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Start the application with personal details form
personal_details()
root.mainloop()


# def generate_receipt(self):
#         self.user_email = simpledialog.askstring("Enter your email: ","Enter your email: ")

#         if self.user_email:
#             self.receipt_details = "\n".join([f"{item['name']} - ₹{item['price']}" for item in self.selected_items])
#             self.receipt_details += f"\n\nTotal: ₹{self.total_price}"

#             with open("receipt.txt", "w") as file:
#                 file.write(self.receipt_details)

#             self.send_email(self.user_email, self.receipt_details)

#             self.show_qr_and_acknowledge_payment()
#         else:
#             messagebox.showerror("Error", "Please provide valid contact info.")

#     def show_qr_and_acknowledge_payment(self):
#         upi_url = f'upi://pay?pa={upi_id}&pn={rec_name}&am={self.total_price}'
#         qr = qrcode.make(upi_url)
#         qr.save("upi_qr.png")

#         qr_window = ttk.Toplevel()
#         qr_window.title("Scan to Pay")
#         qr_window.geometry("400x400")

#         qr_img = Image.open("upi_qr.png")
#         qr_img = qr_img.resize((250, 250), Image.LANCZOS)
#         qr_img = ImageTk.PhotoImage(qr_img)

#         qr_label = ttk.Label(qr_window, image=qr_img)
#         qr_label.image = qr_img
#         qr_label.pack(pady=10)

#         instruction_label = ttk.Label(qr_window, text="Scan the QR code to make the payment")
#         instruction_label.pack(pady=10)

#         pay_button = ttk.Button(qr_window, text="Confirm Payment", command=lambda: self.acknowledge_payment(qr_window))
#         pay_button.pack(pady=10)

#     def acknowledge_payment(self, qr_window):
#         qr_window.destroy()
#         messagebox.showinfo("Payment Successful", "Thank you for your payment!")
#         self.get_review()

#         self.title("Hope you enjoyed the service! Come back again")
#         self.bill_label.config(text="Hope you enjoyed the service! Come back again")

#     def send_email(self, email, content):
#         email_sender = 'sampagaonkar.parivita@gmail.com'
#         email_sender_pswd = 'fnip ajnt ldnn qfdz'
#         email_receiver = self.user_email

#         subject = 'Food Reciept'

#         msg = MIMEText(self.receipt_details)
#         msg['To'] = formataddr(('Recipient', self.user_email))
#         msg['From'] = formataddr(('Binary Resto', 'author@example.com'))
#         msg['Subject'] = 'Reciept'

#         connection = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         connection.ehlo()
#         connection.login(email_sender, email_sender_pswd)
#         connection.sendmail(msg['From'], email_receiver, msg.as_string())
#         connection.close()
#         print(f"Sending email to {email} with content:\n{content}")
#         messagebox.showinfo("Email", f"Receipt sent to {email}")
