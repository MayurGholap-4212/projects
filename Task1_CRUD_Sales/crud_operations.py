import pandas as pd
import os
from tabulate import tabulate
from colorama import Fore, init
init()

# Constants
FILE = "sales_data.csv"

# Helper Functions
def get_valid_input(prompt, input_type=str, allow_blank=False):
    while True:
        user_input = input(prompt).strip()
        if not user_input and allow_blank:
            return None
        try:
            return input_type(user_input)
        except ValueError:
            print(Fore.RED + f"⚠️ Invalid input! Please enter a {input_type.__name__}." + Fore.RESET)

def show_records(df):
    if df.empty:
        print(Fore.YELLOW + "No records found." + Fore.RESET)
    else:
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))

# Core CRUD Functions
def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE, dtype={'Phone': str})
        df['ID'] = df['ID'].astype(int)
        return df
    else:
        print(Fore.YELLOW + "No existing dataset found. Starting with empty database." + Fore.RESET)
        return pd.DataFrame(columns=[
            "ID", "Date", "CustomerName", "Email", "Phone", "Product", 
            "Category", "Quantity", "PricePerUnit", "TotalAmount", 
            "PaymentMethod", "ShippingAddress", "Status"
        ])

def save_data(df):
    df.to_csv(FILE, index=False)
    print(Fore.GREEN + "✅ Data saved successfully!" + Fore.RESET)

def create_record():
    df = load_data()
    new_id = df['ID'].max() + 1 if not df.empty else 1

    print(Fore.CYAN + "\n➕ Add New Sale Record" + Fore.RESET)
    new_record = {
        "ID": new_id,
        "Date": get_valid_input("Date (YYYY-MM-DD): ", str),
        "CustomerName": get_valid_input("Customer Name: ", str),
        "Email": get_valid_input("Email: ", str),
        "Phone": get_valid_input("Phone: ", str),
        "Product": get_valid_input("Product: ", str),
        "Category": get_valid_input("Category: ", str),
        "Quantity": get_valid_input("Quantity: ", int),
        "PricePerUnit": get_valid_input("Price per Unit: ", float),
        "PaymentMethod": get_valid_input("Payment Method: ", str),
        "ShippingAddress": get_valid_input("Shipping Address: ", str),
        "Status": get_valid_input("Status: ", str)
    }
    new_record["TotalAmount"] = new_record["Quantity"] * new_record["PricePerUnit"]

    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    save_data(df)
    print(Fore.GREEN + f"✅ Record with ID {new_id} added successfully!" + Fore.RESET)

def read_records():
    df = load_data()
    if df.empty:
        print(Fore.YELLOW + "No records available to search." + Fore.RESET)
        return

    print(Fore.CYAN + "\n🔎 Search Options:" + Fore.RESET)
    print("1. By ID")
    print("2. By Customer Name")
    print("3. By Product")
    print("4. By Date Range")
    print("5. By Category")
    
    choice = get_valid_input("Choose search option (1-5): ", int)
    
    if choice == 1:
        id_val = get_valid_input("Enter ID: ", int)
        result = df[df['ID'] == id_val]
    elif choice == 2:
        name = get_valid_input("Enter Customer Name: ", str)
        result = df[df['CustomerName'].str.contains(name, case=False)]
    elif choice == 3:
        product = get_valid_input("Enter Product: ", str)
        result = df[df['Product'].str.contains(product, case=False)]
    elif choice == 4:
        start_date = get_valid_input("Start Date (YYYY-MM-DD): ", str)
        end_date = get_valid_input("End Date (YYYY-MM-DD): ", str)
        result = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    elif choice == 5:
        category = get_valid_input("Enter Category: ", str)
        result = df[df['Category'].str.contains(category, case=False)]
    else:
        print(Fore.RED + "⚠️ Invalid choice. Showing all records." + Fore.RESET)
        result = df
    
    print(Fore.CYAN + "\n📄 Search Results:" + Fore.RESET)
    show_records(result)

def update_record():
    df = load_data()
    if df.empty:
        print(Fore.YELLOW + "No records available to update." + Fore.RESET)
        return

    id_val = get_valid_input("\nEnter ID to update: ", int)
    if id_val not in df['ID'].values:
        print(Fore.RED + "⚠️ Record not found." + Fore.RESET)
        return

    record = df[df['ID'] == id_val].iloc[0]
    print(Fore.CYAN + "\n✏️ Editing Record ID", id_val, Fore.RESET)
    print("Leave field blank to keep current value.")
    
    for col in df.columns:
        if col == "ID": continue
        current_val = record[col]
        new_val = get_valid_input(f"{col} (Current: {current_val}): ", str, allow_blank=True)
        if new_val is not None:
            if col in ["Quantity"]:
                df.loc[df['ID'] == id_val, col] = int(new_val)
            elif col in ["PricePerUnit", "TotalAmount"]:
                df.loc[df['ID'] == id_val, col] = float(new_val)
            else:
                df.loc[df['ID'] == id_val, col] = new_val

    # Recalculate TotalAmount
    quantity = df.loc[df['ID'] == id_val, "Quantity"].values[0]
    price = df.loc[df['ID'] == id_val, "PricePerUnit"].values[0]
    df.loc[df['ID'] == id_val, "TotalAmount"] = quantity * price

    save_data(df)
    print(Fore.GREEN + f"✅ Record ID {id_val} updated successfully!" + Fore.RESET)

def delete_record():
    df = load_data()
    if df.empty:
        print(Fore.YELLOW + "No records available to delete." + Fore.RESET)
        return

    id_val = get_valid_input("\nEnter ID to delete: ", int)
    if id_val not in df['ID'].values:
        print(Fore.RED + "⚠️ Record not found." + Fore.RESET)
        return

    record = df[df['ID'] == id_val].iloc[0]
    print(Fore.RED + "\n❌ Confirm Deletion:" + Fore.RESET)
    show_records(pd.DataFrame([record]))
    
    confirm = input("Are you sure you want to delete this record? (y/n): ").lower()
    if confirm == 'y':
        df = df[df['ID'] != id_val]
        save_data(df)
        print(Fore.GREEN + f"✅ Record ID {id_val} deleted successfully!" + Fore.RESET)
    else:
        print(Fore.YELLOW + "Deletion cancelled." + Fore.RESET)

# Main Menu
def main():
    print(Fore.BLUE + "\n=== SALES DATA MANAGER ===" + Fore.RESET)
    print("A user-friendly CRUD application for sales records")
    
    while True:
        print("\n" + Fore.BLUE + "MAIN MENU" + Fore.RESET)
        print("1. ➕ Add New Sale")
        print("2. 🔍 Search Sales")
        print("3. ✏️ Update Sale")
        print("4. ❌ Delete Sale")
        print("5. 🚪 Exit")
        
        choice = get_valid_input("\nChoose an option (1-5): ", int)
        
        if choice == 1:
            create_record()
        elif choice == 2:
            read_records()
        elif choice == 3:
            update_record()
        elif choice == 4:
            delete_record()
        elif choice == 5:
            print(Fore.BLUE + "\nThank you for using Sales Data Manager. Goodbye!" + Fore.RESET)
            break
        else:
            print(Fore.RED + "⚠️ Invalid choice. Please enter 1-5." + Fore.RESET)

if __name__ == "__main__":
    main()