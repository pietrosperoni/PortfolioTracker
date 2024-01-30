## Presentation

A single-user python app to keep track of the investments done. 

It can take stocks, etf, futures, options and crypto. The app lets the user have multiple location for its investments, and for each location it also stores the amount of liquid cash in the various currencies. 

It must be possible to insert both buy actions and sell actions.

For each asset, it also stores the entry price, the date, the location, and if it was bought or sold through the execution of a PUT or a CALL option. And in this case for what price was the option bought or sold. If the asset was never used before it should ask if it is harmonised for financial reasons. The app should support multiple currencies. When extracting the historical net worth it should transform all into a single currency chosen by the owner. And when buying and selling, it should ask what currency it should use (unless it is obvious).

When an asset which was owned is then sold it should use the Last In First Out method to establish which one was sold, and calculate the gain or the loss. To be able to get a glimpse of how much money in taxes will need to be paid.

The user should have a simple user interface, that let it add actions (buy / sell) as well as see the historical graph of the net worth.

The app should provide real time financial data extracted when possible from google finance. Or Kraken (for the cripto). Or Interactive Brokers API (for the options).


The system should use as a minimum time value the day, and as such it should not need to keep track of the time

The system should store all the data as mysql-lite  with a file for user. So a second person can use the same program and store the data as another file

The system should read a file from interactive brokers to extract all the actions, and calculate all the asset owned. It should also avoid storing the same action twice. 

The system should use the conda virtual environment portfolio_env which should already have everything installed.

It should work for macOS. It should not use data encryption since the data should not exit the laptop which is a protected environment.

The system should NOT create a tax report instead just a vague value of the tax estimate should be enough. Considering that we are speaking about Italian tax laws, which means that wash trading is NOT illegal, etf not harmonised pay a different premium so must be kept separated.

it should use the historical exchange rate, and it should store them so not to have to download them every time, the same with all the other assets. The data should be downloaded, and then stored.

## Project Summary:

The project entails the development of a single-user software application, "Portfolio_Manager," to track various investments which include stocks, ETFs, futures, options, and cryptocurrencies. The application will allow the user to manage investments across multiple locations, and for each location, track liquid cash in different currencies. Users will be able to record buy and sell actions while the app stores details such as the asset's entry price, purchase date, location, and whether it was acquired through a PUT or CALL option, including the price of the option.

Assets are recorded by the Last In First Out (LIFO) method to compute gains or losses and provide an estimated tax liability based on the Italian tax law, which recognizes the legality of wash trades and different tax rates for non-harmonized ETFs. The interface will be simple, allowing for the addition of transactions and viewing net worth over time. Transactions will be recorded with the day as the minimum time value. Data will be stored in a MySQL Lite database, with individual files for each user to facilitate multiple users on the same application.

The system will support multiple currencies, converting all values into a user-selected currency for historical net worth calculations. It will also inquire about the currency to use for transactions unless the currency is evident. The application will extract real-time financial data from sources such as Google Finance, Kraken, and the Interactive Brokers API. It will be developed for macOS and integrate a feature to import and compute assets from Interactive Brokers files, avoiding duplicate entries. Security features such as data encryption will not be implemented as the data will remain on a secure environment on the user's laptop. The application will be contained within the "portfolio_env" Conda virtual environment, which is expected to have all necessary packages preinstalled.


## User Stories:


### Creating entries
The user will be able to create an entry for a new investment with details including the asset type (stock, ETF, future, option, cryptocurrency), asset name, entry price, purchase date, location, and any relevant option details (PUT/CALL, option price).

### Viewing and Tracking Investments:
As a user, I want to view the current status of all my investments, so I can understand my portfolio's performance at a glance.
As a user, I want to track the historical performance of my investments, so I can analyze trends and make informed decisions.

### Managing and Updating Investments:
As a user, I want to update the details of an existing investment, so I can keep my portfolio information accurate.
As a user, I want to delete an investment entry, in case I entered information incorrectly or the investment is no longer relevant.

### Financial Analysis and Reporting:
As a user, I want to see an estimated tax liability for my investments, so I can plan for my financial obligations.
As a user, I want to compare different investments, so I can determine which ones are performing better.

### Data Import and Integration:
As a user, I want to import transaction data from external sources like Interactive Brokers, so I can automate the data entry process and reduce errors.

### Multi-Currency Support:
As a user, I want to view my investments in different currencies, so I can understand their value in a global context.



DataBase Schema
    Table: locations
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
    Table: currencies
        id INTEGER PRIMARY KEY,
        code TEXT NOT NULL UNIQUE,
        name TEXT
    Table: location_currencies
        id INTEGER PRIMARY KEY,
        location_id INTEGER,
        currency_id INTEGER,
        FOREIGN KEY (location_id) REFERENCES locations (id),
        FOREIGN KEY (currency_id) REFERENCES currencies (id)
    Table: assets
        id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        name TEXT NOT NULL,
        symbol TEXT,
        description TEXT,
        is_harmonised BOOLEAN
    Table: markets
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
    Table: asset_markets table
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        asset_id INTEGER,
        market_id INTEGER,
        location_id INTEGER,
        currency_id INTEGER,
        FOREIGN KEY (asset_id) REFERENCES assets (id),
        FOREIGN KEY (location_id) REFERENCES locations (id),
        FOREIGN KEY (market_id) REFERENCES markets (id),
        FOREIGN KEY (currency_id) REFERENCES currencies (id)
    Table: transactions
        id INTEGER PRIMARY KEY,
        asset_market_id INTEGER,
        quantity REAL NOT NULL,
        price REAL NOT NULL,
        date TEXT NOT NULL,
        location_id INTEGER,
        FOREIGN KEY (asset_market_id) REFERENCES asset_markets (id),
        FOREIGN KEY (location_id) REFERENCES locations (id)
    Table: accounts
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT
    Table: account_balances
        account_id INTEGER,
        currency_id INTEGER,
        amount REAL,
        FOREIGN KEY (account_id) REFERENCES accounts (id),
        FOREIGN KEY (currency_id) REFERENCES currencies (id)
    Table: Exchange Rates
        date TEXT,
        currency_from_id INTEGER,
        currency_to_id INTEGER,
        rate REAL
        FOREIGN KEY (currency_from_id) REFERENCES currencies (id)
        FOREIGN KEY (currency_to_id) REFERENCES currencies (id)
    Table: User Settings
        setting_key TEXT,
        setting_value TEXT


## Data Retrieval and Storage:

Financial data for various assets (stocks, ETFs, cryptocurrencies, etc.) will be retrieved from different sources, primarily using the yfinance library, but others will be added later.
The application will support manual data entry for assets where automatic data retrieval is not feasible.
Each asset or asset market will be associated with a data source, identified in a revised data_sources table in our SQLite database.
Historical financial data for each asset will be stored persistently in the SQLite database, ensuring data integrity and availability for long-term analysis.

## Data Source Management:

The data_sources table will link each data source to specific assets or asset markets.
This table will record the source type (e.g., 'yfinance', 'manual') and the relationship with assets or asset markets.
A standardized naming convention will be used for storing data files, and the directory path for these files will be stored in the application's settings.

## Data Analysis:

For performing data analysis, trend observation, and generating reports, the application will utilize pandas DataFrames.
Data will be loaded from the SQLite database into pandas DataFrames to leverage pandas' advanced data manipulation and analysis capabilities.
After analysis, any persistent changes will be written back to the SQLite database.

## Hybrid Storage and Analysis Approach:

By combining SQLite and pandas, the application will offer robust and efficient data handling.
SQLite will ensure secure and reliable long-term data storage, while pandas will provide flexibility for in-depth data analysis and manipulation.