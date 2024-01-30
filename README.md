# PortfolioTracker

## Description
PortfolioTracker is an intuitive, single-user application designed for meticulously tracking and analyzing diverse investment portfolios. It supports various investment types, including stocks, ETFs, futures, options, and cryptocurrencies, across multiple accounts and currencies.

## Features
- **Multiple Asset Types**: Track stocks, ETFs, futures, options, and cryptocurrencies.
- **Multi-Account Management**: Manage investments across different locations and track cash balances in various currencies.
- **Transaction Recording**: Record both buy and sell actions with details like entry price, date, and location.
- **LIFO Accounting**: Utilize the Last In First Out method for calculating gains or losses for tax estimates.
- **Real-Time Data**: Extract financial data in real-time from sources like Google Finance and Kraken.
- **User-Friendly Interface**: Simple and straightforward interface for easy navigation and usage.
- **Multi-Currency Support**: Manage and view investments in multiple currencies, with historical net worth calculations in a chosen primary currency.

## Installation
To set up PortfolioTracker, follow these steps:

1. Clone the repository:

```
git clone https://github.com/pietrosperoni/PortfolioTracker.git
```

2. Navigate to the project directory:

```
cd PortfolioTracker
```

3. Install required dependencies (ensure you have Conda installed):

```
conda create --name portfoliotracker_env python=3.11
conda activate portfoliotracker_env
conda env update --file environment.yml
```

After installing new libraries or making significant changes, export your environment:

```
conda env export > environment.yml
```

Remember to activate the portfoliotracker_env environment every time you work on this project.
Keep the environment.yml file updated and commit changes to your Git repository.


## Usage
Describe how users can use the application, including any commands or scripts they need to run.


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- Thanks to ChatGPT for helping transform this into a reality.
