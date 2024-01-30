import sqlite3


def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_tables(db_file):
    """ Create tables in the database """
    conn = create_connection(db_file)
    if conn is not None:
        try:
            c = conn.cursor()

            # data_sources table, like manual, yfinance, kraken, etc.
            c.execute('''CREATE TABLE IF NOT EXISTS data_sources (
                 id INTEGER PRIMARY KEY,
                 source TEXT NOT NULL
             )''')

            # locations table, like Interactive Brokers, Kraken, 
            c.execute('''CREATE TABLE IF NOT EXISTS locations (
                         id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         description TEXT
                         )''')

            # currencies table, like USD, EUR, BTC
            c.execute('''CREATE TABLE IF NOT EXISTS currencies (
                         id INTEGER PRIMARY KEY,    
                         code TEXT NOT NULL UNIQUE,
                         name TEXT NOT NULL
                         )''')

            # location_currencies table
            c.execute('''CREATE TABLE IF NOT EXISTS location_currencies (
                         id INTEGER PRIMARY KEY,    
                         location_id INTEGER,
                         currency_id INTEGER,
                         FOREIGN KEY (location_id) REFERENCES locations (id),
                         FOREIGN KEY (currency_id) REFERENCES currencies (id)
                         )''')       

            # Assets table, like Amazon, Google
            c.execute('''CREATE TABLE IF NOT EXISTS assets (
                         id INTEGER PRIMARY KEY,
                         type TEXT NOT NULL,
                         name TEXT NOT NULL,
                         symbol TEXT,
                         description TEXT,
                         data_source_id INTEGER,
                         is_harmonised BOOLEAN,
                         FOREIGN KEY (data_source_id) REFERENCES data_sources (id)
                         )''')

            # Markets table, like NYSE, NASDAQ, etc.
            c.execute('''CREATE TABLE IF NOT EXISTS markets (
                         id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         description TEXT
                         )''')

            # Asset_Markets table
            c.execute('''CREATE TABLE IF NOT EXISTS asset_markets (
                         id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         description TEXT,
                         asset_id INTEGER,
                         market_id INTEGER,
                         location_id INTEGER,
                         currency_id INTEGER,
                         data_source_id INTEGER,
                         FOREIGN KEY (asset_id) REFERENCES assets (id),
                         FOREIGN KEY (location_id) REFERENCES locations (id),
                         FOREIGN KEY (market_id) REFERENCES markets (id),
                         FOREIGN KEY (currency_id) REFERENCES currencies (id),
                         FOREIGN KEY (data_source_id) REFERENCES data_sources (id)
                         )''')

            # Transactions table
            c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                         id INTEGER PRIMARY KEY,
                         asset_market_id INTEGER,
                         quantity REAL NOT NULL,
                         price REAL NOT NULL,
                         date TEXT NOT NULL,
                         location_id INTEGER,
                         FOREIGN KEY (asset_market_id) REFERENCES asset_markets (id),
                         FOREIGN KEY (location_id) REFERENCES locations (id)
                         )''')

            # Accounts table
            c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                         id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         type TEXT
                         )''')
            # Account Balances table
            c.execute('''CREATE TABLE IF NOT EXISTS account_balances (
                         account_id INTEGER,
                         currency_id INTEGER,
                         amount REAL,
                         FOREIGN KEY (account_id) REFERENCES accounts (id),
                         FOREIGN KEY (currency_id) REFERENCES currencies (id)
                         )''')
            # Exchange Rates table
            c.execute('''CREATE TABLE IF NOT EXISTS exchange_rates (
                         date TEXT,
                         currency_from_id INTEGER,
                         currency_to_id INTEGER,
                         rate REAL,
                         FOREIGN KEY (currency_from_id) REFERENCES currencies (id),
                         FOREIGN KEY (currency_to_id) REFERENCES currencies (id)
                         )''')
            # User Settings table (optional)
            c.execute('''CREATE TABLE IF NOT EXISTS user_settings (
                         setting_key TEXT,
                         setting_value TEXT
                         )''')

            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")


# Data Source Functions
# checks if an asset has a linked data source, or if it is equal to -1.
# if it is equal to -1, then the data source might be linked to the asset_market
def has_data_source(db_file, asset_id):
    """ Check if an asset has a linked data source """
    conn = create_connection(db_file)
    has_data_source = False
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT id FROM data_sources WHERE id = (SELECT data_source_id FROM assets WHERE id = ?)", (asset_id,))
            #  If the query returns a result and the asset has a linked data source different from -1 then the asset has a linked data source
            if c.fetchone() and c.fetchone()[0] != -1:
                has_data_source = True
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return has_data_source

def get_data_sources_from_asset(db_file, asset_id):
    """ Fetch all data sources for an asset """
    conn = create_connection(db_file)
    data_sources = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT id, name FROM data_sources WHERE id = (SELECT data_source_id FROM assets WHERE id = ?)", (asset_id,))
            data_sources = [(data_source[0], data_source[1]) for data_source in c.fetchall()]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return data_sources

def get_data_sources_from_asset_market(db_file, asset_market_id):
    """ Fetch all data sources for an asset market """
    conn = create_connection(db_file)
    data_sources = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT id, name FROM data_sources WHERE id = (SELECT data_source_id FROM asset_markets WHERE id = ?)", (asset_market_id,))
            data_sources = [(data_source[0], data_source[1]) for data_source in c.fetchall()]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return data_sources

def add_data_source_to_asset(db_file, asset_id, asset_market_id, data_source_id, who_to_add_it_to):
    conn = create_connection(db_file)
    if conn is not None:
        try:
            c = conn.cursor()
            if who_to_add_it_to == "asset":
                c.execute("UPDATE assets        SET data_source_id = ? WHERE id = ?", (data_source_id,        asset_id))
                c.execute("UPDATE asset_markets SET data_source_id = ? WHERE id = ?", (            -1, asset_market_id))
            elif who_to_add_it_to == "asset market":
                c.execute("UPDATE asset_markets SET data_source_id = ? WHERE id = ?", (data_source_id, asset_market_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def get_locations(db_file):
    """ Fetch all locations from the database """
    conn = create_connection(db_file)
    locations = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT id, name FROM locations")
            locations = [(location[0], location[1]) for location in c.fetchall()]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return locations
def add_location(db_file, name, description):
    """ Add a new location to the database """
    conn = create_connection(db_file)
    location_id = -1
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO locations (name, description) VALUES (?, ?)", (name, description))
            conn.commit()
            location_id = c.lastrowid # Get the ID of the newly inserted location
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
            return location_id

def get_assets(db_file):
    """ Fetch all assets from the database """
    conn = create_connection(db_file)
    assets = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT id, symbol, name, description, is_harmonised FROM assets")
            assets = [(asset[0], asset[1], asset[2], asset[3], asset[4]) for asset in c.fetchall()]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return assets
def add_asset(db_file, name, symbol, type, description, is_harmonised):
    conn = create_connection(db_file)
    asset_id=-1
    try:
        c = conn.cursor()
        c.execute("INSERT INTO assets (name, symbol, type, description, is_harmonised) VALUES (?, ?, ?, ?, ?)",
                  (name, symbol, type, description, is_harmonised))        
        conn.commit()
        asset_id = c.lastrowid  # Get the ID of the newly inserted asset
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
        return asset_id

def get_asset_name(db_file, asset_id):
    conn = create_connection(db_file)
    asset_name=None
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT name FROM assets WHERE id = ?", (asset_id,))
            asset_name = c.fetchone()[0]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return asset_name




def get_currencies(db_file):
    """ Fetch all currencies from the database """
    conn = create_connection(db_file)
    currencies = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT id, code, name FROM currencies")
            currencies = [(currency[0], currency[1], currency[2]) for currency in c.fetchall()]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return currencies
def add_currency(db_file, code, name):
    conn = create_connection(db_file)
    currency_id = -1
    try:
        c = conn.cursor()
        c.execute("INSERT INTO currencies (code, name) VALUES (?, ?)", (code, name))
        conn.commit()
        currency_id = c.lastrowid  # Get the ID of the newly inserted currency
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
        return currency_id
def get_currency_code(db_file, currency_id):
    conn = create_connection(db_file)
    currency_code=None
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT code FROM currencies WHERE id = ?", (currency_id,))
            result = c.fetchone()
            currency_code = result[0] if result else None
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return currency_code

def get_currency_by_location(db_file, location_id):
    conn = create_connection(db_file)
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT currency_id FROM location_currencies WHERE location_id = ?", (location_id,))
            result = c.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
def add_location_currency(db_file, location_id, currency_id):
    "add a currency to a location but also check if it already exists"
    conn = create_connection(db_file)
    try:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO location_currencies (location_id, currency_id) VALUES (?, ?)", (location_id, currency_id))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

def get_markets(db_file):
    """ Fetch all markets from the database """
    conn = create_connection(db_file)
    markets = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT id, name, description FROM markets")
            markets = [(market[0], market[1], market[2]) for market in c.fetchall()]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return markets
def add_market(db_file, name, description=""):
    conn = create_connection(db_file)
    market_id = -1
    try:
        c = conn.cursor()
        c.execute("INSERT INTO markets (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        market_id = c.lastrowid  # Get the ID of the newly inserted market
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
        return market_id

def get_asset_markets(db_file, location_id):
    """ Fetch all unique asset markets for a given location from the database """
    conn = create_connection(db_file)
    asset_markets = []
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT id, name FROM asset_markets WHERE location_id = ?", (location_id,))
            asset_markets = [(market[0], market[1]) for market in c.fetchall()]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return asset_markets
def add_asset_market(db_file, location_id, name, description, asset_id, market_id, currency_id):
    conn = create_connection(db_file)
    asset_market_id = -1
    try:
        c = conn.cursor()
        c.execute("INSERT INTO asset_markets (location_id, name, description, asset_id, market_id, currency_id) VALUES (?, ?, ?, ?, ?, ?)", (location_id, name, description, asset_id, market_id, currency_id))
        conn.commit()
        asset_market_id = c.lastrowid  # Get the ID of the newly inserted asset_market
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
        return asset_market_id
def get_asset_market_currency(db_file, asset_market_id):
    """ Fetch the currency of an asset market from the database """
    conn = create_connection(db_file)
    result = None
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT currency_id FROM asset_markets WHERE id = ?", (asset_market_id,))
            result = c.fetchone()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return result[0] if result else None

def add_transaction(db_file, asset_market_id, quantity, price, date, location_id):
    ''' Add a new transaction to the transactions table unless it already exists.'''
    conn = create_connection(db_file)
    transaction_id = -1
    try:
        c = conn.cursor()
        c.execute("INSERT INTO transactions (asset_market_id, quantity, price, date, location_id) VALUES (?, ?, ?, ?, ?)", (asset_market_id, quantity, price, date, location_id))
        conn.commit()
        transaction_id = c.lastrowid
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
        return transaction_id


def fetch_all_transactions(db_file):
    """ Fetch all transactions from the database and return them """
    conn = create_connection(db_file)
    transactions = []
    if conn is not None:
        try:
            c = conn.cursor()
            # Adjust the SELECT statement as needed to fetch all necessary data
            c.execute('''SELECT t.date, a.symbol, a.name, am.name, t.price, t.quantity, (t.price * t.quantity) as total, l.name, cu.code 
                         FROM transactions t
                         JOIN asset_markets am ON t.asset_market_id = am.id
                         JOIN assets a ON am.asset_id = a.id
                         JOIN locations l ON t.location_id = l.id
                         JOIN currencies cu ON am.currency_id = cu.id''')
            transactions = c.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return transactions


if __name__ == "__main__":
    create_tables()


