import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests

def fetch_live_exchange_rates():
    api_key = 'de13d0be666eaf67b6ab0982'  # Replace with your ExchangeRate-API key
    url = f"https://v6.exchangerate-api.com/v6/de13d0be666eaf67b6ab0982/latest/CAD"
    
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
        original_price_cad = float(entry_original_price.get())
        trade_in_value_cad = float(entry_trade_in_value.get())
        private_sale_value_cad = float(entry_private_sale_value.get())
        new_car_price_cad = float(entry_new_car_price.get())
        tax_rate = float(entry_tax_rate.get()) / 100
        dealer_fee_cad = float(entry_dealer_fee.get())
        
        # Fetch live exchange rates
        exchange_rate_rmb, exchange_rate_usd = fetch_live_exchange_rates()
        if exchange_rate_rmb is None or exchange_rate_usd is None:
            result_label.config(text="Error fetching exchange rates.")
            return

        # Calculate total original cost including tax
        original_tax_cad = original_price_cad * tax_rate
        total_original_cost_cad = original_price_cad + original_tax_cad

        # Calculate tax credit for trade-in
        tax_credit_cad = trade_in_value_cad * tax_rate
        
        # Calculate total cost for new car with trade-in
        taxable_amount_new_car_trade_in_cad = new_car_price_cad - trade_in_value_cad
        tax_new_car_trade_in_cad = taxable_amount_new_car_trade_in_cad * tax_rate
        total_new_car_trade_in_cad = new_car_price_cad + tax_new_car_trade_in_cad + dealer_fee_cad

        # Calculate financial loss with trade-in
        financial_loss_trade_in_cad = total_new_car_trade_in_cad - trade_in_value_cad
        financial_loss_trade_in_rmb = financial_loss_trade_in_cad * exchange_rate_rmb
        financial_loss_trade_in_usd = financial_loss_trade_in_cad * exchange_rate_usd

        # Calculate total cost for new car with private sale
        tax_new_car_private_sale_cad = new_car_price_cad * tax_rate
        total_new_car_private_sale_cad = new_car_price_cad + tax_new_car_private_sale_cad + dealer_fee_cad

        # Calculate financial loss with private sale
        financial_loss_private_sale_cad = total_new_car_private_sale_cad - private_sale_value_cad
        financial_loss_private_sale_rmb = financial_loss_private_sale_cad * exchange_rate_rmb
        financial_loss_private_sale_usd = financial_loss_private_sale_cad * exchange_rate_usd

        # Calculate loss from selling or trading in the car
        loss_trade_in_cad = total_original_cost_cad - (trade_in_value_cad + tax_credit_cad)
        loss_trade_in_rmb = loss_trade_in_cad * exchange_rate_rmb
        loss_trade_in_usd = loss_trade_in_cad * exchange_rate_usd

        loss_private_sale_cad = total_original_cost_cad - private_sale_value_cad
        loss_private_sale_rmb = loss_private_sale_cad * exchange_rate_rmb
        loss_private_sale_usd = loss_private_sale_cad * exchange_rate_usd

        # Create DataFrames to display the results
        trade_in_data = {
            "Description": ["Original Purchase Price of Car", "Original Tax", "Total Original Cost", "Trade-in Value", "New Car Price", "Tax Credit for Trade-in", "New Car Tax (After Trade-in Credit)", "Dealer Fee", "Total New Car Cost", "Financial Loss (Trade-in)", "Loss from Trade-in"],
            "Amount (in CAD$)": [original_price_cad, original_tax_cad, total_original_cost_cad, trade_in_value_cad, new_car_price_cad, tax_credit_cad, tax_new_car_trade_in_cad, dealer_fee_cad, total_new_car_trade_in_cad, financial_loss_trade_in_cad, loss_trade_in_cad],
            "Amount (in RMB)": [original_price_cad * exchange_rate_rmb, original_tax_cad * exchange_rate_rmb, total_original_cost_cad * exchange_rate_rmb, trade_in_value_cad * exchange_rate_rmb, new_car_price_cad * exchange_rate_rmb, tax_credit_cad * exchange_rate_rmb, tax_new_car_trade_in_cad * exchange_rate_rmb, dealer_fee_cad * exchange_rate_rmb, total_new_car_trade_in_cad * exchange_rate_rmb, financial_loss_trade_in_rmb, loss_trade_in_rmb],
            "Amount (in USD)": [original_price_cad * exchange_rate_usd, original_tax_cad * exchange_rate_usd, total_original_cost_cad * exchange_rate_usd, trade_in_value_cad * exchange_rate_usd, new_car_price_cad * exchange_rate_usd, tax_credit_cad * exchange_rate_usd, tax_new_car_trade_in_cad * exchange_rate_usd, dealer_fee_cad * exchange_rate_usd, total_new_car_trade_in_cad * exchange_rate_usd, financial_loss_trade_in_usd, loss_trade_in_usd]
        }

        private_sale_data = {
            "Description": ["Original Purchase Price of Car", "Original Tax", "Total Original Cost", "Private Sale Value", "New Car Price", "New Car Tax", "Dealer Fee", "Total New Car Cost", "Financial Loss (Private Sale)", "Loss from Private Sale"],
            "Amount (in CAD$)": [original_price_cad, original_tax_cad, total_original_cost_cad, private_sale_value_cad, new_car_price_cad, tax_new_car_private_sale_cad, dealer_fee_cad, total_new_car_private_sale_cad, financial_loss_private_sale_cad, loss_private_sale_cad],
            "Amount (in RMB)": [original_price_cad * exchange_rate_rmb, original_tax_cad * exchange_rate_rmb, total_original_cost_cad * exchange_rate_rmb, private_sale_value_cad * exchange_rate_rmb, new_car_price_cad * exchange_rate_rmb, tax_new_car_private_sale_cad * exchange_rate_rmb, dealer_fee_cad * exchange_rate_rmb, total_new_car_private_sale_cad * exchange_rate_rmb, financial_loss_private_sale_rmb, loss_private_sale_rmb],
            "Amount (in USD)": [original_price_cad * exchange_rate_usd, original_tax_cad * exchange_rate_usd, total_original_cost_cad * exchange_rate_usd, private_sale_value_cad * exchange_rate_usd, new_car_price_cad * exchange_rate_usd, tax_new_car_private_sale_cad * exchange_rate_usd, dealer_fee_cad * exchange_rate_usd, total_new_car_private_sale_cad * exchange_rate_usd, financial_loss_private_sale_usd, loss_private_sale_usd]
        }

        trade_in_df = pd.DataFrame(trade_in_data)
        private_sale_df = pd.DataFrame(private_sale_data)

        display_results(trade_in_df, private_sale_df)
    except ValueError:
        result_label.config(text="Please enter valid numbers.")

def display_results(trade_in_df, private_sale_df):
    # Convert DataFrames to string
    trade_in_text = trade_in_df.to_string(index=False)
    private_sale_text = private_sale_df.to_string(index=False)

    # Combine the text results with extra space
    result_text = f"Trade-in Options:\n{trade_in_text}\n\n\n\nPrivate Sale Options:\n{private_sale_text}"

    # Enable text widget, insert the result text, then disable it
    result_text_widget.configure(state='normal')
    result_text_widget.delete("1.0", tk.END)
    result_text_widget.insert(tk.END, result_text)

    # Highlight specific keywords in the text
    highlight_text(result_text_widget, "Financial Loss (Trade-in)", "Loss from Trade-in", "Financial Loss (Private Sale)", "Loss from Private Sale")
    colorize_columns(result_text_widget, ["Description"], "blue", 12)
    colorize_columns(result_text_widget, ["Amount (in CAD$)"], "green", 10)
    colorize_columns(result_text_widget, ["Amount (in RMB)"], "red", 10)
    colorize_columns(result_text_widget, ["Amount (in USD)"], "orange", 10)
    colorize_text(result_text_widget, ["Trade-in Options:", "Private Sale Options:"], "purple", 14)
    result_text_widget.configure(state='disabled')

    # Adjust height of the text widget to fit content
    result_text_widget.update_idletasks()
    num_lines = int(result_text_widget.index('end-1c').split('.')[0])
    result_text_widget.configure(height=num_lines)

    # Auto resize the window to fit the content
    root.geometry(f"{max(800, result_text_widget.winfo_reqwidth())}x{20 * num_lines + 200}")

def highlight_text(text_widget, *keywords):
    # Function to highlight specific keywords in the text widget
    for keyword in keywords:
        start_idx = text_widget.search(keyword, "1.0", tk.END)
        while start_idx:
            end_idx = f"{start_idx}+{len(keyword)}c"
            text_widget.tag_add("highlight", start_idx, end_idx)
            start_idx = text_widget.search(keyword, end_idx, tk.END)
    text_widget.tag_configure("highlight", font=("TkDefaultFont", 10, "bold"))

def colorize_columns(text_widget, column_names, color, font_size):
    for column_name in column_names:
        start_idx = text_widget.search(column_name, "1.0", tk.END)
        while start_idx:
            end_idx = f"{start_idx}+{len(column_name)}c"
            text_widget.tag_add(column_name, start_idx, end_idx)
            start_idx = text_widget.search(column_name, end_idx, tk.END)
        text_widget.tag_configure(column_name, foreground=color, font=("TkDefaultFont", font_size))

def colorize_text(text_widget, texts, color, font_size):
    for text in texts:
        start_idx = text_widget.search(text, "1.0", tk.END)
        while start_idx:
            end_idx = f"{start_idx}+{len(text)}c"
            text_widget.tag_add(text, start_idx, end_idx)
            start_idx = text_widget.search(text, end_idx, tk.END)
        text_widget.tag_configure(text, foreground=color, font=("TkDefaultFont", font_size, "bold"))

# Create the main window
root = tk.Tk()
root.title("Financial Loss Calculator")

# Create and place the widgets
ttk.Label(root, text="Original Purchase Price (CAD$):").grid(column=0, row=0, padx=10, pady=5)
entry_original_price = ttk.Entry(root)
entry_original_price.grid(column=1, row=0, padx=10, pady=5)
entry_original_price.insert(0, "29500")  # Set default value

ttk.Label(root, text="Trade-in Value (CAD$):").grid(column=0, row=1, padx=10, pady=5)
entry_trade_in_value = ttk.Entry(root)
entry_trade_in_value.grid(column=1, row=1, padx=10, pady=5)
entry_trade_in_value.insert(0, "24000")  # Set default value

ttk.Label(root, text="Private Sale Value (CAD$):").grid(column=0, row=2, padx=10, pady=5)
entry_private_sale_value = ttk.Entry(root)
entry_private_sale_value.grid(column=1, row=2, padx=10, pady=5)
entry_private_sale_value.insert(0, "28000")  # Set default value

ttk.Label(root, text="New Car Price (CAD$):").grid(column=0, row=3, padx=10, pady=5)
entry_new_car_price = ttk.Entry(root)
entry_new_car_price.grid(column=1, row=3, padx=10, pady=5)
entry_new_car_price.insert(0, "36500")  # Set default value

ttk.Label(root, text="Tax Rate (%):").grid(column=0, row=4, padx=10, pady=5)
entry_tax_rate = ttk.Entry(root)
entry_tax_rate.grid(column=1, row=4, padx=10, pady=5)
entry_tax_rate.insert(0, "12")  # Set default value

ttk.Label(root, text="Dealer Fee (CAD$):").grid(column=0, row=5, padx=10, pady=5)
entry_dealer_fee = ttk.Entry(root)
entry_dealer_fee.grid(column=1, row=5, padx=10, pady=5)
entry_dealer_fee.insert(0, "1000")  # Set default value

calculate_button = ttk.Button(root, text="Calculate", command=calculate_financial_loss)
calculate_button.grid(column=0, row=6, columnspan=2, pady=10)

# Text widget to display the results
result_text_widget = tk.Text(root, wrap="word", state="disabled", width=80, height=20)
result_text_widget.grid(column=0, row=7, columnspan=2, padx=10, pady=10, sticky="nsew")

# Label to display messages
result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=8, columnspan=2, padx=10, pady=5)

# Configure the grid to make the text widget resize with the window
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()

