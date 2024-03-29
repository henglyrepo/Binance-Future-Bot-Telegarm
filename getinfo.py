import time
from config import *
from binance.client import Client
from binance.exceptions import BinanceAPIException
from decimal import Decimal

# Initialize Binance client
client = Client(api_key, api_secret)




# Get account Balance 
def get_account_balance(api_key, api_secret):
    client = Client(api_key, api_secret)
    balance = client.futures_account_balance()
    for asset in balance:
        if asset['asset'] == 'USDT':
            return float(asset['balance'])
    return 0.0



#Get position
def get_position(symbol):
    """Function to get the current position for a given symbol"""
    position = client.futures_position_information(symbol=symbol)
    for p in position:
        if p['symbol'] == symbol:
            return p
    return None


# Get the current price for the symbol.
def get_current_price(symbol):
    client = Client()  # create a new Binance API client instance
    ticker = client.get_symbol_ticker(symbol=symbol)  # get the ticker for the given symbol
    if 'price' not in ticker:
        raise ValueError(f"Failed to retrieve current price for symbol {symbol}")
    return float(ticker['price'])


# Calculate position size
account_balance = get_account_balance(api_key, api_secret)
def calculate_position_size(account_balance, leverage, symbol, percentage, stop_loss, take_profit):
    current_price = get_current_price(symbol)
    position_size = (account_balance * leverage * percentage) / ((current_price * stop_loss) - (current_price * take_profit))
    return position_size


# check_position_exists
def check_position_exists(symbol):
    """Function to check if a position already exists for a given symbol"""
    position = get_position(symbol)
    if position is not None:
        if float(position['positionAmt']) != 0:
            return True
    return False


# check_position_exists by ""Check open order""
def check_open_orders(client, symbol):
    """Function to check if there are any open orders for a given symbol"""
    orders = client.futures_get_open_orders(symbol=symbol)
    if orders:
        for order in orders:
            if order['status'] in ['NEW', 'PARTIALLY_FILLED']:
                return True
    return False


# Get position details
def get_position_details(symbol):
    """Function to get position details for a given symbol"""
    position_details = client.futures_position_information(symbol=symbol)[0]
    return position_details


# Get open orders for symbol
def get_open_orders(symbol):
    """Function to get open orders for a given symbol"""
    orders = client.futures_get_open_orders(symbol=symbol)
    return orders


# Current Position INFO ////////////////////////

# Get current position Entry Price
def get_entry_price(symbol):
    """Function to get the entry price of the last filled order for a given symbol"""
    position = client.futures_position_information(symbol=symbol)
    if position:
        entry_price = float(position[0]['entryPrice'])
        return entry_price
    return None

# Check current position is Long or Short 
def get_position_side(symbol):
    """Function to get the position side (LONG or SHORT) for a given symbol"""
    position = get_position(symbol)
    if position is not None:
        if float(position['positionAmt']) > 0:
            return 'LONG'
        elif float(position['positionAmt']) < 0:
            return 'SHORT'
    return position

# Get current position trading amount
def get_quantity_position(symbol):
    """Get the quantity of the currently open position"""
    position = get_position(symbol)
    if position is not None and float(position['positionAmt']) != 0:
        return abs(float(position['positionAmt']))
    return 0


