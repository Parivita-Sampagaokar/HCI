import tkinter as tk
from tkinter import messagebox, StringVar
from ttkbootstrap import Style
from fpdf import FPDF
from datetime import datetime

# Initialize main window
root = tk.Tk()
style = Style(theme='cyborg')
root.title("Hotel Room Booking")
root.geometry("500x600")

# Global variables to store user and booking details
user_details = {}
booking_details = {
    "destination": "",
    "check_in_date": "",
    "check_out_date": ""
}

# Sample data for destination cities in India
cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru", "Hyderabad", "Goa", "Jaipur", "Agra", "Pune"]

# Sample data for hotel options
hotel_options = [
    {"hotel_name": "The Taj Mahal Palace", "room_type": "Deluxe Room", "price": "$200 per night"},
    {"hotel_name": "Oberoi Udaivilas", "room_type": "Luxury Suite", "price": "$350 per night"},
    {"hotel_name": "ITC Grand Chola", "room_type": "Executive Room", "price": "$150 per night"},
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
        hotel_search()
    else:
        messagebox.showerror("Error", "All fields are required!")

# Step 2: Hotel search form
def hotel_search():
    clear_frame()
    
    tk.Label(root, text="Search Hotels").pack(pady=10)
    
    # Dropdown for destination city
    tk.Label(root, text="Destination City:").pack()
    destination_var = StringVar(root)
    destination_var.set(cities[0])  # Default value
    destination_menu = tk.OptionMenu(root, destination_var, *cities)
    destination_menu.pack()
    
    # Date entry for check-in and check-out
    tk.Label(root, text="Check-In Date (YYYY-MM-DD):").pack()
    check_in_entry = tk.Entry(root)
    check_in_entry.pack()
    
    tk.Label(root, text="Check-Out Date (YYYY-MM-DD):").pack()
    check_out_entry = tk.Entry(root)
    check_out_entry.pack()
    
    search_btn = tk.Button(root, text="Search Hotels", command=lambda: display_hotels(destination_var.get(), check_in_entry.get(), check_out_entry.get()))
    search_btn.pack(pady=10)

def display_hotels(destination, check_in_date, check_out_date):
    if destination and check_in_date and check_out_date:
        try:
            # Verify date format
            check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
            if check_in >= check_out:
                messagebox.showerror("Error", "Check-out date must be after check-in date.")
                return
            
            # Save booking search details
            booking_details["destination"] = destination
            booking_details["check_in_date"] = check_in_date
            booking_details["check_out_date"] = check_out_date
            
            clear_frame()
            
            tk.Label(root, text="Available Hotels").pack(pady=10)
            
            # Display multiple hotel options
            for option in hotel_options:
                option_text = f"{option['hotel_name']} - {option['room_type']} - {option['price']}"
                tk.Label(root, text=option_text).pack()
                book_btn = tk.Button(root, text="Book This Hotel", command=lambda opt=option: booking_confirmation(opt))
                book_btn.pack(pady=5)
        
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Step 3: Booking confirmation
def booking_confirmation(selected_hotel):
    clear_frame()
    
    tk.Label(root, text="Confirm Your Booking").pack(pady=10)
    tk.Label(root, text=f"Hotel: {selected_hotel['hotel_name']}").pack()
    tk.Label(root, text=f"Room Type: {selected_hotel['room_type']}").pack()
    tk.Label(root, text=f"Location: {booking_details['destination']}").pack()
    tk.Label(root, text=f"Check-In Date: {booking_details['check_in_date']}").pack()
    tk.Label(root, text=f"Check-Out Date: {booking_details['check_out_date']}").pack()
    tk.Label(root, text=f"Price: {selected_hotel['price']}").pack()
    
    payment_btn = tk.Button(root, text="Proceed to Payment", command=lambda: payment_processing(selected_hotel))
    payment_btn.pack(pady=10)

# Step 4: Payment and booking confirmation PDF generation
def payment_processing(selected_hotel):
    # Dummy payment confirmation
    payment_confirmed = messagebox.askyesno("Payment", "Confirm Payment?")
    if payment_confirmed:
        generate_booking_pdf(selected_hotel)
        thank_you_message()

def generate_booking_pdf(selected_hotel):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hotel Booking Confirmation", ln=True, align='C')
    pdf.cell(200, 10, txt=" ", ln=True)  # Spacer line
    
    # User Details
    pdf.cell(200, 10, txt=f"Name: {user_details['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user_details['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {user_details['phone']}", ln=True)
    
    # Booking Details
    pdf.cell(200, 10, txt=f"Hotel: {selected_hotel['hotel_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Room Type: {selected_hotel['room_type']}", ln=True)
    pdf.cell(200, 10, txt=f"Location: {booking_details['destination']}", ln=True)
    pdf.cell(200, 10, txt=f"Check-In Date: {booking_details['check_in_date']}", ln=True)
    pdf.cell(200, 10, txt=f"Check-Out Date: {booking_details['check_out_date']}", ln=True)
    pdf.cell(200, 10, txt=f"Price: {selected_hotel['price']}", ln=True)
    
    pdf.output("HotelBookingConfirmation.pdf")

def thank_you_message():
    messagebox.showinfo("Thank You", "Your booking is complete. Confirmation saved as HotelBookingConfirmation.pdf.")
    root.destroy()

# Utility function to clear the window
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Start the application with personal details form
personal_details()
root.mainloop()

# from tkinter import messagebox, simpledialog
# from PIL import Image, ImageTk
# import qrcode
# import smtplib
# from email.mime.text import MIMEText
# from email.utils import formataddr


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
