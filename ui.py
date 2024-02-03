import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
from tkcalendar import DateEntry

import datetime

import db

class AssetOverviewPage(tk.Frame):
    def __init__(self, parent, controller, db_file):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db_file = db_file
        label = tk.Label(self, text="Asset Overview")
        label.pack(pady=10, padx=10)

        # Set up the Treeview
        columns = ("Asset Name", "Location", "Quantity Owned")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=25)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.populate_assets()

    def populate_assets(self):
        """ Fetch data from the database and insert into the treeview """
        # Clear the treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Fetch data from the database
        asset_data = db.fetch_asset_overview(self.db_file)
        for asset in asset_data:
            self.tree.insert("", "end", values=asset)

        # Navigation buttons
        transactions_button = tk.Button(self, text="Transactions",
                                        command=lambda: self.controller.show_frame(TransactionsPage))
        transactions_button.pack()

        net_value_button = tk.Button(self, text="NetValue",
                                     command=lambda: self.controller.show_frame(NetValuePage))
        net_value_button.pack()

class PortfolioTrackerApp(tk.Tk):
    def __init__(self, db_file,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_file = db_file
        self.title("Portfolio Tracker")

        # This container holds all the pages
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # A dictionary to hold the pages
        self.frames = {}

        for F in (TransactionsPage, NetValuePage, AssetOverviewPage):
            frame = F(container, self, self.db_file)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Add a button to navigate to the Asset Overview page
        asset_overview_button = tk.Button(self, text="Asset Overview",
                                          command=lambda: self.show_frame(AssetOverviewPage))
        asset_overview_button.pack()

        self.show_frame(TransactionsPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # Brings the selected frame to the top

class TransactionsPage(tk.Frame):
    def __init__(self, parent, controller, db_file):
        tk.Frame.__init__(self, parent)
        self.db_file = db_file
        label = tk.Label(self, text="Transactions List")
        label.pack(pady=10, padx=10)

        # Set up the Treeview
        columns = ("Date", "Symbol", "Asset Name", "Asset-Market", "Price", "Quantity", "Total", "Location", "Currency")  # Update with actual column names
        columns_width={"Date": 85, "Symbol": 50, "Asset Name": 200, "Asset-Market": 90, "Price": 50, "Quantity": 70, "Total": 80, "Location": 50, "Currency": 50}
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=45)
        
        for col in columns:
            self.tree.heading(col, text=col)  # Set the headings
            try:
                self.tree.column(col, width=columns_width[col], anchor="e")  # Set the width and anchor to right justify
            except KeyError:
                self.tree.column(col, width=100, anchor="e")  # Set the width and anchor to right justify
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # TODO: Fetch data from the database and insert into the treeview
        # for transaction in transactions:
        #     self.tree.insert("", "end", values=(data1, data2, data3, data4))

        self.populate_transactions()

        # Navigation buttons
        net_value_button = tk.Button(self, text="NetValue",
                         command=lambda: controller.show_frame(NetValuePage))
        net_value_button.pack()

        def add_and_refresh(self, db_file):
            add_transaction_wizard(db_file)
            self.populate_transactions()

        # Add transaction button with wizard then reload page to show new transaction
        add_transaction_button = tk.Button(self, text="Add Transaction", command=lambda: add_and_refresh(self, db_file))
        add_transaction_button.pack()


    def populate_transactions(self):
        """ Fetch data from the database and insert into the treeview """
        # Clear the treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Fetch data from the database
        transactions = db.fetch_all_transactions(self.db_file )
        for transaction in transactions:
            self.tree.insert("", "end", values=transaction)




class NetValuePage(tk.Frame):
    def __init__(self, parent, controller, db_file):
        tk.Frame.__init__(self, parent)
        self.db_file = db_file

        label = tk.Label(self, text="Net Value of Investments (Under Construction)")
        label.pack(pady=10, padx=10)

        # Navigation buttons
        transactions_button = tk.Button(self, text="Transactions",
                                        command=lambda: controller.show_frame(TransactionsPage))
        transactions_button.pack()

        # Here you will add code to display net value when it's implemented


if __name__ == "__main__":
    app = PortfolioTrackerApp()
    app.mainloop()



def ask_for_db_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Ask for the DB file starting from the current directory
    file_path = filedialog.askopenfilename(filetypes=[("Database files", "*.db")], initialdir=".")
    return file_path if file_path else None

def ask_for_new_db_name():
    """
    Prompt the user to enter a name for a new database file.
    Returns the file name if provided, or None if cancelled.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask for the DB name
    db_name = tk.simpledialog.askstring("New Database", "Enter name for new database:", parent=root)

    if db_name:
        if not db_name.endswith('.db'):
            db_name += '.db'  # Append .db if not already present
        return db_name
    else:
        return None
    

def get_location(db_file):
    """
    Prompts the user to select a location from a dropdown or add a new one.
    """
    def on_confirm():
        nonlocal user_input
        user_input = combo.get()
        root.quit()

    user_input = None
    root = tk.Tk()
    root.title("Select Location")

    # Fetch locations as (id, name) tuples
    location_tuples = db.get_locations(db_file)
    location_names = [location[1] for location in location_tuples] + ["New one"]

    # Create a combobox
    combo = ttk.Combobox(root, values=location_names)
    combo.pack(pady=20)
    
    # Default selection
    combo.set(location_names[0])

    # Button to confirm selection
    button = tk.Button(root, text="Confirm", command=on_confirm)
    button.pack(pady=10)

    root.mainloop()  # Start the main loop
    root.destroy()   # Destroy the root window after loop ends

    # Handle "New one" selection
    if user_input == "New one":
        new_location_name = simpledialog.askstring("New Location Name", "Enter new location name:", parent=None)
        new_location_description = simpledialog.askstring("New Location Description", "Enter new location description:", parent=None)
        location_id=db.add_location(db_file, new_location_name, new_location_description)
        return location_id
    else:
        return location_tuples[location_names.index(user_input)][0]

def get_market(db_file):
    """Prompts the user to select a market or add a new one"""
    def on_confirm():
        nonlocal user_input
        user_input = combo.get()
        root.quit()
    
    user_input = None
    root = tk.Tk()
    root.title("Select Market")

    # Fetch markets as (id, name) tuples
    market_tuples = db.get_markets(db_file)
    market_names = [market[1] for market in market_tuples] + ["New one"]

    # Create a combobox
    combo = ttk.Combobox(root, values=market_names)
    combo.pack(pady=20)
    
    # Default selection
    combo.set(market_names[0])

    # Button to confirm selection
    button = tk.Button(root, text="Confirm", command=on_confirm)
    button.pack(pady=10)

    root.mainloop()  # Start the main loop
    root.destroy()   # Destroy the root window after loop ends

    # Handle "New one" selection
    if user_input == "New one":
        new_market_name = simpledialog.askstring("New Market Name", "Enter new market name:", parent=None)
        new_market_description = simpledialog.askstring("New Market Description", "Enter new market description:", parent=None)
        market_id=db.add_market(db_file, new_market_name, new_market_description)
        return market_id
    else:
        return market_tuples[market_names.index(user_input)][0]

def get_asset(db_file):
    """Prompts the user to select an asset or add a new one"""
    def on_confirm():
        nonlocal user_input
        user_input = combo.get()
        root.quit()
    
    user_input = None
    root = tk.Tk()
    root.title("Select Asset")

    # Fetch asset markets as (id, name) tuples
    asset_tuples = db.get_assets(db_file)
    asset_names = [asset[1] for asset in asset_tuples] + ["New one"]

    # Create a combobox
    combo = ttk.Combobox(root, values=asset_names)
    combo.pack(pady=20)
    
    # Default selection
    combo.set(asset_names[0])

    # Button to confirm selection
    button = tk.Button(root, text="Confirm", command=on_confirm)
    button.pack(pady=10)

    root.mainloop()  # Start the main loop
    root.destroy()   # Destroy the root window after loop ends

    # Handle "New one" selection
    if user_input == "New one":
        new_asset_type = simpledialog.askstring("New Asset Type", "Enter new asset type:", parent=None)
        new_asset_symbol = simpledialog.askstring("New Asset Symbol", "Enter new asset symbol:", parent=None)
        new_asset_name = simpledialog.askstring("New Asset Name", "Enter new asset name:", parent=None)
        new_asset_description = simpledialog.askstring("New Asset Description", "Enter new asset description:", parent=None)
        new_asset_is_harmonised = simpledialog.askstring("New Asset Is Harmonised", "Enter new asset is harmonised (True/False):", parent=None)
        new_asset_is_harmonised = True if   new_asset_is_harmonised == "True" or new_asset_is_harmonised == "true" or new_asset_is_harmonised == "TRUE" or new_asset_is_harmonised == "1" or new_asset_is_harmonised == "T" else False
        
        asset_id=db.add_asset(db_file, new_asset_name, new_asset_symbol, new_asset_type, new_asset_description, new_asset_is_harmonised)
        return asset_id
    else:
        return asset_tuples[asset_names.index(user_input)][0]

def get_currency(db_file):
    """Prompts the user to select a currency or add a new one"""
    def on_confirm():
        nonlocal user_input
        user_input = combo.get()
        root.quit()
    
    user_input = None
    root = tk.Tk()
    root.title("Select Currency")

    # Fetch currencies as (id, code, name) tuples
    currency_tuples = db.get_currencies(db_file)
    currency_codes = [currency[1] for currency in currency_tuples] + ["New one"]

    # Create a combobox
    combo = ttk.Combobox(root, values=currency_codes)
    combo.pack(pady=20)
    
    # Default selection
    combo.set(currency_codes[0])

    # Button to confirm selection
    button = tk.Button(root, text="Confirm", command=on_confirm)
    button.pack(pady=10)

    root.mainloop()  # Start the main loop
    root.destroy()   # Destroy the root window after loop ends

    # Handle "New one" selection
    if user_input == "New one":
        new_currency_code = simpledialog.askstring("New Currency Code", "Enter new currency code:", parent=None)
        new_currency_name = simpledialog.askstring("New Currency Name", "Enter new currency name:", parent=None)

        currency_id=db.add_currency(db_file, new_currency_code, new_currency_name)
        return currency_id
    else:
        return currency_tuples[currency_codes.index(user_input)][0]


def get_asset_market(db_file, location_id):
    """Prompts the user to select an asset market or add a new one for a given location and market."""
    def on_confirm():
        nonlocal user_input
        user_input = combo.get()
        root.quit()
    
    user_input = None
    root = tk.Tk()
    root.title("Select Asset Market")

    # Fetch asset markets as (id, name) tuples
    asset_market_tuples = db.get_asset_markets(db_file, location_id)
    asset_market_names = [asset_market[1] for asset_market in asset_market_tuples] + ["New one"]

    # Create a combobox
    combo = ttk.Combobox(root, values=asset_market_names)
    combo.pack(pady=20)
    
    # Default selection
    combo.set(asset_market_names[0])

    # Button to confirm selection
    button = tk.Button(root, text="Confirm", command=on_confirm)
    button.pack(pady=10)

    root.mainloop()  # Start the main loop
    root.destroy()   # Destroy the root window after loop ends

    # Handle "New one" selection
    if user_input == "New one":
        new_asset_market_name = simpledialog.askstring("New Asset Market Name", "Enter new asset market name:", parent=None)
        new_asset_market_description = simpledialog.askstring("New Asset Market Description", "Enter new asset market description:", parent=None)
        #getting the asset, the market, the currency
        asset_id=get_asset(db_file)
        market_id=get_market(db_file)
        currency_id=get_currency(db_file)
        asset_market_id=db.add_asset_market(db_file, location_id, new_asset_market_name, new_asset_market_description, asset_id, market_id, currency_id)
        db.add_location_currency(db_file, location_id, currency_id)

        # Check if asset has a linked data source and add it if it doesn't
        if not db.has_data_source(db_file, asset_id):
            # Prompt user to select or define a data source
            data_source_id = define_data_source()
            asset_name=db.get_asset_name(db_file, asset_id)
            # Prompt user to define what should actually be connected to the data source
            data_source_connected_to = ask_what_to_link_to(new_asset_market_name, asset_name)
            db.add_data_source_to_asset(db_file, asset_id, asset_market_id, data_source_id, data_source_connected_to)

        return asset_market_id
    else:
        return asset_market_tuples[asset_market_names.index(user_input)][0]


#offers the user to select or define a data source from a dropdown menu
def define_data_source():
    options=['yfinance','manual_entry']
    def on_confirm():
        nonlocal user_input
        user_input = combo.get()
        root.quit()

    user_input = None
    root = tk.Tk()
    root.title("Select Data Source")

    # Create a combobox
    combo = ttk.Combobox(root, values=options)
    combo.pack(pady=20)

    # Button to confirm selection
    button = tk.Button(root, text="Confirm", command=on_confirm)
    button.pack(pady=10)

    root.mainloop()  # Start the main loop
    root.destroy()   # Destroy the root window after loop ends

    return user_input

def ask_what_to_link_to(new_asset_market_name, asset_name):
    options=[asset_name, new_asset_market_name]
    def on_confirm():
        nonlocal user_input
        user_input = combo.get()
        root.quit()

    user_input = None
    root = tk.Tk()
    root.title("Should this source be used just for "+new_asset_market_name+" or for the whole  "+asset_name+" ?")

    # Create a combobox
    combo = ttk.Combobox(root, values=options)
    combo.pack(pady=20)

    # Button to confirm selection
    button = tk.Button(root, text="Confirm", command=on_confirm)
    button.pack(pady=10)

    root.mainloop()  # Start the main loop
    root.destroy()   # Destroy the root window after loop ends

    if user_input==new_asset_market_name:
        return "asset_market"

    return "asset"


def get_asset_symbol(db_file, location, market):
    """
    Prompts the user to select an asset symbol or add a new one for a given location.
    """
    root = tk.Tk()
    root.withdraw()

    asset_symbols = db.get_asset_symbols(db_file, location, market) + ["New one"]
    
    asset_symbol = simpledialog.askstring("Transaction - Asset Symbol", 
                                          "Choose asset symbol:", parent=root, 
                                          initialvalue=asset_symbols[0])
    
    if asset_symbol == "New one":
        asset_symbol = simpledialog.askstring("New Asset", "Enter new asset symbol:", parent=root)
    
    return asset_symbol

def get_quantity():
    """ Prompt the user to enter the quantity for the transaction. """
    quantity = simpledialog.askfloat("Transaction - Quantity", "Enter quantity:")
    return quantity

def get_price(currency_code):
    """ Prompt the user to enter the price for the transaction. """
    price = simpledialog.askfloat("Transaction - Price", "Enter price per unit in " + currency_code+":")
    return price



def get_transaction_date():
    """ Prompt the user to enter the date for the transaction using a calendar widget. """
    def on_confirm():
        nonlocal selected_date
        selected_date = cal.get_date()
        root.quit()

    selected_date = None
    root = tk.Tk()
    root.title("Select Transaction Date")

    # Create a DateEntry widget
    cal = DateEntry(root, selectmode='day', year=datetime.datetime.now().year, 
                    month=datetime.datetime.now().month, day=datetime.datetime.now().day)

    # Configure the style of the widget
    cal.configure(background='blue', foreground='white')  # Set background color to blue and foreground color to white

    cal.pack(pady=20)

    # Button to confirm selection
    button = tk.Button(root, text="Confirm", command=on_confirm)
    button.pack(pady=10)
    root.mainloop()  # Start the main loop
    root.destroy()   # Destroy the root window after loop ends
    return selected_date if selected_date else datetime.date.today().isoformat()


def add_transaction_wizard(db_file):
    """
    Guides the user through the process of adding a transaction.
    """
    location_id = get_location(db_file)
    asset_market_id=get_asset_market(db_file,location_id)
    quantity = get_quantity()
    currency_id = db.get_asset_market_currency(db_file, asset_market_id)
    currency_code = db.get_currency_code(db_file, currency_id)
    price = get_price(currency_code)
    date = get_transaction_date()

    # Add the transaction to the database
    db.add_transaction(db_file,asset_market_id, quantity, price, date, location_id)


    print(f"Adding transaction: {quantity} of {asset_market_id} at {location_id} on {date} for {price} ")


