import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import qrcode
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# UPI Details (mock for the example)
upi_id = '9545731750@ptyes'
rec_name = 'BINARYRESTO20'

# Mock Menu Data
menu = {
    "Starters": [
        {"name": "Samosa", "price": 10, "img": "Images/menu/samosa.jpg", "desc": "A spicy potato filling encased in a crispy pastry", "spice": "High"},
        {"name": "Paneer Pakora", "price": 80, "img": "Images/menu/paneer_pakora.jpg", "desc": "Fried cottage cheese fritters served with mint chutney", "spice": "Medium"},
        {"name": "Spring Rolls", "price": 70, "img": "Images/menu/spring_rolls.jpg", "desc": "Crispy rolls filled with mixed vegetables, served with sauce", "spice": "Medium"},
        {"name": "Vegetable Manchurian", "price": 100, "img": "Images/menu/Veg_manchurian.jpg", "desc": "Deep-fried vegetable balls in a spicy Manchurian sauce", "spice": "High"},
        {"name": "Aloo Tikki", "price": 60, "img": "Images/menu/Aloo_tikki.jpg", "desc": "Spicy potato patties served with tamarind chutney", "spice": "Medium"},
        {"name": "Chilli Paneer", "price": 120, "img": "Images/menu/chilli_paneer.jpg", "desc": "Paneer cubes tossed in a spicy sauce with capsicum and onions", "spice": "High"}
    ],
    "Main Course": [
        {"name": "Chana Masala", "price": 110, "img": "Images/menu/chana_masala.jpg", "desc": "Spiced chickpeas cooked in a tangy tomato gravy", "spice": "Medium"},
        {"name": "Aloo Gobi", "price": 100, "img": "Images/menu/Aloo_gobi.jpg", "desc": "Potatoes and cauliflower cooked with spices", "spice": "Medium"},
        {"name": "Baingan Bharta", "price": 120, "img": "Images/menu/Baingan_bharta.jpg", "desc": "Smoky mashed eggplant cooked with onions and spices", "spice": "Medium"},
        {"name": "Mixed Vegetable Curry", "price": 130, "img": "Images/menu/mix_veg.jpg", "desc": "Assorted vegetables cooked in a spiced gravy", "spice": "Medium"},
        {"name": "Paneer Butter Masala", "price": 180, "img": "Images/menu/paneer_butter_masala.jpg", "desc": "Cottage cheese in a rich, creamy tomato gravy", "spice": "Low"},
        {"name": "Kadai Paneer", "price": 170, "img": "Images/menu/kadai_paneer.jpg", "desc": "Paneer cubes cooked with bell peppers and spices", "spice": "Medium"},
        {"name": "Palak Paneer", "price": 150, "img": "Images/menu/palak_paneer.jpg", "desc": "Cottage cheese cubes simmered in creamy spinach gravy", "spice": "Low"},
        {"name": "Dal Makhani", "price": 120, "img": "Images/menu/dal_makhani.jpg", "desc": "Creamy black lentils cooked with butter and spices", "spice": "Low"},
        {"name": "Veg Pulao", "price": 100, "img": "Images/menu/Veg_pulao.jpg", "desc": "Aromatic rice cooked with seasonal vegetables and mild spices", "spice": "Low"},
        {"name": "Vegetable Biryani", "price": 200, "img": "Images/menu/Veg_biriyani.jpg", "desc": "Fragrant basmati rice cooked with mixed vegetables and spices", "spice": "Medium"},
        {"name": "Jeera Rice", "price": 60, "img": "Images/menu/jeera_rice.jpg", "desc": "Basmati rice tempered with cumin seeds", "spice": "None"},
        {"name": "Butter Naan", "price": 40, "img": "Images/menu/Butter_naan.jpg", "desc": "Soft Indian flatbread with a generous brush of butter", "spice": "None"},
        {"name": "Tandoori Roti", "price": 30, "img": "Images/menu/Tandoor_roti.jpg", "desc": "Whole wheat flatbread cooked in a tandoor", "spice": "None"},
        {"name": "Roti (Plain)", "price": 25, "img": "Images/menu/Roti.jpg", "desc": "Soft Indian flatbread made with whole wheat flour", "spice": "None"},
        {"name": "Methi Thepla", "price": 50, "img": "Images/menu/methi_thepla.jpg", "desc": "Spiced flatbread made with fenugreek leaves", "spice": "Medium"}
    ],
    "Desserts": [
        {"name": "Gulab Jamun", "price": 60, "img": "Images/menu/gulab_jamun.jpg", "desc": "Soft, syrup-soaked dumplings made from milk solids", "spice": "None"},
        {"name": "Ras Malai", "price": 80, "img": "Images/menu/Rasmalai.jpg", "desc": "Soft paneer dumplings soaked in saffron-flavored milk", "spice": "None"},
        {"name": "Kheer", "price": 70, "img": "Images/menu/kheer.jpg", "desc": "Rice pudding made with milk, sugar, and cardamom", "spice": "None"},
        {"name": "Jalebi", "price": 60, "img": "Images/menu/jalebi.jpg", "desc": "Crispy, sweet spiral-shaped dessert soaked in sugar syrup", "spice": "None"},
        {"name": "Ice Cream", "price": 50, "img": "Images/menu/ice_cream.jpg", "desc": "Classic vanilla-flavored ice cream", "spice": "None"}
    ]
}

class FoodOrderingApp(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Food Ordering App")
        self.geometry("1500x1000")

        self._style = None  # Private attribute to hold the style
        self._style = ttk.Style()
        self._style.theme_use('cyborg')

    @property
    def style(self):
        """Getter for style"""
        return self._style

    @style.setter
    def style(self, value):
        """Setter for style"""
        self._style = value

        self.selected_items = []
        self.total_price = 0

        self.details_frame = ttk.Frame(self)
        self.details_frame.pack(pady=20)

        self.name_label = ttk.Label(self.details_frame, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = ttk.Entry(self.details_frame)
        self.name_entry.grid(row=0, column=1)

        self.phone_label = ttk.Label(self.details_frame, text="Phone Number:")
        self.phone_label.grid(row=1, column=0)
        self.phone_entry = ttk.Entry(self.details_frame)
        self.phone_entry.grid(row=1, column=1)

        self.seats_label = ttk.Label(self.details_frame, text="Number of Seats:")
        self.seats_label.grid(row=2, column=0)
        self.seats_entry = ttk.Entry(self.details_frame)
        self.seats_entry.grid(row=2, column=1)

        self.occasion_label = ttk.Label(self.details_frame, text="Is there a Special Occasion?")
        self.occasion_label.grid(row=3, column=0)

        self.occasion_var = ttk.StringVar(self.details_frame)
        self.occasion_dropdown = ttk.Combobox(self.details_frame, textvariable=self.occasion_var, state="readonly")
        self.occasion_dropdown['values'] = ["No", "Yes"]
        self.occasion_dropdown.grid(row=3, column=1)

        self.occasion_dropdown.bind("<<ComboboxSelected>>", self.show_occasion_type)

    def show_occasion_type(self, event):
        if self.occasion_var.get() == "Yes":
            self.occasion_type_label = ttk.Label(self.details_frame, text="Select Occasion:")
            self.occasion_type_label.grid(row=4, column=0)
            
            self.occasion_type_var = ttk.StringVar(self.details_frame)
            self.occasion_type_dropdown = ttk.Combobox(self.details_frame, textvariable=self.occasion_type_var, state="readonly")
            self.occasion_type_dropdown['values'] = ["Birthday", "Anniversary", "Graduation", " Promotion", "Other"]
            self.occasion_type_dropdown.grid(row=4, column=1)

            self.occasion_type_dropdown.bind("<<ComboboxSelected>>", self.display_congratulatory_message)
        else:
            self.submit_button = ttk.Button(self.details_frame, text="Submit", command=self.submit_details)
            self.submit_button.grid(row=5, column=1, padx=10, pady=10)

    def display_congratulatory_message(self, event):
        selected_occasion = self.occasion_type_var.get()
        if selected_occasion:
            messagebox.showinfo("Congratulations!", f"Congratulations on your {selected_occasion}!")

        self.submit_button = ttk.Button(self.details_frame, text="Submit", command=self.submit_details)
        self.submit_button.grid(row=5, column=1, padx=10, pady=10)

    def submit_details(self):
        self.user_name = self.name_entry.get()
        self.user_phone = self.phone_entry.get()
        self.user_seats = self.seats_entry.get ()

        if not (self.user_name and self.user_phone and self.user_seats):
            messagebox.showerror("Error", "Please fill in all the details.")
            return

        self.details_frame.pack_forget()
        self.show_menu()

    def show_menu(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=ttk.BOTH, expand=True)

        self.canvas = ttk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0),  window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        #self.canvas.pack(side="left", fill="both", expand=True, padx=400)
        self.canvas.pack(side='top', anchor='center',fill="both",expand=True, padx=400)
    
        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(pady=10, expand=True)
        #self.notebook.place(relx=0.5, rely=0.5, anchor="center")

        for category, items in menu.items():
            self.create_menu_tab(category, items)

    

        self.bill_frame = ttk.Frame(self)
        self.bill_frame.pack(pady=20)
        self.bill_label = ttk.Label(self.bill_frame, text="Bill Preview", font=('Arial', 16, 'bold'))
        self.bill_label.pack(anchor="center", padx=350)

        self.bill_text = ttk.Text(self.bill_frame, height=10, width=50, state='disabled')
        self.bill_text.pack()

        self.end_meal_button = ttk.Button(self, text="End Meal", command=self.end_meal)
        self.end_meal_button.pack(pady=10)

        self.pay_button = ttk.Button(self, text="Pay & Finish", command=self.generate_receipt)
        self.pay_button.pack(pady=10)
        self.pay_button.pack_forget()

    def create_menu_tab(self, category, items):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=category)

        for item in items:
            self.create_menu_item(frame, item)

    def create_menu_item(self, frame, item):
        item_frame = ttk.Frame(frame)
        item_frame.pack(pady=10)

        img = Image.open(item['img'])
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        img_label = ttk.Label(item_frame, image=img)
        img_label.image = img
        img_label.pack(side="left")

        desc_frame = ttk.Frame(item_frame)
        desc_frame.pack(side="left", padx=20)

        name_label = ttk.Label(desc_frame, text=item['name'], font=('Arial', 14))
        name_label.pack(anchor='w')

        desc_label = ttk.Label(desc_frame, text=item['desc'])
        desc_label.pack(anchor='w')

        spice_label = ttk.Label(desc_frame, text=f"Spice Level: {item['spice']}")
        spice_label.pack(anchor='w')

        price_label = ttk.Label(desc_frame, text=f"Price: ₹{item['price']}")
        price_label.pack(anchor='w')

        add_button = ttk.Button(desc_frame, text="Add to Order", command=lambda: self.add_to_order(item))
        add_button.pack(pady=5)

    def add_to_order(self, item):
        self.selected_items.append(item)
        self.update_bill()

    def update_bill(self):
        self.total_price = sum([item['price'] for item in self.selected_items])

        self.bill_text.config(state='normal')
        self.bill_text.delete('1.0', ttk.END)
        for item in self.selected_items:
            self.bill_text.insert(ttk.END, f"{item['name']} - ₹{item['price']}\n")
        self.bill_text.insert(ttk.END, f"\nTotal: ₹{self.total_price}")
        self.bill_text.config(state='disabled')

    def end_meal(self):
        if self.selected_items:
            confirm = messagebox.askyesno("End Meal", "Are you sure you want to end your meal?")
            if confirm:
                self.pay_button.pack()
        else:
            messagebox.showerror("Error", "You haven't ordered anything yet!")

    def generate_receipt(self):
        self.user_email = simpledialog.askstring("Enter your email: ","Enter your email: ")

        if self.user_email:
            self.receipt_details = "\n".join([f"{item['name']} - ₹{item['price']}" for item in self.selected_items])
            self.receipt_details += f"\n\nTotal: ₹{self.total_price}"

            with open("receipt.txt", "w") as file:
                file.write(self.receipt_details)

            self.send_email(self.user_email, self.receipt_details)

            self.show_qr_and_acknowledge_payment()
        else:
            messagebox.showerror("Error", "Please provide valid contact info.")

    def show_qr_and_acknowledge_payment(self):
        upi_url = f'upi://pay?pa={upi_id}&pn={rec_name}&am={self.total_price}'
        qr = qrcode.make(upi_url)
        qr.save("upi_qr.png")

        qr_window = ttk.Toplevel()
        qr_window.title("Scan to Pay")
        qr_window.geometry("400x400")

        qr_img = Image.open("upi_qr.png")
        qr_img = qr_img.resize((250, 250), Image.LANCZOS)
        qr_img = ImageTk.PhotoImage(qr_img)

        qr_label = ttk.Label(qr_window, image=qr_img)
        qr_label.image = qr_img
        qr_label.pack(pady=10)

        instruction_label = ttk.Label(qr_window, text="Scan the QR code to make the payment")
        instruction_label.pack(pady=10)

        pay_button = ttk.Button(qr_window, text="Confirm Payment", command=lambda: self.acknowledge_payment(qr_window))
        pay_button.pack(pady=10)

    def acknowledge_payment(self, qr_window):
        qr_window.destroy()
        messagebox.showinfo("Payment Successful", "Thank you for your payment!")
        self.get_review()

        self.title("Hope you enjoyed the service! Come back again")
        self.bill_label.config(text="Hope you enjoyed the service! Come back again")

    def send_email(self, email, content):
        email_sender = 'sampagaonkar.parivita@gmail.com'
        email_sender_pswd = 'fnip ajnt ldnn qfdz'
        email_receiver = self.user_email

        subject = 'Food Reciept'

        msg = MIMEText(self.receipt_details)
        msg['To'] = formataddr(('Recipient', self.user_email))
        msg['From'] = formataddr(('Binary Resto', 'author@example.com'))
        msg['Subject'] = 'Reciept'

        connection = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        connection.ehlo()
        connection.login(email_sender, email_sender_pswd)
        connection.sendmail(msg['From'], email_receiver, msg.as_string())
        connection.close()
        print(f"Sending email to {email} with content:\n{content}")
        messagebox.showinfo("Email", f"Receipt sent to {email}")


    def get_review(self):
        review_window = ttk.Toplevel()
        review_window.title("Leave a Review")
        review_window.geometry("400x400")

        review_label = ttk.Label (review_window, text="Please leave a review")
        review_label.pack(pady=10)

        stars_label = ttk.Label(review_window, text="Rating (1-5 stars):")
        stars_label.pack(pady=5)

        stars = ttk.Combobox(review_window, values=["1", "2", "3", "4", "5"], state='readonly')
        stars.pack(pady=5)

        review_text = ttk.Text(review_window, height=5, width=30)
        review_text.pack(pady=10)

        submit_button = ttk.Button(review_window, text="Submit", command=lambda: [self.save_review(stars.get(), review_text.get("1.0", ttk.END)), review_window.destroy(), self.show_thank_you()])
        submit_button.pack()

    def save_review(self, rating, comment):
        print(f"Rating: {rating}, Comment: {comment}")

    def show_thank_you(self):
        thank_you_window = ttk.Toplevel()
        thank_you_window.title("Thank You!")
        thank_you_window.geometry("500x150")

        thank_you_label = ttk.Label(thank_you_window, text="Thank you for your review!\nWe hope to see you again soon!", font=('Arial', 14))
        thank_you_label.pack( pady=20)

        thank_you_window.after(1000, lambda: [thank_you_window.destroy(), self.destroy()])

if __name__ == "__main__":
    app = FoodOrderingApp()
    app.style = "cyborg"
    app.mainloop()