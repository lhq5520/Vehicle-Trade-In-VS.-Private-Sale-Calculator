import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests
from PIL import Image, ImageTk

def fetch_live_exchange_rates():
    api_key = 'de13d0be666eaf67b6ab0982'  # Replace with your ExchangeRate-API key
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/CAD"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data['conversion_rates']['CNY'], data['conversion_rates']['USD']
    except Exception as e:
        print("Error fetching exchange rate:", e)
        return None, None

def calculate_financial_loss():
    try:
        # Get values from input fields
        original_price_cad = round(float(entry_original_price.get()))
        trade_in_value_cad = round(float(entry_trade_in_value.get()))
        private_sale_value_cad = round(float(entry_private_sale_value.get()))
        new_car_price_cad = round(float(entry_new_car_price.get()))
        tax_rate = float(entry_tax_rate.get()) / 100
        dealer_fee_cad = round(float(entry_dealer_fee.get()))
        
        # Fetch live exchange rates
        exchange_rate_rmb, exchange_rate_usd = fetch_live_exchange_rates()
        if exchange_rate_rmb is None or exchange_rate_usd is None:
            result_label.config(text="Error fetching exchange rates.")
            return

        # Calculate total original cost including tax
        original_tax_cad = round(original_price_cad * tax_rate)
        total_original_cost_cad = round(original_price_cad + original_tax_cad)

        # Calculate tax credit for trade-in
        tax_credit_cad = round(trade_in_value_cad * tax_rate)
        
        # Calculate total cost for new car with trade-in
        taxable_amount_new_car_trade_in_cad = new_car_price_cad - trade_in_value_cad
        tax_new_car_trade_in_cad = round(taxable_amount_new_car_trade_in_cad * tax_rate)
        total_new_car_trade_in_cad = round(new_car_price_cad + tax_new_car_trade_in_cad + dealer_fee_cad)

        # Calculate financial loss with trade-in
        financial_loss_trade_in_cad = round(total_new_car_trade_in_cad - trade_in_value_cad)
        financial_loss_trade_in_rmb = round(financial_loss_trade_in_cad * exchange_rate_rmb)
        financial_loss_trade_in_usd = round(financial_loss_trade_in_cad * exchange_rate_usd)

        # Calculate total cost for new car with private sale
        tax_new_car_private_sale_cad = round(new_car_price_cad * tax_rate)
        total_new_car_private_sale_cad = round(new_car_price_cad + tax_new_car_private_sale_cad + dealer_fee_cad)

        # Calculate financial loss with private sale
        financial_loss_private_sale_cad = round(total_new_car_private_sale_cad - private_sale_value_cad)
        financial_loss_private_sale_rmb = round(financial_loss_private_sale_cad * exchange_rate_rmb)
        financial_loss_private_sale_usd = round(financial_loss_private_sale_cad * exchange_rate_usd)

        # Calculate loss from selling or trading in the car
        loss_trade_in_cad = round(total_original_cost_cad - (trade_in_value_cad + tax_credit_cad))
        loss_trade_in_rmb = round(loss_trade_in_cad * exchange_rate_rmb)
        loss_trade_in_usd = round(loss_trade_in_cad * exchange_rate_usd)

        loss_private_sale_cad = round(total_original_cost_cad - private_sale_value_cad)
        loss_private_sale_rmb = round(loss_private_sale_cad * exchange_rate_rmb)
        loss_private_sale_usd = round(loss_private_sale_cad * exchange_rate_usd)

        # Calculate equilibrium private sale value
        equilibrium_private_sale_value_cad = round(total_new_car_private_sale_cad - financial_loss_trade_in_cad)

        # Create DataFrames to display the results
        trade_in_data = {
            "Description": ["🚗 Original Purchase Price of Car", "💸 Original Tax", "📊 Total Original Cost", "🚘 New Car Price", "💰 Tax Credit for Trade-in", "💸 New Car Tax (After Trade-in Credit)", "📜 Dealer Fee", "📈 Total New Car Cost", "❗ Financial Loss (Trade-in)", "❗ Loss from Trade-in"],
            "Amount (CAD$)": [f"{original_price_cad}", f"{original_tax_cad}", f"{total_original_cost_cad}", f"{new_car_price_cad}", f"{tax_credit_cad}", f"{tax_new_car_trade_in_cad}", f"{dealer_fee_cad}", f"{total_new_car_trade_in_cad}", f"{financial_loss_trade_in_cad}", f"{loss_trade_in_cad}"],
            "Amount (RMB)": [f"¥{round(original_price_cad * exchange_rate_rmb)}", f"¥{round(original_tax_cad * exchange_rate_rmb)}", f"¥{round(total_original_cost_cad * exchange_rate_rmb)}", f"¥{round(new_car_price_cad * exchange_rate_rmb)}", f"¥{round(tax_credit_cad * exchange_rate_rmb)}", f"¥{round(tax_new_car_trade_in_cad * exchange_rate_rmb)}", f"¥{round(dealer_fee_cad * exchange_rate_rmb)}", f"¥{round(total_new_car_trade_in_cad * exchange_rate_rmb)}", f"¥{financial_loss_trade_in_rmb}", f"¥{loss_trade_in_rmb}"],
            "Amount (USD)": [f"${round(original_price_cad * exchange_rate_usd)}", f"${round(original_tax_cad * exchange_rate_usd)}", f"${round(total_original_cost_cad * exchange_rate_usd)}", f"${round(new_car_price_cad * exchange_rate_usd)}", f"${round(tax_credit_cad * exchange_rate_usd)}", f"${round(tax_new_car_trade_in_cad * exchange_rate_usd)}", f"${round(dealer_fee_cad * exchange_rate_usd)}", f"${round(total_new_car_trade_in_cad * exchange_rate_usd)}", f"${financial_loss_trade_in_usd}", f"${loss_trade_in_usd}"]
        }

        private_sale_data = {
            "Description": ["🚗 Original Purchase Price of Car", "💸 Original Tax", "📊 Total Original Cost", "🚘 New Car Price", "💸 New Car Tax", "📜 Dealer Fee", "📈 Total New Car Cost", "❗ Financial Loss (Private Sale)", "❗ Loss from Private Sale"],
            "Amount (CAD$)": [f"{original_price_cad}", f"{original_tax_cad}", f"{total_original_cost_cad}", f"{new_car_price_cad}", f"{tax_new_car_private_sale_cad}", f"{dealer_fee_cad}", f"{total_new_car_private_sale_cad}", f"{financial_loss_private_sale_cad}", f"{loss_private_sale_cad}"],
            "Amount (RMB)": [f"¥{round(original_price_cad * exchange_rate_rmb)}", f"¥{round(original_tax_cad * exchange_rate_rmb)}", f"¥{round(total_original_cost_cad * exchange_rate_rmb)}", f"¥{round(new_car_price_cad * exchange_rate_rmb)}", f"¥{round(tax_new_car_private_sale_cad * exchange_rate_rmb)}", f"¥{round(dealer_fee_cad * exchange_rate_rmb)}", f"¥{round(total_new_car_private_sale_cad * exchange_rate_rmb)}", f"¥{financial_loss_private_sale_rmb}", f"¥{loss_private_sale_rmb}"],
            "Amount (USD)": [f"${round(original_price_cad * exchange_rate_usd)}", f"${round(original_tax_cad * exchange_rate_usd)}", f"${round(total_original_cost_cad * exchange_rate_usd)}", f"${round(new_car_price_cad * exchange_rate_usd)}", f"${round(tax_new_car_private_sale_cad * exchange_rate_usd)}", f"${round(dealer_fee_cad * exchange_rate_usd)}", f"${round(total_new_car_private_sale_cad * exchange_rate_usd)}", f"${financial_loss_private_sale_usd}", f"${loss_private_sale_usd}"]
        }

        equilibrium_data = {
            "Description": ["Equilibrium Private Sale Value"],
            "Amount (CAD$)": [f"C${equilibrium_private_sale_value_cad}"],
            "Amount (RMB)": [f"¥{round(equilibrium_private_sale_value_cad * exchange_rate_rmb)}"],
            "Amount (USD)": [f"${round(equilibrium_private_sale_value_cad * exchange_rate_usd)}"]
        }

        trade_in_df = pd.DataFrame(trade_in_data)
        private_sale_df = pd.DataFrame(private_sale_data)
        equilibrium_df = pd.DataFrame(equilibrium_data)

        show_results_window(trade_in_df, private_sale_df, equilibrium_df, trade_in_value_cad, private_sale_value_cad)
    except ValueError:
        result_label.config(text="Please enter valid numbers.")

def show_results_window(trade_in_df, private_sale_df, equilibrium_df, trade_in_value, private_sale_value):
    # Close existing results window if it exists
    if hasattr(show_results_window, 'results_window') and show_results_window.results_window.winfo_exists():
        show_results_window.results_window.destroy()

    results_window = tk.Toplevel(root)
    show_results_window.results_window = results_window  # Store reference to the window
    results_window.title("Calculation Results")

    # Set the position of the new window to the right of the main window
    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    results_window.geometry(f"+{x}+{y}")

    # Function to update the position of the results window
    def update_results_window_position(event):
        try:
            if abs(root.winfo_x() + root.winfo_width() - results_window.winfo_x()) > 10 or abs(root.winfo_y() - results_window.winfo_y()) > 10:
                x = root.winfo_x() + root.winfo_width()
                y = root.winfo_y()
                results_window.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass

    def update_main_window_position(event):
        try:
            if abs(results_window.winfo_x() - root.winfo_width() - root.winfo_x()) > 10 or abs(results_window.winfo_y() - root.winfo_y()) > 10:
                x = results_window.winfo_x() - root.winfo_width()
                y = results_window.winfo_y()
                root.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass

    # Delay updating the positions to reduce frequency
    root.bind("<Configure>", lambda event: root.after(100, update_results_window_position, event))
    results_window.bind("<Configure>", lambda event: root.after(100, update_main_window_position, event))

    # Function to create a treeview for displaying the data
    def create_treeview(data, title, value, image, height):
        frame = ttk.Frame(results_window)
        frame.pack(pady=5)

        title_frame = ttk.Frame(frame)
        title_frame.grid(row=0, column=0, columnspan=2)
        title_label = ttk.Label(title_frame, text=f"{title}: ${value}", image=image, compound="left", font=("TkDefaultFont", 12, "bold"))
        title_label.pack(pady=5)

        tree = ttk.Treeview(frame, columns=("Description", "CAD", "RMB", "USD"), show="headings", height=height)
        tree.heading("Description", text="Description")
        tree.heading("CAD", text="Amount (in CAD$)")
        tree.heading("RMB", text="Amount (in RMB)")
        tree.heading("USD", text="Amount (in USD)")

        tree.column("Description", anchor="w", width=300)
        tree.column("CAD", anchor="center", width=120)
        tree.column("RMB", anchor="center", width=120)
        tree.column("USD", anchor="center", width=120)

        for i in range(len(data["Description"])):
            tree.insert("", "end", values=(data["Description"][i], data["Amount (CAD$)"][i], data["Amount (RMB)"][i], data["Amount (USD)"][i]))

        for column in ["CAD", "RMB", "USD"]:
            for row in tree.get_children():
                value = tree.set(row, column)
                if "Financial Loss" in tree.item(row, "values")[0] or "Loss from" in tree.item(row, "values")[0]:
                    tree.tag_configure("highlight", background="yellow")
                    tree.item(row, tags="highlight")

        tree.grid(row=1, column=0, columnspan=2, pady=5)

    # Load images for section titles
    trade_in_img = ImageTk.PhotoImage(Image.open("trade_in_value.png").resize((20, 20)))
    private_sale_img = ImageTk.PhotoImage(Image.open("private_sale_value.png").resize((20, 20)))

    create_treeview(trade_in_df.to_dict(), "Trade-in Options", trade_in_value, trade_in_img, height=10)
    create_treeview(private_sale_df.to_dict(), "Private Sale Options", private_sale_value, private_sale_img, height=9)

    equilibrium_text = f"Equilibrium Private Sale Value: {equilibrium_df['Amount (CAD$)'][0]}, {equilibrium_df['Amount (RMB)'][0]}, {equilibrium_df['Amount (USD)'][0]}"
    ttk.Label(results_window, text=equilibrium_text, font=("TkDefaultFont", 12, "bold")).pack(pady=5)

# Create the main window
root = tk.Tk()
root.title("Financial Loss Calculator")

# Load images for input labels
original_price_img = ImageTk.PhotoImage(Image.open("original_price.png").resize((20, 20)))
trade_in_value_img = ImageTk.PhotoImage(Image.open("trade_in_value.png").resize((20, 20)))
private_sale_value_img = ImageTk.PhotoImage(Image.open("private_sale_value.png").resize((20, 20)))
new_car_price_img = ImageTk.PhotoImage(Image.open("new_car_price.png").resize((20, 20)))
tax_rate_img = ImageTk.PhotoImage(Image.open("tax_rate.png").resize((20, 20)))
dealer_fee_img = ImageTk.PhotoImage(Image.open("dealer_fee.png").resize((20, 20)))

# Create and place the widgets
ttk.Label(root, text="Original Purchase Price (CAD$):", image=original_price_img, compound="left").grid(column=0, row=0, padx=10, pady=5)
entry_original_price = ttk.Entry(root)
entry_original_price.grid(column=1, row=0, padx=10, pady=5)
entry_original_price.insert(0, "29500")  # Set default value

ttk.Label(root, text="Trade-in Value (CAD$):", image=trade_in_value_img, compound="left").grid(column=0, row=1, padx=10, pady=5)
entry_trade_in_value = ttk.Entry(root)
entry_trade_in_value.grid(column=1, row=1, padx=10, pady=5)
entry_trade_in_value.insert(0, "24000")  # Set default value

ttk.Label(root, text="Private Sale Value (CAD$):", image=private_sale_value_img, compound="left").grid(column=0, row=2, padx=10, pady=5)
entry_private_sale_value = ttk.Entry(root)
entry_private_sale_value.grid(column=1, row=2, padx=10, pady=5)
entry_private_sale_value.insert(0, "26000")  # Set default value

ttk.Label(root, text="New Car Price (CAD$):", image=new_car_price_img, compound="left").grid(column=0, row=3, padx=10, pady=5)
entry_new_car_price = ttk.Entry(root)
entry_new_car_price.grid(column=1, row=3, padx=10, pady=5)
entry_new_car_price.insert(0, "36500")  # Set default value

ttk.Label(root, text="Tax Rate (%):", image=tax_rate_img, compound="left").grid(column=0, row=4, padx=10, pady=5)
entry_tax_rate = ttk.Entry(root)
entry_tax_rate.grid(column=1, row=4, padx=10, pady=5)
entry_tax_rate.insert(0, "12")  # Set default value

ttk.Label(root, text="Dealer Fee (CAD$):", image=dealer_fee_img, compound="left").grid(column=0, row=5, padx=10, pady=5)
entry_dealer_fee = ttk.Entry(root)
entry_dealer_fee.grid(column=1, row=5, padx=10, pady=5)
entry_dealer_fee.insert(0, "500")  # Set default value

calculate_button = ttk.Button(root, text="Calculate", command=calculate_financial_loss)
calculate_button.grid(column=0, row=6, columnspan=2, pady=10)

# Frame to display the results
results_frame = ttk.Frame(root)
results_frame.grid(column=0, row=7, columnspan=2, padx=10, pady=10, sticky="nsew")

# Label to display messages
result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=8, columnspan=2, padx=10, pady=5)

# Configure the grid to make the results frame resize with the window
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()
