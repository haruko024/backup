import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk

ITEMS = {
    "Chicken With Rice": 120,
    "Samgyup": 399,
    "Amerikano": 150,
    "Ramen": 800
}

cart = []
total = 0

def add_item(item):
    global total
    price = ITEMS[item]
    cart.append((item, price))
    total += price
    update_cart_display()

def remove_item():
    global total
    selection = cart_list.curselection()
    if not selection:
        messagebox.showwarning("Remove Item", "Please select an item to remove.")
        return
    index = selection[0]
    item, price = cart.pop(index)
    total -= price
    update_cart_display()

def reset_cart():
    global cart, total
    cart = []
    total = 0
    update_cart_display()
    cash_entry.delete(0, tk.END)

def update_cart_display():
    cart_list.delete(0, tk.END)
    for item, price in cart:
        cart_list.insert(tk.END, f"{item} - ₱{price}")
    total_label.config(text=f"Total: ₱{total}")

def process_payment():
    method = payment_var.get()
    if method == "":
        messagebox.showwarning("Payment", "Please select a payment method")
        return

    if method == "Cash":
        process_cash_payment()
    elif method == "Online pay":
        simulate_online_payment()
    elif method == "Credit Card":
        simulate_credit_card_payment()

def toggle_cash_entry():
    if payment_var.get() == "Cash":
        cash_entry.config(state="normal")
    else:
        cash_entry.delete(0, tk.END)
        cash_entry.config(state="disabled")

# ---------------- CASH PAYMENT ----------------
def process_cash_payment():
    global total
    try:
        paid_amount = int(cash_entry.get())
        if paid_amount < total:
            messagebox.showerror("Error", "Insufficient amount!")
        else:
            change = paid_amount - total
            messagebox.showinfo(
                "Payment Complete",
                f"Paid: ₱{paid_amount}\nChange: ₱{change}"
            )
            reset_cart()
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")

# ---------------- ONLINE PAYMENT ----------------
def simulate_online_payment():
    if total == 0:
        messagebox.showwarning("Payment", "Your cart is empty!")
        return

    pay_window = Toplevel(root)
    pay_window.title("Online Payment")
    pay_window.geometry("300x350")
    pay_window.config(bg="white")

    tk.Label(pay_window, text="Scan to Pay", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    try:
        qr_img = Image.open("qr.png")  # Replace with your QR image file
        qr_img = qr_img.resize((200, 200))
        qr_photo = ImageTk.PhotoImage(qr_img)
        tk.Label(pay_window, image=qr_photo, bg="white").pack(pady=10)
        pay_window.qr_photo = qr_photo
    except FileNotFoundError:
        tk.Label(pay_window, text="[QR Code Missing]", bg="white", fg="red", font=("Arial", 12)).pack(pady=20)

    tk.Label(pay_window, text=f"Amount: ₱{total}", font=("Arial", 12), bg="white").pack(pady=5)

    def confirm_payment():
        messagebox.showinfo("Payment Complete", "Online payment successful!\nThank you for your purchase.")
        pay_window.destroy()
        reset_cart()

    tk.Button(pay_window, text="Confirm Payment", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
              command=confirm_payment).pack(pady=10)

# ---------------- CREDIT CARD PAYMENT ----------------
def simulate_credit_card_payment():
    if total == 0:
        messagebox.showwarning("Payment", "Your cart is empty!")
        return

    card_window = Toplevel(root)
    card_window.title("Credit Card Payment")
    card_window.geometry("300x300")
    card_window.config(bg="white")

    tk.Label(card_window, text="Enter Card Details", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    tk.Label(card_window, text="Card Number:", bg="white").pack(anchor="w", padx=20)
    card_number = tk.Entry(card_window)
    card_number.pack(padx=20, fill="x")

    tk.Label(card_window, text="Expiry (MM/YY):", bg="white").pack(anchor="w", padx=20)
    expiry = tk.Entry(card_window)
    expiry.pack(padx=20, fill="x")

    tk.Label(card_window, text="CVV:", bg="white").pack(anchor="w", padx=20)
    cvv = tk.Entry(card_window, show="*")
    cvv.pack(padx=20, fill="x")

    tk.Label(card_window, text=f"Amount: ₱{total}", font=("Arial", 12), bg="white").pack(pady=10)

    def confirm_card_payment():
        if not card_number.get().isdigit() or len(card_number.get()) not in [13, 16]:
            messagebox.showerror("Error", "Invalid card number!")
            return
        if not expiry.get() or "/" not in expiry.get():
            messagebox.showerror("Error", "Invalid expiry date!")
            return
        if not cvv.get().isdigit() or len(cvv.get()) != 3:
            messagebox.showerror("Error", "Invalid CVV!")
            return

        messagebox.showinfo("Payment Complete", "Credit card payment approved!\nThank you for your purchase.")
        card_window.destroy()
        reset_cart()

    tk.Button(card_window, text="Confirm Payment", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
              command=confirm_card_payment).pack(pady=10)

# ---------------- MAIN UI ----------------
root = tk.Tk()
root.title("Store Payment System")
root.geometry("800x350")

frame_style = {"bg": "#ffffff", "bd": 3, "relief": "ridge"}

item_frame = tk.LabelFrame(root, text="Items", font=("Arial", 12, "bold"), **frame_style)
item_frame.place(x=20, y=20, width=200, height=300)

for item, price in ITEMS.items():
    btn = tk.Button(
        item_frame,
        text=f"{item} - ₱{price}",
        bg="#ffb84d",
        fg="black",
        font=("Arial", 10, "bold"),
        command=lambda i=item: add_item(i)
    )
    btn.pack(fill="x", padx=5, pady=2)

cart_frame = tk.LabelFrame(root, text="Cart", font=("Arial", 12, "bold"), **frame_style)
cart_frame.place(x=240, y=20, width=250, height=300)

cart_list = tk.Listbox(cart_frame, height=10, width=30, font=("Arial", 10))
cart_list.pack()

total_label = tk.Label(cart_frame, text="Total: ₱0", font=("Arial", 14, "bold"), bg="#ffffff")
total_label.pack(pady=5)

tk.Button(cart_frame, text="Remove Selected", bg="#ff6666", fg="white", font=("Arial", 10, "bold"), command=remove_item).pack(pady=3)
tk.Button(cart_frame, text="Reset Cart", bg="#66b3ff", fg="white", font=("Arial", 10, "bold"), command=reset_cart).pack(pady=3)

payment_frame = tk.LabelFrame(root, text="Payment", font=("Arial", 12, "bold"), **frame_style)
payment_frame.place(x=520, y=20, width=250, height=300)

payment_var = tk.StringVar()

tk.Radiobutton(payment_frame, text="Cash", variable=payment_var, value="Cash", bg="#ffffff", command=toggle_cash_entry).pack(anchor="w")
tk.Radiobutton(payment_frame, text="Credit Card", variable=payment_var, value="Credit Card", bg="#ffffff", command=toggle_cash_entry).pack(anchor="w")
tk.Radiobutton(payment_frame, text="Online Payment (Gcash, Paymaya)", variable=payment_var, value="Online pay", bg="#ffffff", command=toggle_cash_entry).pack(anchor="w")

cash_entry = tk.Entry(payment_frame)
cash_entry.pack(pady=5)
cash_entry.config(state="disabled")

tk.Button(payment_frame, text="Pay", bg="#ffb84d", font=("Arial", 10, "bold"), command=process_payment).pack(pady=10)

root.mainloop()
