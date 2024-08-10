from fake_useragent import UserAgent
import re
# Function to get headers with a random user agent

def get_headers():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1',  # Do Not Track Request Header
        'Upgrade-Insecure-Requests': '1'
    }
    return headers


# Function to convert strings to appropriate financial values

# Exchange rates to USD for  commonly used currencies
exchange_rates = {'USD': 1.0, 'EUR': 1.09, 'GBP': 1.28,  'JPY': 0.0068,  'AUD': 0.65, 'CHF':1.17, 'CAD':1.37, 'R':18.74}

def convert_values(value_text):
    """
    Convert a string value representing a financial figure to billions.
    
    Parameters:
    value_text (str): The financial figure as a string, e.g., '1.5B USD', '2T EUR', '871.10K', '0.00'.
    
    Returns:
    float: The financial figure converted to billions.
    
    Raises:
    ValueError: If the format of the value is unsupported.
    """
    match = re.match(r'(-?[\d\.]+)([BTMK]?)\s*([A-Z]{3})?', value_text)
    if not match:
        raise ValueError(f"Unsupported format in value: {value_text}")
    
    numeric_value, magnitude, currency = match.groups()
    numeric_value = float(numeric_value)
    
    if currency is None:
        currency = 'USD'
    
    if currency not in exchange_rates:
        raise ValueError(f"Unsupported currency: {currency}")
    
    # Convert to USD
    numeric_value *= exchange_rates[currency]
    
    if magnitude == 'B':
        return numeric_value
    elif magnitude == 'T':
        return numeric_value * 1000  # Convert trillions to billions
    elif magnitude == 'M':
        return numeric_value / 1000  # Convert millions to billions
    elif magnitude == 'K':
        return numeric_value / 1_000_000  # Convert thousands to billions
    elif magnitude == '':
        return numeric_value / 1_000_000_000  # Convert plain numbers to billions
    else:
        raise ValueError(f"Unsupported magnitude in value: {value_text}")
